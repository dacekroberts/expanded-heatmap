# Where every piece of this project's data comes from

One row per source, per city. This is the master provenance list: if a map
shows something, its source is named here, with the endpoint it came from and
the filter applied at download.

It exists because the endpoints were previously scattered — some in a city's
`config.py` comment header, some only inside a `step*.py` error message, and
several (San Francisco's boundary layer) nowhere at all. That is a problem for
three reasons: a reader cannot check the work, a dead endpoint is invisible
until a rebuild fails, and the licence question below cannot be answered
source by source if the sources are not listed.

**Every source is a public government dataset.** Nothing here is scraped,
purchased, or behind a login.

## How to keep this current

- **Adding a city adds its rows here, in the same commit** — provenance *and*
  licence together. The `add-city` skill makes both a Step 0 requirement and
  re-checks them at Step 9; a city whose data is mapped but whose terms are
  unrecorded is not finished, because afterwards that gap is invisible — it
  looks exactly like a city that was checked.
- Record the **endpoint**, the **server-side filter** (the download is often
  filtered — that filter is part of the provenance), and the **date retrieved**.
- Record the **licence, and anything the source requires this project to
  display**. Do not infer permissive terms from the fact that a source is
  government open data: the review below found everything from public-domain
  dedications to a feed that forbids modifying its data, and both extremes
  inside one city. Socrata states a licence directly at
  `<domain>/api/views/<id>.json` (`license`, `licenseId`, `attribution`); a
  missing value there means "go read the terms", not "no restrictions".
- **A new required notice goes in the notices section below**, which gates the
  public deploy. A new clause needing a human decision goes to the owner and
  then to `DECISIONS.md` — not resolved by reading it generously.
- When an endpoint dies, leave the old row and mark it dead with the date,
  rather than overwriting it. Dataset IDs get retired: New York's borough
  boundaries moved from `tqmj-j8zm` (now 404) to `gthc-hcne`, and the MTA
  retired its `web.mta.info/developers` GTFS path in favour of an S3 bucket.
  A silently-replaced URL loses that history.
- Raw downloads are **not** committed (`data/<city>/raw/` is gitignored). Only
  the rendered `outputs/` are. So these endpoints plus the recorded filters are
  the only way to reproduce a build.
- **Declare the source encoding.** Every city's `config.py` sets
  `SOURCE_ENCODING` and every raw read passes it, rather than relying on the
  default. pandas defaults to UTF-8 and *raises* on anything else, which is
  safe — but the failure lands on whoever adds the next city, and the tempting
  fix (reach for `latin-1` to make the `UnicodeDecodeError` go away) corrupts
  accented characters **without failing**, so nothing catches it downstream.
  Declaring it makes the choice reviewable and part of the provenance. Every
  built city so far is `utf-8`; this bites on non-US cities, where Quebec data
  in particular is still often published in `latin-1`. Note that mojibake
  in a *terminal* is usually the Windows console codepage, not the file — check
  the bytes before changing the declaration.
- **Read a new city's whole catalogue, do not grep it.** Listing every package
  name and reading them costs about a minute and ~3 KB; keyword-filtering the
  list reintroduces exactly the bias that pulling the full list was meant to
  remove. Montréal proved it on 2026-09-21: `locaux-commerciaux`, a 28,621-row
  agglomeration-wide survey of street-level commerce with NAICS codes and 100%
  coordinates, contains none of the words *business*, *licence*, *permis*,
  *entreprise* or *commerce*, and a keyword scan wrongly concluded the city was
  food-only. Neither does `unités d'évaluation foncière`, its property roll.

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| San Diego | City Business Tax Certificates | All three buckets, via NAICS | `https://seshat.datasd.org/business_tax_certificates/` (`sd_businesses_active_datasd.csv`) | none (whole file) | 2026-09-18 |
| San Diego | **SanGIS/SANDAG countywide tax parcels** (ArcGIS FeatureServer, 1,089,758 polygons) | Not businesses — **joined** to the above for the residence check. San Diego was recorded as the city with NO residence signal, on a 0.03% reading that was a MEASUREMENT GAP rather than a clean result; `ownerocc` is `Y` on 472,498 parcels and is the genuine owner-occupancy flag it was thought to lack | `https://geo.sandag.org/server/rest/services/Hosted/Parcels/FeatureServer/0/query` | **One buffered query PER PERSON-LIKE PIN, not a bulk download** — `where=1=1`, a point `geometry` with `distance` in metres, `outFields=apn,asr_landuse,ownerocc`, `returnGeometry=false` and **`returnCentroid=true`**, then the nearest centroid is chosen locally. Only pins whose displayed name reads as a person's are queried (2,463 of them): the filter cannot fire on anything else and this is a shared public service. **The bulk alternative was tried and abandoned** — `orderByFields` forces a sort over 664,662 rows and `resultOffset` deep-pages at ~26 s per 2,000-row page, about two hours — so `PARCEL_QUERY_BBOX` and `PARCEL_PAGE_SIZE` survive in `config.py` as dead constants that no script reads. **Nearest, not containing:** these coordinates sit 5-15 m outside their own parcel because they are placed at the street frontage and SanGIS parcels exclude road right-of-way, so on 30 sampled pins an exact point-in-parcel test matched 1 and a 25 m buffer matched 30. `asr_landuse` has no published coded-value domain, so `11` = single-family detached was established empirically; `17` = condominium is deliberately excluded, as a unit in a shared building may be ground-floor retail | 2026-09-21 |
| San Francisco | DataSF Registered Business Locations (Socrata `g8m3-pdis`) | All three buckets, via NAICS | `https://data.sf.gov/resource/g8m3-pdis.csv` | San Francisco only | ≈2026-09-19 |
| San Francisco | **Assessor Historical Secured Property Tax Rolls** (Socrata `wv5m-vpq2`) | Not businesses — **joined** to the above for the residence check. 217 pins (1.19%) displayed a person's name at a parcel the Assessor calls Single Family Residential *and* claiming a homeowner's exemption, California's homestead analogue, granted only on an owner-occupied primary residence | `https://data.sf.gov/resource/wv5m-vpq2.csv` | `$where=closed_roll_year = '2025' AND the_geom IS NOT NULL`, `$select=block, lot, use_definition, number_of_units, homeowner_exemption_value, the_geom`, `$limit=400000`. **`the_geom` is a POINT per parcel, and selecting it is what makes this a SPATIAL join rather than an address one** — an address join reaches only 43.8%, because `property_location` is a fixed-width composite (`'0000 2801 LEAVENWORTH         ST0000'`) and stripping direction words destroys "North Point" and "South Van Ness" on both sides. 43.8% is not enough to filter on: it would remove home businesses only where the address text happened to match, which is arbitrary but looks complete. Nearest-parcel tolerance 40 m (93.4% matched, median 1.4 m). **"Multi-Family Residential" is deliberately NOT treated as residential** although it is the largest category under this city's pins (5,733) — San Francisco puts ground-floor retail in residential buildings. Same host rule as the boundary layer: `data.sf.gov`, never `data.sfgov.org`, which 403s on `/resource/` | 2026-09-21 |
| Los Angeles | Listing of Active Businesses (Socrata `6rrh-rzua`) | All three buckets, via NAICS | `https://data.lacity.org/resource/6rrh-rzua.csv` | `$where=location_1 IS NOT NULL`, selected columns, `$order=location_account` | ≈2026-09-19 |
| Los Angeles | **LA County Assessor parcels** (ArcGIS MapServer, 92 fields) | Not businesses — **joined** to the above for the residence check. A 400-point sample put **7.2%** of this city's person-like pins on a Residential parcel claiming a homeowner's exemption — roughly 1,000-2,000 pins, **the largest such exposure in the project** | `https://public.gis.lacounty.gov/public/rest/services/LACounty_Cache/LACounty_Parcel/MapServer/0/query` | One query per person-like pin: `f=json`, point `geometry` with `inSR=4326`, `spatialRel=esriSpatialRelIntersects`, and `outFields=UseType,UseDescription,Roll_HomeOwnersExemp` — three fields of the 92. **Containing parcel first, 25 m buffer only as a fallback** for points inside no parcel at all: an exact point-in-parcel test matches only ~49% of these pins, because the 9% of LA coordinates recovered by Census geocoding sit on street centrelines. Filtering on the unbuffered 49% would have been San Francisco's 43.8% mistake. **Owner names are absent by law** (Cal. Gov. Code §7928.205), so there is nothing here to publish by accident — a structural privacy position rather than a column omission | 2026-09-21 |
| Chicago | Business Licenses (Socrata `r5kz-chrr`) | All three buckets, via its own licence taxonomy | `https://data.cityofchicago.org/resource/r5kz-chrr.csv` | `license_status='AAI' AND expiration_date >= '2026-09-20'`, `$order=id` | 2026-09-20 |
| Washington D.C. | **Basic Business License** (DCRA/DLCP, ArcGIS FeatureServer) | **All three buckets, via its own `BUSINESSACTIVITY` taxonomy** — the first non-NAICS source here that covers all three on its own | `https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/DCRA/FeatureServer/0/query` (`outSR` not needed — `returnGeometry=false`, `orderByFields=OBJECTID ASC`, paged at 2,000) | `LICENSESTATUS='Active' AND PREMISEINDC='Yes' AND BUSINESSACTIVITY NOT IN (<the five residential rental types>)`, and an explicit 16-column `outFields` list that omits every owner/agent name and the billing address | 2026-09-21 |
| New York | DOHMH Restaurant Inspection Results (Socrata `43nn-pn8j`) | **Food service** | `https://data.cityofnewyork.us/resource/43nn-pn8j.csv` | selected columns, `$limit=500000` (unfiltered: it is an inspection history, collapsed to one row per establishment in step 2) | 2026-09-21 |
| New York | NYS Retail Food Stores (Socrata `9a8c-vfzj`, data.ny.gov) | **Retail** — grocery, bodegas, delis, supermarkets | `https://data.ny.gov/resource/9a8c-vfzj.csv` | `county in('KINGS','QUEENS','BRONX','NEW YORK','RICHMOND')` | 2026-09-21 |
| New York | NYS Active Appearance Enhancement & Barber *Business* Licensees (Socrata `y3u4-jbgh`, data.ny.gov) | **Personal services** — salons, nail, skin care, barbers | `https://data.ny.gov/resource/y3u4-jbgh.csv` | selected columns; **`license_holder_name` deliberately not selected** (it is an individual's name) | 2026-09-21 |
| New York | DCWP Issued Licenses (Socrata `w7w3-xahh`) | **Retail**, a narrow regulated slice | `https://data.cityofnewyork.us/resource/w7w3-xahh.csv` | `license_status='Active' AND license_type='Premises'` | 2026-09-21 |
| Philadelphia | L&I Business Licenses (Carto SQL API, table `business_licenses`) | **Food service** and **Retail** only — see below | `https://phl.carto.com/api/v2/sql` (`format=csv`) | `licensestatus='Active' AND licensetype IN (…13 types…)`, built from `config.KEPT_LICENSETYPES`; selected columns, **no registrant-name column** (`legalfirstname`, `legallastname`, `legalname`, `opa_owner`, `ownercontact*name` are all deliberately unselected and asserted absent in step 2) | 2026-09-21 |
| Philadelphia | OPA Property Assessments (Carto SQL API, table `opa_properties_public`, 583,779 rows) | Not businesses — **joined** to the above for the residence check | `https://phl.carto.com/api/v2/sql` (`format=csv`) — the same endpoint as the licence data | `LEFT JOIN opa_properties_public p ON b.opa_account_num = p.parcel_number`, which matches 94% of licences. Only two derived values are selected — the City's own `category_code_description` land-use category and a boolean for whether a homestead exemption is claimed. The exemption AMOUNT is not downloaded and no mailing address is downloaded at all | 2026-09-21 |
| Miami | Miami-Dade County **Local Business Tax** (ArcGIS FeatureServer, 194,099 rows, all `YEAR`=2026) | All three buckets, via the county's own `CATGRYNAME` (150 values). **Its `BUSNAICSCD` column is NULL on all 194,099 rows**, so NAICS is unavailable despite being in the schema | `https://services.arcgis.com/8Pc9XBTAsYuxx9Ny/arcgis/rest/services/Local_Business_Tax_Feature_Layer_View/FeatureServer/0/query` | `ACCSTATUS='Active'` (175,982 rows), selected columns, `orderByFields=OBJECTID` for stable deep paging. **`OWNERNAME` and every `MAIL*` column are deliberately NOT downloaded** — `OWNERNAME` is populated on 100% of rows and is frequently a person; step 2 asserts all eight stay absent | 2026-09-21 |
| Boston | Food Establishment Inspections (CKAN resource `4582bec6-2b4f-4f9e-bc55-cbaa73117f4c`, 902,651 rows) | **Food service** (`FS`, `FT`) and **Retail** (`RF`) — see below | `https://data.boston.gov/api/3/action/datastore_search_sql` | `licstatus='Active'`, **collapsed to one row per `property_id` + `licensecat` in SQL** with `GROUP BY`, so the download is ~2,900 rows rather than ~900,000. `legalowner`, `namelast` and `namefirst` exist in this table and are deliberately NOT selected; step 2 asserts they and five more stay absent | 2026-09-21 |
| Boston | Licensing Board Licenses (CKAN resource `04dc653b-1789-4374-9669-b07df7233344`, 3,587 rows) | **Retail** — package stores only | same endpoint | `status='Active' AND (license_type LIKE 'Retail%' OR license_type = 'Druggist')` → 307 rows. Its 2,578 Common Victualler licences are the same restaurants as the ISD source and are excluded to avoid double-counting. Coordinates are `gpsx`/`gpsy` in **EPSG:2249** (state plane, US survey feet), reprojected in step 2 — not lat/lon. `applicant`, `manager`, `day_phone` and `evening_phone` are NOT selected | 2026-09-21 |
| Boston | Cannabis Active Licenses (CKAN resource `e395fd88-0f81-4399-a57a-3e94a74b145c`, 43 rows) | **Retail** — dispensaries | same endpoint | `status='Active'`; same `gpsx`/`gpsy` convention as the Licensing Board set. The one `Delivery (operator)` row is excluded — no shopfront | 2026-09-21 |
| Boston — **recorded, deliberately NOT used** | Business Inventory (CKAN resource `47bd8208-f648-4309-8f65-de7416d63157`, 2,634 rows) | Would cover **all three buckets**, and is the only Boston source that reaches Personal services | same endpoint | — | 2026-09-21 |
| Edmonton | City of Edmonton Business Licences (Socrata `qhi4-bdpu`) | All three buckets, via its own `business_licence_category` taxonomy | `https://data.edmonton.ca/resource/qhi4-bdpu.csv` | none (`$limit=60000`; the whole file is 43,672 rows, so the raw capture stays a faithful snapshot and step 2 does the filtering) | 2026-09-21 |
| Toronto | Municipal Licensing & Standards (CKAN `169e90ba-3ae0-43dd-8b2f-919e87002f50`) | **Food service and Personal services**, via its own MLS `Category`. **NOT general retail** — see below | `https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/169e90ba-3ae0-43dd-8b2f-919e87002f50?format=csv` | none at download; step 2 drops cancelled licences and reads only 6 of 19 columns | 2026-09-21 |
| Toronto — **geocoder, not a business source** | One Address Repository (CKAN `64d4e54b-738f-4cd9-a9e7-8050fac8a52f`) | 525,440 address points, same licence as the business data | `https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/address-points-municipal-toronto-one-address-repository/resource/64d4e54b-738f-4cd9-a9e7-8050fac8a52f/download/Address%20Points%20-%204326.csv` (~183 MB; the space in the filename is percent-encoded and the resource id is the one in the row above) | none (whole file) | 2026-09-21 |
| Vancouver | City of Vancouver Business Licences (Opendatasoft Explore v2.1, dataset `business-licences`) | All three buckets, via its own `businesstype` — 93 values and **single-valued**. Three of the six Canadian registers profiled hold several categories per row, each with a different delimiter; this is not one of them, so it needs no splitting | `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences/exports/csv` — **SEMICOLON-delimited**, an Opendatasoft portal-wide default rather than a Vancouver quirk, requested with `with_bom=false` | `where=folderyear='26' AND status='Issued'`, plus an explicit 14-column `select` — `licencersn,licencenumber,businessname,businesstradename,businesstype,businesssubtype,unit,unittype,house,street,city,localarea,numberofemployees,geo_point_2d` — that deliberately omits `geom` (the full geo_shape; only `geo_point_2d` is needed and the polygon would multiply the download for nothing). **`folderyear` is the licence vintage and it ROLLS** — `'26'` was verified current on 2026-09-21 at 73,075 rows against 69,889 for `'25'`, so re-check it before a rebuild rather than trusting the string. This registry publishes NO registrant-name column, so there is nothing to omit at the download boundary; `businesstradename` is blank on 49.6% of mappable rows, and the `businessname` fallback is handled at the label by `NAME_FALLBACK_POLICY`, not here | 2026-09-21 |
| Vancouver | **Property Parcel Polygons** and **Property Tax Report** (Opendatasoft, same portal) | Not businesses — **joined** to the above for the residence check. Vancouver is the only Canadian city with no licence-level home-business flag, and BC Assessment is not open data, so the US-style parcel inference is the only residence signal available | `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/property-parcel-polygons/exports/geojson` and `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/property-tax-report/exports/csv` | Parcels: none. Tax report: `where=report_year='2026'` and `select=land_coordinate,legal_type,zoning_classification,zoning_district`, exported with the same `delimiter=;` and `with_bom=false` as every other Opendatasoft CSV here — four columns of one year, ~229k rows against the full file's 1,553,448 across seven report years. **The address join is REJECTED, not untried:** tested 2026-09-21 at 6.5% matched (direction prefixed in licences and suffixed in the tax roll, `AV` against `AVE`, civic numbers stored as ranges), so the join is spatial — business point → parcel `tax_coord` → `land_coordinate` → `zoning_classification`. No mailing address and no owner field is downloaded, and neither value is ever published | 2026-09-21 |
| Surrey | Surrey Business Directory (ArcGIS Hub item `468ff5ff67354da5be095a9bce006137`) — **licence-derived despite the name** | All three buckets, via its own `BusinessCategory`. The column is **newline-delimited** and 4,837 of 27,082 rows carry more than one category, so a naive `value_counts()` returns 628 *combinations* against **210** real values | `https://hub.arcgis.com/api/download/v1/items/468ff5ff67354da5be095a9bce006137/csv` (`layers=0`) | **None server-side — the Hub export takes no field list and no `where`.** Scope is applied in step 2 on `LicenseType`: Home Occupation (14,015 of 27,082, 51.8%) is dropped and Commercial/Industrial kept, which is a scope correction first and a privacy one second, and it is the City's own assertion rather than this project's inference. **Two traps at the endpoint itself:** the download is **asynchronous** — the first call returns **HTTP 202** with a JSON job status (whose body usefully carries `recordCount`) and the CSV only on a later call — and it serves `application/octet-stream`, **not `text/csv`**, so a content-type check for "csv" rejects a perfectly good 4.4 MB download, which it did twelve times during Step 0. `PhoneNumber` comes back from the server, is dropped in step 2 and asserted absent | 2026-09-21 |
| Montréal | Ville de Montréal **`locaux-commerciaux`** — an annual FIELD SURVEY of street-level commerce, not a licence register (CKAN resource `01ded48e-f982-4703-975e-4be0769ef3ee`, `occupation-commerciale-2025.csv`, 28,621 rows) | All three buckets, via `SCIAN` — **which IS NAICS**, so `pipeline/taxonomies/naics.py` applies unchanged and this is the only Canadian city needing no taxonomy module of its own | `https://donnees.montreal.ca/dataset/f8582c4d-a933-4306-bb27-d883e13dd207/resource/01ded48e-f982-4703-975e-4be0769ef3ee/download/occupation-commerciale-2025.csv` | None (whole file). **A plain client gets `RBAC: access denied`** — browser headers are required, and that is portal-wide rather than specific to this dataset. The package holds 2021-2025 as separate resources and **gains one a year**, so re-check `package_show` for `locaux-commerciaux` rather than trusting this resource id. There is no registrant-name column at all, so no pin can display a person's name this pipeline substituted — a structural claim, as in New York and Miami, not a measurement | 2026-09-21 |
| Calgary | City of Calgary Business Licences (Socrata `vdjc-pybd`, 23,203 rows) | All three buckets, via its own `licencetypes` taxonomy — **a register that names premises itself**, which most here leave to be inferred, suffixing its categories `- PREMISES`, `- NO PREMISES`, `(MOBILE)`, `(HOME BASED)`, `(MAIL ORDER)` and `(DIRECT SALES)`. The column is **`,\n`-delimited — a comma AND a newline** — with 9,136 rows carrying more than one category; splitting on the bare newline shreds each value and counts the fragments, which is what produced the "173 categories" the Canada profile recorded. The real count is **96** | `https://data.calgary.ca/resource/vdjc-pybd.csv` | `$limit=60000` and nothing else — the whole table, so the raw capture stays a faithful snapshot and step 2 does the filtering (`jobstatusdesc` keeps five of seven values, dropping the 194 rows that are mid-move or mid-close: a relocating premises' recorded address is the one thing this map depends on and the one thing in doubt). **`$limit` is not optional — Socrata's default page is 1,000 rows.** `point` is a WKT `POINT` string on 100% of rows, so there is no geocoding step; `tradename` is blank on ZERO rows, so there is no name fallback and no personal-name exposure from one. `homeoccind` is `N` on all 23,203 rows — constant, not merely unreliable, so it is not a usable home-business discriminator and is not used at all. The register publishes no owner, agent or contact column; step 2 asserts the absence anyway | 2026-09-21 |
| Mexico City | **INEGI DENUE** — Directorio Estadístico Nacional de Unidades Económicas, entidad federativa **09 (Ciudad de México)**. A **national statistical register**, not a municipal licence file: the first business source here that is neither, and the reason one description covers every Mexican city | All three buckets, via **SCIAN** — `pipeline/taxonomies/scian.py`, **never `naics.py`**: SCIAN numbers retail **46** where NAICS uses 44-45 (and wholesale 43 against 42), so NAICS prefixes match nothing under 44/45 and would leave **45.87% of the file** unclassified. 462,732 units in the entidad → 442,146 `Fijo` → 283,346 in the three storefront buckets. `latitud`/`longitud` are populated on **100%** of rows and `nom_estab` on 99.95%, so this city needs no geocoding leg at all | `https://www.inegi.org.mx/contenidos/masiva/denue/denue_09_csv.zip` — 45,439,249 bytes, confirmed a real ZIP **by magic bytes rather than by the served filename**; member `conjunto_de_datos/denue_inegi_09_.csv` (**note the trailing underscore before `.csv` — INEGI's own naming, not a typo**); **latin-1, and a UTF-8 decode raises** | **None, and none is possible — INEGI serves one static ZIP per entidad and accepts no query.** For this city the download IS the scope: entidad 09 is the city, which is why no `CITY_KEEP` exists here and one does for Guadalajara. Step 2 reads **10 of DENUE's 42 columns** and drops `Semifijo` street stalls (95.55% of rows are `Fijo`). **The ZIP holds a plausible near-miss:** `diccionario_de_datos/denue_diccionario_de_datos.csv` parses cleanly as CSV and returns 43 rows of column documentation — which looks like a very small city rather than an error. Name the member explicitly; never take the first `.csv` in the archive. The DENUE **API** (`/app/api/denue/v1/consulta/`) is deliberately not used: it 404s without a token and is less complete | 2026-09-22 |
| Guadalajara | **INEGI DENUE**, entidad federativa **14 (Jalisco)** — the same national register, licence, encoding, taxonomy and forbidden columns as Mexico City, which is why Guadalajara became the first city here to need **no new notice at all** | All three buckets, via **SCIAN**, transferred from Mexico City unchanged. 401,813 units statewide; **196,907 in the four municipios this build keeps** → 193,139 `Fijo` → 117,698 storefront | `https://www.inegi.org.mx/contenidos/masiva/denue/denue_14_csv.zip` — 39,432,220 bytes, magic-bytes checked; member `conjunto_de_datos/denue_inegi_14_.csv`; **latin-1** | **None server-side.** **Unlike Mexico City the entidad is NOT the city** — Jalisco holds 125 municipios including Puerto Vallarta 300 km away — so step 2 scopes on DENUE's own `municipio` spelling to Guadalajara (97,134), Zapopan (53,311), **San Pedro Tlaquepaque** (26,832) and Tlajomulco de Zúñiga (19,630). **The spelling IS the join interface: "San Pedro Tlaquepaque", not the "Tlaquepaque" SITEUR's own prose uses** — matching the operator's wording keeps ZERO rows, which is Los Angeles' `CITY_KEEP` trap and Toronto's "former Toronto" trap in one. **Tonalá is deliberately excluded** although DENUE holds 19,897 units there: no line reaches it, and a municipio with no station contributes businesses no ring can ever contain. `Fijo` only — 97.94% here against Mexico City's 95.55%, so street commerce is a smaller share of this city | 2026-09-22 |
| Madrid | Ayuntamiento de Madrid **Censo de locales, sus actividades y terrazas de hostelería y restauración** (CKAN package `200085-0-censo-locales`, resource `200085-5-censo-locales` — the locales × actividades join, 225,660 rows × 47 columns) | All three buckets, via the city's own `epigrafe` scheme — a **premises field survey**, not a licence register, so the Montréal and Barcelona shape rather than the Philadelphia one | **Resolved at fetch time**, not hardcoded: `https://datos.madrid.es/api/3/action/package_show` is queried for the package and the download URL taken from the resource whose id is `200085-5-censo-locales`. **THE DOWNLOAD URL ROTS** — it embeds a build timestamp (`200085_20260922_053829.csv`) that changes on every refresh, so a hardcoded URL 404s silently within days. The first source in this project whose URL is not durable. Note `datos.madrid.es` is **CKAN 2.9.11 at the bare host**; an earlier screen recorded it unreachable on the path `/egob`, which was a fact about the guess rather than about the portal | none server-side (CKAN serves the whole file). **UTF-8 WITH BOM and SEMICOLON-delimited**, both declared in `config.py` rather than inferred — a BOM read as data corrupts the first column name. Step 2 keeps `desc_situacion_local == 'Abierto'`, which is also the residence filter: the register carries **`Uso vivienda` (8,486)** as its own status, so residence is answered by the source rather than inferred, Canada's licence-level pattern rather than the US parcel join. **This register carries NO registrant name at all** — all 47 columns were listed on 2026-09-22 and not one is an owner, titular, NIF/CIF, razón social or contact field, the same structural position as Edmonton's register; step 2 asserts twelve personal column names stay absent and **raises** if a kept premises lacks its `rotulo` | 2026-09-22 |
| Barcelona | Ajuntament de Barcelona **Cens de locals en planta baixa amb activitat econòmica** (CKAN package `cens-locals-planta-baixa-act-economica`, resource `99764d55-b1be-4281-b822-4277442cc721`) | All three buckets, via the census's own four-level Catalan activity scheme — a **premises field survey**, not a licence register, so the Montréal and Madrid shape rather than the licence cities'. **THE YEAR IS A DECISION:** the **2022** survey holds 66,088 rows and is complete; the **2024** resource (`38babeec-5c47-43d3-84e7-b13a4b89004f`) holds 44,000 and is **geographically incomplete** — Sant Andreu −83%, Nou Barris −76%, Horta-Guinardó −69% against 2022, while Ciutat Vella is −5%, so a map built on it would show the periphery as commercially dead | `https://opendata-ajuntament.barcelona.cat/data/api/3/action` — `datastore_search`, paged at 10,000 | `fields=` restricted to **11 of the census's 50 columns**, and that list IS the privacy control. `Nom_Local` is a trade name and 100% populated, so there is **no registrant-name column to fall back to**; `Referencia_Cadastral` exists in the source and is deliberately never requested. **The vacancy filter is applied in step 2 and is mandatory**: `Nom_Principal_Activitat` is `Actiu` on 58,908 rows and `Sense activitat Econòmica` on 7,180 — empty units for sale or to let. Licence **CC BY 4.0** plus the Open Data BCN terms — notice **21**, and the outstanding duty to notify the Council | 2026-09-22 |
| Dublin | Tailte Éireann **rateable valuation register** (the Irish non-domestic valuation list), queried per local authority across the four Dublin councils | All three buckets, via the register's own `Uses` field — a **rateable-property register**, a fourth shape after the licence registers, the national establishment registers and the premises field surveys. **`Category` (13 values) cannot be used**: it puts 1,483 of 2,335 food-service rows and 677 of 744 personal-service rows inside `RETAIL (SHOPS)`, so all three buckets collapse. `Uses` (963 values, 318 distinct segments) is the only level that separates them, and it is keyed by SEGMENT because the field is comma-separated with `-` as a null placeholder | `https://opendata.tailte.ie/api/Property/GetProperties?Fields=*&LocalAuthority=<AUTHORITY>&Format=json&Download=false` — no key, no account. **Two predecessor hosts are dead and neither redirects**: `api.valoff.ie` is NXDOMAIN and `www.valoff.ie` answers 000, which is why an earlier screen recorded the whole country as negative | none server-side. ⚠️ **`LocalAuthority` is matched EXACTLY and a wrong string returns HTTP 200 with an EMPTY LIST**, not an error — the register spells one council `DUN LAOGHAIRE RATHDOWN CO CO` where the boundary layer spells it `DUN LAOGHAIRE-RATHDOWN COUNTY COUNCIL`, so the join is an explicit mapping table and `fetch_sources.py` asserts a non-trivial row count per authority. **This register carries NO name column of any kind** — no trade name, no occupier, no ratepayer, no owner; step 2 asserts that and EXITS if one ever appears, so the pin label is the street address and Los Angeles' blank-trade-name failure cannot occur here. **`Eircode` is dropped at load** (third-party database right). Licence CC BY 4.0 — notice **22** | 2026-09-22 |
| Milan | Comune di Milano, **six premises registers** on one CKAN portal: `ds49-economia-esercizi-vicinato-sede-fissa` (28,131 neighbourhood shops), `ds58_economia_pubblici_esercizi_in_piano` (9,269 bars and restaurants inside the commercial plan), `ds62_economia_parrucchieri_estetisti_centri_abbronzatura` (5,732 personal services), `ds59-economia-pubblici-esercizi-fuori-piano` (3,799 outside the plan), `ds250-economia-artigianato-settore-alimentare` (1,471) and `ds251-economia-panificatori` (443 bakers) | All three buckets, and **the register IS the classification**. Every in-dataset classification field is unusable — `codice_ateco` **7.1% populated**, `settore_merceologico` 66 distinct values for what should be three (half of it pure case variation, plus 2,759 concatenated rows), `tipo_eser_storico_pe` 60% blank, `settore_storico_pe` 64% — while `Area di Competenza` is a single clean value per dataset at 100%. So bucket = source, which is `multi-source-city`'s *membership is often the classification* in its purest form | `https://dati.comune.milano.it/api/3/action/datastore_search`, paged at 10,000, one call per register. Search control-tested: `zzqqxxnonsense` returns 0 where `esercizi di vicinato` returns 64 | none server-side. ⚠️ **NO CROSS-SOURCE DEDUPLICATION, which runs OPPOSITE to New York's decision** — the six are measurably disjoint (`Codice` unique within each, **zero** collisions between any pair, distinct prefixes EV/PA/AE/PE/FP), address cannot be a key (**15,613 of 28,131** `vicinato` rows already share one with another row in the SAME register) and `insegna` is too sparse to merge on. A shop and a bar at one Milan address are two premises. ⚠️ **`fuori piano` is at least 15.9% not a public storefront** — 472 staff canteens, 132 private clubs, 53 parish clubs — and that is a FLOOR, because its clause column is 62.4% blank. **No register carries a personal name** (no `titolare`, `ragione_sociale` or `nominativo`; step 2 exits if one ever appears), so the pin falls back to the address and Los Angeles' failure mode cannot occur. Licence **CC BY 4.0** — notice **23** | 2026-09-22 |
| Paris | **INSEE SIRENE `StockEtablissement`** (the national *établissement* register, 44,064,115 rows) **joined on `siret` to INSEE's separate geolocation file** (37,901,783 rows) — two datasets, one city row, because neither is usable without the other | All three buckets, via **NAF rév. 2 at the sous-classe** (`pipeline/taxonomies/france_naf.py`, national — five French cities share it). **148,633** active Paris rows in divisions 47/56/96. Coordinates are a JOIN, not a geocode: coverage is **99.96%** (148,576 of 148,633), so Paris has no geocoding step, no key and no rate limit anywhere in the build | `https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/` → the **parquet** resource whose title carries the trailing ` -` (2,210 MB; the ZIP is 2,867 MB), and `https://www.data.gouv.fr/api/1/datasets/geolocalisation-des-etablissements-du-repertoire-sirene-pour-les-etudes-statistiques/` → parquet, 811 MB. **Use the parquet**: it is columnar, so step 2 reads ten columns of fifty-four, and its footer is readable over HTTP range requests — which is how every figure here was measured without downloading 3 GB | `codeCommuneEtablissement` prefix **`751`**. ⚠️ **ACTIVE IS THE LETTER `A`, NOT THE LABEL `Actif`** — filtering on `Actif` returned **zero rows for all six French cities** and was caught only because Paris ran first as a control against a known-good number; keep the control. ⚠️ **`StockUniteLegale` is a DIFFERENT resource** sitting beside it (30,020,346 legal units keyed on `siren`) and mapping it produces the registered-office map this project exists not to make — it was pulled first by mistake while writing France's profile. It is nonetheless the file the natural-person suppression test reads (`categorieJuridiqueUniteLegale`), so it is named rather than avoided. ⚠️ **`etablissementSiege` does NOT separate premises from offices here** — 90.8% of active bucket rows are siège, because a sole trader's shop is its own siège. ⚠️ **13.4%** of active bucket rows are masked at source (`statutDiffusionEtablissement` ≠ `O` hides the name, the address **and** the geolocation), so France does part of the privacy work upstream — per `read-licence` 6b, check what survived rather than only what was removed. ⚠️ The geolocation file carries a **per-row `epsg` column** (2154 Lambert-93 on 99.3%, plus 2975/5490/2972 for the DOM) and its own `qualite_xy` confidence, where **class 33 is commune-centroid grade** and must not be drawn as a street address. Licence **Licence Ouverte 2.0** (`lov2`) | 2026-09-22 |
| Marseille | **INSEE SIRENE `StockEtablissement`**, the same national parquet Paris reads, joined on `siret` to the same INSEE geolocation file — **one register, one cache, five cities** | All three buckets via NAF rév. 2 at the sous-classe, `pipeline/taxonomies/france_naf.py`. **18,177 storefronts** built 2026-09-23 from 20,448 rows in divisions 47/56/96, coordinate coverage **99.94%** | The two dataset endpoints are Paris's row above, unchanged — resolved through the data.gouv API, never hard-coded. ⚠️ **The parquets are cached ONCE for the country** at `data/france/raw/`, not per city: they are 3 GB for the pair and identical for every French city, so the per-city layout the scaffold implies would hold 15 GB across five. Mexico is deliberately NOT treated this way — DENUE is partitioned per *entidad federativa*, so its two cities read genuinely different files | `codeCommuneEtablissement` prefix **`132`** (16 arrondissements, 13201–13216). ⚠️ **`13055` is Marseille's code for the BOUNDARY API and is NOT this column's value** — two code systems for one city, and mixing them returns zero rows silently. Every national trap is Paris's: active is the letter **`A`** not `Actif`, `StockUniteLegale` is a different file and is never joined, the `epsg` column is read per row. **Catch-all verdict measured independently and matched Paris almost exactly**: `96.09Z` 9.8% here against Paris's 9.6%, `56.29B` 1.0% against 1.0% — both excluded on INSEE's own class labels. Licence **Licence Ouverte 2.0** (`lov2`) | 2026-09-23 |
| Toulouse | **INSEE SIRENE `StockEtablissement`**, the same national parquet Paris and Marseille read, joined on `siret` to the same INSEE geolocation file — **one register, one cache, three cities so far** | All three buckets via NAF rév. 2 at the sous-classe, `pipeline/taxonomies/france_naf.py`. **8,635 storefronts** built 2026-09-23 from 13,741 rows in divisions 47/56/96, coordinate coverage **99.93%** | The two dataset endpoints are Paris's row above, unchanged — resolved through the data.gouv API, never hard-coded. The 3 GB parquet pair was already cached by Paris's run at `data/france/raw/`, so this city downloaded **nothing**: the shared-cache decision paying off for the second time | `codeCommuneEtablissement` **`31555`**. ⚠️ **An EXACT code, not a prefix family** — Toulouse has no arrondissement subdivision, unlike Paris (751xx) and Marseille (132xx), and here the SIRENE code and the boundary code coincide, which is a coincidence rather than a rule. ⚠️ **20.2% of active rows are masked at source** (`statutDiffusion` ≠ `O`) — the highest of the six French candidates and well over double Paris's 8.5%; INSEE strips name, address and geolocation together, so those rows cannot reach the map at all. The brief estimated 16.0% from a sample and was **low**. **Catch-all verdict measured independently and DIVERGED from both siblings**: `96.09Z` **13.9%** here against Paris's 9.6% and Marseille's 9.8%, `56.29B` 1.6% against 1.0% — both excluded on INSEE's own class labels, and the exclusion flattened step 2's own discriminator from 26.4%/8.8% catch-all-by-employee-band to 5.8%/5.8%. Licence **Licence Ouverte 2.0** (`lov2`) | 2026-09-23 |
| Lille (Regional) | **INSEE SIRENE `StockEtablissement`**, the same national parquet every French city reads, joined on `siret` to INSEE's geolocation file — **the fourth French city on one cache, and the first whose filter is a set of communes rather than one** | All three buckets via NAF rév. 2 at the sous-classe, `pipeline/taxonomies/france_naf.py`. **11,833 storefronts** built 2026-09-23 from 18,811 rows in divisions 47/56/96, coordinate coverage **99.98%** | The two dataset endpoints are Paris's row above, unchanged; the 3 GB pair was already cached | `codeCommuneEtablissement` in the **eleven communes the network serves** (59009, 59163, 59328, 59350, 59368, 59378, 59410, 59421, 59512, 59599, 59646) plus the legacy codes **59355** (Lomme, 22 rows) and **59298** (Hellemmes, 2). ⚠️ **MEL codes Lomme and Hellemmes as communes of their own; SIRENE does not** — 226,204 rows sit under 59350 — so a filter built from MEL's labels would not have matched INSEE's. Masked at source **16.6%** across the eleven (the brief's 9.6% was the commune of Lille alone, from a sample: a different denominator, not a correction). **Catch-all measured**: `96.09Z` 11.2%, `56.29B` 1.6%, both excluded, with Toulouse's discriminator signature (23.4% vs 7.5% catch-all by employee band). Licence **Licence Ouverte 2.0** (`lov2`) | 2026-09-23 |
| Rennes | **INSEE SIRENE `StockEtablissement`**, the same national parquet every French city reads, joined on `siret` to INSEE's geolocation file — **the fifth and last French city on one cache** | All three buckets via NAF rév. 2 at the sous-classe, `pipeline/taxonomies/france_naf.py`. **3,479 storefronts** built 2026-09-23 from 5,451 rows in divisions 47/56/96, coordinate coverage **99.97%** | The two dataset endpoints are Paris's row above, unchanged; the 3 GB pair was already cached | `codeCommuneEtablissement` **`35238`**, an EXACT code like Toulouse's — Rennes has no arrondissements. Masked at source **17.5%** of active rows, and **15.9%** of active rows in the three divisions. ⚠️ **The brief's 9.8% was measured on that same bucket denominator, from a 12.6% sample, and was low** — Toulouse's brief was low the same way (16.0% against 20.2%). **Catch-all measured**: `96.09Z` 14.0%, `56.29B` 1.7%, both excluded, with Toulouse's discriminator signature — 28.8% vs 9.8% catch-all by employee band, measured with NOTHING excluded because step 2 prints it after the exclusion. Premises name on **59.1%** of storefronts, the best of the five. Licence **Licence Ouverte 2.0** (`lov2`) | 2026-09-23 |

**The two Mexican cities are one source, not two**, and that is why each takes a
single row where Vancouver/Surrey takes two. DENUE is national, so
`pipeline/countries/mexico.py` holds the URL shape, the member path, the
encoding, the column names, the `Fijo` filter and the licence, and a city
config contributes **only its two-digit entidad code**. Guadalajara spans four
municipios and still takes one row, because all four arrive in one ZIP from one
publisher under one set of terms — the opposite of Vancouver/Surrey, which
needs two rows because it is genuinely two registries, two portals and two
licences.

**Neither Mexican city loads a personal column, and the claim is structural
rather than measured.** `FORBIDDEN_COLUMNS` — `telefono` (35.6% populated in
CDMX), `correoelec` (22.6%), `www` (10.6%) and `raz_social` (25.9%) — are
absent from `USECOLS`, and each city's step 2 asserts they never arrive, which
is New York's pattern. INEGI already omits `raz_social` where the owner is a
*persona física*, and says so in its own data dictionary; it is still not
loaded, because `nom_estab` is DENUE's name for the sign *"visible y escrito en
rótulos, fachadas o anuncios luminosos"* — the shopfront — and is populated on
99.95% of rows, so there is no blank-name fallback of the kind that published
~4,000 individuals' names in Los Angeles. `numero_int`, the structured
interior/unit number, **is** loaded so its rate can be reported (13.4% in CDMX,
7.1% in the Guadalajara region) and is deliberately never written to
`businesses_clean.csv`: publishing a unit number in order to check for unit
numbers would defeat the purpose. `scripts/check_personal_exposure.py`
therefore records both cities' residence check as a **GAP**, as San Diego's and
Boston's are, rather than as a pass.

The Philadelphia parcel join exists to answer one privacy question the address
text cannot: **is this "business" someone's home?** Only two derived values are
selected — the City's own `category_code_description` land-use category, and a
boolean for whether a homestead exemption is claimed (Philadelphia grants that
only on an owner's primary residence). The exemption *amount* is not
downloaded, and no mailing address is downloaded at all. Neither value is ever
published: the rendered map emits only name, category, station and ring. Same
"City of Philadelphia License" as the licence data, already recorded below.

New York needs four because it has **no general business licence** — see
`pipeline/taxonomies/new_york.py`. Most cities here need one.

Philadelphia is the opposite lesson: a **multi-source hunt that came back
empty**, which is why it maps two buckets from one registry rather than three
from several. Each archetype in the `multi-source-city` skill was checked live
on 2026-09-21 and failed, and each is recorded here so it is not re-checked
from scratch:

| Candidate for Philadelphia's missing buckets | Why it is unusable |
|---|---|
| PA Professional Licensee Data (Socrata `fwj2-whnj`, data.pa.gov) | Aggregate `active_count` **by county**, with no addresses. Pennsylvania does not publish licensee locations; the State Board of Cosmetology's PALS system is a per-licence lookup with no bulk export |
| PA Agriculture food inspections (Socrata `etb6-jzdg`, data.pa.gov) | Does reach Philadelphia, but `organization_name` is "City of Philadelphia" — it relays the city's own inspections, so it duplicates the registry above rather than adding to it |
| Philadelphia Commercial Activity Licenses (Carto `com_act_licenses`) | The general licence every city business needs, and unusable on three counts: **0 of 528,413 active rows have geometry**, there is no business address at all (only the owner's *mailing* address), and `licensetype` is the single value "Activity" with no classification. It also carries `legalfirstname`/`legallastname` |
| Carto `li_business_licenses` | A **stale copy** of the registry above — 360,192 rows vs 435,143, "Towing" where the current table says "Tow Truck", and missing `unit_type`. Not a second source |

An `ILIKE` sweep for hair / barber / salon / nail / cosmet / massage / tattoo /
laundry across both Carto licence tables returns nothing, so **Personal
services has no source in Philadelphia at all**. That is recorded in
`docs/excluded_categories.md` under what is *missing* rather than *excluded*.

**Edmonton's register publishes NO name column but the business's**, as
Madrid's does. No registrant, owner, licensee or contact field exists, so its
privacy position is structural rather than measured: no pin *can* be a person's
name. `pipeline/edmonton/fetch_sources.py` asserts this at download rather than
assuming it. Its `licencetype` field separates commercial premises from
`Home Based` (14,114), `Non-Resident` (2,108) and two individual-held types, so
Edmonton needs no residence inference at all — and the City replaces the
address with `<REDACTED FOR PRIVACY>` on 4,074 rows, **taking the coordinates
with it** (redacted rows carrying coordinates: zero).

**Toronto's register carries NO coordinates**, and unlike France's SIRENE -
which also carries none, but has a separate INSEE geolocation file to join to -
nothing but the address can place a row. So the address repository is a
required input rather than a convenience — Canada has no national bulk
geocoder. The join key is `Licence Address Line 1` with the unit
stripped (the register writes `280 SPADINA AVE, #308`; the repository carries no
units), which takes the match from 48.1% to **93.8%** of storefront rows.

**Its `MUNICIPALITY_NAME` is NOT a city filter**, despite looking like one: it
holds the six pre-1998 municipalities that amalgamated into Toronto, so matching
"Toronto" keeps 30% of the city. Los Angeles' `CITY_KEEP` trap. The boundary
polygon (`regional-municipal-boundary`, 641.4 km²) is the check.

**Toronto also publishes THREE personal columns** — `Client Name`, `Business
Phone`, `Business Phone Ext.` — and step 2 excludes them at `usecols`, so they
never enter the process. The Canada profile recorded one of the three.

These rows, with the transit and boundary rows below, close a gap a NOTE
here recorded from 2026-09-21 to 2026-09-22: Vancouver, Surrey, Montréal and Calgary were built with their
endpoints in [`canada_step0_endpoints.md`](canada_step0_endpoints.md) and their
notices below, but never in these three tables.
**Where the two files disagree, these tables win** — they were written from
each city's own `config.py` after the build, and three Step 0 findings did not
survive it. Surrey's declared-4326-but-actually-26910 CRS trap belongs to the
Hub's **file export**, not to the service the build reads. Calgary's real
category count is 96, not 173. TransLink's feed does carry `feed_info.txt`; it
is the mirror that does not. `canada_step0_endpoints.md` stays as the evidence
trail for how each source was found and what was tried; every city it covers
is now built.

Montréal's survey has one consequence no licence register has: it **records
VACANT units**, `USAGE1 == 'VACANT'` on 3,500 of 28,621 rows (12.2%), and they
are excluded in step 2 because an empty shopfront is not a business. The
narrower `VACANT_A_LOUER` flag ("vacant and for rent", `Oui` on 712) is not a
substitute for it.

### Boston — Step 0 findings, 2026-09-21

Probed but **not built**; the verdict on whether to build it is open in
`PLAN.md`. Four things here are worth not rediscovering.

**Boston licenses food, and almost nothing else.** Inspectional Services
licenses food; the Licensing Board licenses alcohol, lodging, billiards and
bowling. There is no general business licence and no personal-service licence.
Deduplicated to premises: **Food service 2,237**, **Retail 385** unambiguous
(`RF`-only), plus 306 package stores and 43 cannabis shops that *overlap* the
`RF` set — "Go Fresh 365 / Ming's Supermarket" holds both an `RF` licence and a
`Retail All Alc.` licence at 1102 Washington St, so cross-source dedup is
mandatory rather than optional.

**The official "Active Food Establishment Licenses" extract silently drops a
category, so do not use it.** Resource `f1e13724-284d-478c-b8bc-ef042aa5b70b`
(3,345 rows) is exactly `FS` 1,762 + `FT` 1,583 licences and contains no `RF`
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
| Massachusetts Board of Registration of Cosmetology and Barbering | The state licenses salons, barbershops and manicuring shops, and publishes **no address-bearing export**. Its register is the ePLACE / MADOL portal (`occupationallicensingandpermitting.mass.gov/madol/s/license-search-page`), a per-licence lookup with no bulk download — the same shape as San Jose's rejected third-party tool and Pennsylvania's PALS |
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
deliberately unused. Its licence is also the only "not specified" one on the
portal.


### Madrid — endpoints and findings, verified 2026-09-22

**The first Spanish city, and the first anywhere in this project whose rail
comes from an operator's ArcGIS feature services rather than a feed.** Country
profile: `docs/spain_step0_endpoints.md`. Step 0 evidence and its checks:
`docs/build_briefs/madrid.md` (13/13).

**Businesses** — Ayuntamiento de Madrid, *Censo de locales, sus actividades y
terrazas de hostelería y restauración*. `datos.madrid.es` is **CKAN 2.9.11 at
the bare host** (an earlier screen recorded it unreachable on the path
`/egob` — a fact about the guess). Package `200085-0-censo-locales`, resource
**`200085-5-censo-locales`**, the locales × actividades join: 225,660 rows ×
47 columns, **UTF-8 with BOM, semicolon-delimited**, coordinates in
**EPSG:25830**.

> **THE DOWNLOAD URL ROTS.** It embeds a build timestamp
> (`200085_20260922_053829.csv`) that changes on every refresh, so
> `step2_clean_businesses.py` resolves it from `package_show` by **resource
> id** at fetch time. This is the first source in the project whose URL is not
> durable, and a hardcoded one 404s silently within days.

A **premises field survey**, not a licence register — the Montréal and
Barcelona shape — so the "79% of this register is landlords" correction that
Philadelphia and Washington D.C. need does not apply.

**This register carries no registrant name at all** - the same structural
position as Edmonton's, where no pin can be a person's name. All 47 columns
were listed on
2026-09-22 and not one is an owner, titular, NIF/CIF, razón social or contact
field; the only name-shaped column is `nombre_agrupacion`, which names a
**market or shopping centre** a unit sits inside, and step 2 does not load it.
New York, Philadelphia, Miami and Boston all HAVE such a column and decline to
download it. Madrid has none to decline. Step 2 asserts twelve personal column
names stay absent, loads columns by name, and **raises** if any kept premises
lacks a `rotulo` (shop sign) — so there is no fallback path even in principle.

**Residence is answered by the source, not inferred.** `desc_situacion_local`
carries **`Uso vivienda` (8,486)** — the unit reverted to residential use — as
its own status value, and step 2 keeps only `Abierto`. Canada's licence-level
pattern rather than the US parcel join.

> **THE COORDINATE COLUMNS ARE 100% POPULATED AND PARTLY INVALID**, and the
> zeros are stored as the **string `'0.0'`**, so an is-it-populated test passes
> them. In EPSG:25830 a zero projects to the Atlantic off West Africa and
> vanishes on a station-radius map rather than erroring. Measured on the full
> download: **34,316 of 159,787 open rows (21.48%)**, but only **9.21%** once
> the storefront filter is applied — the zeros concentrate in tourist flats
> (85.9%), hostales (74.7%) and offices, categories this project does not map.
> **Unlike Los Angeles the loss is biased AWAY from the mapped rows**, so no
> geocoding leg is needed and Spain's CartoCiudad stays unprobed.

**Rail** — Consorcio Regional de Transportes de Madrid (CRTM),
`services5.arcgis.com/UxADft6QPcvFyDU1/arcgis/rest/services/M4_Red/FeatureServer`,
layer **0 `M4_Estaciones`** (293 station-per-line points) and layer
**4 `M4_Tramos`** (560 polylines). Both natively **EPSG:25830**, the same CRS as
the premises data, so the build never reprojects for geometry.

> **NOT the GTFS, and that is a LICENCE consequence rather than a preference.**
> CRTM publishes the same network twice: a GTFS feed it stopped refreshing in
> **2025-05-30**, and feature services it still edits (**2026-06-05**). Its
> licence obliges a reuser to keep displayed information *"siempre
> actualizada"*, which a feed abandoned sixteen months ago cannot satisfy.
> `scripts/brief_check.py` watches the feature layers' `editingInfo.lastEditDate`
> with the `arcgis_layer` check kind, because the pre-existing tripwire watched
> the FEED and would have kept passing while the decision it guarded went stale.

**Boundary** — *Término municipal de Madrid*,
`geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/LIMITES_ADMINISTRATIVOS/Termino_Municipal/Termino_Municipal.zip`
(shapefile, EPSG:25830). Step 1 checks its **area (604.0 km²)** and its
coordinate magnitudes rather than its declared CRS — Surrey's declared
EPSG:4326 and contained UTM metres.

**Licences — both PERMITTED WITH CONDITIONS, both `Ley 37/2007` reuse
licences**, which is Spain's country-level pattern.

- **Ayuntamiento de Madrid**: CKAN declares `cc-by` / **CC BY 4.0**, but CC BY
  is not the whole instrument — the portal's *Condiciones generales* are
  **binding by use** (*"obligan a cualquier persona y/o empresa que reutilice
  datos por el mero hecho de hacer uso"*). Reuse for commercial purposes is
  authorised, expressly including *modificación, adaptación, extracción,
  reordenación y combinación*. Conditions: do not distort the sense of the
  information; **cite the source** (a form is offered — *"Origen de los datos:
  Ayuntamiento de Madrid"*); **state the last-update date**; do not suggest the
  Ayuntamiento sponsors the reuse; preserve reuse metadata; and
  **re-identification of anonymised data is expressly prohibited**.
  `/pages/aviso-legal` is a **website disclaimer** written for web pages rather
  than data, so it is recorded as read and not as governing.
- **CRTM**: `https://www.crtm.es/licencia-de-uso`, a *licencia-tipo* under
  Ley 37/2007 art. 4.2(b). Commercial reuse and modification granted.
  Share-alike binds **the data**; *"las obras derivadas añadiendo valor pueden
  ofrecerse bajo licencias diferentes"*, and a ring-density map is a
  value-added derivative rather than a redistribution. Conditions: cite CRTM
  **"especificando si son datos en bruto o explotados"** (a
  disclosure-of-transformation duty, the Montréal and INEGI family — a bare
  credit does not satisfy it); display **"Powered by CRTM"** with a link to
  `http://www.crtm.es/`; do not falsify or damage CRTM's image; preserve reuse
  metadata; do not imply sponsorship. **CRTM monitors access** and may block a
  reuser whose fetching degrades its systems.

> **A CITED LICENCE URL THAT 404s IS NOT AN ABSENT DOCUMENT.** CRTM's own
> dataset metadata points at `datos.madrid.es/egob/catalogo/aviso-legal`, which
> returns 404; the live pages are `/pages/aviso-legal` and
> `/pages/condiciones-de-uso`, found by listing the portal's own links rather
> than guessing a second path.

> ### ✅ RESOLVED 2026-09-22 — the "siempre actualizada" clause is a
> misrepresentation rule, not a liveness requirement
>
> Raised as an owner decision and settled by reading the clause **in place**
> rather than in isolation. It is not free-standing: it is one of **four
> sub-obligations** under a single governing prohibition —
>
> > *"El agente reutilizador tiene expresamente prohibido **desnaturalizar el
> > sentido de la información**, estando obligado a:"*
> > — no manipular con mala fe ni falsear la información
> > — **garantizar que la información mostrada en su sistema esté siempre actualizada**
> > — no menoscabar o dañar la imagen pública del CRTM
> > — no utilizar la información en sitios … actos ilegales
>
> Its three siblings are all about **misrepresentation and reputational harm**,
> so the clause targets presenting stale data *as though it were current* — not
> a requirement that the system be live. No static derivative could satisfy the
> literal reading, and a licence expressly granting *"copia, difusión,
> modificación, adaptación, extracción, reordenación y combinación"* plainly
> does not intend to forbid every static product.
>
> **The next clause confirms the mechanism**: *"Deben conservarse, no alterarse
> ni suprimirse los metadatos sobre **la fecha de actualización**"*. The licence
> expects the data to carry a date and the reuser to preserve it, which is
> exactly how a dated snapshot meets a currency obligation.
>
> **What this project does, which is stricter than the clause requires.** It
> rejected CRTM's own Metro GTFS — which downloads cleanly — precisely BECAUSE
> CRTM stopped refreshing it in May 2025, and took the maintained feature
> layers instead. The notice states CRTM's own last-update date (5 June 2026)
> and that the map shows the network as recorded then. And
> `scripts/brief_check.py`'s `arcgis_layer` check carries `max_age_days` on
> both layers, so this is a commitment a check FAILS on rather than one a
> comment promises.
>
> This is a reasoned position on a clause that is clear once read in context,
> not a generous reading of an ambiguous one — the distinction `read-licence`
> step 8 draws. The full text is stored at
> `docs/licenses/crtm-licencia-de-uso.txt` so the reading can be checked against
> the document rather than against this summary.

**Gate 3 — the operator's published count — RUNS for Madrid and reconciles.**
`metromadrid.es/es/quienes-somos/metro-de-madrid-en-cifras`: **303 estaciones**,
296,78 km, updated 2026-05-18. Against CRTM's 293 station-per-line records plus
Metro Ligero ML1's 9, that is 302 — a residual of **one**, consistent with
Pinar de Chamartín being counted by the operator in both networks. Two of the
operator's own conventions have to be applied first: it counts a station **once
per line** (which is why 303 sits against 242 distinct names) and it **includes
ML1**, which it operates. **303 must never reach the page**: this project maps
**193 distinct stations inside the término municipal**, a different quantity in
three ways at once.

### Dublin — endpoints and findings, verified 2026-09-22

**Not yet built.** Step 0 only, recorded as verified per `add-city` Step 0's
instruction to write endpoints down while they are in front of you. Full
evidence and its checks: `docs/build_briefs/dublin.md` (6/6).

**The first Irish city, and Ireland yields only this one**, so the
`add-country` national questions are answered inside the city brief rather
than in a separate country file.

**Businesses** — Tailte Éireann, the Irish rateable valuation register, through
a keyless JSON API:

```
https://opendata.tailte.ie/api/Property/GetProperties
    ?Fields=*&LocalAuthority=<AUTHORITY>&Format=json&Download=false
```

No key, no account, no registration. **38,265 rows across the four Dublin local
authorities**, of which **13,945 are storefront**. Coordinates are `Xitm`/`Yitm`
in **EPSG:2157 (Irish Transverse Mercator), already in metres, on 99.87% of
rows** — so there is no geocoding step and no reprojection step.

> **TWO PREDECESSOR HOSTS ARE DEAD AND NEITHER REDIRECTS.** `api.valoff.ie` is
> **NXDOMAIN** and `www.valoff.ie` answers **000**. An earlier screen recorded
> Ireland as *negative* on the strength of those two corpses. The API moved
> twice and left no forwarding, and `opendata.tailte.ie/` is itself a 404 with
> no documentation page, no `robots.txt` and no Swagger — the contract is
> stated only in the error body: `Use either Property Number or Local
> Authority`.

> **`LocalAuthority` IS MATCHED EXACTLY, AND A WRONG STRING RETURNS HTTP 200
> WITH ZERO ROWS.** The register spells one authority
> `DUN LAOGHAIRE RATHDOWN CO CO`; the spelled-out
> `DUN LAOGHAIRE RATHDOWN COUNTY COUNCIL` silently returns nothing. The
> **boundary layer spells the same place `DUN LAOGHAIRE-RATHDOWN COUNTY
> COUNCIL`** — hyphenated and unabbreviated. Two strings for one authority, in
> the two sources that must be joined, so the join is an explicit mapping table
> and never string equality.

The four values, with row counts measured 2026-09-22: `DUBLIN CITY COUNCIL`
19,810 · `FINGAL COUNTY COUNCIL` 6,528 · `SOUTH DUBLIN COUNTY COUNCIL` 6,926 ·
`DUN LAOGHAIRE RATHDOWN CO CO` 5,001.

**The register carries no business name.** No trade name, no occupier, no
ratepayer, no owner — 19 fields, all address, classification, valuation and
geometry, checked against
`name|occupier|tenant|owner|ratepayer|proprietor|person|contact` with zero
matches. It records premises, and the Irish valuation list is non-domestic by
statute. This is the strongest privacy position of any source in this project
and it is structural rather than measured.

**Classification is `Uses` (963 distinct values), not `Category` (13).**
`Category` cannot separate this project's three buckets: 1,483 of 2,335
food-service rows and 677 of 744 personal-service rows both sit inside
`RETAIL (SHOPS)`. See the brief for the catch-all measurement, which inverts
Barcelona's rule.

> **TAILTE WITHHOLDS FLOOR-LEVEL DETAIL FOR NAMED PROPERTY TYPES, AND IT DOES
> NOT AFFECT THIS BUILD — MEASURED.** `tailte.ie/home/api/` warns of missing
> detail for "Hotels, Pubs, Cinemas, Service Stations, Guesthouses…" on
> confidentiality grounds. Measured with a control: all 767 `PUB`, 210 `HOTEL`,
> 184 `SERVICE STATION` and 116 guesthouse/hostel/cinema rows arrive **present
> and fully classified**, with `ValuationReport` empty on **100%** of them and
> on **0%** of hairdressers, pharmacies and clothes shops. What is withheld is
> the per-floor valuation, which this project never reads. **It would bite
> totally, and precisely on food service, if the build ever weighted by floor
> area.**

**Boundary** — Tailte Éireann, *Local Authorities — National Statutory
Boundaries — Ungeneralised — 2026*, layer 3:

```
https://services-eu1.arcgis.com/FH5XCsx8rYXqnjF5/arcgis/rest/services/
  National_Statutory_Boundaries_-_Local_Authorities__Ungeneralised_-_2026/
  FeatureServer/3
```

Authority name is `ENG_NAME_VALUE` (Irish `GLE_NAME_VALUE`), spatial reference
**wkid 2157**, 937.3 km² over the four authorities. Unwrapped, for the
provenance check and for copying:

`https://services-eu1.arcgis.com/FH5XCsx8rYXqnjF5/arcgis/rest/services/National_Statutory_Boundaries_-_Local_Authorities__Ungeneralised_-_2026/FeatureServer/3`

> **USE THE FEATURESERVER, NOT THE HUB DOWNLOAD.** `data.gov.ie`'s resource
> list points at `data-osi.opendata.arcgis.com/api/download/v1/items/...`,
> which is the **async job endpoint that answers HTTP 202** — the Surrey trap
> in `add-country`. The FeatureServer above is synchronous and takes a
> where-clause.

> **THE LAYER IS MULTIPART.** Fingal returns **46** polygons and Dún
> Laoghaire–Rathdown **42** — islands and coastal outcrops, most under
> 0.1 km². Dissolve by `ENG_NAME_VALUE` before any point-in-polygon test, or a
> station gets tested against Lambay Island.

**Rail** — the **National Transport Authority's national GTFS**, not
OpenStreetMap. ⚠️ **This corrects what this section said when Dublin's brief
was written.**

`https://www.transportforireland.ie/transitData/Data/GTFS_All.zip`

**The feed is current, measured rather than assumed:** `feed_info.txt` declares
`feed_end_date` **20270922**, a year out, and it carries **Woodbrook
(`8220WBROK`), a station that opened in 2025** — so it is maintained, not a
re-uploaded archive. Three routes are drawn: `10000 GREEN g a` (Luas Green,
`route_type 0`), `10000 RED g a` (Luas Red, `0`) and `BRAY-HOWTH-I` (DART,
`2`). Commuter and InterCity are other `route_id`s under the same
`route_type 2` and are excluded.

> **THE BRIEF ASSERTED "OPENSTREETMAP, NOT A FEED" WITHOUT CHECKING FOR ONE,
> AND THAT WAS MADRID'S FAILURE REPEATED.** The `osm-rail` order is agency GIS
> layers → agency GTFS → OSM **on a recorded ground**; neither of the first two
> had been run. Both pass. The NTA also publishes a **Feature Service already
> in EPSG:2157** — 14,079 stops, 6,507 route polylines, at
> `services-eu1.arcgis.com/p0UmGrpumWZYhF0p/` — whose `GTFS - Stops` layer even
> carries `local_authority` pre-populated in the boundary layer's spelling.

> **THE FEED IS 158 MB AND ITS `shapes.txt` IS 372 MB OVER 8.0M ROWS.**
> `fetch_sources.py` trims it once to the three routes (→ 1.9 MB) so no step
> and no drift check ever parses the national file.

> **`route_color` IS EMPTY FOR ALL THREE ROUTES**, in both the feed and the
> feature service, so the palette is chosen rather than inherited — and it is
> chosen against `map_common`'s CIE76 separation check, not by eye. OSM's
> community colours scored 21.7–27.5 against the category pins the lines are
> drawn under. See `pipeline/dublin/config.py` for the measurements: Luas Red
> `#8B0000`, Luas Green `#006400`, DART `#F57C00`.

> **DART'S `route_long_name` IS "Bray - Howth", WHICH UNDERSTATES IT** — its
> own stops run Malahide to Greystones. The drawn label is `route_short_name`,
> `DART`.

**OpenStreetMap is retained as a cross-check**, not as the source — 42 route
relations in the Dublin bbox, cached and compared against the feed every run
(GTFS 98 station names, OSM 100, 88 shared; the differences are spelling).
Madrid's three sources agreeing on 13 lines while landing at 243 / 236 / 230
stations is why a second opinion is kept.

> **OSM TAGS ALL FOUR DART RELATIONS `network=Commuter`** — the same value the
> Northern, Western and South Western services carry. A `network` filter drops
> Dublin's principal line, which a run proved before the source changed. The
> `osm-rail` rule that a `network` tag is a label and not evidence, measured.

> **`overpass.osm.ch` RETURNED AN EMPTY 200 FOR THIS QUERY ON 2026-09-22.**
> `pipeline/osm.py` rejects that; a hand-rolled fetch does not, and the first
> attempt here would have recorded "0 relations" against a real 42.

## Transit feeds

**Titled “Transit feeds (GTFS)” until 2026-09-22.** The table immediately below
is still all GTFS and always was; what changed is that the section now also
holds a subsection for rail that is **not** a feed, and a parent heading
claiming GTFS would have misdescribed its own contents. Every row in the first
table is a feed; everything under “Rail geometry that is not a GTFS feed” is
not.

| City | Agency / system | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| San Diego | MTS Trolley | `https://www.sdmts.com/google_transit_files/google_transit.zip` | 2026-09-18 | |
| San Francisco | SFMTA Muni Metro | `https://muni-gtfs.apps.sfmta.com/data/muni_gtfs-current.zip` | ≈2026-09-19 | **Mirror.** The official host (`sfmta.com/reports/gtfs-transit-data`) timed out from this environment; this URL is linked from the agency's own page |
| Los Angeles | LA Metro Rail | `https://gitlab.com/LACMTA/gtfs_rail/raw/master/gtfs_rail.zip` | ≈2026-09-19 | Metro's rail-only feed |
| Chicago | CTA | `https://www.transitchicago.com/downloads/sch_data/google_transit.zip` | 2026-09-20 | |
| New York | MTA subway + Staten Island Railway | `https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip` | 2026-09-21 | The `web.mta.info/developers/data/nyct/subway/google_transit.zip` path is **dead** |
| Boston | MBTA rapid transit | `https://cdn.mbta.com/MBTA_GTFS.zip` | 2026-09-21 | 24.9 MB, 32 files. Drawn: `Red`, `Orange`, `Blue`, `Mattapan` and `Green-B`/`-C`/`-D`/`-E` as five line groups; the 14 `CR-*` Regional Rail routes and the ferries are not. `feed_info.txt` declares **no licence field at all**, so the terms are the MassDOT agreement — which requires a notice, now ACTIVE. Branching lines need several shapes each (Red splits to Ashmont and Braintree; Green is four branches), and `parent_station` is populated so platforms collapse cleanly |
| Washington D.C. | WMATA Metrorail | `https://api.wmata.com/gtfs/rail-gtfs-static.zip` | 2026-09-21 | **The only feed in this project behind an API key** — 401 unauthenticated. Free developer account at `developer.wmata.com`, subscribe to the **GTFS** product, key sent as an `api_key` header. Take the **`Rail GTFS Static`** operation, *not* `Rail & Bus Combined GTFS Static` (bus routes this project never draws) and not any `RT` feed. Verified 2026-09-21: 6 routes (Red, Blue, Green, Yellow, Orange, Silver, all `route_type 1`, `network_id Metrorail`), **98 parent stations, all with coordinates**, 270,784 `stop_times` rows, 340 shape_ids, no bus contamination. **`feed_info.txt` declares `feed_start_date 20260915`, `feed_end_date 20260925` — a ten-day validity window, the shortest of any feed here, so a rebuild must re-download rather than reuse a stored copy.** Terms are the WMATA Transit Data Terms of Use, stored at `docs/licenses/wmata-transit-data-terms-of-use.html`; the key is WMATA's property, must stay out of the repo, and cannot be sold, transferred or sublicensed (§5). **Built 2026-09-21.** `fetch_sources.py` reads the key from a `WMATA_API_KEY` environment variable, never echoes it (not even in the 401 message), and re-checks `feed_end_date` on EVERY run including runs that skip the download — an expired copy is an error, not a warning, because a stale feed still parses, still has 98 stations and still builds a map. Shape selection needed care this feed alone required: WMATA publishes 26-101 shapes per route, so "the most-used shape" could be a short turn (the Yellow Line's second-most-used stops at Mt Vernon Square, nine stations short of Greenbelt). Each drawn shape is the most-used among those serving the route's full stop count |
| Miami | Miami-Dade Transit (Metrorail + Metromover) | `https://www.miamidade.gov/transit/googletransit/current/google_transit.zip` | 2026-09-21 | 8.4 MB. **Note the host**: `transitdata.miamidade.gov` does not resolve; this URL is also the one the Mobility Database lists as official. Four rail routes; three are drawn (`31009` Metrorail, `14457`/`14456` the Metromover loops) and the MIA Airport People Mover `14458` is not. **No `feed_info.txt` at all**, so no licence is declared in the feed. Metrorail publishes NINE shapes because the line branches, and has **no `parent_station`** — its 46 stop_ids are 23 stations x 2 directions |
| Philadelphia | SEPTA Metro | `https://github.com/septadev/GTFS/releases/latest/download/gtfs_public.zip` | 2026-09-21 | **A zip of zips.** Contains `google_bus.zip` and `google_rail.zip`; `fetch_sources.py` extracts the **bus** one, because SEPTA's City Transit Division — and therefore the Market-Frankford Line, Broad Street Line and every trolley — is in that feed, not the "rail" one. `google_rail.zip` is Regional Rail, which this project does not draw. The naming is not guessable; both route tables were read to establish it |
| Edmonton | Edmonton Transit Service LRT | `https://gtfs.edmonton.ca/TMGTFSRealTimeWebService/GTFS/gtfs.zip` | 2026-09-21 | **The URL is not published as a readable link.** The catalogue's entry for the feed (`urjq-fvmq`) is an `href`-type asset with no rows and no download button; the URL lives in its metadata under `accessPoints.DOWNLOAD`, which is why two guessed URLs 404'd during the Canada profile. 16.7 MB, 18 files, and it **declares a validity window** (`feed_start_date` 20260911, `feed_end_date` 20261128) where Calgary's and Toronto's do not. **Do not substitute either republication:** the eight individual Socrata GTFS tables (`d577-xky7`, `4vt2-8zrq`, `ctwr-tvrd`, `greh-g7ac`, `7f8n-igfx`, `f2sy-bth7`, `isug-45sj`, `hnhf-yaps`) expire 2026-08-29 and the Mobility Database mirror (id 714) expired 2026-06-20 |
| Toronto | TTC subway (Lines 1/2/4) and LRT (Lines 5/6) | `https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/7795b45e-e65a-4465-81fc-c36b9dfff169/resource/cfb6b2b8-6191-41e3-bda1-b175c51148cb/download/opendata_ttc_schedules.zip` | 2026-09-21 | **The City's own CKAN package, and the Mobility Database mirror must NOT be substituted: its copy was three months expired and contained NO SUBWAY AT ALL** (209 bus, 17 tram, 2 ferry, zero `route_type 1`), which produced the false claim that Toronto codes its subway as route_type 0 and is why `screen_rail.py` now prints feed expiry. 36 MB, 8 files, no `feed_info.txt` — so like Calgary's there is no validity window to check. The 18 streetcar routes share `route_type 0` with the two LRT lines and are separated by `^Line \d` |
| Vancouver / Surrey | TransLink SkyTrain (Expo, Millennium, Canada) | `https://gtfs-static.translink.ca/gtfs/google_transit.zip` | 2026-09-21 | **TransLink's own host, not the Mobility Database mirror — and here the mirror was not stale but INCOMPLETE.** The Canada profile recorded that this feed carries no `feed_info.txt`; that is true of the mirror and false of the agency's copy, which declares `feed_start_date` 20260907, `feed_end_date` 20270103 — a 118-day window. Toronto's stale-mirror lesson one step further on: a mirror can be missing a file the source publishes, not merely out of date. The window is re-checked on **every** run including runs that skip the download, because an expired feed still parses, still has 54 stations and still builds a map. **One feed covers both cities** — Surrey has no agency of its own, which is why the regional build needs only one transit licence. **Match routes on `route_id`, NEVER `route_short_name`: it is EMPTY on all three rail routes** and the public names live in `route_long_name` — `30053` Expo, `30052` Millennium, `13686` Canada. The West Coast Express (`6770`) is `route_type 2` commuter rail and the SeaBus is `route_type 4`, both excluded as everywhere. Branching lines need a shape TUPLE rather than the modal shape, which would silently drop a whole branch: the Canada Line splits for YVR-Airport and Richmond-Brighouse, the Expo Line for King George and Production Way-University. Every rail stop is named `<Station> @ Platform N` (a few `@ <Line>`), two to four rows per station; the pattern is regular enough to strip without an alias dict, and step 1 asserts every `@`-bearing name matched so a new suffix form fails loudly |
| Montréal | STM Métro (4 lines) | `https://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip` | 2026-09-21 | **STM's own host, and this city is the proof that it matters.** Measured 2026-09-21: the agency feed was valid to 20261025 (+34 days) while the Mobility Database mirror (id 2126) was **29 days EXPIRED**. The station counts happened to agree — but Toronto's mirror hid an entire mode, so a build never takes the mirror. It declares a validity window, so the `feed_end_date` guard applies as it does for D.C. and Vancouver. Routes match on exact `route_id` — `1` Verte, `2` Orange, `4` Jaune, `5` Bleue — and unlike Vancouver there is nothing to exclude: the STM runs the Métro and buses only, with no commuter-rail or ferry route in the feed. 68 parent stations, 64 of them on the island. The four that are not (Cartier, De la Concorde and Montmorency in Laval, Longueuil-Université de Sherbrooke in Longueuil) are dropped by the SPATIAL filter, never by name — but STM also marks them structurally, appending ` -Zone B` (its fare zone) to exactly the off-island set, and step 1 asserts the two agree so a silent change in either is caught |
| Calgary | Calgary Transit CTrain (Red Line, Blue Line) | `https://data.calgary.ca/download/npk7-z3bj/application%2Fx-zip-compressed` | 2026-09-21 | Calgary Transit's own feed, not the Mobility Database mirror; verified 2026-09-21 to reproduce the mirror's rail half exactly (2 `route_type 0` routes, 83 served stops, 83 distinct names). **`route_id` EMBEDS A FEED VERSION and no other city here does that** — the mirror gives `201-20780`, the agency feed `201-20786` — so routes match on `route_short_name` (`201`, `202`); a config pinning the id matches nothing after the next release, and matches it silently. The other 258 routes are buses. **NEITHER Calgary copy carries `feed_info.txt`**, so unlike D.C., Montréal and Vancouver there is no validity window and the expiry guard cannot be written; staleness is judged from the Socrata resource's own `updatedAt`, which `fetch_sources.py` prints. **The feed publishes 83 PLATFORMS, not 83 stations, and the whole Canada ranking recorded the platform count.** There is no `parent_station` column and every stop name carries a direction prefix, so each name is unique and nothing looks wrong; they collapse to the CTrain's real 45. What caught it was the spacing — an uncollapsed nearest-neighbour median of 17 m. Collapse by normalised NAME, never by proximity: 7 Avenue downtown is a ONE-WAY COUPLET, so 7 of the 45 stations legitimately have one platform and `EB 3 Street SW` and `WB 4 Street SW` are different places on different streets |
| Paris | Île-de-France Mobilités (IDFM) — Métro, 16 lines | `https://eu.ftp.opendatasoft.com/stif/GTFS/IDFM-gtfs.zip` | 2026-09-22 | **IDFM's own host** (`stif/` on Opendatasoft), and the choice is not incidental: the NAP lists **two third-party GTFS beside it** and both are unusable — Google's (`gtech-transit-prod.apigee.net`) stale since 2023-11-17, and ITO World's with `is_available: false`. Building from a modified third-party copy is not acceptable. ⚠️ **The feed carries NO `feed_info.txt`** — 14 files, measured by `brief_check.py`, which **disproved this brief's own original claim** that it self-attests. So the artifact declares no validity window at all: the `end_date` of 2026-10-21 is `transport.data.gouv.fr`'s metadata **about** the feed, not the file's own word. Staleness must therefore be read from the NAP or a content hash, and **`fetch_sources.py` must record the download date, because nothing inside the file will.** This bears directly on the licence — Art. 5.7 requires the data's date **and** update interval to be stated, and neither is inside the artifact. ⚠️ **IDFM's network maps and plans are CC BY-NC-ND 3.0 France**: redrawing from *data* avoids this entirely, but no IDFM plan or schematic may be used as a source or overlay. Licence **Licence Mobilités** — notice **24** |
| Paris | **`transport.data.gouv.fr` NAP API — METADATA, not geometry** | `https://transport.data.gouv.fr/api/datasets` | 2026-09-23 | **Not a feed, and it is here because notice 24 makes it load-bearing.** Licence Mobilités Art. 5.7 requires the data's last-updated date **and** its update interval to be DISPLAYED — and the IDFM zip carries no `feed_info.txt`, so neither value exists inside the artifact. `fetch_sources.py` reads them here at download time and writes them to `outputs/paris/provenance.json`, which the city page renders. Measured 2026-09-23: `start_date` 2026-09-20, `end_date` **2026-10-22** (the brief recorded 2026-10-21 — the feed has refreshed since). Without this row the build would be displaying a compliance value from a source nothing recorded |
| Marseille | RTM — Métro 1–2 and Tramway 1–3 | `https://app.mecatran.com/utw/ws/gtfsfeed/static/mamp?apiKey=60327e505a214c77303f52206f11483069257343` | 2026-09-23 | **The feed is the WHOLE Métropole Aix-Marseille-Provence** — "Référentiel complet (tous les réseaux)", measured at 737 bus, 17 TER, 6 ferry, 4 tram, 2 métro. Selecting by mode is not sufficient: **one of the four trams is AUBAGNE's** (`AUB-T`, Le Charrel ⇄ Gare), so routes are matched on exact `route_id`. The 17 TER routes reach **Nice and Geneva** and go by the standing commuter-rail rule; the 6 ferry routes (Vieux-Port shuttles, the Frioul islands) are excluded by owner's decision 2026-09-23, **recorded as revisitable** because they are genuine urban transit, which no other excluded mode here is. ✅ **UNLIKE PARIS, THIS FEED SELF-ATTESTS**: `feed_info.txt` gives publisher **Mecatran** and `20260922`–`20261231`, so staleness is readable from the artifact and no NAP-metadata capture is needed. ⚠️ **The API key is not a secret** — the operator publishes it as part of the feed URL through France's National Access Point. A key that were private would belong in the environment, not a committed file. Licence **`lov2`** | 
| Toulouse | Tisséo — Métro A–B, Tramway T1 and the **Téléo cable car** | `https://data.toulouse-metropole.fr/explore/dataset/tisseo-gtfs/files/fc1dda89077cf37e4f7521760e0ef4e9/download/` | 2026-09-23 | 11,962,958 bytes, 11 files, no key and no account. ⚠️ **The file id is load-bearing and long** — a truncated copy returns HTTP 404 "Unknown image" naming the id you sent rather than refusing you, so a typo reads as a dead dataset. Measured at 120 bus, 2 métro (`route_type 1`), 1 tram (`0`) and **1 aerial lift (`6`)**. ⚠️ **`route_type 6` IS DRAWN** — Téléo, the project's **first non-rail mode**, owner's decision 2026-09-23. The brief's stated precedent for it ("it does draw a funicular (Paris)") was **false and was corrected during the build**: `pipeline/paris/config.py` says "the Metro, and only the Metro" and lists "1 funicular, 1 cable" among what Paris *excluded*. ⚠️ **NO `feed_info.txt`** — Paris's gap rather than Marseille's self-attestation, so staleness is unreadable from the artifact; the portal's own `modified` timestamp (`2026-09-23T02:15:22+00:00`) is captured at fetch time instead. **Gate 3 passed exactly on all four lines** against `arrets-itineraire`, the operator's own layer: A 18=18, B 20=20, T1 25=25, TELEO 3=3. Licence **ODbL 1.0** (`odc-odbl`) — **notice 25 (Tisséo)**, which the OpenStreetMap notice does not discharge because ODbL §4.3 requires the notice to name *which* database and Tisséo's is not OSM's | 
| Rennes | STAR (Keolis Rennes) — **Métro a and b** | `https://eu.ftp.opendatasoft.com/star/gtfs/GTFS_STAR_BUS_METRO_EN_COURS.zip` | 2026-09-23 | 13,119,510 bytes, no key and no account. Measured at 150 bus and **2 métro (`route_type 1`)**; STAR runs no tram. ⚠️ **`EN_COURS`, never `A_VENIR`** — the sibling resource is the FORTHCOMING timetable. ✅ **The feed self-attests**: `feed_info.txt` names Keolis Rennes, **2026-09-22 to 2026-10-18** — a four-week window, so `brief_check` will flag it early; that means refetch, not alarm. ⚠️ **This file host is not the portal's API.** `data.explore.star.fr` runs a DOMAIN-WIDE quota of 150,000 calls a day shared by every anonymous caller, and it was spent on 2026-09-23 (HTTP 429, errorcode 10003, reset 00:00 UTC) while this host kept answering. **Gate 3 exact on both lines against OpenStreetMap** (`network=FR:STAR`, 4 relations, one per line per direction): a 15=15, b 15=15. Licence **ODbL 1.0** (`odc-odbl`) — **notice 26 (STAR)**, which neither the OpenStreetMap notice nor Tisséo's discharges, because ODbL §4.3 requires the notice to name *which* database | 

### Rail geometry that is not a GTFS feed

**These cities are kept OUT of the feed table rather than filed under a
heading that would misdescribe them**, because a non-feed source has no
`feed_info.txt`, no validity window and no `route_id` — three of the things
every note in that table turns on — so a row there would have meant empty
columns. Same section, its own subsection, its own columns.

**Two different reasons land here, and they are not the same case.**

- **Mexico City and Guadalajara come from OpenStreetMap via Overpass**, because
  no usable feed exists. An OSM source also has no agency holding the licence:
  both are **ODbL 1.0**, covered by **notice 1**, which since these builds
  covers *data* and not only basemap tiles. See `.claude/skills/osm-rail/`
  before adding another.
- **Madrid comes from CRTM's own ArcGIS feature services**, and there the
  operator's feed exists and downloads cleanly — it is rejected because CRTM's
  licence obliges a reuser to keep displayed information *“siempre
  actualizada”* and that feed has not been refreshed since 2025-05-30. A
  licence consequence rather than an absence, and the licence is CRTM's own,
  not OpenStreetMap's. **Madrid sat under the OpenStreetMap heading for part of
  2026-09-22**, which was wrong in the way this subsection exists to prevent.

| City | System / operator | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Mexico City | **STC Metro** (12 lines) + **STE Tren Ligero** (1). Tren Ligero is a different operator and a different mode and is kept on the same reasoning that put Metromover on Miami's map and the Valley Line on Edmonton's — it is urban rail inside the city, and dropping it would leave the whole southern corridor to Xochimilco blank while the register still counts its shops. Metrobús is BRT and is **not** rail | Overpass API, POSTed to three mirrors in order: `https://overpass-api.de/api/interpreter`, `https://overpass.kumi.systems/api/interpreter`, `https://overpass.osm.ch/api/interpreter` | 2026-09-22 | **Why not the agency: every `*.cdmx.gob.mx` host is unreachable from here** — the city open-data portal, STC Metro and STE alike, ConnectTimeout on `www.` and bare, http and https, re-confirmed 2026-09-22, and the feed's S3 `direct_download` returns 403. No block page names an IP, so this is a dead host rather than a client refusal, and a browser does not help. Owner-approved 2026-09-22 as a documented per-city exception. Stations: `node["railway"]` in bbox `18.95,-99.45,19.75,-98.85`, then a **WHITELIST** of `railway=station` — a whitelist and not a blacklist because OSM carries 13 **proposed** Texcoco light-rail stations in this bbox and **five are tagged `railway=prpopsed`, misspelled in the source data**, which a blacklist would admit and which would draw rings around building sites. 447 `railway=subway_entrance` nodes against 184 stations (2.4x) are excluded on the same principle. **Match on the MODE, never on the network label alone:** seven real stations carry no `network` tag at all, and OSM tags Lechería `network=STC Metro` although it is a Ferrocarril Suburbano station, so the test is `station in (subway, light_rail) or subway=yes`. Lines come from a union of `relation[type=route][route=subway]` and `relation[type=route][route=light_rail]`, fetched with **`out geom`, not `out tags`** — the member way geometry is this project's OSM analogue of `shapes.txt`, and without it the city would have station dots and no lines, breaking the every-line-drawn invariant. **Collapse is BY NAME**, a fourth mechanism after Edmonton's `parent_station`, Calgary's direction prefix and Toronto's naming conventions: OSM has one node per line at an interchange (Pantitlán 4, La Raza/Jamaica/Oceanía/Tasqueña 2 each). **Gate 3 is UNAVAILABLE** — STC Metro's published counts live on the unreachable host, so `STATION_COUNT_GATE_3 = None` records the reason rather than a figure typed from memory; the spacing gate, the whitelist and cross-direction agreement run instead. **163 stations kept** |
| Guadalajara | **SITEUR Mi Tren** (Tren Ligero), 4 lines — Línea 4 included, and it is the reason this city is not GTFS | The same three mirrors, in the same order | 2026-09-22 | **Why not the agency: the feed was found, downloaded and REJECTED** — a different finding from Mexico City's dead host, and the numbers are recorded so nobody re-adopts it. The only Guadalajara rail feed in the Mobility Database (mdb **1925**, also inside **2366**) declares `feed_end_date = 20230128` in its own `feed_info.txt`, names **Nubenautas** (`gtfs.studio`) as publisher rather than SITEUR, and carries **three** light-rail routes where SITEUR runs **four**: **Línea 4 opened 2025-12-15**, almost three years after the feed stopped. Building from it would have drawn a map missing an operating line, 8 stations and 21 km, while looking complete — the Toronto stale-mirror lesson with the staleness declared in the artifact itself. `https://www.siteur.gob.mx/` answers HTTP 200 but publishes no GTFS. Owner-approved 2026-09-22 as a second documented exception, on incompleteness rather than unreachability. **This city's station object is not Mexico City's, and that is the most important line here:** Mexico City has 184 `railway=station` nodes and Guadalajara has **one** — its stations are `railway=stop`, 96 nodes at exactly 2 per name for 48 names, so Mexico City's whitelist would have found a single station and the build would have looked like a scope problem rather than a tagging one. **Stations come from ROUTE-RELATION MEMBERSHIP, not from node labels.** The first query here was `node["railway"]["network"="Mi Tren"]`, which returned 96 nodes and **silently omitted every one of Línea 4's 8 stops**, because that line's nodes carry no `network` tag — a 49-station set with zero stations in Tlajomulco, missing the same line the rejected feed was missing, reached by a different route. All 8 relations *are* `network`-tagged, so the filter is safe at relation level and was only ever wrong at node level. **Gate 3 RUNS here and passes:** SITEUR publishes 10 stations for Línea 2 and 8 for Línea 4, and OSM route-relation membership gives 10 and 8. It publishes no count for Líneas 1 or 3, so none is recorded — a partial gate 3 with its gaps named beats a complete-looking one filled in from memory. **56 stations** across four municipios |
| Madrid | **CRTM Metro — ArcGIS feature services, NOT a GTFS feed** (Consorcio Regional de Transportes de Madrid) | `https://services5.arcgis.com/UxADft6QPcvFyDU1/arcgis/rest/services/M4_Red/FeatureServer` — layer **0 `M4_Estaciones`** (293 station-per-line points) and layer **4 `M4_Tramos`** (560 polylines) | 2026-09-22 | **The first rail in this project from an operator's feature services rather than a feed, and the reason is a LICENCE condition rather than a preference.** CRTM publishes the same network twice: a Metro GTFS it stopped refreshing on **2025-05-30**, and these services it still edits (**2026-06-05**). Its licence obliges a reuser to keep displayed information *"siempre actualizada"*, which a feed abandoned sixteen months ago cannot satisfy — so the feed is rejected although it downloads cleanly. `scripts/brief_check.py` watches these layers' `editingInfo.lastEditDate` with its `arcgis_layer` check kind, because the pre-existing tripwire watched the FEED and would have kept passing while the decision it guarded went stale. Both layers are natively **EPSG:25830**, the same CRS as the premises register, so the build never reprojects for geometry |
| Barcelona | **OpenStreetMap** — 14 metro refs (L1–L12, with L9 and L10 each split into two disconnected segments) plus the **Montjuic (TMB)** and **Vallvidrera (FGC)** funiculars: 16 drawn lines across **two operators** | The three Overpass mirrors in `pipeline/osm.py`, bbox `41.30,2.03,41.50,2.30` | 2026-09-22 | **Why not the agency feed:** TMB's GTFS is registration-gated (`api.tmb.cat` returns **401** unauthenticated, watched by `brief_check.py`), and the agency route would need **four feeds** — TMB, FGC, TRAM and TRAM Besos — with four licences and four cadences. OSM returns the network in one query with **every line carrying its own name and colour**, so no palette is invented. **Scope is the operators' own `network` tag**: the 14 metro refs and both funiculars are tagged `Metro de Barcelona` or `Metro del Valles`; **FT (Tibidabo)** carries no network tag and is run by the municipal parks company, and trams T1–T6 are `Trambaix`/`Trambesos` — both excluded. ⚠️ **The mirrors disagree about this bbox** (tram/funicular counts, and `L10N` vs `L10 Nord`), so the fetch is cached and the build normalises refs. ODbL 1.0 — notice **1** and the rail-geometry notice |
| Dublin | **National Transport Authority national GTFS** — 3 drawn routes: `10000 GREEN g a` (Luas Green, `route_type 0`), `10000 RED g a` (Luas Red, `0`) and `BRAY-HOWTH-I` (DART, `2`) | `https://www.transportforireland.ie/transitData/Data/GTFS_All.zip` | 2026-09-22 | **The brief said "OpenStreetMap, not a feed" and was WRONG — corrected during the build.** Neither agency route had been probed, which is Madrid's failure in its general form. Both pass: this feed declares `feed_end_date` **20270922** (a year out) and carries **Woodbrook, a station that opened in 2025**, so it is maintained rather than a re-uploaded archive; the NTA also publishes a **Feature Service already in EPSG:2157** (14,079 stops, 6,507 route polylines) at `services-eu1.arcgis.com/p0UmGrpumWZYhF0p/`. **The feed is 158 MB and its `shapes.txt` 372 MB over 8.0M rows**, so `fetch_sources.py` trims it once to the three routes (→ 1.9 MB) and no step or drift check ever parses the national file. **`route_color` is EMPTY for all three routes**, so the palette is chosen against `map_common`'s CIE76 check rather than inherited. **OSM is retained as the CROSS-CHECK** and runs every build (GTFS 98 station names, OSM 100, 88 shared; differences are spelling) — ⚠️ it tags all four DART relations `network=Commuter`, so a network filter drops the city's principal line, and the whitelist is on `ref`. ODbL 1.0 for the cross-check — notice **1** |
| Milan | **ATM's own GIS layers, plus the agency GTFS** — `ds535_atm-fermate-linee-metropolitane` (130 station points), `ds539_atm-percorsi-linee-metropolitane` (31 alignments) and `ds533_atm-composizione-percorsi-linee-metropolitane` (650-row join table). **5 metro lines drawn, M1–M5; the 17 trams are not** | The same CKAN portal as the registers; the GTFS at the stable short URL `https://dati.comune.milano.it/gtfs.zip` | 2026-09-22 | **Both `osm-rail` steps were run and BOTH passed, so OpenStreetMap is not used** — this is the check Dublin's brief skipped one city earlier. The GTFS supplies what the GIS layers lack: **`route_color` for the five metro lines** (`#ff0000` rossa, `#73ff01` verde, `#fcff01` gialla, `#0000ee` blu, `#c876b1` lilla), which are the agency's own, so the project's rule keeps them although M5 scores 39.7 against the Food service pin. ⚠️ **ds533's `id_ferm` is a STRING where ds535's `id_amat` is an INT** — a raw join gives **130 of 130 misses**, which reads as a scope problem rather than a type one. ⚠️ **ds535's 130 features are NOT 130 stations**: interchanges are modelled two incompatible ways, and a distance threshold is wrong in BOTH directions (WAGNER/BUONARROTI at 277 m are different stations; LORETO M2 and LORETO M1 at 231 m are one), so the collapse is by name and gives **125**. ⚠️ **`stops.txt` cannot select metro stations** — `location_type` and `parent_station` are empty on all 4,897 stops, and 532 names match `m1`–`m5` because bus stops are named after the metro station they serve. ⚠️ **The GIS tram layer `ds538` is MISSING TRAM 27**, which is Guadalajara's Línea 4 again — immaterial while the trams are undrawn, and the reason their geometry would have to come from `shapes.txt` if they ever are. **Gate 3 RUNS and passes**: ATM's own join table gives M1 38 / M2 35 / M3 21 / M4 21 / M5 19, union 130, 130 of 130 resolving. The S-line suburban network is cleanly separate (no `route_type=2`, zero matching stop names) and is excluded by not fetching it |
| Lille (Regional) | **ilévia** — Métro 1–2 and Tram R–T. **The first hybrid here: stations and tram lines from the agency's GIS, métro lines from OpenStreetMap** | MEL WFS `https://data.lillemetropole.fr/geoserver/wfs`: `mel_mobilite_et_transport:stations_metro` (62 rows), `tramway_arrets` (66), `tramway_lignes` (4 sections), `dsp_ilevia:couleurs_lignes` (344, the livery). Overpass: route relations of mode subway or tram with `network=Ilévia`, bbox 50.55,2.95,50.80,3.25, `out geom` — one query, cached | 2026-09-23 | **No GTFS is read.** ilévia's feed has no `shapes.txt`, and every station it would supply MEL publishes first-party — so the brief's open question about `media.ilevia.fr`'s Mentions légales was sidestepped rather than settled. ⚠️ **Never `sdit_ligne` / `sdit_station`**: MEL's PLANNED network — projected tram and BHNS corridors, `status: Variante` rows, no métro. ⚠️ **The OSM network filter excludes three `route=tram` relations in the same bbox** that are not ilévia's: two for the Amitram heritage tourist tram and one tagged on an abandoned railway. The tram layer comes in SECTIONS (R, T, and the shared trunk twice); step 1 assembles each line from its branch's own `tramway` id. **Gate 3 exact on all four lines against OSM**: M1 18, M2 44, R 23, T 22. ⚠️ **The operator gives the tram ONE colour** (`#009FE3`, `code_ligne_public: TRAM`): R keeps it and T takes the same hue darkened to `#005D85` — Paris's bis-line precedent, forced by the shared colour check refusing two drawn lines at ΔE 0. `tramway_lignes` carries no citation date, only a metadata `dateStamp` of 2024-06-03, so the page cites the RETRIEVAL date and says which. Licences: **`lov2`** for MEL, with **Ilévia** co-producer on the `dsp_ilevia` layer; **ODbL 1.0** for the métro lines, covered by notice 1 |

**Why three Overpass mirrors, and how one is chosen.** They are tried **in the
configured order**, and the first host returning HTTP 200 with a **non-empty
`elements` list** wins; every other outcome — a non-200, an exception, or a 200
with an empty body — sleeps briefly and advances to the next. Three, because
across these two builds each of the three failed at least once and none failed
consistently: `overpass-api.de` returned 504 several times and 429 once,
`overpass.kumi.systems` 504 several times, and `overpass.osm.ch` **answered 200
with an empty body** — all at different times, for the same query. A failure is
a fact about that host at that moment and not about the city, so one mirror
would make the build's success a coin flip.

**A 200 with no elements is treated as a host FAILURE and is never cached**,
which is the half that is not obvious. `overpass.osm.ch` once returned 272
bytes and an empty element list for the routes query; the fetcher cached it,
and the caller then reported *"every ref has exactly 2 direction relations"* —
**a vacuous truth over an empty set**. Both cities' step 1 now assert
non-emptiness before any check that could pass vacuously. Responses that do
succeed are cached to the gitignored `data/<city>/raw/osm_*.json`, so a re-run
or a drift check never depends on which mirror answered. Guadalajara makes
**two passes** over the host list before giving up where Mexico City makes one,
and sleeps 3 s between hosts where Mexico City sleeps 2.

## Boundary layers

Used to scope stations and businesses to the city. Not optional: San Diego's
Trolley serves six other cities, and 54 of Los Angeles' 110 rail stations lie
in 23 other municipalities.

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| San Diego | SANDAG regional municipal boundaries | `https://geo.sandag.org/server/rest/directories/downloads/Municipal_Boundaries.geojson` | `SAN DIEGO` |
| San Francisco | Socrata "Bay Area County Polygons" (`wamw-vt4s`) | `https://data.sf.gov/resource/wamw-vt4s.geojson?$where=county='San Francisco'&$limit=10` | `San Francisco` |
| Los Angeles | LA County Planning, incorporated cities | `https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/admin_dist_SDE_DIST_DRP_CITY_COMM_BDY/FeatureServer/0/query` (`JURISDICTION='INCORPORATED CITY'`, `outSR=4326`, `f=geojson`) | `LOS ANGELES` |
| Chicago | Socrata "Boundaries - City" (`qqq8-j68g`) | `https://data.cityofchicago.org/resource/qqq8-j68g.geojson?$limit=10` | whole city |
| New York | Borough Boundaries (`gthc-hcne`) | `https://data.cityofnewyork.us/resource/gthc-hcne.geojson?$limit=10` | all five boroughs = the city |
| Philadelphia | OpenDataPhilly "City Limits" (Dept of Planning and Development) | `https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/City_Limits/FeatureServer/0/query` (`where=1=1`, `outSR=4326`, `f=geojson`) | whole city (one polygon, 2,957 vertices) |
| Boston | **MassGIS Massachusetts Municipalities**, layer 1 ("Areas") — 351 town polygons statewide, with a `TOWN` field | `https://services1.arcgis.com/hGdibHYSPO59RG1h/arcgis/rest/services/Massachusetts_Municipalities/FeatureServer/1/query` (`outFields=TOWN`, `outSR=4326`, `f=geojson`) | a spatial **envelope** around the rapid-transit network rather than all 351 towns → 61 polygons. Used both to filter to `TOWN='BOSTON'` and to NAME the 43 out-of-town stations |
| Boston — **considered, not used** | "City of Boston Outline Boundary (Water Excluded)" | `https://data.boston.gov/dataset/a70595d2-fd38-4bcb-8a81-6f7807621d38/resource/dade0744-a486-44c7-be7d-07240a89dca4/download/city_of_boston_outline_boundary_water_excluded.geojson` | whole city, one polygon. Would filter but could not NAME the other towns, which is the bigger job here — see the note below |
| Washington D.C. | **DC Boundary**, layer 10 of the District's administrative-boundaries service — a single clean polygon | `https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Administrative_Other_Boundaries_WebMercator/MapServer/10/query` (`where=1=1`, `outFields=*`, `outSR=4326`, `f=geojson`) | whole District, one polygon. Used to filter: 40 of 98 Metrorail stations are inside it |
| Washington D.C. — **naming layer** | **Census TIGERweb states** — three polygons, so an excluded station can be NAMED and not merely counted | `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/0/query` (`NAME IN ('Maryland','Virginia','District of Columbia')`, `outSR=4326`, `f=geojson`) | the three jurisdictions Metrorail runs through. 58 stations are outside the District — 32 Virginia, 26 Maryland — the second-largest station exclusion here after San Diego's, which is why it has to be citable. Census TIGER products are US federal works and carry no copyright |
| Miami | Miami-Dade County **municipal boundaries** (same publisher as its business data) | `https://services.arcgis.com/8Pc9XBTAsYuxx9Ny/arcgis/rest/services/Municipalitypoly_gdb/FeatureServer/0/query` (`outFields=MUNICID,NAME`, `outSR=4326`, `f=geojson`) | **not filtered — used to NAME, not to exclude.** 77 polygons across 34 municipalities; `MUNICID` joins to the business file's `MUNBUSLOC` prefix |
| Edmonton | **City of Edmonton — Corporate Boundary (current)** (Socrata `qqvh-dp5m`) | `https://data.edmonton.ca/api/geospatial/qqvh-dp5m?method=export&format=GeoJSON` | Whole city, 1 Polygon, 783.1 km². **FOUR layers on this portal are named some variant of "Corporate Boundary" and they are not the same polygon:** `qqvh-dp5m` and `a62q-eaea` give 783.1 km², `3trg-p57p` and `gtx5-kghy` give 699.8 km². The 83.3 km² difference is Edmonton's 2019 annexation from Leduc County, so the smaller pair predates it and is stale. This is Calgary's two-boundary trap with twice the ways to get it wrong, so `fetch_sources.py` asserts the area rather than trusting the name. Also the vocabulary trap: a search for "city boundary" misses it, because Edmonton calls it *corporate* |
| Toronto | **Regional Municipal Boundary** (CKAN `41bf97f0-da1a-46a9-ac25-5ce0078d6760`), a zipped shapefile geopandas reads directly | `https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/841fb820-46d0-46ac-8dcb-d20f27e57bcc/resource/41bf97f0-da1a-46a9-ac25-5ce0078d6760/download/toronto-boundary-wgs84.zip` | Whole city, 1 feature, 641.4 km² against Toronto's ~630 km² of land. It does real work here rather than being a formality: Line 1 runs past the city limit into York Region, so Highway 407 and Vaughan Metropolitan Centre are excluded by it |
| Vancouver | **`local-area-boundary`, DISSOLVED** — *not* `city-boundary` (Opendatasoft Explore v2.1) | `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/local-area-boundary/exports/geojson` | Whole city: 22 local areas union to **ONE** Polygon (not a multipart one — the local areas tile the city with no gaps), **118.8 km²** against the city's ~115, asserted at ±3.0. **`city-boundary` returns a single MultiLineString, not a polygon**, and a point-in-polygon test against it matches nothing *silently* — San Francisco's nine-county layer in another form. **The area check is the load-bearing part:** a dissolve that dropped a local area would still return a perfectly valid Polygon, and only the km² and the containment rate catch it. 99.84% of the 29,660 geocoded Vancouver businesses measured at Step 0 fall inside, the 47 outside being a plausible edge/waterfront residue |
| Surrey | Surrey City Boundaries (ArcGIS FeatureServer) | `https://services5.arcgis.com/YRpe0VKTJytZSSIB/arcgis/rest/services/Surrey City Boundaries/FeatureServer/0/query` (`where=1=1`, `outFields=*`, `f=geojson`) | `NAME='SURREY'`, equivalently `BOUNDARY_TYPE=2` — **the layer has 10 features and 9 of them are town centres** (Grandview, Clayton, Cloverdale, South Surrey, City Centre, Fleetwood, Guildford, Whalley, Newton), so an unfiltered read tests containment against a neighbourhood. Dissolving all ten would also work but is fragile if the town-centre set changes. **Read the SERVICE, not the Hub's file export.** The file export declares `EPSG:4326` while carrying **EPSG:26910 UTM metres** (503148, 5427696 — not degrees); reprojecting from the declared CRS puts the polygon millions of metres away and every containment test returns zero, which cost a full wrong run during Step 0. `f=geojson` on the service returns real degrees, correctly reprojected, so this build needs no `set_crs(..., allow_override=True)` anywhere — and step 1 asserts the boundary really is in degrees, so a switch back to the file export fails loudly instead of quietly matching nothing |
| Vancouver / Surrey — **naming layer** | **BC ABMS municipalities** (WFS 2.0), so an excluded station can be NAMED and not merely counted | `https://openmaps.gov.bc.ca/geo/pub/WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_MUNICIPALITIES_SP/ows` (`service=WFS`, `version=2.0.0`, `request=GetFeature`, `typeName=pub:WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_MUNICIPALITIES_SP`, `outputFormat=application/json`, `srsName=EPSG:4326`, `count=500`, `bbox=49.0,-123.35,49.45,-122.55,urn:ogc:def:crs:EPSG::4326`) | **Not filtered — used to NAME, not to exclude**, as D.C.'s Census states layer is. 30 of SkyTrain's 54 stations lie outside both cities, in Burnaby, Richmond, New Westminster, Coquitlam and Port Moody, and each is named from this layer rather than guessed from the station name. **A `urn:` CRS in the bbox means the AUTHORITY's axis order — lat,lon, not lon,lat.** Given lon,lat the service returns zero features and no error |
| Montréal | Limites administratives de l'agglomération (CKAN `limites-administratives-agglomeration`) — **the WGS 84 resource** | `https://donnees.montreal.ca/dataset/9797a946-9da8-41ec-8815-f6b276dec7e9/resource/e18bfd07-edc8-4ce8-8a5a-3b617662a794/download/limites-administratives-agglomeration.geojson` | Whole agglomeration: all **34** features dissolved — 19 `Arrondissement` (the Ville de Montréal) plus 15 `Ville liée`. `TYPE` is read and printed but not used to filter; it is recorded because it is what makes city-only scope one filter away. **Take the WGS 84 resource, not the `-nad83` sibling**, which is MTM zone 8 (EPSG:32188), a CRS this project uses nowhere else. **Area is checked against a FLOOR of 450 km², not a tolerance:** this boundary follows the river channel rather than the shoreline and measures 619.0 km² against the agglomeration's ~499 km² of land, so Vancouver's ±3 km² must not be copied here — a loose sanity floor is all this layer can support. Same `RBAC: access denied` browser-header requirement as the business download |
| Calgary | City Boundary (Socrata `erra-cqp9`) — **the `dataset` view** | `https://data.calgary.ca/api/geospatial/erra-cqp9?method=export&format=GeoJSON` | Whole city, 1 MultiPolygon, EPSG:4326, **852.9 km²** dissolved against Calgary's ~825 km² of land; step 1 rejects anything outside 600-1100 km². **Calgary publishes TWO datasets called "City Boundary" and one is broken:** `7t9h-2z9s` is the `map` view and returns valid but empty GeoJSON — 53 bytes on export, and a single feature with `"geometry": null` at 184 bytes as the Canada profile measured it — so it fails only when the geometry is used. **The rule generalises on this portal: take the `dataset` view, never the `map` one.** Nothing is excluded by this layer: the CTrain does not leave Calgary, so all 45 stations are in scope and `excluded_stations.csv` is written EMPTY rather than skipped |
| Mexico City | **OpenStreetMap** — the `admin_level=4` relation named `Ciudad de México`, polygonised from its `outer` member ways. The first boundary here that is not a published GIS layer but an assembled one | Overpass, the same three mirrors and the same order as the rail subsection above (`https://overpass-api.de/api/interpreter` first) | Whole city, one assembled polygon, **gated at 1,300-1,700 km²** against CDMX's 1,495. **The area gate is the load-bearing part, not a formality:** the usual Overpass boundary failure is a ring that does not close, leaving a sliver or the whole bbox, and both shapes of that error return a perfectly valid geometry that only fails when stations are counted three steps later — Surrey's wrong-CRS polygon and Vancouver's MultiLineString in a third form. **Exactly one relation is required**, because two layers sharing a name is a real hazard here (Calgary published two "City Boundary" layers, one of them 184 bytes of useless GeoJSON). It does real work: Lines A and B run into Estado de México, where this build has no business data, so **10 stations are cut** and written to `outputs/mexico_city/excluded_stations.csv` rather than left to anchor rings over a blank |
| Guadalajara | **OpenStreetMap** municipio relations at `admin_level=6` — **and `admin_level=8` is asked for in the same query rather than assumed absent**, because an empty result would look like "no stations in scope" three steps later | Overpass, the same three mirrors and order | The four municipios of `MUNICIPIOS_KEEP`, matched on exact name and unioned; **gated at 1,500-4,500 km²**, a deliberately wide band because this is a union of four rather than one city and the gate exists to catch a ring that did not close rather than to pin a figure. **THE BBOX IS LOAD-BEARING, and leaving it off produced a confidently wrong answer on the first run:** an unbounded name search matched **Guadalajara in SPAIN** — also `admin_level=6`, also named Guadalajara — and a "keep the largest polygon" tie-breaker then selected it *on purpose*, giving a 26,814 km² "Guadalajara" against the municipio's ~151. The union-area gate caught it. Two lessons kept here rather than in a commit message: **a name search without a geographic filter is a global search**, and **a tie-breaker on SIZE is exactly backwards when the wrong candidate is a province** — so duplicate names inside the bbox now RAISE and ask to be named by explicit `admin_level`, rather than being resolved by size. All four municipios are required; a missing one would silently drop that municipio's stations. Which municipio each kept station lies in is written to `outputs/guadalajara/station_municipios.csv`, as Miami's and Vancouver's regional builds do |
| Madrid | **Término municipal de Madrid** (Ayuntamiento geoportal, zipped shapefile) | `https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/LIMITES_ADMINISTRATIVOS/Termino_Municipal/Termino_Municipal.zip` | Whole city, native **EPSG:25830**. Step 1 checks its **area (604.0 km², accepted only within 500-700)** and the magnitude of its coordinates rather than its declared CRS — Surrey's layer declared EPSG:4326 while containing UTM metres, and a district polygon would pass a feature-count check. 49 stations fall outside the city and are excluded |
| Barcelona | **OpenStreetMap** — the `admin_level=8` relation named `Barcelona`, polygonised from its `outer` member ways | The three Overpass mirrors in `pipeline/osm.py`, bbox `41.30,2.03,41.50,2.30` | Whole municipality. **The bbox is load-bearing**: an unbounded name search for `Barcelona` also matches the province and the comarca, which is the shape of the error that selected *Guadalajara, Spain* during that build. Step 1 gates the **area at 101.4 km² ± 4** and measured **101.3**. It matters more here than in most cities — L8 and L10 Sud run to Cornellà, Sant Boi and El Prat and L9 Sud to the airport, so **50 of 162 stations fall outside** and are recorded in `outputs/barcelona/excluded_stations.csv` rather than silently kept |
| Dublin | Tailte Éireann **Local Authorities — National Statutory Boundaries — Ungeneralised — 2026**, layer 3 | `https://services-eu1.arcgis.com/FH5XCsx8rYXqnjF5/arcgis/rest/services/National_Statutory_Boundaries_-_Local_Authorities__Ungeneralised_-_2026/FeatureServer/3` | The four Dublin councils, **937.3 km²** dissolved (Dublin City 130.1, Fingal 457.2, South Dublin 223.4, Dún Laoghaire-Rathdown 126.5), name field `ENG_NAME_VALUE`, native **wkid 2157**. ⚠️ **Use the FeatureServer, NOT the resource data.gov.ie lists** — that is the ArcGIS Hub async download endpoint which answers HTTP 202 with a job id, the Surrey trap. ⚠️ **THE LAYER IS MULTIPART**: Fingal returns **46** polygons and Dún Laoghaire-Rathdown **42**, nearly all islands and coastal outcrops under 0.1 km², so it must be dissolved by name before any point-in-polygon test or a station is tested against Lambay Island. Only 2 stations fall outside (Bray Daly and Greystones, both County Wicklow), recorded in `outputs/dublin/excluded_stations.csv` |
| Milan | **Confini Amministrativi del Comune di Milano** (`ds2841-confini-amministrativi-del-comune-di-milano`) | `https://dati.comune.milano.it/dataset/ds2841-confini-amministrativi-del-comune-di-milano/resource/f56cb432-83e6-48de-ae30-d39b4be61e85/download` | Whole comune, **1 feature, 1 Polygon, EPSG:4326, 181.8 km²** measured in UTM 32N against Milan's ~181.8 km²; step 1 rejects anything outside 175–190. No multipart dissolve needed — the contrast with Dublin's 90-part layer is the point — and it is not the async Hub download endpoint. It does real work: the metro runs well past the comune, so **21 of 125 stations fall outside** and are recorded in `outputs/milan/excluded_stations.csv` rather than left to anchor rings over municipalities this build has no business data for |
| Paris | **`geo.api.gouv.fr` commune contour**, code INSEE **`75056`** — France's own official commune geometry, not OpenStreetMap | `https://geo.api.gouv.fr/communes/75056?geometry=contour&format=geojson` (11,463 bytes, one Feature). ⚠️ **`geometry=contour` is the parameter, NOT `fields=contour`** — the latter returns HTTP 200 with a 120-byte **Point**, the commune's centre, which would scope the whole build to a single coordinate without erroring | the commune alone — **105.4 km², matching Paris's ~105 km²**, which is what confirms the polygon is the real contour. **Commune-only scope**, decided 2026-09-22: 245 of 322 métro stations fall inside (76.1%) and **all 16 lines survive the boundary**, while the two modes mostly outside it — RER/Transilien at 8.0% and tram at 20.9% — are excluded by standing rule in every built city anyway, so scope is not what decides them. OpenStreetMap was **not** used here: its mirrors 504'd on both real hosts mid-probe, which is a fact about the host rather than about the city |
| Paris | **Every Île-de-France commune, with contours** — 1,266 polygons, the NAMING layer rather than the scoping one | `https://geo.api.gouv.fr/communes?codeRegion=11&format=geojson&geometry=contour&fields=nom,code,contour` (6.2 MB). ⚠️ **The path forms do not exist**: `/regions/11/communes` and a comma-separated `/departements/75,92,…/communes` both return **404**; the region filter is a QUERY PARAMETER | not used to scope anything — the single commune contour above does that. This layer exists so the **76 excluded métro stations are named with the commune each stands in** (34 communes), which is Los Angeles' standard: "54 of 110 stations, across 23 other places" is a readable record and a bare count is not. Same publisher and licence as the contour |
| Marseille | **`geo.api.gouv.fr` commune contour**, code INSEE **`13055`** — France's own official geometry, as Paris uses | `https://geo.api.gouv.fr/communes/13055?geometry=contour&format=geojson` (154,148 bytes, one MultiPolygon — Marseille includes the Frioul islands). ⚠️ **`geometry=contour`, NOT `fields=contour`**: the latter answers HTTP 200 with a 120-byte Point | the commune alone — **238.1 km², 2.3× Paris's 105.4**. **Commune-only scope, settled by measurement 2026-09-23** and not inherited from Paris, which the brief was explicit about: all five RTM lines are **100% inside**, 82 station-line pairs, none lost, where Paris lost 76 of 321. ⚠️ **This boundary is also what excludes Aubagne's tram** — `AUB-T` has zero stations inside, so the spatial filter that scopes the city drops another operator's network as a side effect, which is more durable than a hard-coded exclusion |
| Toulouse | **`geo.api.gouv.fr` commune contour**, code INSEE **`31555`** — France's own official geometry, as Paris and Marseille use | `https://geo.api.gouv.fr/communes/31555?geometry=contour&format=geojson` (25,030 bytes, one Polygon). ⚠️ **`geometry=contour`, NOT `fields=contour`**: the latter answers HTTP 200 with a 120-byte Point | the commune alone — **118.1 km²**, between Paris's 105.4 and Marseille's 238.1. **Commune-only, owner's call 2026-09-23 with both alternatives put and declined** — and unlike Marseille it **costs something**: Métro A loses 1 station, Métro B 1, and **Tramway T1 loses 12 of its 25**, the entire Blagnac/Beauzelle branch including the Airbus works and the exhibition centre. 62 stations → **48 inside, 14 out**, each recorded with the commune it lies in. ⚠️ **Marseille's "every line survives" test passes here only on a technicality** — T1 survives at half strength — so `config.EXPECTED_INSIDE_PER_LINE` asserts the per-line split instead, and step 1 exits if it moves |
| Lille (Regional) | **`geo.api.gouv.fr` commune contours for the Métropole Européenne de Lille**, EPCI **`200093201`** — all 95 communes, one request | `https://geo.api.gouv.fr/epcis/200093201/communes?format=geojson&geometry=contour&fields=nom,code` (427,844 bytes) | **the eleven communes that hold a station**, derived by placing all 91 stations in the official contours — 132.2 km². **Regional by owner's call 2026-09-23**: commune 59350 alone would keep Métro 2 at 19 of 44 stations and the tram at **3 of 36**, and SIRENE makes the wider filter free — one national file, Miami's situation. ⚠️ **Lambersart is absent from MEL's own station labels** and holds one Métro 2 station; the attribute would have dropped it, the spatial test did not. The set is asserted in config, so a change is a decision |
| Rennes | **`geo.api.gouv.fr` commune contour**, code INSEE **`35238`** — France's own official geometry, as every French city uses | `https://geo.api.gouv.fr/communes/35238?geometry=contour&format=geojson` (22,207 bytes, one Polygon). ⚠️ **`geometry=contour`, NOT `fields=contour`** | the commune alone — **50.3 km²**, the smallest of the five French cities. **Commune-only, owner's call 2026-09-23**, taken against a measurement that corrected the brief's "the métro is city-contained": Métro a keeps **15 of 15**, Métro b **11 of 15** and loses **both termini** — Atalante and Cesson - Viasilva in Cesson-Sévigné, La Courrouze and Saint-Jacques - Gaîté in Saint-Jacques-de-la-Lande. The worst line's survival (73%) is better than Toulouse's T1 (52%), which stayed commune-only; Lille's stub (3 of 36) is what went regional. `config.EXPECTED_INSIDE_PER_LINE` asserts the split, and step 1 exits if it moves |
| Rennes | **Every commune of Rennes Métropole, with contours** — EPCI `243500139`, 43 polygons, the NAMING layer rather than the scoping one | `https://geo.api.gouv.fr/epcis/243500139/communes?fields=nom,code&geometry=contour&format=geojson` (435,062 bytes) | not used to scope anything. It exists so the **4 excluded métro stations are named with the commune each stands in**, Paris's naming layer in miniature; `fetch_sources.py` refuses it unless it holds 35238, 35051 and 35281, since a wrong EPCI code would answer 200 with another intercommunality. Same publisher and licence as the contour |

Chicago note: the sibling asset `ewy2-6yfk` ("Boundaries - City - Map") has
null geometry; `qqq8-j68g` is the usable one.
New York note: `tqmj-j8zm`, the borough-boundary ID still in wide circulation,
now returns 404.
Boston note: **MassGIS's multi-town layer is used rather than Boston's own outline**, because naming the other towns is the bigger job here — the network is regional and 43 of 100 stations are in another municipality, a scale of exclusion that has to be citable as it is for San Diego's 16 and Los Angeles' 54. One layer then does both jobs.
This also settled a question Step 0 had left open. Boston's own water-excluded outline put four stations marginally outside the city (Boston College 6.7 m, Central Avenue 29.7 m, Longwood 51.8 m, Saint Mary's Street 58.4 m) and the Step 0 note asserted that **Boston College was "really a Boston station"** and so a distance tolerance could not separate them. That assertion was wrong: MassGIS places Boston College in **NEWTON**, 6.6 m outside Boston — two independent boundary layers agreeing on the same ~6.6 m. Four of the 43 out-of-town stations sit within 100 m of Boston, but every one is unambiguously *named*, so no tolerance is needed at all. Naming beat measuring.
Washington D.C. note: **the boundary needed no multi-jurisdiction layer to disambiguate, which is the contrast with Boston.** Only one station is even arguably marginal — Southern Av, 40.1 m outside — and the next two are Capitol Heights at 111.2 m and Arlington Cemetery at 130.0 m, both unambiguous. Boston needed MassGIS because four of its stations sat within 60 m of the line and a tolerance could not separate them. Here the states layer is for NAMING only; the District's own single polygon does the filtering.
San Francisco note: **use the host `data.sf.gov`, never `data.sfgov.org`.**
This row said `data.sfgov.org` until 2026-09-21, when re-running the recorded
command showed the old host **301-redirects** and the documented `curl -sG`
carries no `-L` — so it silently wrote a 654-byte HTML redirect stub into
`sf_county_boundary.geojson` and exited 0, with the failure surfacing later
inside geopandas. That is the same host rule the assessor roll already needed
for a different symptom (403 on `/resource/`), so treat it as one rule for this
city. Unfiltered, the same request returns 989,873 bytes of all nine counties.

`wamw-vt4s` is a **nine-county** Bay Area layer, so the
`county` filter is not optional — unfiltered it would scope the city to the
whole region. This endpoint was recovered on 2026-09-21 (it had been recorded
nowhere) by identifying the raw file from its own fields, `objectid` /
`fipsstco` / `county` with FIPS `06075`; the endpoint reproduces the file
byte-for-byte at 38,822 bytes with identical geometry, so it is the confirmed
original source and not a lookalike.

Vancouver note: this is the only city here scoped to **two municipalities with
two boundary layers**, because Surrey has no rail of its own and SkyTrain is
TransLink's. A station is in scope if it falls inside *either* polygon, and
every kept station is written to `outputs/vancouver/station_municipalities.csv`
with the municipality it sits in — so the regional scope is readable rather
than inferred. Miami is the precedent, but the easy version of it: one
publisher, one schema, one set of terms across all 34 of its municipalities.

## Geocoding

| Service | Used by | Endpoint | Note |
|---|---|---|---|
| US Census Bureau bulk geocoder | Los Angeles, New York, Washington D.C. | `https://geocoding.geo.census.gov/geocoder/locations/addressbatch` | Free, no API key, US addresses only. Benchmark `Public_AR_Current`. Responses cached by batch content hash, so re-runs and drift checks stay offline and deterministic. D.C.'s use is different in kind from Los Angeles': LA's flagged rows had CORRUPT coordinates, D.C.'s have none at all, and Step 0's expectation that `MAR_ID` would recover them was wrong — the same 452 rows lack both. 387 of 451 were matched and every one fell inside the District polygon |

## Basemap tiles

Rendered maps use Folium's default OpenStreetMap tiles. Attribution is in the
rendered HTML. Choosing a tile provider deliberately is still open in
`PLAN.md`.

## Licences and terms of use

Reviewed 2026-09-21. This records what each source's own published terms say,
and what could not be established. It is a developer's reading of public
documents, not legal advice, and none of it has been reviewed by a lawyer.

A separate question is already settled: what is *appropriate* to publish,
independent of what is *permitted*. That is in `docs/excluded_categories.md`.

### Explicit and permissive — confirmed

| Source | Licence | Attribution declared |
|---|---|---|
| San Francisco businesses (`g8m3-pdis`) | **Open Data Commons PDDL 1.0** (public domain dedication) | "City and County of San Francisco" |
| San Francisco boundary (`wamw-vt4s`) | **Open Data Commons PDDL 1.0** | none declared |
| Los Angeles businesses (`6rrh-rzua`) | **CC0 1.0 Universal** (public domain dedication) | "Office of Finance" |
| San Diego businesses | Portal terms explicitly permit use and **"Derivative Work"**, defined as "a work that is based in any way or to any extent on the Data". No attribution requirement stated | — |
| Boston — every source used above (food inspections, Licensing Board, cannabis, city boundary, plus the neighbourhood, SAM address and Property Assessment layers) | **Open Data Commons PDDL** (public domain dedication), declared per-dataset in CKAN's `license_id` as `odc-pddl` | none declared |
| **Brazil — IBGE CNEFE 2022** (**candidate, not built**; São Paulo and Rio first) | **Free use by federal law** — Decree 8.777/2016 art. 4 and Lei 14.129/2021 art. 29 — subject to LGPD principles. **No IBGE licence document exists.** Read 2026-09-23; four restrictive readings recorded in the Brazil section below | **Required** (the decree's definition of open data: *"limitando-se a creditar a autoria ou a fonte"*). No wording prescribed; use `Fonte: IBGE, Cadastro Nacional de Endereços para Fins Estatísticos (CNEFE), Censo Demográfico 2022.` |
| **Seoul** — the eight `인허가 정보` datasets below (**candidate, not built**) | **공공누리 제1유형 / KOGL Type 1** — attribution required, commercial use and derivative works permitted | 저작권자 **서울특별시**; 제3저작권자 **없음** (none) |
| **Province of British Columbia** — the ABMS municipalities layer (`WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_MUNICIPALITIES_SP`), which NAMES Vancouver/Surrey's 30 out-of-city stations | **Open Government Licence – British Columbia v2.0** — "worldwide, royalty-free, perpetual, non-exclusive licence… including for commercial purposes"; free to "Copy, modify, publish, translate, adapt, distribute". **Terminates automatically on breach.** Excludes Personal Information and the Province's own marks — neither of which a boundary polygon is. The WFS is also subject to the separate **API Terms of Use for OGL Information** (read 2026-09-22), which add operational limits and **no new notice**. Read 2026-09-22, stored at `docs/licenses/bc-open-government-licence.txt` | **Required, verbatim** — `Contains information licensed under the Open Government Licence – British Columbia.` See notice 17. **Two sibling BC layers are licensed "Access Only" and would NOT permit this**; see the stored file's header |
| San Francisco assessor roll (`wv5m-vpq2`) — the residence-filter join | **Open Data Commons PDDL 1.0** (public domain dedication), declared in the dataset's own `license` field as "Open Data Commons Public Domain Dedication and License" | none declared |
| **LA County Assessor parcels** (`public.gis.lacounty.gov`) — the residence-filter join | **Explicit grant**, read 2026-09-22 from the County's Enterprise GIS Terms of Use: "you are granted a license to **copy, publish, distribute and/or transmit the Data, to adapt the Data and to exploit the Data for commercial and/or personal use**". Automatically voided on violation. Grants "no right to use the Data in any way that suggests County's endorsement of your use" | **Recommended, not required** — a citation format is offered as "the recommeded citation format", so this adds no notice. The service's `copyrightText` is "Los Angeles County Office of the Assessor" |
| **SanGIS/SANDAG tax parcels** (`geo.sandag.org`) — San Diego's residence-filter join | **Permitted with conditions**, and the conditions are unlike any other source here — see below. Redistribution is "discouraged, but **not** prohibited". Read 2026-09-22 from the layer item's own `licenseInfo`, which carries the full *SanGIS GIS Data End User Use Agreement* | **PROHIBITED at this project's scale** — see below. "Copyright SanGIS 2015 - All Rights Reserved" |

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
add one. It is also the reason `check_provenance.py` checks that notices and
`_NOTICES` correspond, rather than that every source has a notice.

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

**Not established, and flagged rather than assumed:** San Diego's municipal
**boundary** layer sits on the same `geo.sandag.org` host but is a different
service (`rest/directories/downloads/Municipal_Boundaries.geojson`) and its own
terms have not been read. **It is now its own row under “Still not
established” below**, rather than a caveat inside this entry — a caveat is
not a work item, and this one contradicted that table's own claim to list
every unread source for half a day. Its row predates this review. Do not extend the
parcel agreement to it by proximity — that is the Philadelphia mistake, where a
licence on one page turned out not to govern the dataset beside it.


PDDL and CC0 are both public-domain dedications, so neither compels
attribution; the maps credit these agencies anyway, which is good practice.

San Diego's terms carry a strong disclaimer worth knowing about: the data is
"as is" and "as available", the city "makes no representation or warranty that
the information contained in the Data is accurate, true or correct", and the
user indemnifies the city for claims arising from their use of it.

#### Madrid — `censo de locales`, read 2026-09-22 (**BUILT 2026-09-22**)

**PERMITTED WITH CONDITIONS.** Two documents apply and both were read.

**1. The declared licence.** `datos.madrid.es` CKAN gives `license_id = "cc-by"`,
`"Creative Commons Attribution 4.0 International (CC BY 4.0)"`, `isopen: true`,
author `Ayuntamiento de Madrid`, on both `200085-0-censo-locales` and its
historical twin. **A deliberate choice**: the portal's `license_list` also
offers `cc-by-nc` and `cc-by-nc-sa`, which would forbid this project, plus four
bespoke restrictive sets (Madrid Destino, Bibliotecas, EMT, the general
conditions below).

**2. The general conditions, which bind by conduct.** *Condiciones de uso*
links *"Condiciones generales para la modalidad general de puesta a disposición
de los documentos reutilizables del Ayuntamiento de Madrid"*, and that document
opens by making itself binding **without any acceptance step**:

> "Las presentes condiciones generales **obligan a cualquier persona y/o empresa
> que reutilice datos por el mero hecho de hacer uso** de los documentos
> sometidos a ellas."

Structurally this is Philadelphia's shape — terms incorporated by the act of
use rather than by a licence field. **The content is the opposite.** The grant
is broad and explicit:

> "permiten la reutilización de los documentos y datos sometidos a ellas **para
> fines comerciales y no comerciales** … la reutilización autorizada incluye
> actividades como la **copia, difusión, modificación, adaptación, extracción,
> reordenación y combinación** de la información."

plus a free, non-exclusive assignment of any IP rights, worldwide, for the
maximum term the law allows. It expressly covers data "en sus niveles más
desagregados o 'en bruto'".

**Six obligations, and four of them go beyond CC-BY:**

| | Obligation |
|---|---|
| 1 | **Prescribed attribution wording** — *"Origen de los datos: Ayuntamiento de Madrid"*. CC-BY wants attribution; Madrid says what it must say |
| 2 | **State the last-update date** of the documents reused, where the original carried one. **CC-BY does not require this** |
| 3 | **No implied endorsement** — must not "indicar, insinuar o sugerir que el Ayuntamiento de Madrid participa, patrocina o apoya" the reuse |
| 4 | **Do not distort the meaning** — *"Está prohibido desnaturalizar el sentido de la información"* |
| 5 | **Preserve the metadata** on update date and reuse conditions; do not alter or delete it |
| 6 | **Re-identification is expressly prohibited** — "está expresamente prohibido realizar labores de re-identificación de personas a partir de estos datos y otras fuentes" |

**Obligation 4 is the fourth appearance of the transformation family** — after
INEGI, Montréal and Seoul's KOGL. Ring density, bucketing and storefront
filtering are all interpretation, so the notice must say the map interprets the
data rather than merely crediting the source. **Obligation 6 is the first time
a licence has contractually forbidden what this project's privacy invariant
already forbids voluntarily**, and it bears directly on the `rotulo` field:
combining a trade name with a precise address is exactly the operation the
clause is about, so the existing `check_personal_exposure.py` gate is a licence
obligation here, not only a house rule.

Also recorded: the disclaimer is ordinary (no warranty, no guarantee of
continuity, reuser bears the risk), and reusers are placed under the sanctions
regime of **article 11 of Ley 37/2007** on public-sector information reuse.

**6b — privacy work already done at source?** Not applicable in the French or
Edmonton sense: the census carries premises, not people. `rotulo` is a shop
sign. Obligation 6 above makes the project's own residence check contractual.

#### Seoul — eight `인허가 정보` datasets, read 2026-09-22 (CANDIDATE, not built)

Recorded now because the licence was read now; **no Korean city is built, so
nothing here is an active obligation yet.** Source: `data.seoul.go.kr`,
downloaded via the SHEET CSV export (`ssUserId=SAMPLE_VIEW`, no account — see
`docs/global_country_shortlist.md`).

| `infId` | Dataset | Bucket | Active premises |
|---|---|---|---|
| `OA-16094` | 서울시 일반음식점 인허가 정보 | Food | 120,182 |
| `OA-16095` | 서울시 휴게음식점 인허가 정보 | Food | 37,113 |
| `OA-16063` | 서울시 미용업 인허가 정보 | Personal services | 33,679 |
| `OA-16064` | 서울시 이용업 인허가 정보 | Personal services | 2,366 |
| `OA-16065` | 서울시 세탁업 인허가 정보 | Personal services | 3,263 |
| `OA-16146` | 서울시 목욕장업 인허가 정보 | Personal services | 673 |
| `OA-16044` | 서울시 숙박업 인허가 정보 | Personal services | 2,788 |
| `OA-16007` | 서울시 동물병원 인허가 정보 | Personal services | 981 |

**All eight carry identical metadata**, checked individually rather than
inferred from one: `이용허락범위` = **공공누리 1유형 : 출처표시 (상업적 이용 및
변경 가능)**, `저작권자` = 서울특별시, **`제3저작권자` = 없음**, `갱신주기` =
매일 (daily). `원본시스템` is 공공데이터포털(지방행정 인허가정보) — i.e. these
are Seoul's republication of the national LOCALDATA register.

**`제3저작권자: 없음` is the check that matters most here.** It is the field
that would disclose rights incorporated *by reference* — the trap that hid
Philadelphia's prohibition behind a licence forbidding nothing. Seoul declares
none, on all eight.

**KOGL Type 1, from `kogl.or.kr` itself rather than from the label.** Three
obligations, and one of them is easy to miss:

1. **출처표시 — attribution.** The prescribed form names the institution, the
   year, the KOGL type and the dataset title. And: *"온라인에서 출처
   웹사이트에 대한 하이퍼링크를 제공하는 것이 가능한 경우에는 링크를
   제공하여야 합니다"* — **where a hyperlink is possible, one must be
   provided.** That is an obligation of the same shape as ODbL's, not a
   courtesy, and it is the part a plain "Source: Seoul Metropolitan Government"
   string would fail.
2. **No implied endorsement.** *"이용자는 공공기관이 이용자를 후원한다거나
   공공기관과 이용자가 특수한 관계에 있는 것처럼 제3자가 오인하게 하는 표시를
   해서는 안됩니다"* — nothing may suggest Seoul sponsors this project or has
   any special relationship with it.
3. **저작인격권 — moral rights, which bear on transformation.** Modified use
   must not mislead; the licence's own second example is *"연구보고서의
   연구성과나 통계수치 등을 수정하여 제3자로 하여금 착오를 불러일으킬 수 있는
   경우"* — altering figures so as to mislead a third party. This project
   aggregates premises into per-station counts, which is exactly a statistical
   transformation, so it falls under the same disclosure duty already met for
   **INEGI** and **Montréal**: say plainly that the counts are this project's
   derivation and not Seoul's published figures.

**The publisher already did the privacy work — verified, not assumed.** All
eight files were checked for a proprietor-name column (`대표자`, `성명`, `이름`,
`주민`, `생년`): **none exists** in any of them, across 37–39 columns. The only
name field is `사업장명`, the registered trade name, which this project's
invariant explicitly permits. Same posture as France's *non-diffusible*,
Edmonton's `<REDACTED FOR PRIVACY>` and Austria's GISA.

**One privacy item left for build time, not resolved here.** Korean salon and
restaurant trade names very often *contain* a personal name — `김은미장`
("Kim Eun-mi salon") among 미용업, and ~30% of 사업장명 values are a bare 2–4
hangul token. These are registered trade names, so the invariant allows them,
but `scripts/check_personal_exposure.py` will need a Korean-aware pass rather
than its current one, and Personal services is the bucket where a salon
operating from a residential address is most plausible. **Flagged for
`add-city` Step 0, not pre-judged.**

### 🇧🇷 Brazil — IBGE's CNEFE 2022 (candidate, not built): the grant is a LAW, not a document

**Source:** *Cadastro Nacional de Endereços para Fins Estatísticos*, Censo
Demográfico 2022 — one CSV per município, keyless, at
`ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/`.
Every address in the country with a field-collected coordinate; rows with
`COD_ESPECIE = 6` carry `DSC_ESTABELECIMENTO`, the enumerator's
identification of the establishment. **It is Brazil's business leg AND its
coordinate leg** — no CNPJ, no geocoder. Read 2026-09-23 by the `licence-read`
agent; its full working is in the session scratchpad, not the repository.

**PERMITTED WITH CONDITIONS — and no IBGE document grants it.** No licence
exists anywhere machine-readable: the FTP is a bare listing, the zips hold
only the CSV, the dictionary is silent, and CNEFE is **not on dados.gov.br**.
The grant is federal law that binds IBGE as a public foundation:

- **Decree 8.777/2016, art. 4** (as reworded by Decree 9.903/2019): *"Os
  dados disponibilizados pelo Poder Executivo federal e as informações de
  transparência ativa são de livre utilização pelos Poderes Públicos e pela
  sociedade."*
- **Lei 14.129/2021, art. 29**: *"...são de livre utilização pela sociedade,
  observados os princípios dispostos no art. 6º da Lei nº 13.709 [LGPD]."*
- The FTP's own line: *"Todos os arquivos aqui disponíveis são públicos."*
  — a statement that they are public, not a licence.

**Two conditions, neither of them an act owed to IBGE:**

1. **Credit the source.** No wording is prescribed. Use IBGE's own form:
   **`Fonte: IBGE, Cadastro Nacional de Endereços para Fins Estatísticos
   (CNEFE), Censo Demográfico 2022.`** Add it to the numbered notices when
   the first Brazilian page ships, not before — `check_provenance.py` pairs
   that list with `app/components.py`.
2. **LGPD principles for any personal data published** (art. 29's proviso;
   LGPD art. 7 §3 — *finalidade, boa-fé e interesse público*). **This makes
   the privacy rule below a licence condition, not house style.**

**Four restrictive readings were found and NOT resolved in this project's
favour by the reader. The owner decided on 2026-09-23 to proceed on the law**,
on a recorded reasoned position — the Philadelphia shape:

| | Reading | Why the project proceeds |
|---|---|---|
| **A** | A **2009 IBGE service-desk email**, surviving only in an OSM mailing-list archive: its dissemination policy *"não contempla a modalidade de disponibilizar o produto do seu trabalho em sites de terceiros"* | Informal, unpublished, about mirroring maps and orthophotos, and **predates both the 2016 decree and the 2021 law**. A second reply in the same thread allowed reuse with citation |
| **B** | The decree's **copyright waiver** (art. 4 §1) covers databases whose rights belong to **the União**; IBGE is a foundation and its PDFs say "© IBGE" | The **caput** and **Lei 14.129 art. 29** grant free use regardless; the CSVs carry no © notice |
| **C** | **Lei 5.534/1968**: informants' data are secret and *"usadas exclusivamente para fins estatísticos"* | The duty is **IBGE's**, and IBGE discharged it: its methodological note (Notas metodológicas n. 04) says establishment names were **published deliberately**, and its secrecy review withholds what identifies informants |
| **D** | CNEFE is **not in IBGE's open-data plan** and not on dados.gov.br | Art. 4 speaks of data *"disponibilizados"*, not only catalogued datasets |

**What may not be SAID** (from IBGE's own documentation, not its terms):
the names were **not checked against any register or standardised**, so never
present them as verified business names; **IBGE did not classify the
establishments** — the three buckets are this project's reading of free text;
and **the data are not current** — they are the 2022 census fieldwork.

**Privacy rule, decided 2026-09-23:** at any address that also holds a
dwelling (`COD_ESPECIE` 1 or 2 at the same address), the tooltip shows the
**category, never the description text**. Structural rather than a name list.
Measured before deciding: a first name at a dwelling address is **2.1%** of
Rio's mapped rows and **1.1%** of São Paulo's; the structural rule reaches
**55.4%** and **37.3%**, which is the price of not trusting a name list —
and like Milan, where ~82% of pins carry no trade name, fewer published names
is a privacy asset rather than a loss.

#### Brazil's rail sources, read 2026-09-23 by the `licence-read` agent

| Source | Verdict | What it requires |
|---|---|---|
| **Rio de Janeiro** — `pgeo3.rio.rj.gov.br/.../Transporte_Trafego/Transporte_publico/MapServer` layers 19, 18, 9, 10 (metro stations and lines, VLT stops and lines) | **PERMITTED WITH CONDITIONS — CC BY 4.0**, declared at SERVICE level (`info/iteminfo`: *"This work is licensed under a Creative Commons Attribution 4.0 International License"*) and on all four Data.Rio items | Credit **"Prefeitura da Cidade do Rio de Janeiro / Instituto Pereira Passos (IPP)"**, the licence link, a link to the data, and **a statement that the data was modified** (CC BY §3(a)(1)(B) — required, not optional). Operator names and colours (MetrôRio, VLT Carioca) come from elsewhere and are **not licensed** by it |
| **São Paulo** — GeoSampa WFS `estacao_metro`, `linha_metro` | ⚠️ **AMBIGUOUS IN A WAY THAT MATTERS — owner decision** | See below |

**Rio: the "sem alteração" clause does NOT apply.** Data.Rio's *"Uso público,
citadas as fontes e sem alteração das informações originais"* is set **item by
item** — 2,727 of the PrefeituraRio account's 5,069 items, 2,671 of them PDFs,
2,722 last changed in 2018 — and is **absent from all four rail items, the
service record and its metadata.** Any OTHER Data.Rio source needs its own
check; the portal is split roughly in half.

**Rio: one clause RAISED, not resolved.** The IPP's *Termo de Uso do SIURB.RIO*
(v3.0, Aug 2025) governs the system that owns the server: §1 *"Ao utilizar o
Sistema, o usuário ... estará legalmente vinculado"*, and §6 iv makes the user
liable for *"todos e quaisquer danos, diretos ou indiretos"* caused to the
Administration or third parties. **Reading that binds:** fetching from the
server is using the System. **Reading that does not:** the Termo defines users
as *"pessoas naturais que utilizarem o Sistema por meio de login de acesso"*.
Even if it binds, it prohibits nothing the build does — it is **fault-based
liability for damage caused**, narrower than Hong Kong's indemnity, closer to
IBGE's portal clause. **Owner call — ✅ ACCEPTED 2026-09-23**: Rio's rail
comes from these layers, with OSM as the colour source and cross-check.

**São Paulo: the licence may not reach the layers.** GeoSampa declares
**CC BY-SA 4.0** on these layers, but its own *Créditos › Licença dos dados*
says: *"A licença CC BY-SA exibida no mapa aplica-se exclusivamente aos dados
geoespaciais das camadas, produzidos pelos órgãos da Prefeitura de São
Paulo."*

- **Reading A — covered:** the ISO lineage says the geometry is the
  Prefeitura's own photogrammetry (*"localizados por meio do Mapeamento Digital
  da Cidade de São Paulo - MDC"*); the portal attaches *"© Produzido por
  SMUL-PMSP-PRODAM - CC-BY-SA"* to exactly these layers; Lei 16.051/2014 art. 1
  §1 makes published Prefeitura data *"livremente utilizados, reutilizados e
  redistribuídos"*, including *"mapas"*.
- **Reading B — not covered:** both ISO records name the author as the **State's
  Companhia do Metropolitano (METRÔ)**; `sg_fonte_original = METRO` on all 94
  stations; the portal's attribution string is a blanket default on all 502
  layers; a municipal law cannot license a State company's work; Metrô's own
  portal says *"License Not Specified"*.
- **And if CC BY-SA applies, SHARE-ALIKE reaches the derived geometry**
  (§3(b)) — the repository is MIT. Narrow reading: only the station, line and
  ring geometry must be offered under CC BY-SA; broad: the rendered São Paulo
  map is Adapted Material.

**Not resolved in this project's favour.** The one party who can settle A
against B is `geosampa@prefeitura.sp.gov.br`.

✅ **DECIDED 2026-09-23 by the owner — the question is AVOIDED, not answered:
São Paulo's line and station geometry comes from OpenStreetMap**, as Mexico
City's and Barcelona's do, and **GeoSampa is used only to decide WHICH lines
operate** — a fact read from it, not a reproduction of its geometry. That also
keeps OSM's unbuilt Lines 6 and 17 off the map. OSM's terms are already
settled by precedent: under ODbL §4.5(b) the rendered map is a Produced Work,
so share-alike does not reach it; the committed station file carries an ODbL
notice and the linked public repository offers the method (§4.6) — the
Toulouse/Rennes discharge, `docs/licenses/odbl-toulouse-rennes.md`. **Why the
precedent does not simply carry over to GeoSampa:** CC BY-SA 4.0 has no
Produced Work carve-out, so its share-alike question stays open and is now
not this project's to answer. If São Paulo's build ever wants GeoSampa's
geometry, the email above comes first.

### 🇹🇼 Taiwan (candidate, not built) — read 2026-09-23 by the `licence-read` agent

| Source | Verdict | What it requires |
|---|---|---|
| **Taipei door plates** — `臺北市門牌位置數值資料` (民政局, data.taipei, dataset 155472), used as the GEOCODING REFERENCE | **PERMITTED WITH CONDITIONS — 政府資料開放授權條款-第1版 (OGDL v1)**, declared on the publisher's own portal and on data.gov.tw. Grant §二(一): *"不限目的、時間及地域、非專屬、不可撤回、免授權金進行利用 ... 編輯、改作 ... 衍生物"* | **The annex's attribution statement (顯名聲明), and it is LOAD-BEARING**: §三(二) — failing it means *"視為自始未取得開放資料之授權"*, never licensed at all — and it covers **derivatives**, so the published coordinates carry it though the door-plate table is never published. Form: `提供機關／臺北市政府民政局 [2026] [臺北市門牌位置數值資料 20260902]` + *"此開放資料依政府資料開放授權條款 (Open Government Data License) 進行公眾釋出，使用者於遵守本條款各項規定之前提下，得利用之。"* + `https://data.gov.tw/license`. No patents or trademarks licensed |
| **The national business tax register** — `全國營業(稅籍)登記資料集` (財政部財政資訊中心 / FIA, `eip.fia.gov.tw/data/BGMOPEN1.zip`, data.gov.tw 9400) — the BUSINESS leg for every Taiwanese city | **PERMITTED WITH CONDITIONS — OGDL v1** (`license: "1"`), plus the FIA's own *政府網站資料開放宣告*, which repeats the grant and adds: cite the source (*"應註明出處"*); no marks or emblems; no implied endorsement; and **§二(二): personal data that is public must still be handled under the Personal Data Protection Act by the user** | The same prescribed 顯名聲明, e.g. `財政部財政資訊中心 2026 全國營業(稅籍)登記資料集（資料日期 YYYY-MM-DD）` — the CSV's first data row carries its own date. ⚠️ **Do not present the filtered, geolocated points as the register itself** (FIA 四) |
| **TDX** (交通部運輸資料流通服務平臺) metro endpoints | ⛔ **NOT USED.** Its own terms (not OGDL): scripted access needs a **registered member key**; keyless is a browser-only visitor mode, 20 calls/day per IP; registration wants a Taiwanese mobile number or manual review. The server now enforces it (curl 401, browser 200) and **it is not worked around** | — |

**A fault-based liability clause — RAISED, owner call.** OGDL v1 §六(三):
*"使用者...因故意或過失，致資料提供機關遭受損害，或第三人因此向資料提供機關請求賠償損害，使用者應對各機關負賠償責任。"*
The same class as Rio's SIURB clause and IBGE's portal terms — liability for
damage the user causes deliberately or negligently, narrower than Hong Kong's
indemnity. **It rides on every OGDL v1 source in Taiwan**, so one decision
covers them. ✅ **ACCEPTED by the owner 2026-09-23, for all of Taiwan.**

**The personal-name question — the one ambiguity that mattered, DECIDED.**
For small sole proprietors (獨資) the registered business name IS the owner's
name (`黃信雄`, `陳雅娟`); in Taipei, **3,763 storefronts (4.9%)** read that way,
63% of them market stalls. **The FIA itself refuses to publish owners' names**
— it removed them in 2016 and refused again on 2026-08-14: *"如將負責人姓名無任何
限制下全數公開，恐有過度揭露個人資料、侵害資訊隱私、違反比例原則之疑慮"* —
relying on Ministry of Justice letter 法律字第10503516500號. The Personal Data
Protection Act reaches a foreign reuser of Taiwanese residents' data (第51條
第2項). **Decided 2026-09-23: a name is shown only when it is a TRADE name** —
for companies and branches (legal entities), and for sole proprietors only
when the name carries a business marker (行/店/社/館/坊…); otherwise the tooltip
shows the category. It errs toward hiding, which the publisher's own refusal
argues for. Removal requests under PDPA 第3條/第19條 are honoured, which the
project's standing commitment already says.

**Taiwan's rail comes from the agencies instead**, keyless and under OGDL v1
(one read covers the licence; each source still needs its attribution line):
Taipei's `臺北都會區大眾捷運系統路網圖` and `車站點位圖`, Taichung Metro's
Green Line stations, the national land-survey centre's `捷運車站` layer.

**Not a source here: CNPJ.** Receita Federal's CNPJ open data moved in early
2026 to a Nextcloud share (`arquivos.receitafederal.gov.br/index.php/s/YggdBLfdninEJX9`;
the old `dados_abertos_cnpj/` directory has returned **404 since 2026-01-30**)
and **the host refuses connections from outside Brazil** — measured
2026-09-23 from 16 check nodes: **the Brazilian one 200, all 15 others in 11
countries reset.** A publisher's access control, not an outage, so this
project does not route around it. Its terms were never read.

### Permissive on reading the terms themselves

| Source | What its terms say |
|---|---|
| **NYS retail food (`9a8c-vfzj`), NYS salons (`y3u4-jbgh`)** | The datasets declare no licence field, but the portal's "OPEN-NY Terms of Use" (dataset `77gx-ii52`, last modified 2013-03-08) is explicit: "At their core, the OPEN-NY Terms of Service are among the least restrictive of any terms of service … The OPEN-NY Terms of Service do **not** contain restrictions requiring members of the public to use attribution, to re-post the license terms with any re-uses of the data, to impose share-alike or technical restrictions, nor require the public to obtain pre-approval before re-use of the data." And: "So long as you are not doing anything malicious with NYS data, you may use it as you wish, subject to no other requirements." Conditions: lawful use; the State may require you in writing to stop displaying its content if it believes you are in breach. |
| **Chicago businesses (`r5kz-chrr`), Chicago boundary (`qqq8-j68g`)** | Reuse and derivative applications are contemplated, but **conditionally** — see the required notice below. The city "may require a user of this data to terminate any and all display, distribution or other use … for any reason", reserves all intellectual-property rights, and requires the user to indemnify it. |
| **Philadelphia businesses (`business_licenses`), Philadelphia boundary (`City_Limits`)** | Both carry a **named licence, "City of Philadelphia License"**, whose text is a rights reservation and disclaimer rather than a grant: the City "reserves all rights in the database and any data contained therein", the data is "as is" without warranty, the user "will assume complete responsibility for any and all occurrences resulting from its use or display" and holds the City harmless, and "browsing City data on this site constitutes acceptance". Its own text forbids nothing and requires no notice — **but the dataset page also binds a reader to the City's separate Terms of Use, which DO prohibit republication and modification without written permission (read 2026-09-21; see the open question below). This is the one source in the project whose terms, read literally, do not permit what is built here.** The clearest affirmative signal is on the boundary dataset, which states **"Usage: Public use; Free"**; the business-licence dataset's page carries no such field, so that statement covers the boundary layer specifically. Both sit in the City's Open Data Program, whose stated purpose is public reuse. **One judgment call follows — see below.** |
| **NYC DOHMH (`43nn-pn8j`), NYC DCWP (`w7w3-xahh`), NYC boroughs (`gthc-hcne`)** | **The absent licence field is required by law, not an oversight.** NYC's Open Data Technical Standards Manual states that Local Law 11 of 2012 "requires that data sets must be available **without registration requirement, license requirement, or usage restrictions**". The city therefore cannot attach a licence to these datasets. The "All Rights Reserved" notice in the nyc.gov footer covers nyc.gov's own website content, not datasets published under the Open Data Law. One condition does attach — see the notice below. |
| **Census TIGERweb state polygons** (used by Washington D.C. to name the 58 excluded stations' state) | A **US federal government work**, so not copyrightable — the Census Bureau's own terms say its data are in the public domain and may be used freely, asking only that the Bureau not be cited as endorsing a derived product. No attribution required, none claimed here beyond the endpoint record above. |

### Still not established

| Source | Status |
|---|---|
| **US Census bulk geocoder** | Terms page not read. A US federal government work, used only to derive coordinates stored in this project's own outputs. Low priority. **It was described here as "the only item left unread" until 2026-09-22**, which stopped being true the moment the row below was added — a count kept by hand in one row about the contents of its own table. |
| **Boston "Business Inventory" (`47bd8208`)** | The one dataset on `data.boston.gov` whose `license_id` is `notspecified` rather than `odc-pddl`. Not established, and not pursued, because the source is deliberately unused (its coverage is downtown plus three corridors). **If it is ever used, the governing terms must be established first** — the portal's own "Open and Protected Data Policy" and the 2014 open-data executive order are the documents to read, not the boston.gov site footer. That is the NYC lesson: the parent site's notice covers the website, not the datasets. |
| **San Diego municipal boundaries** (`geo.sandag.org/server/rest/directories/downloads/Municipal_Boundaries.geojson`) | Terms not read. It sits on the same host as the SanGIS tax parcels, whose End User Use Agreement WAS read on 2026-09-22, but it is a **different service** and the agreement is deliberately not extended to it by proximity — that is the Philadelphia mistake, where a licence on one page turned out not to govern the dataset beside it. Its row in the boundary table predates the licence review entirely: it is this project's very first city, and the layer has been in use since 2026-09-18. **Higher priority than the Census geocoder**, because this one scopes a published map rather than deriving a coordinate. Raised 2026-09-22 by the SanGIS reading, and listed here so it is an open item rather than a sentence buried in another source's entry. |
| **Miami-Dade Local Business Tax, its municipal boundary layer, and Miami-Dade Transit's GTFS** | All three carry a disclaimer and no grant. The ArcGIS items' `licenseInfo` is purely about ACCURACY — “Miami-Dade County provides this data for use 'as is'… not accurate to surveying or engineering standards… assumes no responsibility for errors or omissions” — and says nothing whatever about reuse, redistribution, modification or attribution. The GTFS has no `feed_info.txt`, and no separate MDT developer terms were located. **ESTABLISHED 2026-09-21, by reading rather than asking — and this row's earlier claim that no document existed was wrong.** One does: the Open Data Hub's own designated Terms of Use at `https://opendata.miamidade.gov/pages/terms-of-use`. Its entire substance is the accuracy disclaimer quoted above. The county-wide "Liability Disclaimer and User Agreement" at `miamidade.gov/global/disclaimer/disclaimer.page` was read too, and is liability terms only — no copyright claim, no reuse restriction. So three County documents now say nothing whatever about reuse, redistribution, modification or attribution, which is a **definitive absence of restriction from the County's own authoritative pages** rather than an unexamined gap. No enquiry to the County is needed. The affirmative signals stand: all three sources are published by the County's own ITD Geospatial group on its public open-data portal, in formats meant for reuse. |

Note the shape of this. **The business registries are mostly permissive and the
transit feeds are mostly not** — and the two are inverted within Los Angeles,
whose business data is CC0 while its GTFS terms are the most restrictive of
anything here. Canada inverts it again: there the registries almost all
prescribe their own sentence and the feeds mostly ride on the same municipal
licence.

**The sentence that used to end this paragraph is gone, and it is the third
hand-kept count in this file to turn out wrong.** It read "New York contributes
four of the eight registries and is the only source whose reuse position could
not be established at all" — and by 2026-09-22 there were **37** rows in the
business table rather than eight, while New York's position *is* established:
Local Law 11 of 2012 forbids the City attaching a licence at all, which is why
it sits under *Permissive on reading the terms themselves* two tables up. An
established absence is not an unestablished position, and conflating the two is
how a source gets re-investigated every time somebody reads this section.

The durable point the count was reaching for: **an unread source and a source
read to silence look identical in a summary and are completely different in
kind.** This table is only for the first. Anything read and found to impose no
restriction belongs above, named, with the pages that were read — Miami-Dade is
the worked example, and it moved up here after the reading rather than before.

### Transit feeds (GTFS) — checked 2026-09-21

Line geometry is redrawn from each feed's `shapes.txt` into every map, so these
terms bear directly on what is published. **No feed in this project declares a
licence in `feed_info.txt`** — LA Metro's even includes a `feed_license` column
and leaves it empty, pointing to its developer terms instead. Several feeds ship
no `feed_info.txt` at all (Miami, Calgary, Toronto), and two ship one that
carries a validity window but no licence (Montréal, Vancouver), so in every case
the agency's own terms page is the only source and every row below was read from
one.

| Agency | Redistribution | Attribution | Other conditions |
|---|---|---|---|
| **MTS** (San Diego) | Permitted: "non-exclusive, limited and revocable rights to use, reproduce, and redistribute" | Not required | MTS trademarks "may not be used in association with GTFS Data". As-is, no liability; may withdraw the data at any time |
| **SFMTA** | Permitted: "use, reproduce, and redistribute" | **Required, in specific wording** (below) | Must also display liability disclaimers; no trademarks or logos without written permission |
| **LA Metro** | **Restricted** — prohibits "unauthorized redistribution and publication" and requires you "not change, tamper, dismantle, augment, misrepresent or otherwise modify the Transport Information" | **Required** — must "acknowledge Metro as the provider of the Transport Information" and not claim ownership | No Metro trademark; must not "integrate Transport Information as part of any advertisement"; on termination you "shall immediately remove the Transport Information and all references to it" |
| **CTA** | Permitted: "use, reproduce, distribute, display, process and create derivative works" | Optional but encouraged: "Data provided by Chicago Transit Authority", "Data provided by CTA" or "Powered by CTA data" | **Purpose-limited** — the licence is granted to "assist mass transit riders or promote public transportation"; may not sell CTA Data separate from the application; may not imply affiliation or endorsement |
| **MTA** (New York) | Permitted: the feeds are "provided without charge", and the agreement "authorizes you to download and host the data on a non-MTA server ... and to make the data available to others who will access that non-MTA server". No API key needed for the static subway feed | Not required, but you "will not state or imply in any manner that your app is licensed by MTA"; you may state the data was obtained from MTA and is redistributed from your own server | **Corrected 2026-09-21 — this row previously recorded only the "Our data feeds are free to use" line from `mta.info/developers`, which is the landing page, not the terms.** The actual agreement (`https://new.mta.info/developers/terms-and-conditions`, page dated 2024-03-13) says **"You will not modify or delete any of the data"**, though its next sentence permits "an app that uses some but not all of the data". Also: must not "state or imply that the data is accurate, complete, or timely"; must serve the data from a non-MTA server and never directly from MTA's; MTA may change or terminate the agreement at any time without notice. Logos, maps and symbols need a separate licence application (free of charge but must be applied for). **An open decision, not a settled one — see `PLAN.md`.** Local copy: `docs/licenses/mta-terms-and-conditions.txt` |
| **MBTA / MassDOT** (Boston) | Permitted: §3.1 grants "non-exclusive, limited, and revocable rights to use, reproduce, and redistribute the Data" | **Required** — §4.1 "Clearly acknowledge MassDOT as the provider of the Data" | §4.2 **expressly permits** combining the Data with other data. §4.1 forbids reproducing "MassDOT or any of its agencies or authorities logos or trademarks in connection with the Data", misrepresenting the Data, claiming ownership of it, or representing yourself as MassDOT or its agent. As-is with "all faults"; MassDOT may alter the terms or revoke the Data at any time without notice; Massachusetts law, venue Suffolk County. Document dated 2009-11-13, at `https://cdn.mbta.com/sites/default/files/2023-08/mbta-massdot-develop-license-agreement.pdf` — reachable from `mbta.com/developers/gtfs`, and the only route to the terms, since `feed_info.txt` declares none. **A local copy is kept at `docs/licenses/mbta-massdot-develop-license-agreement.pdf`**, because MassDOT may alter or revoke the terms without notice (§5.1, §8) and `mass.gov` returns 403 to automated fetches |
| **SEPTA** (Philadelphia) | Permitted: a "non-exclusive, non-assignable, non-transferable, limited and **revocable** right to use, reproduce and redistribute the datasets" | **Not required** — no attribution or notice clause anywhere in the agreement | "Licensee may not use SEPTA's trademarks and copyrighted materials for any commercial or profit-making use and may not alter them in any way." SEPTA "maintains title, ownership, rights and interest in and to the datasets", may revoke or modify the agreement at any time, and "reserves the right to institute a license fee at any time". As-is, no warranty, indemnification required; governed by Pennsylvania law, venue Philadelphia County. At `https://wwww.septa.org/license-agreement/` — the four-w host is **SEPTA's real domain, not the repo-README typo this row previously called it**: `www.septa.org` and `wwww.septa.org` each return 200 independently, with no redirect between them (checked 2026-09-21). Local copy: `docs/licenses/septa-license-agreement.html` |
| **WMATA** (Washington D.C. — **BUILT 2026-09-21**) | Permitted within your own app: "a limited, non-exclusive, non-assignable, non-transferrable, non-sublicensable, revocable license to download, use, reproduce, and redistribute WMATA's Transit Data within your Application". **Third-party redistribution is prohibited** — "sharing (except with your Application's users), transferring, sublicensing, selling or leasing any Transit Data, directly or indirectly...to any other person", unless authorised in writing and "inseparably commingled with or supplemented by additional data that you have provided" | **Not required** — no attribution or notice clause | **No modification clause at all**, which makes it more permissive than LA Metro's on the point that matters most. Access is gated: `api.wmata.com/gtfs/rail-gtfs-static.zip` returns **401** without a registered key from `developer.wmata.com/signup`; keys "remain WMATA's property and may be revoked or otherwise limited at any time", cannot be sold, transferred or sublicensed, and "enable WMATA to associate your API activity with your Application". Trademarks: "prohibited from using WMATA Intellectual Property, including any confusingly similar variants, in association with the Transit Data or API unless you have entered into a separate, written license agreement", and must not "state or imply affiliation, sponsorship or endorsement". **§6 additionally forbids stating or implying that the data your Application provides "is accurate, complete, or timely"** — the identical clause MTA carries, making this the **second** feed to constrain city-page prose that way, so it is a cross-city sweep rather than a D.C. footnote. **§9 termination is the sharpest in the project:** on termination "you must permanently delete all Transit Data or other data which you stored pursuant to your use of the API or GTFS", and "WMATA may request that you certify in writing your compliance with this section" — LA Metro requires removal, but only WMATA asks for written certification. Read 2026-09-21 from `https://developer.wmata.com/license`; local copy at `docs/licenses/wmata-transit-data-terms-of-use.html` |
| **TransLink** (Vancouver *and* Surrey — **BUILT 2026-09-21**) | Permitted: "a limited, revocable and non-exclusive license to **use, reproduce, and redistribute** the Data" | **Required, in specific wording** — notice 11. "Route and arrival data used in this product or service is provided by permission of TransLink…" | **TWO documents mandate TWO different legends, and only one of them governs.** The Open API terms require "Some of the data used in this product or service…" and add an approval gate, an API key, a 1,000-request cap and a ten-day termination clause; the **static GTFS terms have none of those** and mandate the "Route and arrival data" wording instead. Using the API legend for GTFS data would not satisfy these terms. Both texts are stored; `translink-gtfs-static-terms-of-use.txt` is the operative one. No marks beyond the Legend. **"You must provide TransLink sufficient information as TransLink may request to identify you"** — read as an obligation to answer rather than a precondition of use, a stated position in the same family as LA Metro's modification clause (`DECISIONS.md`, 2026-09-21). Commercial users charging end users may have additional terms imposed. The feed itself carries `feed_info.txt` but **declares no licence in it** |
| **STM** (Montréal — **BUILT 2026-09-21**) | Permitted: CC BY 4.0 via the Ville de Montréal portal, which grants reproduction, modification and distribution including commercially | **Required, and credited to STM rather than to the City** — notice 13 | The dataset sits on the City's portal but is **STM's property**, and its own note says so: "selon la clause d'attribution de la licence Creative Commons 4.0, la paternité des données doit être attribuée à la Société de transport de Montréal". Its coverage is stated to extend to "les tracés des lignes de bus et de métro", which is exactly what this project redraws. The portal's **broader-than-CC-BY** condition applies here too: the credit must state whether the data was modified **"ou si des interprétations en ont été tirées"** — and ring density, bucketing and storefront filtering are all interpretations, so a bare credit does not satisfy it. No `feed_info.txt` licence field |
| **Calgary Transit** (**BUILT 2026-09-21**) | Permitted: the Open Government Licence – City of Calgary grants a "worldwide, royalty-free, perpetual, non-exclusive license to use the Information, including for commercial purposes", and you are free to "Copy, modify, publish, translate, adapt, distribute or otherwise use" it | **Required, in specific wording** — notice 14, and **ONE notice covers both the business data and the transit data**, which no other Canadian city manages | Feed and register are published through the same portal under the same licence. **Terminates automatically on breach.** The Socrata `license` field on the business register reads `See Terms of Use` — the `SEE_TERMS_OF_USE` marker `read-licence` step 1 flags — and the OGL is the document it points at. **Neither Calgary copy of the feed carries `feed_info.txt` at all**, so there is no licence field and no validity window; staleness is judged from the Socrata resource's `updatedAt` |
| **Edmonton Transit Service** (**BUILT 2026-09-21**) | Permitted under the City's Open Data Terms of Use | **Required — but NOT as a credit**, which is the trap. Notice 15 | **Recorded as needing nothing, and that was wrong.** The Terms say credit is "not required" but "encouraged", and both the Canada profile and `docs/build_briefs/edmonton.md` concluded from that sentence that Edmonton had no display obligation. The obligation is in a **different clause and is not about credit**: distributing the datasets "in original or modified form" requires including "a copy of, or this Uniform Resource Locator (URL) for, these Terms of Use" and ensuring downstream users are bound "without introducing any further restrictions of any kind". `outputs/edmonton/` is that dataset in modified form, so it engages. **Unlike the four municipal OGLs this does NOT terminate automatically** — the City may cancel access "at any time for any reason, in its sole discretion". The portal's own copy is now behind a sign-in; the PDF in `docs/licenses/` is the readable one |
| **TTC** (Toronto — **BUILT 2026-09-21**) | Permitted: the Open Government Licence – Toronto grants a "worldwide, royalty-free, perpetual, non-exclusive licence to use the Information, including for commercial purposes", free to "Copy, modify, publish, translate, adapt, distribute or otherwise use" | **Required, in specific wording** — notice 16, and **one notice covers both** the MLS business register and the TTC feed | Both are City of Toronto CKAN resources under the same licence. **Both declare "License not specified" at dataset level**, which is exactly the case the standing rule is for — a missing licence field means "go read the terms", not "no restrictions" — so the text was captured from `open.toronto.ca/open-data-licence/` rather than read from a field. **Terminates automatically on breach.** No `feed_info.txt`, so no licence field and no validity window |

**The agreements quoted above are stored locally**, in
[`licenses/`](licenses/) — source URL, retrieval date and SHA-256 for each are
in that directory's `README.md`, **which is the list**; a count kept here said
“six”, then “seven”, while the directory grew past twenty. Every one of them is revocable and amendable
without notice, so the clauses quoted above are checkable against the text that
was actually agreed to rather than against a URL that may have moved on.

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
   that **the right to publish the page has lapsed.** An earlier version of
   this note anchored on (iv) and the derived-work grey area, which was the
   less important half.

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
  they are this project's own computed values rather than Metro's data. See the
  note in `load_line_shapes()` in `pipeline/map_common.py`, and `DECISIONS.md`
  for the full measurement. The same check clears MTA's "you will not modify or
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
construction rather than by interpretation — unlike SEPTA's, which remains
open.

**Three permission questions are OPEN as of 2026-09-21** — two from
Philadelphia and one from Miami. All are recorded unresolved rather than read
generously, per the `multi-source-city` skill's Step 3. None blocks building
its city; all three should be settled before the public deploy, alongside the
required notices. They are the same question in three forms: **what does
silence mean?**

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
  position meanwhile, with the footer disclosing the question. The drafted
  request is at `docs/notifications/philadelphia-permission-request.md`,
  addressed to
  `maps@phila.gov` copying `LIGISTEAM@phila.gov`, and was **SENT 2026-09-21**.
  No reply as of that date; follow-up due a week later. Silence will not be
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
each city's values live in one dict (`LINE_NAMES`, or the `LINE_SPECS` in its
map step) and nothing in the rendering depends on them being the agency's.
Nothing in the project reproduces a logo, wordmark or route-bullet artwork from
any agency, which is the part every one of these clauses most clearly covers.

### Basemap tiles — one active compliance item

The maps render **OpenStreetMap** tiles, fetched directly from
`https://tile.openstreetmap.org/{z}/{x}/{y}.png`.

- **Data licence: ODbL 1.0.** Attribution is required — credit OpenStreetMap
  and link to the licence, visibly, not "beneath UI, behind toggles, or
  off-screen".
- **This requirement is met.** Every rendered map emits
  `© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>
  contributors` in the map corner, and the link is present in the committed
  HTML.
- **The tile service itself is the open question.** The OSMF Tile Usage Policy
  makes availability "best-effort: there is no SLA or guarantee", forbids
  "bulk downloading … any pre-emptive fetching of tiles other than those a
  user is actively viewing", requires HTTPS (this project uses HTTPS) and a
  caching-respectful client. A portfolio site drawing tiles only for what a
  visitor is looking at is ordinary interactive use, not bulk use — but the
  policy is explicit that there is no guarantee behind it. This is the same
  decision already open in `PLAN.md` as "tile provider"; it should be settled
  deliberately before launch rather than by default.

## Commitment: removal requests are honoured, not argued

Every licence reviewed here enforces the same way. Chicago's terms say the
city "may require a user of this data to terminate any and all display,
distribution or other use"; Open NY says the State may require you, "by
providing you with a notice in writing", to cease using or displaying its
content; LA Metro says that on termination you "shall immediately remove the
Transport Information and all references to it". The remedy contemplated
throughout is a request to stop.

**A second trigger, added 2026-09-21: an unresolved licence position is
enough.** Points 1-5 below all fire on a publisher *asking*. This one fires on
finding out. **It now has exactly one live subject, Philadelphia** - the three
questions this was written for were investigated on 2026-09-21 and two closed:
SEPTA expressly grants the right to use, reproduce and redistribute its
datasets and claims only its Logo as a trademark, and Miami-Dade's own Open
Data Hub Terms of Use turns out to exist and to contain nothing but an accuracy
disclaimer. Philadelphia is different in kind: its dataset page incorporates
the City's Terms of Use, which prohibit republication and modification without
written permission. So the commitment stands and is aimed where it belongs:
**if the City of Philadelphia confirms that those terms govern its datasets,
Philadelphia comes off the site without waiting to be asked.** This is disclosed on the site itself rather than kept
here - `app/components.py`'s `render_site_notices()` carries the same wording
in the footer of every page, beside the required attributions, so a reader
learns it at the same moment they learn where the data came from. Keep those
two wordings and `excluded_categories.md` consistent; all three are one
promise.

**A third trigger, added 2026-09-22: a licence that ENDS BY ITS OWN TERMS.**
The first two fire on a publisher asking and on this project finding out.
This one fires on neither — **Licence Mobilités Art. 11.1 terminates *de plein
droit, sans préavis* on breach**, so the grant can simply stop, with no notice
to receive and nothing to discover. It is the first revocable grant in this
project: CC BY, Licence Ouverte, the PSI licences and ODbL are all perpetual,
and none of them can lapse without someone saying so.

**Owner's decision 2026-09-22: this is ACCEPTED, and Paris is built on it.**
The response is the same as for the other two triggers and is decided in
advance rather than under pressure — **if the grant lapses, Paris is archived:
its page comes off the site and its entry out of `app/cities.py`, while its
pipeline, brief and `DECISIONS.md` record stay in the repository.** That is
the distinction worth keeping: a city coming *down* is not the same as a city
being *deleted*, and the build remains reproducible if the position changes
back. The rejected alternative was declining to build Paris at all, which
would have cost the only national register in the screen that buys six cities,
to avoid a risk that is answerable by taking one page down.

**This project commits, in advance, to honouring such a request.** Stated so
that it is a standing position rather than a decision made under pressure:

1. **If a data publisher asks this project to stop displaying its data, it
   will stop.** The affected layer, or the whole city, comes down. No case
   will be argued first, no justification will be requested, and compliance
   will not be made conditional on the publisher explaining itself.
2. **If a business owner asks for their listing to be removed, it will be
   removed** — see `excluded_categories.md`, which says the same thing to the
   people it concerns. They do not have to give a reason.
3. **If anyone raises a privacy concern about a specific pin**, it is treated
   as a removal request under point 2 and actioned first; any disagreement
   about whether the concern was well-founded is separate from taking the pin
   down.
4. **A request is honoured even if this project believes it is in the right.**
   The licence review found nothing forbidding what is built here, and that
   conclusion does not change the answer to a request. Being permitted to
   display something is not a reason to insist on displaying it.
5. **Removal is the immediate action; the reasoning gets recorded afterwards**
   in `DECISIONS.md`, with what was removed and who asked, so the trail stays
   honest.

This is not a legal position and it does not waive or create anything. It is
a statement of how this project behaves, published because a reader who might
want something removed should be able to see it without asking first.

#### CRTM (Consorcio Regional de Transportes de Madrid) — read 2026-09-22 (**BUILT 2026-09-22**)

**Source:** `http://www.crtm.es/licencia-de-uso`, the *Licencia de datos
estáticos del CRTM*, which `mdb-794` (Metro de Madrid GTFS) declares. Read in
the browser because it is the licence Madrid's rail leg depends on, and no
transit licence is ever assumed from the city's business licence — LA Metro's
GTFS forbids modifying data while the same city's registry is CC0.

**Verdict: PERMITTED WITH CONDITIONS.** The granting sentence:

> *"Las presentes condiciones generales definidas en esta licencia permiten la
> reutilización de los documentos sometidos a ellas para fines comerciales y no
> comerciales"*

and reuse is defined to include *"la copia, difusión, modificación,
adaptación, extracción, reordenación y combinación de la información"* — so
redrawing line geometry onto a map is squarely inside it. Rights are ceded
*"gratuita y no exclusiva"*, worldwide.

**On share-alike — it applies to the DATA, not to this project's map.** The
scope section requires sharing CRTM data *"bajo el mismo tipo de licencia"*,
but says in the next breath that **"las obras derivadas añadiendo valor pueden
ofrecerse bajo licencias diferentes"** — value-added derivative works may be
offered under different licences. A ring-density map is a derivative work
adding value, not a redistribution of the feed. Recorded explicitly because
ODbL-style share-alike is a live question elsewhere in this project (CDMX).

**The condition that decides Madrid's rail route:**

> *"Garantizar que la información mostrada en su sistema esté siempre
> **actualizada**"*

**Displaying an expired feed is in direct tension with this.** `mdb-794`'s
calendar ended 2026-05-27. The build brief had listed "use the expired feed
anyway, since station positions do not expire" as a defensible third option.
**It is no longer defensible on these terms** — not because station geometry
goes stale, but because the licence obliges the reuser to keep what is shown
up to date, and this project cannot honour that with a feed CRTM has stopped
refreshing. Madrid's rail leg must come from a current CRTM item or from
OpenStreetMap.

**Obligations, all of them conditions rather than courtesies:**

| | |
|---|---|
| 1 | **Prescribed wording — "Powered by CRTM"**, with a link to `http://www.crtm.es/`. The licence says it *"debe quedar claramente"* on digital platforms: *"webs, foros, blogs, apps"*. **This is a sixth prescribed notice for this project, and the first from a Spanish source** |
| 2 | **Cite CRTM as the data source, stating whether the data is raw or processed** — *"especificando si son datos en bruto o explotados"*. This is the disclosure-of-transformation family, like Montréal's and INEGI's: a bare credit does not satisfy it, the notice has to say the data was processed |
| 3 | **Keep the information shown up to date** (above) |
| 4 | **Do not distort the meaning**, manipulate in bad faith, or falsify |
| 5 | **Preserve the metadata** on update date and reuse conditions; do not alter or delete it |
| 6 | **No implied endorsement** — must not *"indicar, insinuar o sugerir que el CRTM … participa, patrocina o apoya"* the product |
| 7 | Must not be used to damage CRTM's public image or the public transport system, nor placed alongside illegal acts |
| 8 | CRTM **monitors access** and may block a reuser whose fetching degrades its systems. A pipeline that re-downloads politely is fine; a tight retry loop is not |

**What this project must therefore display for Madrid:** *"Powered by CRTM"*
linked to crtm.es, plus a statement that the data is processed rather than
raw. Both are in addition to the Ayuntamiento de Madrid wording already
recorded above for the business leg — **Madrid owes two separate attributions
from two separate licences.**

#### Barcelona — Open Data BCN, read 2026-09-22 **from the Internet Archive** (**BUILT 2026-09-22**)

**How it was read, and the limit on that.** `opendata-ajuntament.barcelona.cat`
serves **hCaptcha** on `/en/avis-legal`, `/ca/avis-legal` and
`/es/aviso-legal` alike, and this project does not defeat CAPTCHAs. The legal
notice and the terms it points to were therefore read from the **Internet
Archive**: the notice at snapshot **2025-01-18**, the terms of use
(`/en/condicions-us`) at **2025-03-28** — the newest capture of that page that
exists. That is a public archive of a public page, not a bypass.

⚠️ **An archived copy is not the live document**, and these terms explicitly
reserve the right to change: *"Barcelona City Council may at all times add to,
remove or amend the data sets published as well as these Terms of use … any
change that is made shall take effect as soon as it is published."*

### ✅ DECIDED 2026-09-22 — Barcelona is published on a DISCLOSED POSITION

This section previously said a human should confirm the live page before
publishing. That was attempted on 2026-09-22 and **the page returned
hCaptcha** — *"PLEASE PROVE THAT YOU ARE HUMAN"* — which this project does not
defeat. The owner's decision was to publish anyway, on a disclosed position,
rather than hold the city. Recorded here because **a precondition that is
knowingly not met has to say so**, rather than sit in the file reading like a
plan somebody will get to.

**What IS verified, live, today.** The *declared licence* needs no CAPTCHA:
`package_show` on the CKAN API returns `license_id: CC-BY-4.0`, `license_title:
Creative Commons Attribution 4.0`, with the package last modified 2025-12-02.
So the grant this project relies on is confirmed current from the publisher's
own machine-readable metadata. It is only the *terms page* that is unconfirmed.

**What the gap actually risks, stated plainly.** The stored terms impose four
obligations; this project meets three on the page and records the fourth as an
owner action. If the live terms have since become **more permissive**, nothing
is wrong. If they have become **more restrictive**, this project would be
complying with a superseded version — and that is the real exposure, sized by
the fact that no capture since March 2025 shows any change at all.

**Why that is tolerable here and was NOT in Philadelphia.** Philadelphia's
operative sentence is a flat prohibition on redistribution, read from the live
page; the question there is what a clause MEANS. Here the clause is not in
doubt and neither is the grant — the question is only whether a page has
changed since its last capture, and the licence field says it has not. Same
shape of answer as Philadelphia (publish on a disclosed reasoned position), a
weaker premise required to reach it.

**What happens if that turns out to be wrong.** The standing commitment applies
unchanged and is the reason this is safe to decide rather than agonise over: a
removal request from Barcelona City Council is honoured, not argued — the layer
or the whole city comes down first and the reasoning is recorded afterwards.
**Re-read the live terms whenever the CAPTCHA can be passed**, and record the
result here either way.

**Verdict: PERMITTED WITH CONDITIONS.** The granting text:

> *"… the conditions of Creative Commons-Attribution (CC-BY 4.0) licence,
> under which such data are allowed: to be copied, distributed and published
> … to provide the basis for derived works as a result of their analysis or
> study … to be used for commercial or non-commercial purposes, provided that
> such use does not constitute a public-authority activity … to be amended,
> changed and adapted."*

"Derived works as a result of their analysis or study" describes this project
directly.

⚠️ **A carve-out that must be checked per dataset: CC BY-ND.**

> *"However, any data involving third-party participation may be reused under
> a Creative Commons Attribution-**NoDerivs** (CC BY-ND 4.0) licence"*

The census declares `CC-BY-4.0` in the CKAN API, so it is not in the ND class
on its own metadata — but the carve-out exists and any *second* Barcelona
source has to be checked for it separately. (The clause is also internally
odd: it lists *"to be amended, changed and adapted"* among the permissions
**under a NoDerivs licence**, which NoDerivs by definition forbids. Treat the
named licence as controlling, not the bullet list.)

**Obligations — four of them, and two are unusual:**

| | |
|---|---|
| 1 | **Prescribed attribution wording**: *"Source of the data: Barcelona City Council"*, with suggested HTML markup linking `barcelona.cat/opendata` |
| 2 | **Modifications must be identified at distribution** — *"Any amendment or change made to the data sets … shall be identified as such at the time of their distribution."* The disclosure-of-transformation family again: ring density and storefront filtering are changes, so a bare credit does not satisfy this |
| 3 | ⚠️ **Users must NOTIFY the Council of the project** — *"Users are required to inform Barcelona City Council of every project relating to or derived from their use of the data sets."* **This is a new obligation class for this project**: an affirmative action owed to the publisher, not a line of text on a page. Nothing in the built cities has required it |
| 4 | Council **may require reuse statistics** from the user |

**Plus the Spanish Act 37/2007 Article 8 general conditions**, which the terms
incorporate expressly:

- the content of the information **may not be altered**
- the meaning **may not be distorted**
- **the source must be cited**
- ⚠️ **"the most up-to-date data are referred to"**

**That last one bears directly on the census-year decision.** The build brief
recommends the **2022** resource because the 2024 one is geographically
incomplete (down 69–83% in four districts). Article 8 pulls the other way.
The two are reconcilable — using the most recent *complete* survey, and saying
so on the page — but it must be a stated decision, not a silent one, and the
page must name the census year either way.

**Not claimed:** the *"Open Data BCN"* denomination and logo are registered
trademarks (M 3713011, M 3746181) and are excluded from reuse, as are images
and icons. Line names and category labels are not claimed.

**No warranty**: the Council disclaims integrity, updating and accuracy, and
excludes liability.

## Obligations that are NOT notices — four classes, one per publisher

**A notice is text on a page. These are not.** Each was found by reading a
licence that also granted permission freely, which is why they are easy to
miss: the grant is the headline and the obligation is a subordinate clause.

| Class | Who | What it actually requires |
|---|---|---|
| **An act owed to the publisher** | **Barcelona** 🇪🇸 | *"Users are required to inform Barcelona City Council of every project relating to or derived from their use of the data sets."* A message a person sends. Drafted at `docs/notifications/barcelona-city-council.md`, **not yet sent** |
| **A live account that must STAY live** | **WMATA** (Washington D.C.) 🇺🇸 | The terms are an API agreement, so §9(i) ends the grant when the account ends — and what lapses is the right to **publish the page**. Gate item 10 |
| ✅ **A liability ACCEPTED** | **Hong Kong** 🇭🇰 *(candidate)* | **ACCEPTED BY THE OWNER 2026-09-22.** *"you shall **indemnify** the Government and the Relevant Organisations against any allegations or claims of infringement of the rights of any person and all costs, losses, damages and liabilities incurred … which in any case arise **directly or indirectly** in relation to your use, reproduction and/or distribution of the Data"*. See the section below for what the earlier record omitted |
| 🔧 **AN ACCESS A PERSON MUST OBTAIN** | **Copenhagen / Denmark** 🇩🇰 *(candidate)* | **Added 2026-09-23 at the owner's request.** CVR's premises data needs a **Datafordeler account the owner creates by hand**, and the terms pages sit behind a **Cloudflare interactive challenge** this project does not defeat — so both the registration and the reading are **human-only work**. ⚠️ **This is NOT WMATA's class, and the difference matters.** WMATA's terms are an **API agreement**, so §9(i) ends the grant when the account ends. Copenhagen's licence is **CC BY 4.0, which attaches to the DATA and is irrevocable** — so the owner's standing practice (*register, take the data, terminate, revoke*) is **safe here and unsafe there**. ✅ **Close the account freely; the right to publish survives.** The similarity is the registration effort, not the obligation |

**Copenhagen and WMATA look alike at the signup form and diverge immediately after it.** Both made the owner register; only one made the account load-bearing. **The test is what the terms ARE** — an API agreement licenses *you*, so it can be withdrawn from you, while a public licence licenses *the data*, and nothing you do to your account reaches it. Recording the two in one row would have told a later reader to keep a Danish account alive forever, and implied that closing it revokes the right to publish Copenhagen. **Neither is true.**

**Hong Kong's is the one to weigh before building, not after.** Everything
else in `data.gov.hk`'s Terms of Use v1.2 (26 May 2025) is generous — download,
distribution and reproduction are permitted for **commercial and
non-commercial purposes, free of charge**, subject only to identifying the
source, acknowledging Government ownership of the IP, and proper attribution.

**The indemnity is not a notice, not a credit, and not a step in a build.** It
is an open-ended undertaking to cover the Government's costs if a third party
alleges the data infringed their rights. No other source in this project asks
for one. **It is an owner decision, and the right moment to take it is before
35,808 premises are wired into a page**, not once the city is live.

### Hong Kong's indemnity — ACCEPTED 2026-09-22, and what the first record omitted

**The owner accepted this on 2026-09-22, in chat, after the live clause was
re-read.** It is the only uncapped liability in this project. Recorded here
with its reasoning so it is a decision rather than a drift.

**Two things the first record's quote left out**, both found by reading
`https://data.gov.hk/en/terms-and-conditions` (Terms v1.2) rather than the
earlier citation of it — which is the failure mode `read-licence` exists for:

1. **"arise directly or indirectly"** — the earlier quote elided it. Broad
   causation, not just proximate.
2. **There is NO notice-and-defend clause.** The Government need not tell you a
   claim exists, you have no right to control or even join the defence, and
   nothing obliges them to mitigate or to seek your consent before settling.
   Most commercial indemnities temper exposure exactly there. This one does
   not.

**And the pairing is deliberate.** The *Disclaimer and Limitation of Liability*
section expressly disclaims any warranty of **non-infringement** — so the
Government does not promise the Data is clean **and** you indemnify them if it
is not. That section caps **their** liability to you, not yours to them: the
indemnity is one-directional and has no cap.

**What narrows it**, and why acceptance is reasonable rather than reckless: the
scope is **infringement of the rights of any person**, not general liability.
It is not "anything that goes wrong because of the map". A third party must
assert *their rights* against the Government, over this project's use of a
**government public register** republished with the attribution the same
paragraph requires. That is a narrow path, and the project's standing
commitment to **honour removal requests without argument** cuts off the likeliest
escalation before it becomes a claim.

**Probability low, magnitude unbounded** — which is the combination that gets
mis-priced, so it was priced deliberately.

#### THREE CONDITIONS, accepted with it and binding on the build

1. **Display all three required elements exactly** — identify the **source**
   of the Data, **acknowledge the Government's and the Relevant Organisations'
   ownership of the intellectual property** in it, and give **proper
   attribution to the Government, the Relevant Organisations and
   DATA.GOV.HK**. These are the same paragraph as the indemnity, and
   **unattributed use is the most likely way to draw a complaint in the first
   place.** They become numbered notices when Hong Kong is committed, not
   before.
2. **Run `python scripts/check_personal_exposure.py hong-kong` and exclude
   catch-all categories** — the Los Angeles NAICS 812990 precedent. The
   realistic complainant is an individual whose name sits at what looks like a
   home, so the privacy filter is the risk control, not a formality.
3. **This entry is condition three**, dated and reasoned.

#### One consistency note

**Lyon's Grand Lyon CGU 9.4 is the same shape** and was recorded as the
project's second indemnity. Accepting Hong Kong's does **not** automatically
accept Lyon's — Lyon carries two further gates (an account this project does
not create, and a trademark clause that collides with an invariant), so it
stays deferred on those grounds regardless.

## Notices this project MUST display when published

This is the operative output of the licence review. As of 2026-09-21, for the
**nine** cities built: **five sources require specific text or
acknowledgement, and one of the five is already satisfied** (OpenStreetMap);
Chicago, SFMTA, LA Metro and — since Boston was built — MassDOT were
outstanding until **2026-09-21, when all five were put on every page**
by `app/components.py`'s `render_site_notices()` — Chicago's and
SFMTA's verbatim, LA Metro's and MassDOT's in this project's own words
because neither prescribes any. They render inline rather than inside a
collapsible: Streamlit keeps a collapsed expander's contents out of the
DOM, and a notice behind a toggle is not displayed. New York adds a conditional identification requirement that is
largely already met, and CTA encourages but does not require credit.
**Building Washington D.C. added no sixth notice**, correcting what an
earlier note in this file predicted: WMATA requires no attribution and no
acknowledgement of any kind. What it did add is a second copy of MTA's
accuracy clause (§6), which is prose work on the city pages rather than a
notice to display — see item 5a below. These are obligations, not courtesies. They belong with the app work that surfaces this
page and `excluded_categories.md` (see `PLAN.md`) — publishing the maps
without them would breach terms this project has now read.

**1. OpenStreetMap — required, and ALREADY SATISFIED.** ODbL 1.0 requires
visible credit and a licence link, "not beneath UI, behind toggles, or
off-screen". Every rendered map emits, in the map corner:

> `© OpenStreetMap contributors` — linked to
> `https://www.openstreetmap.org/copyright`

This comes from Folium's default tile attribution and is present in every
committed `heatmap.html`. **Do not remove or restyle it away.** If the tile
provider ever changes, its own attribution replaces this one — it does not
simply disappear.

**2. City of Chicago — required, and DISPLAYED.** Chicago's Data Terms of
Use require any "secondary or derivative application" to carry this disclaimer,
verbatim, "at the site where the software application … can be accessed":

> "This site provides applications using data that has been modified for use
> from its original source, www.cityofchicago.org, the official website of the
> City of Chicago. The City of Chicago makes no claims as to the content,
> accuracy, timeliness, or completeness of any of the data provided at this
> site. The data provided at this site is subject to change at any time. It is
> understood that the data provided at this site is being used at one's own
> risk."

**3. SFMTA — required, and DISPLAYED.** Its transit-data licence requires
derivative works to include:

> "Reproduced with permission granted by the City and County of San Francisco.
> The information has been provided by means of a nonexclusive, limited, and
> revocable license granted by the City and County of San Francisco."

**4. LA Metro — required, and DISPLAYED.** Must acknowledge Metro as the
provider of the transit information and must not claim ownership of it. No
exact wording is prescribed; "Rail alignment data provided by LA Metro" would
meet the stated requirement.

**These three were marked NOT YET DISPLAYED until 2026-09-22, and all three
were displayed.** `app/components.py`'s `_NOTICES` carries Chicago, SFMTA and
LA Metro as its first three entries, and `render_site_notices()` is called from
every page. The labels were written before the footer existed and nothing
brought them forward when it shipped — so the list that GATES THE PUBLIC
DEPLOY understated this project's own compliance, in the direction that makes a
deploy look blocked when it is not. Found by `scripts/check_stale_claims.py` on
its first real run, which is the argument for the tool in one line.

**5. New York City — conditional, and largely already met.** Local Law 11
forbids licence requirements, but the Technical Standards Manual reserves one
condition: "DoITT may require third party entities such as application
developers to explicitly identify the **source, version, and modifications**
made to a public data set" where it is "publicly re-publish[ed] … elsewhere or
incorporate[d] … into an application."

This project already produces all three, which is a good argument for
surfacing both documents rather than only one:

- **source** — this file, with endpoint and download filter per dataset;
- **version** — the retrieval date per source, and `AS_OF_DATE` for the
  snapshot-based feeds;
- **modifications** — `excluded_categories.md`, which is precisely a
  statement of what was removed and why.

**6. CTA — encouraged, not required.** If credited, use one of CTA's own
forms: "Data provided by Chicago Transit Authority", "Data provided by CTA",
or "Powered by CTA data".

**7. MassDOT / MBTA — required, and DISPLAYED.** §4.1 of the MassDOT Developers
License Agreement requires the licensee to "Clearly acknowledge MassDOT as the
provider of the Data". No exact wording is prescribed. Same shape as LA Metro's
obligation. The agreement itself is kept at
`docs/licenses/mbta-massdot-develop-license-agreement.pdf`.

**8. INEGI (Mexico City) — required, and DISPLAYED since 2026-09-22. It is TWO
obligations rather than one.** The Términos de Libre Uso de la Información del
INEGI (`docs/licenses/inegi-terminos-libre-uso-informacion.pdf`, retrieved
2026-09-22) grant more than most sources here — §1(b)-(e) permit publishing,
adapting, extracting and even **commercial** exploitation — in exchange for:

- **§1(f), attribution in a prescribed form:** credit INEGI as author and,
  where technically possible, name the source as *"Fuente: INEGI, nombre del
  producto de donde se extrae la información"* plus the update date. For this
  project that is **"Fuente: INEGI, Directorio Estadístico Nacional de Unidades
  Económicas (DENUE)"** with DENUE's own edition date.
- **§1(g), DISCLOSURE OF TRANSFORMATION, which a source credit does not
  satisfy.** The user must be notified of *"cualquier análisis o transformación
  que haga a la información"*, and the presentation must not suggest INEGI
  performed it. **This project triggers that clause on every map**: ring
  assignment, bucketing into three categories, the storefront filter and the
  `Fijo`-only filter are all transformations. Treat attribution and disclosure
  as two separate duties — the Montréal licence has the same split, and it is
  easy to satisfy the first and miss the second.
- **§1(h), non-endorsement:** the use must not appear to represent an official
  INEGI position, nor to be endorsed, integrated, sponsored or supported by the
  source. The site-wide non-affiliation notice already covers the shape of
  this; INEGI is named explicitly for safety.
- **§1(a)** additionally forbids altering or suppressing the metadata of
  distributed copies. This project distributes no copy of DENUE — only derived
  points — so it does not bite, and is recorded so nobody has to re-derive it.

Note the two-document split: `inegi-terminos-sitio.pdf` governs **inegi.org.mx
as a website** and is NOT the data licence. Both are stored, because reading a
site-terms document as though it governed the data is what made New York look
prohibited.

**Guadalajara (Regional) needed NO new notice, which is a first.** Its
business data is the same register under the same licence, and notice 8 names
INEGI and DENUE rather than a city - so a second Mexican city is covered by the
text already displayed. Its rail credit is OpenStreetMap's, likewise already
displayed. Recorded because every previous city added at least one line to
`render_site_notices()`, and the reason this one does not is that the notice
was written around the SOURCE instead of the city.

**Guadalajara's endpoints, verified 2026-09-22:**

- **Businesses** — INEGI DENUE, entidad federativa **14 (Jalisco)**, keyless
  bulk CSV: `https://www.inegi.org.mx/contenidos/masiva/denue/denue_14_csv.zip`
  (39,432,220 bytes, real ZIP by magic bytes; member
  `conjunto_de_datos/denue_inegi_14_.csv`; **latin-1**). Scoped in step 2 to
  four municipios by DENUE's own `municipio` spelling — note **"San Pedro
  Tlaquepaque"**, not the "Tlaquepaque" SITEUR's prose uses; matching the
  operator's wording would keep zero rows.
- **Rail** — OpenStreetMap via Overpass, route relations tagged
  `network="Mi Tren"`, `route` in (`light_rail`, `subway`). ODbL 1.0.
- **Boundaries** — OpenStreetMap `admin_level=6` municipio relations, bounded
  by bbox. ODbL 1.0.

**A REJECTED SOURCE, recorded with its date because a replaced URL that leaves
no trace hides why:** the only Guadalajara rail feed in the Mobility Database
(mdb **1925**, also contained in **2366**) downloads cleanly and is **not
used**. Its own `feed_info.txt` declares `feed_end_date = **20230128**`, its
`feed_publisher_name` is **Nubenautas** (`gtfs.studio`) rather than SITEUR, and
it carries **three** light-rail routes where SITEUR publishes **four** —
**Línea 4 opened 2025-12-15**, almost three years after the feed stopped.
Using it would have omitted an operating line, 8 stations and 21 km.
`https://www.siteur.gob.mx/` itself answers HTTP 200 and is the source for this
project's gate-3 station counts (Línea 2: 10; Línea 4: 8), but publishes no
GTFS.

**Mexico City's rail geometry is OpenStreetMap, so notice 1 now covers DATA and
not only basemap tiles.** Every `*.cdmx.gob.mx` host is unreachable, so the
lines are drawn from OSM route relations (owner-approved 2026-09-22 as a
per-city exception). ODbL 1.0 attribution was already satisfied for the
basemap; the same credit now also covers line geometry, and notice 1's wording
should not imply it is only about tiles.

**This heading read "NOT YET DISPLAYED" until 2026-09-21 and was stale**, which
is worth leaving a note about because a compliance document that understates
compliance invites someone to re-fix a closed item and to doubt the rest of the
gate. The outstanding part had been that the acknowledgement appeared only on
Boston's own city page rather than "where the *site* is accessed"; that was
closed when `app/components.py`'s `render_site_notices()` began carrying all
five outstanding notices on **every** page, and this heading was not updated
with the others. Verified against `_NOTICES` on 2026-09-21.

Not required by anyone, but good practice and already partly done in the city
pages' prose: naming each business registry's publishing agency.

### What closing this fully requires

1. ~~Read Chicago's data terms of use~~ — **done 2026-09-21**, and it produced
   a mandatory notice (above).
2. ~~Read the Open NY Terms of Use document~~ — **done**, explicitly permissive.
3. ~~Establish the reuse position for NYC Open Data~~ — **done**. Local Law 11
   of 2012 forbids licence requirements and usage restrictions on NYC open
   data, so the missing licence field is compliance, not an omission. One
   condition attaches (identify source, version and modifications), which this
   project already satisfies in substance.
4. ~~Check the five GTFS feeds' terms~~ — **done**, and three of the five carry
   conditions worth acting on.
5. ~~Decide LA Metro's "modification" clause and CTA's purpose limitation~~ —
   **decided 2026-09-21**, see the notes under the GTFS table.
5b. **Decide the three "what does silence mean?" questions** — raised
   2026-09-21, all still open. SEPTA's trademark clause; the City of
   Philadelphia License's rights reservation; and **Miami-Dade's total absence
   of a reuse position** across its business registry, its boundary layer and
   its GTFS (which has no `feed_info.txt`). See the notes under the GTFS table.
   Miami's is the weakest paperwork in the project and should be decided
   first — it is also the only one of the three where no agency document exists
   to read, so settling it may mean asking the County rather than reading
   anything.
5c. **Decide the agency-branding question — official route colours AND the
   line names beside them.** Affects the cities whose agency prescribes a
   palette: San
   Diego (MTS), Los Angeles (LA Metro), Chicago (CTA), New York (MTA),
   Philadelphia (SEPTA) and — since 2026-09-21 — Washington D.C. (WMATA),
   whose wording is the one that names "confusingly similar variants". San Francisco and Miami
   are out of scope, already drawing their own palettes. **MTS's wording is the
   tightest in the project** — its trademarks "may not be used in association
   with GTFS Data", a flat prohibition rather than an application process — so
   start there rather than with MTA's, which merely needs a free application.
   The owner chose on 2026-09-21 to keep the official colours and record this
   rather than pre-emptively substituting palettes. Colours are cheap to
   reverse (one dict per city); **line names are not**, because a standing
   invariant requires every drawn line to carry its real public name. See the
   table under the GTFS notes.
6. **Display the required notices** (above) — the one thing that still blocks
   publishing, and part of the same app job as surfacing this page.
7. **Decide the tile provider deliberately**, given that OSM's tile service is
   explicitly best-effort with no SLA.
8. Optionally, read the Census geocoder's terms, which are still unread - as
   San Diego's municipal-boundary layer's are (see its row). The licence table
   is the list of what is unread; this line used to call the geocoder "the
   only source left unread" while that row said otherwise.
9. **REBOOT THE APP AFTER ANY PUSH THAT CHANGES A MODULE THE APP IMPORTS** —
   `app/cities.py`, `app/components.py`, or anything under `pipeline/` that
   `app/` pulls in. This is an operational step, not a courtesy, and it is in
   this gate because the live site spent **over three hours down** on
   2026-09-22 for want of it.

   **Streamlit Cloud's "🔄 Updated app!" re-runs the ENTRY SCRIPT only.** It
   pulls the new files and re-executes `app/Overview.py`, but every module
   already in `sys.modules` — `cities`, `components`, every `pipeline` config —
   stays as it was when the process started. So a push that adds a name to
   `cities.py` and imports it from `Overview.py` leaves the running process
   with the new script and the old module, and every page load raises
   `ImportError: cannot import name 'DEFAULT_REGION' from 'cities'`.

   The log that proves it, because the symptom is confusing enough to send
   anyone hunting a phantom: the traceback printed the **old** one-line
   `from cities import CITIES, IN_DEFAULT_VIEW, MAP_ONLY_NAV` — which does not
   mention `DEFAULT_REGION` at all — above an error naming `DEFAULT_REGION`.
   Python renders traceback source by re-reading the file from disk while
   executing a cached code object, so disk and runtime were different
   versions. Five pulls and five "Updated app!" across three hours never
   cleared it; only **Manage app → ⋮ → Reboot app** does.

   **Two routes reach that reboot, and only one works reliably on a phone.**
   In the app, **Manage app** sits in the lower-right corner - but only in a
   browser signed in to Streamlit as the app's owner. Signed out, the same
   corner shows Community Cloud's red "Hosted with Streamlit" badge and a
   round creator avatar instead, so there is no button to find, and on a
   phone that corner is exactly where one gets looked for. The dashboard
   route never touches the app page: **share.streamlit.io → sign in → the ⋮
   beside `expanded-heatmap` → Reboot**. Use it on mobile. Neither the badge
   nor the avatar is this project's - both are the host's chrome around the
   app, which app code cannot move. Recorded 2026-09-23, after the owner hit
   it on a phone for the second time.

   **`app/cities.py` changes every time a city is added**, so every future city
   carries this exact risk. Treat the reboot as the last step of adding a city,
   alongside the drift check and the `DECISIONS.md` entry.

   Before the push, run **`python scripts/check_deploy_imports.py`**, which
   tests a clean clone under `.venv-lean` — the closest local approximation of
   what the deploy pulls. It catches the mismatched-export case and the
   missing-`label_offset` case that crashed the Overview the same day. It
   cannot catch the stale-module case: nothing local can, because a fresh
   process is the one thing the live app does not do.

10. **CONFIRM THE WMATA ACCOUNT IS STILL LIVE** — before every public deploy,
    for as long as the D.C. page is published. This is a gate item rather
    than a note because **nothing in the codebase can check it**: verifying an
    account means holding its key, and this project never handles one. It is
    a human step by construction, which is exactly the kind that gets skipped.
    WMATA's terms are an **API agreement**, so §9(i) terminates the grant the
    moment the account goes — and the right that lapses is the right to
    *publish the page*, not merely to store a file. **Re-confirmed live by the
    owner on 2026-09-22.** If it ever lapses, D.C. comes down until a new
    account is registered. The full reasoning is under the WMATA entry above;
    the standing list of items like this is `docs/gated_access.md`.

**Where this leaves the project:** nothing found anywhere forbids what this
project does, and the count of **mandatory notices to display is five**.
Neither Philadelphia nor Miami added one, because SEPTA, the City of
Philadelphia License and Miami-Dade all require no attribution at all. The
fifth is **MassDOT's acknowledgement, active since Boston was built on
2026-09-21**. This paragraph also predicted a sixth from WMATA once D.C. was
built: **that was wrong, and D.C. is now built.** WMATA's terms require no
attribution and no acknowledgement — its constraints are on what may be SAID
(§6 accuracy, §9 deletion on termination, the trademark clause), not on what
must be shown.

**9. City of Vancouver — required, and DISPLAYED.** The Open Government
Licence – Vancouver requires this exact sentence wherever its information is
used:

> `Contains information licensed under the Open Government Licence – Vancouver.`

Note the British spelling "Licence" and the EN DASH. This licence
**terminates automatically on breach** — "if you fail to comply with any of
them, the rights granted to you under this licence… will end automatically" —
so the notice is not cosmetic. In `app/components.py`'s `_NOTICES` since
2026-09-21, when Vancouver was built.

**10. City of Surrey — required, and DISPLAYED.** The same OGL template, with
Surrey's own wording, which is **not interchangeable with Vancouver's**:

> `Contains information licensed under the Open Government License - City of Surrey.`

Note the American spelling "License" and the HYPHEN. Surrey's OGL also
terminates automatically on breach. Required because the Vancouver map is
regional and includes Surrey's own business licences.

**11. TransLink — required, and DISPLAYED. Its wording is a TRAP.** The GTFS
Static Terms of Use require the Legend to be "prominently displayed" in
exactly this text:

> "Route and arrival data used in this product or service is provided by
> permission of TransLink. TransLink assumes no responsibility for the accuracy
> or currency of the Data used in this product or service."

**TransLink mandates TWO different legends and this is the GTFS STATIC one.**
Its Open API terms mandate a different text beginning "Some of the data used in
this product or service…", which would **not** satisfy the GTFS terms. This
project uses static GTFS, so the "Route and arrival data" wording is the
correct one. Both texts are stored in `docs/licenses/`;
`translink-gtfs-static-terms-of-use.txt` is the operative file and
`translink-open-api-terms-of-use.txt` is kept only because it looks like it
governs and does not.

One Legend covers both cities: Surrey has no rail of its own, so the regional
build inherits TransLink's terms once rather than twice. Two further
obligations come with it and are not notices: **no TransLink marks beyond the
Legend** (satisfied by construction — this project draws its own geometry from
`shapes.txt` and reproduces no roundel), and **responsiveness if TransLink asks
who is using the data**, which was read as an obligation to answer rather than
a precondition of use (`DECISIONS.md`, 2026-09-21).

**12. Ville de Montréal — required, and DISPLAYED. Its condition is BROADER
than standard CC-BY, and this project triggers the broad part every time.**
`locaux-commerciaux` is CC-BY 4.0 (`license_id: cc-by`, confirmed from CKAN
`package_show`). The City's own licence page,
`donnees.montreal.ca/pages/licence-d-utilisation`, adds three conditions, read
2026-09-21:

> "Vous devez créditer les données et les contenus que vous utilisez et
> **préciser si des modifications ont été effectuées ou si des interprétations
> en ont été tirées**."

— credit the data **and state whether modifications were made or
interpretations drawn**. Ring density, category bucketing and storefront
filtering are all interpretations, so **a bare source credit does not
comply**; the displayed notice says the data is modified and interpreted, and
what was done. The other two conditions: no indicating or suggesting that the
City "vous soutient ou endosse votre usage" (explicitly extending to
integrating its data into a database you own), and no restricting access to the
originals "sous la forme de conditions légales ou de mesures techniques".

**13. Société de transport de Montréal — required, and DISPLAYED.** The Métro
geometry is a SEPARATE owner from the business data, though both sit on the
City's portal. The STM dataset's own note:

> "Le présent ensemble de données est la propriété de la Société de transport
> de Montréal. Conséquemment, selon la clause d'attribution de la licence
> Creative Commons 4.0, la paternité des données doit être attribuée à la
> Société de transport de Montréal."

So credit **STM**, not the City, for the lines and stations. Its note confirms
the coverage extends to "les tracés des lignes de bus et de métro", which is
exactly what this project redraws.

**A trap avoided, and it is the New York footer for the third time.** The
City's licence page points at `montreal.ca/articles/mentions-legales-2654`,
which states "L'ensemble des contenus de montreal.ca est la propriété exclusive
de la Ville de Montréal, **tous droits réservés**" and forbids reproducing "les
images du site" commercially. Read alone, that makes Montréal look prohibited.
It is not: applying `read-licence` step 4, that document is written entirely in
**web-page** language (page, site, navigation, hyperlien) and contains **no
data language at all** — no "données ouvertes", "jeu de données",
"redistribuer", "base de données" or "réutiliser" — and its operative sentences
name montreal.ca's own contents and photos. The open data is governed by the
separate licence page above. Same shape as nyc.gov's "All Rights Reserved"
footer and Philadelphia's terms-of-use, and the reason step 4 exists.

**14. City of Calgary — required, and DISPLAYED. One notice covers BOTH the
business data and the transit data**, which no other Canadian city manages:

> `Contains information licensed under the Open Government Licence – City of Calgary.`

En dash, British "Licence" — Surrey's sibling notice uses a hyphen and
"License" and the two are not interchangeable. Like Toronto's, Vancouver's and
Surrey's, this licence **terminates automatically on breach**. The Socrata
`license` field on the business register reads `See Terms of Use`, which is the
`SEE_TERMS_OF_USE` marker `read-licence` step 1 flags: the OGL is the document
it points at, and it is stored in `docs/licenses/calgary-open-government-licence.txt`.

**15. City of Edmonton — required, and DISPLAYED. It was recorded as needing
NOTHING, and that was wrong.** One notice covers both the business register and
ETS's GTFS, as Calgary's does, because the feed is published through the same
Open Data Catalogue.

Edmonton's Terms of Use say credit is "not required" but "encouraged", and both
the Canada profile and `docs/build_briefs/edmonton.md` concluded from that
sentence that Edmonton was the one Canadian city with no display obligation.
**The obligation is in a different clause and it is not about credit:**

> If you distribute or provide access to the datasets to any other person,
> whether in original or modified form, you agree to include a copy of, or this
> Uniform Resource Locator (URL) for, these Terms of Use and to ensure any such
> person agrees to, and is bound by, them **without introducing any further
> restrictions of any kind**.

`outputs/edmonton/` is committed to a public repository and carries the
register's business names, categories and coordinates — that is the dataset in
modified form, so the clause engages. What it requires is **the URL**, which is
now displayed:

> `https://www.edmonton.ca/sites/default/files/public-files/documents/Web-version2.1-OpenDataAgreement.pdf`

The second half, "without introducing any further restrictions", is already
satisfied and was before this was noticed: the repository's own `LICENSE`
disclaims MIT over everything under `outputs/` and points here. That was written
for a different reason and turns out to discharge this clause.

**Two things about reading this licence at all.** The portal's own copy is now
behind a SIGN-IN — `data.edmonton.ca/stories/s/Open-Data-Terms-of-Use/msh4-e6be/`
redirects to a login page, in a browser as well as to `curl`. The readable copy
is the PDF above, and `docs/licenses/edmonton-open-data-terms-of-use.pdf` is a
verified capture of it (SHA-256 in that directory's README, re-checked
2026-09-21). A licence that cannot be read at the URL its dataset points at is
a reason to keep the local copy, not a reason to trust a summary of it.

Unlike Toronto's, Vancouver's, Surrey's and Calgary's, this licence does **not**
terminate automatically on breach — the City may cancel access "at any time for
any reason, in its sole discretion", which is discretionary rather than
automatic. It also bars implying City endorsement or affiliation and bars use of
its marks, which `render_site_notices()`'s standing non-affiliation line covers.

**16. City of Toronto — required, and DISPLAYED. ONE notice covers BOTH the
business register and the TTC's GTFS**, as Calgary's does, because both are City
of Toronto CKAN resources under the same licence:

> `Contains information licensed under the Open Government Licence – Toronto.`

En dash, British "Licence". Like Vancouver's, Surrey's and Calgary's, this
licence **terminates automatically on breach**. Both datasets declare "License
not specified" at dataset level, which is why the licence text was captured from
`open.toronto.ca/open-data-licence/` and stored at
`docs/licenses/toronto-open-government-licence.txt` rather than read from a
field.

**The counts that used to sit here are gone, and their going is the point.**
This paragraph asserted "fourteen cities" and "thirteen sources" and was wrong
on both by the time anyone read it — two cities and three notices had been
added without it being touched, and the sentence disagreed with itself
("thirteen sources", then "six of the twelve"). A hand-maintained tally beside
a hand-maintained list drifts, silently, in the one section that gates a public
deploy. `scripts/check_provenance.py` now asserts the relationship instead:
every entry in `app/components.py`'s `_NOTICES` has a numbered item here, every
numbered item has an entry there, and the numbers are unique and contiguous.
Run it rather than counting.

What does not drift is the shape, and it is worth stating for the next country:

- **The US sources mostly prescribed no wording; the Canadian ones almost all
  prescribe their own.** Budget a notice per SOURCE, not per city.
- **Vancouver added three at once** — the first city to add more than one —
  because it is regional across two municipalities and each Open Government
  Licence prescribes its own sentence. It later added a fourth, the Province's.
- **Montréal added two**, because its business data and its transit data have
  different owners; and Montréal's is the first attribution here that has to
  describe what this project **did to** the data rather than merely name its
  source. INEGI's and CRTM's are the same family.
- **A notice can come from a publisher that is not a city at all.** The
  Province of British Columbia (item 17) is the first, and it arrived through
  the naming layer rather than through any of the three provenance tables —
  which is why the check looks at sources, not at cities.

**17. Province of British Columbia — required, and DISPLAYED since 2026-09-22.
It is the first PROVINCIAL or STATE publisher in this project**, and neither
Vancouver's nor Surrey's municipal licence reaches it:

> `Contains information licensed under the Open Government Licence – British Columbia.`

En dash, British "Licence" — the third notice in this list with that exact
shape, after Vancouver's and Calgary's, and still not interchangeable with
Surrey's hyphen-and-"License". Like the four municipal OGLs it **terminates
automatically on breach**. Read 2026-09-22 and stored at
`docs/licenses/bc-open-government-licence.txt` (version 2.0, last updated
2025-04-11).

**What engages it:** the BC ABMS municipalities layer, read over WFS from
`openmaps.gov.bc.ca`, is what NAMES the 30 SkyTrain stations lying outside
Vancouver and Surrey. `outputs/vancouver/excluded_stations.csv` is committed to
a public repository and carries those names, so the Information is distributed
and the attribution clause engages — the same reasoning that turned Edmonton
from "no obligation" into item 15.

**Why it was missed for a day.** It is not a business registry, not a transit
feed and not the city boundary: it is the **naming layer**, a fourth kind of
input that no per-city checklist had a slot for. D.C.'s Census TIGERweb states
layer is the same role and needed no notice only because US federal works carry
no copyright — so this project had met the category once and drawn exactly the
wrong lesson from it. `scripts/check_provenance.py` now fails when any source
in the three provenance tables has no licence position recorded, which is the
check that would have caught it on the day.

**Two pointers were followed and both mattered.** The licence page opens "as
per B.C. Government Copyright, the following licence only applies to records in
the B.C. Data Catalogue that specify it" — so the catalogue record is the
authority, and it declares OGL-BC. And the page links a **second** document,
"API Terms of Use for OGL Information", which applies here because this project
reads a WFS rather than downloading a file. Read 2026-09-22: it adds
operational conditions (limits "without notice", credentials revocable if
misused, terms changeable without notice, automatic termination) and **no new
notice**. That is TransLink's two-documents shape with the opposite answer —
TransLink's two documents mandate *different legends*, BC's second mandates
none.

**A near miss worth recording.** Three BC layers carry near-identical names and
**two are licensed "Access Only"**, which does not permit redistribution:
`tantalis-municipalities` and `legally-defined-administrative-areas-of-bc`.
Only `municipalities-legally-defined-administrative-areas-of-bc` is OGL-BC. The
build is on the right one — confirmed not by its name but because that
package's own metadata names the exact `openmaps.gov.bc.ca/geo/pub/…
ABMS_MUNICIPALITIES_SP/ows` endpoint the config calls, and because TANTALIS
describes itself as superseded: "[Replacement Dataset: ABMS_MUNICIPALITIES_SP]".
Calgary's two-boundary trap, with a licence consequence instead of a geometry
one.

**18. Seoul Metropolitan Government — WILL BE REQUIRED. Not yet, because no
Korean city is built.** Read 2026-09-22 and recorded here so the cost is known
before the build rather than discovered during it. All eight `인허가 정보`
datasets are **공공누리 제1유형 (KOGL Type 1)**, and it is a **one-notice
country on current evidence** — every dataset carries the same licence, the
same 저작권자 and `제3저작권자: 없음`, so one notice covers the whole city
however many business types it ends up using. The Korean pattern is therefore
the US one, not the Canadian one.

Three things it will require, from `kogl.or.kr`'s own text rather than the
label on the dataset page:

- **Attribution naming institution, year, KOGL type and dataset title — with a
  hyperlink.** KOGL says a link *must* be provided where providing one is
  possible online, which it is here. This is ODbL-shaped, so
  `render_site_notices()` is the right home and a bare source string will not
  discharge it.
- **A non-affiliation line.** Already covered by the standing one that
  `render_site_notices()` emits for Edmonton and Toronto — no new text needed.
- **A statement that the per-station counts are this project's derivation, not
  Seoul's published figures.** KOGL's moral-rights clause names misleading
  modification of statistics specifically. This is the **third** source to
  impose a describe-what-you-did-to-the-data duty, after INEGI and Montréal,
  which is now enough of a pattern to expect it rather than be surprised:
  budget it for any national statistical or licensing register.

Nothing is displayed for this yet and nothing should be — displaying a notice
for data the site does not carry would itself be misleading.

**19. Ayuntamiento de Madrid — required, and DISPLAYED.** The Censo de locales
declares CC BY 4.0, which the *Condiciones generales de reutilización* then
extend by conduct rather than by agreement: *"la mera obtención o el uso de los
documentos sometidos a estas condiciones supone la aceptación"*. Two of those
conditions bear on what is shown, and neither is satisfied by a bare credit:

> **Source and date.** *"Se deberá citar como fuente al Ayuntamiento de
> Madrid"*, together with *"la fecha de la última actualización"* of the
> documents reused.
>
> **Non-distortion.** *"No se desnaturalice el sentido de la información"*, and
> the reuser must not suggest the Ayuntamiento participates in or endorses the
> reuse.

The displayed text therefore names the Ayuntamiento, carries the census date,
states that the ring density, storefront filtering and three-category grouping
are this project's work rather than the city's, and disclaims endorsement.

**20. CRTM (Consorcio Regional de Transportes de Madrid) — required, and
DISPLAYED.** Its *licencia de uso* prescribes the wording, and this is the only
notice in the project whose exact string the publisher dictates:

> **"Powered by CRTM - www.crtm.es"**

Two further conditions travel with it. The reuser must disclose whether the
data is shown *en bruto* or *explotados* — raw or worked — and this project's
is emphatically the latter, so the notice says so. And CRTM's *"siempre
actualizada"* clause requires the displayed data to carry its update date; that
clause was raised as an owner decision and resolved on 2026-09-22 (see above)
as a misrepresentation rule rather than a liveness requirement, discharged by
naming CRTM's own last-update date beside the map.

**21. Ajuntament de Barcelona — required, and DISPLAYED.** The Cens de locals
declares CC BY 4.0, and the Open Data BCN *terms of use* — incorporated by the
legal notice, and read from the Internet Archive because the live pages serve
hCaptcha — prescribe the wording:

> **"Source of the data: Barcelona City Council"**

and require, separately, that **modifications be identified at the point of
distribution**: *"Any amendment or change made to the data sets … shall be
identified as such at the time of their distribution."* That is the
disclosure-of-transformation family for the fourth time, after Montréal, INEGI
and Madrid, and a source credit alone does not discharge it — so the displayed
text names the survey year, states that the vacancy filter, storefront
filtering, three-category grouping and ring measurement are this project's
work, and disclaims endorsement.

⚠️ **A fourth obligation is NOT a notice and is not discharged by this page.**
The same terms require the reuser to *inform Barcelona City Council of every
project* derived from the data — an affirmative act owed to the publisher
rather than text on a page, and the first of its kind in this project. The
clause's own tail gives its purpose: *"so that they are open to the public for
the purpose of encouraging policies for reusing information from the public
sector"*, which makes it a reuse-showcase notification rather than a permission
gate. **It is an owner action, outstanding**; the draft is at
`docs/notifications/barcelona-city-council.md`.

**The displayed notice now reports that act's status**, added 2026-09-22 on the
owner's call: *"That notification is written and not yet delivered: on 22
September 2026 the portal's own contact form stalled, and the enquiry channel
the terms themselves name did not respond. It will be sent when that service is
reachable again."* It is worded as a **status report and never as though it
performed the act** — text on this project's own page is precisely what does
not discharge a duty owed to the publisher, and a sentence that blurred the two
would be worse than no sentence. When the notification is sent, that wording
and the attempt log in the notifications file change together.

**The live terms were read on 2026-09-22** — by the owner, in a browser, past
the hCaptcha — which closes the precondition this file had carried since the
licence review and which Barcelona was published without. Stored at
`licenses/barcelona-condicions-us-live.txt`. Three things changed, none of them
adverse:

- **The notification clause is unchanged, word for word**, so the obligation is
  current and not an artefact of an eighteen-month-old snapshot.
- **The terms name the channel**, which no earlier reading had established:
  *"Any doubts or comments on these Terms of use may be forwarded to the
  following link"* → `bcn.cat/cgi-bin/consultesIRIS?id=241`, which redirects
  to the Council's online enquiry service pre-categorised to city data
  (`atencioenlinia.ajuntament.barcelona.cat`, `origen=DADES_CIUTAT`). **That
  settles a question this project could not answer**: the portal publishes no
  contact email — the dataset's CKAN metadata carries no `maintainer_email` or
  `author_email`, `datos.gob.es` names a web form and no address, and the
  portal's own contact page is behind the same CAPTCHA — so any email address
  would have been invented.
- **A CC BY-ND clause exists and does not apply.** *"any data involving
  third-party participation may be reused under a Creative Commons
  Attribution-NoDerivs (CC BY-ND 4.0) licence"*. ND would forbid this project
  outright, every map being a derivative. It does not bind, because *"Every
  data set that is offered in the Open Data BCN service states its relevant
  Terms of use"* and the Cens de locals declares `CC-BY-4.0` in its own CKAN
  metadata — verified live through `package_show` on 2026-09-22, an endpoint
  that needs no CAPTCHA. Recorded because a clause that would have sunk the
  city deserves to be on the record as checked, not as unnoticed.

⚠️ **Article 8's "content may not be altered" is a DISCLOSED POSITION, not a
resolved one.** The terms import Spanish Act 37/2007 Article 8 — *"the content
of the information may not be altered"*, *"the meaning of the information may
not be distorted"* — and this project filters 10,722 premises rows to three
categories and derives ring density from them. Read literally, that is
alteration. Read in context, the same document permits data *"to provide the
basis for derived works as a result of their analysis or study"*, permits it
*"to be amended, changed and adapted"*, and requires that *"Any amendment or
change … shall be identified as such at the time of their distribution"* — a
requirement that is incoherent if amendment were forbidden. Article 8 is
standard Spanish PSI wording and reads as barring misrepresentation rather than
analysis.

**Owner's decision 2026-09-22: publish on the second reading, stated openly**,
which is Philadelphia's shape. Every transformation is disclosed on the city
page and itemised in the notification, which is what the identify-amendments
clause asks for. The rejected alternatives were asking the Council to confirm
it — inviting a "no" to a question nobody had asked — and holding a finished
city indefinitely on a body under no obligation to reply. **If the Council
reads it the other way, Barcelona comes down**: the standing removal commitment
below covers this without needing to be invoked.

**22. Tailte Éireann — required, and DISPLAYED.** Written at Step 0 so the
obligation existed before the city did, and wired into
`app/components.py`'s `_NOTICES` when Dublin was published on 2026-09-22. The valuation register declares `CC-BY-4.0` on `data.gov.ie`
(`package_show`, verified 2026-09-22), and the licence is Circular 12/2016
Annex 1, which Tailte's own open-data page links. Four obligations converge and
one paragraph discharges all four — the PSI attribution string, Tailte's own
requirement to be named as content creator, **CC BY 4.0 §3(a)(1)'s duty to
indicate modification**, and non-endorsement:

> Contains Irish Public Sector Information licensed under a Creative Commons
> Attribution 4.0 International (CC BY 4.0) licence. Source: Tailte Éireann
> valuation data, via the Tailte Éireann Valuation open API. This map filters,
> re-categorises and aggregates that data into density measures; the filtering,
> categories and densities are this project's own interpretation and are not
> produced or endorsed by Tailte Éireann. The data is published "as is"; Tailte
> Éireann gives no warranty as to its accuracy, completeness or currency.

That is the **disclosure-of-transformation family for the fifth time**, after
Montréal, INEGI, Madrid and Barcelona — a bare source credit does not discharge
it.

⚠️ **Three different attribution strings are live on Irish government sites**,
differing in one word: Circular 12/2016 says *"Irish Public Sector
Information"*, `data.gov.ie/license` says *"Irish Public Sector Data"*, and
`data.gov.ie/technical-framework` says *"Irish Government Data"*. No document
ranks them. The wording above follows the **Circular**, because it is the
instrument Tailte's own page points to and the only one of the three that is a
licence rather than guidance. **Recorded as a disclosed position**, not as a
settled fact.

**Nothing must be DONE.** No registration, notification, permission request or
statistics return is owed — swept for the full affirmative-obligation phrase
set across every document read, with zero hits. **This is explicitly the
opposite of Barcelona's finding** and is recorded positively so it is not
re-opened. Channels exist anyway for corrections:
`opendataofficer@tailte.ie` and `opendata@tailte.ie`, both live, neither
CAPTCHA-walled.

**What must NOT be said**: nothing implying official status or Tailte
endorsement; **no claim the data is accurate, complete or current** (Tailte
disclaims all three, and `tailte.ie/home/api/` states the API "is not
guaranteed to be complete") — the MTA/WMATA prose rule again; and no Tailte
logo, crest or official symbol, which the PSI licence excludes and CC BY 4.0
§2(b) does not license.

✅ **The `Eircode` column is DROPPED — owner's call, 2026-09-22.** The Eircode
database is third-party IP (An Post / OSi via GeoDirectory, licensed through
Capita), and both the PSI licence and `data.gov.ie/license` carve out
third-party database rights the Information Provider is not authorised to
license. Tailte publishes Eircodes inside a dataset it declares CC BY 4.0,
which is an argument that it holds the right to; republishing ~38,000 of them
is a substantial extraction from a database whose *sui generis* right belongs
to someone else, which is an argument that it does not.

**The decision does not resolve that — it removes it.** The build has
`Xitm`/`Yitm` and five address lines and never reads `Eircode`, so dropping the
column costs the map nothing and leaves the source with no third-party-rights
exposure at all. The rejected alternative was publishing on the permissive
reading with the position disclosed, which is what Philadelphia and Barcelona
do — declined because **those two had no cheaper option and this one does.**
Step 2 must drop it at load so it never reaches a processed file.

One page that reads alarmingly and does not apply:
`tailte.ie/map-shop/map-licences-and-copyright/` requires "prior permission"
for reproducing Tailte **surveying** material. It mentions valuation, open
data, API, Eircode, PSI and Creative Commons **zero times each** and governs
the paid Map Shop products. Read and inapplicable — recorded so the next
reader does not re-establish it.

**23. Comune di Milano — required, and DISPLAYED.**

This took the wrong number for an hour. The Tailte Éireann item immediately
above had already reached master with Dublin's *brief* commit, which is
docs-only, while Dublin's build sat on a branch — so the next free number read
one lower than it was. `check_provenance.py` caught the duplicate within the
same session, then caught the stale citation left behind by fixing it. It is
the check that once found two item 8s and two item 15s, and this is the third
time it has earned its place. Recorded at build time so the obligation exists
before the city is live; **this item is a deploy blocker for Milan
specifically**, not an outstanding defect on the cities now published. All six
premises registers and all three ATM rail layers declare **CC BY 4.0**.

⚠️ **The version is invisible where anyone would look.** CKAN's `package_show`
reports `license_id: cc-by` with **no version at all**, and its `license_url`
points at opendefinition's version-less register entry. Three independent
sources give 4.0: the portal's **DCAT-AP_IT** serialisation
(`owl:versionInfo "4.0"`), the portal footer, and the national catalogue
`dati.gov.it`. `scripts/brief_check.py` gained an `http_contains` kind for
exactly this, and Milan's brief pins its licence claim to the `.ttl` rather
than to `package_show` — a check that cannot see the thing it guards is the
failure shape this project keeps writing scripts against.

**No wording is prescribed**, so CC BY 4.0 §3(a)(2) applies ("any reasonable
manner"). The components are still mandatory, and one of them is work:

> Contains data from the Comune di Milano, licensed under a Creative Commons
> Attribution 4.0 International (CC BY 4.0) licence. This map filters,
> re-categorises and aggregates that data into density measures; the
> filtering, categories and densities are this project's own and are not
> produced or endorsed by the Comune di Milano.

That discharges attribution, **CC BY 4.0 §3(a)(1)'s duty to indicate
modification** — the disclosure-of-transformation family for the **sixth**
time, after Montréal, INEGI, Madrid, Barcelona and Tailte Éireann — and the
§2(a)(5)(C) non-endorsement clause. Note it is the *weaker* form of the
disclosure duty: CC BY 4.0 requires disclosing **modification** and says
nothing about interpretation, where Montréal's licence names both.

**MUST DO: nothing.** The Italian trigger phrases (`informare`, `comunicare
al`, `registraz`, `previa autorizzazione`, `obbligo di`) return **zero** across
the dataset pages and the portal's `/about`. A channel exists if the project
ever wants to notify voluntarily: `opendatamilano@comune.milano.it`, consistent
across three sources.

⚠️ **Do not generalise this licence to the portal.** Neighbouring datasets in
the same searches carry `other-at` and `cc-zero`; any further Milan dataset
needs its own `package_show`. Two decoys, both real and both about something
else: the portal footer's `CC-BY 3.0` link is attribution the portal owes
**upstream** for its theme icons, and `comune.milano.it`'s *Note Legali*
licenses **the institutional website** under CC BY 3.0 IT — that page names
*"il sito ufficiale"* and self-defers with *"salvo dove è diversamente
specificato"*.

**Prudential, not an obligation:** the publisher's own description warns the
register is not internally consistent — *"le informazioni contenute nel dataset
non sono necessariamente omogenee, perché riferite al momento dell'ultima
comunicazione"*. Nothing forbids calling the data current; the publisher's own
statement makes it unwise.

**24. Île-de-France Mobilités — required, and DISPLAYED.**

Recorded at scaffold time so the obligation existed before the city did, then
**missed anyway**: the map rendered, the gate was run, and the notice was still
absent from every page. A verification pass on 2026-09-23 found
`verbatimIDFMNotice: false` on `/Paris_Heatmap` with 21 sources in the notices
block and not one of them French. Added to `app/components.py`'s `_NOTICES` the
same day.

⚠️ **Nothing automated caught it, and that is the more useful finding.**
`check_provenance.py` checks these notices in bijection with `_NOTICES` and
prints `notices: 24 numbered, 21 displayed` — as a line of output, passing
regardless. A required notice that is documented, numbered, called a deploy
blocker in this very entry, and simply not rendered is exactly the gap this
file's own reasoning says a script should close rather than a paragraph.

**This is the first notice here whose licence is not a standard public one.**
`mobility-licence` covers exactly **2 of 799** NAP datasets, there is no
government-hosted text, and the authoritative document is a 14-page PDF behind
a community wiki. It is ODbL-*derived* but **not ODbL-compatible**, so nothing
in the OpenStreetMap posture transfers to it. Art. 3.1 grants worldwide, free,
commercial use including **« l'affichage public »** — redrawing is permitted.

**MUST DISPLAY**, verbatim:

> Contient des informations de Réseaux urbains et interurbains d'Île-de-France
> Mobilités (IDFM), présentement mises à disposition aux conditions de la
> « Licence Mobilités »

⚠️ **Art. 5.4(a) prescribes the LINKING as well as the words** — the database
name must hyperlink to the dataset URI, and « Licence Mobilités » to the
licence text. No other notice in this file constrains markup, so
`render_site_notices()` cannot carry this one as plain text the way it carries
LA Metro's.

⚠️ **Two obligation shapes this project has never carried**, both from Art. 5.7,
which forbids use misleading « quant … à sa date de mise à jour »: the **date
the data was last updated**, and its **update interval**. A pre-rendered static
map built from a frozen snapshot is exactly that unless the snapshot date is
shown. This is where the missing `feed_info.txt` becomes a compliance problem
rather than a curiosity — **neither value exists inside the artifact**, so both
must be captured at fetch time or they cannot be displayed honestly.

**MUST DO**, three things, none of them a permission gate:

- **Report source errors** to `contact-prim@iledefrance-mobilites.fr` « sans
  délai ». A data-quality duty.
- **Supply modifications to recipients** (Art. 5.8). A public repository
  carrying the pipeline code and the derived CSVs, linked from the site,
  satisfies it — which this project already does for every other city.
- **Republish the derived station table on the NAP** as a *ressource
  communautaire* (Art. 5.6(b)). Arguably not owed: that article says a rendered
  map is a *Création Produite* rather than a Derivative Database, and the NAP's
  own published example — *"Calcul de la distance à l'arrêt de bus le plus
  proche pour une liste de commerces"*, which is close to this project's exact
  shape — is filed under **"Non"**. But this project commits `outputs/<city>/`,
  so the derived table is published either way and **one upload moots the
  argument** rather than requiring it to be won.

**MUST NOT:** Art. 5.7's duty is the *inverse* of MTA's and WMATA's. Where those
forbid claiming accuracy, this one requires currency and
« l'**exhaustivité** des données disponibles », with a relevance proviso that
covers deliberate exclusions. **So the page should state what was excluded
rather than leave it implicit** — commuter rail, tram, and the 77 out-of-commune
métro stations.

⚠️ **REVOCABLE.** Art. 11.1 terminates *de plein droit, sans préavis* on
breach. Unlike Licence Ouverte this is a revocable grant, and the owner
accepted it on 2026-09-22 with the response decided in advance — see the
removal-commitment section above, where the archive-not-delete posture is
recorded.

⚠️ **IDFM's own licences page contradicts the NAP**, saying its *tracés du
réseau ferré* are Licence **Ouverte**, reserving Licence Mobilités for
timetables this project does not publish. **The stricter reading was adopted
deliberately.** If the looser one were ever relied on, this entire item is
replaced by an Etalab attribution — which is a reason to keep the contradiction
recorded rather than resolve it silently in the project's favour.

**25. Tisséo (Toulouse) — required, and DISPLAYED.**

**ODbL 1.0**, declared `odc-odbl` on France's National Access Point. The full
reading is at `docs/licenses/odbl-toulouse-rennes.md`, which also governs
Rennes — hence the filename covering both.

**MUST DISPLAY**, verbatim. This is ODbL §4.3's own notice template with the
database named, so the wording is the licence's rather than this project's:

> Contains information from Réseau urbain Tisséo, which is made available
> here under the Open Database License (ODbL).

⚠️ **The OpenStreetMap notice at item 1 does NOT discharge this**, and that is
worth stating because the opposite is the natural assumption. Both sources are
ODbL, so one credit looks like it ought to cover both — but §4.3 requires the
notice to name *which* database, and "© OpenStreetMap contributors" names
OSM's. **Two ODbL sources need two notices.**

**MUST DO — §4.6.** Offer the Derivative Database, or the method. The public
repository carries the pipeline code and the derived CSVs and satisfies it,
**provided it stays linked from the site** — the same standing condition
IDFM's Art. 5.8 already imposes at item 24, so nothing new is owed as an act.

**✅ The publisher's own CGU adds nothing harmful.** Read 2026-09-23 at
`data.toulouse-metropole.fr/terms/terms-and-conditions/`:

- **No indemnity clause**, unlike Grand Lyon's CGU 9.4.
- **The marks clause is Opendatasoft's own**, and it expressly excludes
  « les données publiées sur le DOMAINE ». ✅ So naming *Tisséo* on the map is
  not barred — which was the specific risk here, since Grand Lyon's equivalent
  clause is the reason Lyon is deferred rather than built.
- The express extraction bar applies only « en dehors d'une LICENCE
  consentie », and this project is inside one.

⚠️ **OPEN — the station CSV under §4.4.** Whether the derived station table and
`outputs/toulouse/excluded_stations.csv` are themselves a Derivative Database
that must carry the notice is unresolved, and unlike Paris there is **no
publisher gloss** to lean on. **Cheap discharge: put the ODbL notice on the
station CSV** rather than try to win the argument.

**26. STAR (Rennes) — required, and DISPLAYED.**

**ODbL 1.0**, declared `odc-odbl` on France's National Access Point, read in
`docs/licenses/odbl-toulouse-rennes.md` alongside Tisséo's.

**MUST DISPLAY**, verbatim - ODbL §4.3's own notice template with the database
named:

> Contains information from Réseau urbain STAR, which is made available
> here under the Open Database License (ODbL).

⚠️ **Neither the OpenStreetMap notice (1) nor Tisséo's (25) discharges this.**
Three ODbL sources now, and §4.3 asks each notice to name its own database.

**MUST DO — §4.6**, as for Tisséo: the linked public repository offers the
method, and satisfies it while it stays linked.

**✅ The publisher's CGU adds nothing harmful**, read 2026-09-23 at
`data.explore.star.fr/terms/terms-and-conditions/` - the same Opendatasoft
template as Toulouse Métropole's: no indemnity, and a marks clause that is
Opendatasoft's own with « les données publiées sur le DOMAINE » excluded, so
naming *STAR* on the map is not barred. Watched by the brief check
`star-cgu-still-clean`.

⚠️ **OPEN — the station CSV under §4.4**, exactly as for Tisséo:
`outputs/rennes/excluded_stations.csv` is left in the same state as Toulouse's,
and the same cheap discharge is available if the question is ever pressed.

What has grown instead is the pile of **permission questions**, now four: three
"what does silence mean?" calls and the route-colour one. They are questions
about permission rather than implementation, and they are the only items of
that kind outstanding. Two sources' positions remain formally unestablished —
the Census geocoder, whose terms are simply unread, and **Miami-Dade, whose
terms do not address reuse at all.** Those two are different in kind: one is a
document nobody has opened, the other is a document that does not exist.

## Gaps

- ~~San Francisco's boundary layer endpoint is not recorded anywhere.~~
  **Closed 2026-09-21:** identified as `wamw-vt4s` and confirmed byte-for-byte
  against the raw file. Every built city can now be rebuilt from scratch from
  this document alone, which `scripts/check_provenance.py` asserts rather than
  this sentence claiming it — it said “all five cities” until 2026-09-22, long
  after there were sixteen.
- Retrieval dates marked ≈ are inferred from commit history, not recorded at
  download time. Dates for cities added from now on are recorded exactly.
- Licences, as above — the one substantive gap left.
