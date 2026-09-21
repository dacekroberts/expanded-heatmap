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
| San Francisco | DataSF Registered Business Locations (Socrata `g8m3-pdis`) | All three buckets, via NAICS | `https://data.sf.gov/resource/g8m3-pdis.csv` | San Francisco only | ≈2026-09-19 |
| Los Angeles | Listing of Active Businesses (Socrata `6rrh-rzua`) | All three buckets, via NAICS | `https://data.lacity.org/resource/6rrh-rzua.csv` | `$where=location_1 IS NOT NULL`, selected columns, `$order=location_account` | ≈2026-09-19 |
| Chicago | Business Licenses (Socrata `r5kz-chrr`) | All three buckets, via its own licence taxonomy | `https://data.cityofchicago.org/resource/r5kz-chrr.csv` | `license_status='AAI' AND expiration_date >= '2026-09-20'`, `$order=id` | 2026-09-20 |
| Washington D.C. | **Basic Business License** (DCRA/DLCP, ArcGIS FeatureServer) | **All three buckets, via its own `BUSINESSACTIVITY` taxonomy** — the first non-NAICS source here that covers all three on its own | `https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/DCRA/FeatureServer/0/query` (`outSR` not needed — `returnGeometry=false`, `orderByFields=OBJECTID ASC`, paged at 2,000) | `LICENSESTATUS='Active' AND PREMISEINDC='Yes' AND BUSINESSACTIVITY NOT IN (<the five residential rental types>)`, and an explicit 16-column `outFields` list that omits every owner/agent name and the billing address | 2026-09-21 |
| New York | DOHMH Restaurant Inspection Results (Socrata `43nn-pn8j`) | **Food service** | `https://data.cityofnewyork.us/resource/43nn-pn8j.csv` | selected columns, `$limit=500000` (unfiltered: it is an inspection history, collapsed to one row per establishment in step 2) | 2026-09-21 |
| New York | NYS Retail Food Stores (Socrata `9a8c-vfzj`, data.ny.gov) | **Retail** — grocery, bodegas, delis, supermarkets | `https://data.ny.gov/resource/9a8c-vfzj.csv` | `county in('KINGS','QUEENS','BRONX','NEW YORK','RICHMOND')` | 2026-09-21 |
| New York | NYS Active Appearance Enhancement & Barber *Business* Licensees (Socrata `y3u4-jbgh`, data.ny.gov) | **Personal services** — salons, nail, skin care, barbers | `https://data.ny.gov/resource/y3u4-jbgh.csv` | selected columns; **`license_holder_name` deliberately not selected** (it is an individual's name) | 2026-09-21 |
| New York | DCWP Issued Licenses (Socrata `w7w3-xahh`) | **Retail**, a narrow regulated slice | `https://data.cityofnewyork.us/resource/w7w3-xahh.csv` | `license_status='Active' AND license_type='Premises'` | 2026-09-21 |
| Philadelphia | L&I Business Licenses (Carto SQL API, table `business_licenses`) | **Food service** and **Retail** only — see below | `https://phl.carto.com/api/v2/sql` (`format=csv`) | `licensestatus='Active' AND licensetype IN (…13 types…)`, built from `config.KEPT_LICENSETYPES`; selected columns, **no registrant-name column** (`legalfirstname`, `legallastname`, `legalname`, `opa_owner`, `ownercontact*name` are all deliberately unselected and asserted absent in step 2) | 2026-09-21 |
| Philadelphia | OPA Property Assessments (Carto SQL API, table `opa_properties_public`, 583,779 rows) | Not businesses — **joined** to the above for the residence check | same endpoint, `LEFT JOIN opa_properties_public p ON b.opa_account_num = p.parcel_number` (matches 94% of licences) | 2026-09-21 |
| Miami | Miami-Dade County **Local Business Tax** (ArcGIS FeatureServer, 194,099 rows, all `YEAR`=2026) | All three buckets, via the county's own `CATGRYNAME` (150 values). **Its `BUSNAICSCD` column is NULL on all 194,099 rows**, so NAICS is unavailable despite being in the schema | `https://services.arcgis.com/8Pc9XBTAsYuxx9Ny/arcgis/rest/services/Local_Business_Tax_Feature_Layer_View/FeatureServer/0/query` | `ACCSTATUS='Active'` (175,982 rows), selected columns, `orderByFields=OBJECTID` for stable deep paging. **`OWNERNAME` and every `MAIL*` column are deliberately NOT downloaded** — `OWNERNAME` is populated on 100% of rows and is frequently a person; step 2 asserts all eight stay absent | 2026-09-21 |
| Boston | Food Establishment Inspections (CKAN resource `4582bec6-2b4f-4f9e-bc55-cbaa73117f4c`, 902,651 rows) | **Food service** (`FS`, `FT`) and **Retail** (`RF`) — see below | `https://data.boston.gov/api/3/action/datastore_search_sql` | `licstatus='Active'`, **collapsed to one row per `property_id` + `licensecat` in SQL** with `GROUP BY`, so the download is ~2,900 rows rather than ~900,000. `legalowner`, `namelast` and `namefirst` exist in this table and are deliberately NOT selected; step 2 asserts they and five more stay absent | 2026-09-21 |
| Boston | Licensing Board Licenses (CKAN resource `04dc653b-1789-4374-9669-b07df7233344`, 3,587 rows) | **Retail** — package stores only | same endpoint | `status='Active' AND (license_type LIKE 'Retail%' OR license_type = 'Druggist')` → 307 rows. Its 2,578 Common Victualler licences are the same restaurants as the ISD source and are excluded to avoid double-counting. Coordinates are `gpsx`/`gpsy` in **EPSG:2249** (state plane, US survey feet), reprojected in step 2 — not lat/lon. `applicant`, `manager`, `day_phone` and `evening_phone` are NOT selected | 2026-09-21 |
| Boston | Cannabis Active Licenses (CKAN resource `e395fd88-0f81-4399-a57a-3e94a74b145c`, 43 rows) | **Retail** — dispensaries | same endpoint | `status='Active'`; same `gpsx`/`gpsy` convention as the Licensing Board set. The one `Delivery (operator)` row is excluded — no shopfront | 2026-09-21 |
| Boston — **recorded, deliberately NOT used** | Business Inventory (CKAN resource `47bd8208-f648-4309-8f65-de7416d63157`, 2,634 rows) | Would cover **all three buckets**, and is the only Boston source that reaches Personal services | same endpoint | — | 2026-09-21 |

The Philadelphia parcel join exists to answer one privacy question the address
text cannot: **is this "business" someone's home?** Only two derived values are
selected — the City's own `category_code_description` land-use category, and a
boolean for whether a homestead exemption is claimed (Philadelphia grants that
only on an owner's primary residence). The exemption *amount* is not
downloaded, and no mailing address is downloaded at all. Neither value is ever
published: the rendered map emits only name, category, station and ring. Same
"City of Philadelphia License" as the licence data, already recorded below.

New York needs four because it has **no general business licence** — see
`pipeline/taxonomies/new_york.py`. Every other city needed one.

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

## Transit feeds (GTFS)

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

### Still not established

| Source | Status |
|---|---|
| **US Census bulk geocoder** | Terms page not read. A US federal government work, used only to derive coordinates stored in this project's own outputs. Low priority, and the only item left unread.
| **Boston "Business Inventory" (`47bd8208`)** | The one dataset on `data.boston.gov` whose `license_id` is `notspecified` rather than `odc-pddl`. Not established, and not pursued, because the source is deliberately unused (its coverage is downtown plus three corridors). **If it is ever used, the governing terms must be established first** — the portal's own "Open and Protected Data Policy" and the 2014 open-data executive order are the documents to read, not the boston.gov site footer. That is the NYC lesson: the parent site's notice covers the website, not the datasets.
| **Miami-Dade Local Business Tax, its municipal boundary layer, and Miami-Dade Transit's GTFS** | All three carry a disclaimer and no grant. The ArcGIS items' `licenseInfo` is purely about ACCURACY — “Miami-Dade County provides this data for use 'as is'… not accurate to surveying or engineering standards… assumes no responsibility for errors or omissions” — and says nothing whatever about reuse, redistribution, modification or attribution. The GTFS has no `feed_info.txt`, and no separate MDT developer terms were located. **ESTABLISHED 2026-09-21, by reading rather than asking — and this row's earlier claim that no document existed was wrong.** One does: the Open Data Hub's own designated Terms of Use at `https://opendata.miamidade.gov/pages/terms-of-use`. Its entire substance is the accuracy disclaimer quoted above. The county-wide "Liability Disclaimer and User Agreement" at `miamidade.gov/global/disclaimer/disclaimer.page` was read too, and is liability terms only — no copyright claim, no reuse restriction. So three County documents now say nothing whatever about reuse, redistribution, modification or attribution, which is a **definitive absence of restriction from the County's own authoritative pages** rather than an unexamined gap. No enquiry to the County is needed. The affirmative signals stand: all three sources are published by the County's own ITD Geospatial group on its public open-data portal, in formats meant for reuse. |

Note the shape of this. **The business registries are mostly permissive and the
transit feeds are mostly not** — and the two are inverted within Los Angeles,
whose business data is CC0 while its GTFS terms are the most restrictive of
anything here. New York contributes four of the eight registries and is the
only source whose reuse position could not be established at all.

### Transit feeds (GTFS) — checked 2026-09-21

Line geometry is redrawn from each feed's `shapes.txt` into every map, so these
terms bear directly on what is published. No feed declares a licence in
`feed_info.txt`; LA Metro's feed even includes a `feed_license` column and
leaves it empty, pointing to its developer terms instead.

| Agency | Redistribution | Attribution | Other conditions |
|---|---|---|---|
| **MTS** (San Diego) | Permitted: "non-exclusive, limited and revocable rights to use, reproduce, and redistribute" | Not required | MTS trademarks "may not be used in association with GTFS Data". As-is, no liability; may withdraw the data at any time |
| **SFMTA** | Permitted: "use, reproduce, and redistribute" | **Required, in specific wording** (below) | Must also display liability disclaimers; no trademarks or logos without written permission |
| **LA Metro** | **Restricted** — prohibits "unauthorized redistribution and publication" and requires you "not change, tamper, dismantle, augment, misrepresent or otherwise modify the Transport Information" | **Required** — must "acknowledge Metro as the provider of the Transport Information" and not claim ownership | No Metro trademark; must not "integrate Transport Information as part of any advertisement"; on termination you "shall immediately remove the Transport Information and all references to it" |
| **CTA** | Permitted: "use, reproduce, distribute, display, process and create derivative works" | Optional but encouraged: "Data provided by Chicago Transit Authority", "Data provided by CTA" or "Powered by CTA data" | **Purpose-limited** — the licence is granted to "assist mass transit riders or promote public transportation"; may not sell CTA Data separate from the application; may not imply affiliation or endorsement |
| **MTA** (New York) | Permitted: the feeds are "provided without charge", and the agreement "authorizes you to download and host the data on a non-MTA server ... and to make the data available to others who will access that non-MTA server". No API key needed for the static subway feed | Not required, but you "will not state or imply in any manner that your app is licensed by MTA"; you may state the data was obtained from MTA and is redistributed from your own server | **Corrected 2026-09-21 — this row previously recorded only the "Our data feeds are free to use" line from `mta.info/developers`, which is the landing page, not the terms.** The actual agreement (`https://new.mta.info/developers/terms-and-conditions`, page dated 2024-03-13) says **"You will not modify or delete any of the data"**, though its next sentence permits "an app that uses some but not all of the data". Also: must not "state or imply that the data is accurate, complete, or timely"; must serve the data from a non-MTA server and never directly from MTA's; MTA may change or terminate the agreement at any time without notice. Logos, maps and symbols need a separate licence application (free of charge but must be applied for). **An open decision, not a settled one — see `PLAN.md`.** Local copy: `docs/licenses/mta-terms-and-conditions.txt` |
| **MBTA / MassDOT** (Boston) | Permitted: §3.1 grants "non-exclusive, limited, and revocable rights to use, reproduce, and redistribute the Data" | **Required** — §4.1 "Clearly acknowledge MassDOT as the provider of the Data" | §4.2 **expressly permits** combining the Data with other data. §4.1 forbids reproducing "MassDOT or any of its agencies or authorities logos or trademarks in connection with the Data", misrepresenting the Data, claiming ownership of it, or representing yourself as MassDOT or its agent. As-is with "all faults"; MassDOT may alter the terms or revoke the Data at any time without notice; Massachusetts law, venue Suffolk County. Document dated 2009-11-13, at `https://cdn.mbta.com/sites/default/files/2023-08/mbta-massdot-develop-license-agreement.pdf` — reachable from `mbta.com/developers/gtfs`, and the only route to the terms, since `feed_info.txt` declares none. **A local copy is kept at `docs/licenses/mbta-massdot-develop-license-agreement.pdf`**, because MassDOT may alter or revoke the terms without notice (§5.1, §8) and `mass.gov` returns 403 to automated fetches |
| **SEPTA** (Philadelphia) | Permitted: a "non-exclusive, non-assignable, non-transferable, limited and **revocable** right to use, reproduce and redistribute the datasets" | **Not required** — no attribution or notice clause anywhere in the agreement | "Licensee may not use SEPTA's trademarks and copyrighted materials for any commercial or profit-making use and may not alter them in any way." SEPTA "maintains title, ownership, rights and interest in and to the datasets", may revoke or modify the agreement at any time, and "reserves the right to institute a license fee at any time". As-is, no warranty, indemnification required; governed by Pennsylvania law, venue Philadelphia County. At `https://wwww.septa.org/license-agreement/` — the four-w host is **SEPTA's real domain, not the repo-README typo this row previously called it**: `www.septa.org` and `wwww.septa.org` each return 200 independently, with no redirect between them (checked 2026-09-21). Local copy: `docs/licenses/septa-license-agreement.html` |

**All six of these agreements are stored locally**, in
[`licenses/`](licenses/) — source URL, retrieval date and SHA-256 for each are
in that directory's `README.md`. Every one of them is revocable and amendable
without notice, so the clauses quoted above are checkable against the text that
was actually agreed to rather than against a URL that may have moved on.

| **WMATA** (Washington D.C. — **BUILT 2026-09-21**) | Permitted within your own app: "a limited, non-exclusive, non-assignable, non-transferrable, non-sublicensable, revocable license to download, use, reproduce, and redistribute WMATA's Transit Data within your Application". **Third-party redistribution is prohibited** — "sharing (except with your Application's users), transferring, sublicensing, selling or leasing any Transit Data, directly or indirectly...to any other person", unless authorised in writing and "inseparably commingled with or supplemented by additional data that you have provided" | **Not required** — no attribution or notice clause | **No modification clause at all**, which makes it more permissive than LA Metro's on the point that matters most. Access is gated: `api.wmata.com/gtfs/rail-gtfs-static.zip` returns **401** without a registered key from `developer.wmata.com/signup`; keys "remain WMATA's property and may be revoked or otherwise limited at any time", cannot be sold, transferred or sublicensed, and "enable WMATA to associate your API activity with your Application". Trademarks: "prohibited from using WMATA Intellectual Property, including any confusingly similar variants, in association with the Transit Data or API unless you have entered into a separate, written license agreement", and must not "state or imply affiliation, sponsorship or endorsement". **§6 additionally forbids stating or implying that the data your Application provides "is accurate, complete, or timely"** — the identical clause MTA carries, making this the **second** feed to constrain city-page prose that way, so it is a cross-city sweep rather than a D.C. footnote. **§9 termination is the sharpest in the project:** on termination "you must permanently delete all Transit Data or other data which you stored pursuant to your use of the API or GTFS", and "WMATA may request that you certify in writing your compliance with this section" — LA Metro requires removal, but only WMATA asks for written certification. Read 2026-09-21 from `https://developer.wmata.com/license`; local copy at `docs/licenses/wmata-transit-data-terms-of-use.html` |

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
  request is at `docs/licenses/phila-permission-request.md`, addressed to
  `maps@phila.gov` copying `LIGISTEAM@phila.gov`, and is **not sent yet**.
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

**2. City of Chicago — required, NOT YET DISPLAYED.** Chicago's Data Terms of
Use require any "secondary or derivative application" to carry this disclaimer,
verbatim, "at the site where the software application … can be accessed":

> "This site provides applications using data that has been modified for use
> from its original source, www.cityofchicago.org, the official website of the
> City of Chicago. The City of Chicago makes no claims as to the content,
> accuracy, timeliness, or completeness of any of the data provided at this
> site. The data provided at this site is subject to change at any time. It is
> understood that the data provided at this site is being used at one's own
> risk."

**3. SFMTA — required, NOT YET DISPLAYED.** Its transit-data licence requires
derivative works to include:

> "Reproduced with permission granted by the City and County of San Francisco.
> The information has been provided by means of a nonexclusive, limited, and
> revocable license granted by the City and County of San Francisco."

**4. LA Metro — required, NOT YET DISPLAYED.** Must acknowledge Metro as the
provider of the transit information and must not claim ownership of it. No
exact wording is prescribed; "Rail alignment data provided by LA Metro" would
meet the stated requirement.

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

**7. MassDOT / MBTA — required, NOT YET DISPLAYED. Boston was built on 2026-09-21, so this is now ACTIVE rather than conditional.**
§4.1 of the MassDOT Developers License Agreement requires the licensee to
"Clearly acknowledge MassDOT as the provider of the Data". No exact wording is
prescribed. Boston's city page already carries **"Rail alignment data provided by MassDOT/MBTA"**, which meets the requirement for that page; the outstanding part is the same as for the other three — it must appear where the *site* is accessed, not only on one city page. Same shape as LA Metro's obligation. The agreement
itself is kept at `docs/licenses/mbta-massdot-develop-license-agreement.pdf`.

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
   line names beside them.** Affects **six of the nine built cities**: San
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
8. Optionally, read the Census geocoder's terms — the only source left unread.

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
  against the raw file. All five cities can now be rebuilt from scratch from
  this document alone.
- Retrieval dates marked ≈ are inferred from commit history, not recorded at
  download time. Dates for cities added from now on are recorded exactly.
- Licences, as above — the one substantive gap left.
