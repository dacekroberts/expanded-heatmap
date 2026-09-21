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

- **Adding a city adds its rows here, in the same commit.** The `add-city`
  skill lists this as a step; a city is not finished until its sources are
  recorded.
- Record the **endpoint**, the **server-side filter** (the download is often
  filtered — that filter is part of the provenance), and the **date retrieved**.
- When an endpoint dies, leave the old row and mark it dead with the date,
  rather than overwriting it. Dataset IDs get retired: New York's borough
  boundaries moved from `tqmj-j8zm` (now 404) to `gthc-hcne`, and the MTA
  retired its `web.mta.info/developers` GTFS path in favour of an S3 bucket.
  A silently-replaced URL loses that history.
- Raw downloads are **not** committed (`data/<city>/raw/` is gitignored). Only
  the rendered `outputs/` are. So these endpoints plus the recorded filters are
  the only way to reproduce a build.

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| San Diego | City Business Tax Certificates | All three buckets, via NAICS | `https://seshat.datasd.org/business_tax_certificates/` (`sd_businesses_active_datasd.csv`) | none (whole file) | 2026-09-18 |
| San Francisco | DataSF Registered Business Locations (Socrata `g8m3-pdis`) | All three buckets, via NAICS | `https://data.sf.gov/resource/g8m3-pdis.csv` | San Francisco only | ≈2026-09-19 |
| Los Angeles | Listing of Active Businesses (Socrata `6rrh-rzua`) | All three buckets, via NAICS | `https://data.lacity.org/resource/6rrh-rzua.csv` | `$where=location_1 IS NOT NULL`, selected columns, `$order=location_account` | ≈2026-09-19 |
| Chicago | Business Licenses (Socrata `r5kz-chrr`) | All three buckets, via its own licence taxonomy | `https://data.cityofchicago.org/resource/r5kz-chrr.csv` | `license_status='AAI' AND expiration_date >= '2026-09-20'`, `$order=id` | 2026-09-20 |
| New York | DOHMH Restaurant Inspection Results (Socrata `43nn-pn8j`) | **Food service** | `https://data.cityofnewyork.us/resource/43nn-pn8j.csv` | selected columns, `$limit=500000` (unfiltered: it is an inspection history, collapsed to one row per establishment in step 2) | 2026-09-21 |
| New York | NYS Retail Food Stores (Socrata `9a8c-vfzj`, data.ny.gov) | **Retail** — grocery, bodegas, delis, supermarkets | `https://data.ny.gov/resource/9a8c-vfzj.csv` | `county in('KINGS','QUEENS','BRONX','NEW YORK','RICHMOND')` | 2026-09-21 |
| New York | NYS Active Appearance Enhancement & Barber *Business* Licensees (Socrata `y3u4-jbgh`, data.ny.gov) | **Personal services** — salons, nail, skin care, barbers | `https://data.ny.gov/resource/y3u4-jbgh.csv` | selected columns; **`license_holder_name` deliberately not selected** (it is an individual's name) | 2026-09-21 |
| New York | DCWP Issued Licenses (Socrata `w7w3-xahh`) | **Retail**, a narrow regulated slice | `https://data.cityofnewyork.us/resource/w7w3-xahh.csv` | `license_status='Active' AND license_type='Premises'` | 2026-09-21 |

New York needs four because it has **no general business licence** — see
`pipeline/taxonomies/new_york.py`. Every other city needed one.

## Transit feeds (GTFS)

| City | Agency / system | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| San Diego | MTS Trolley | `https://www.sdmts.com/google_transit_files/google_transit.zip` | 2026-09-18 | |
| San Francisco | SFMTA Muni Metro | `https://muni-gtfs.apps.sfmta.com/data/muni_gtfs-current.zip` | ≈2026-09-19 | **Mirror.** The official host (`sfmta.com/reports/gtfs-transit-data`) timed out from this environment; this URL is linked from the agency's own page |
| Los Angeles | LA Metro Rail | `https://gitlab.com/LACMTA/gtfs_rail/raw/master/gtfs_rail.zip` | ≈2026-09-19 | Metro's rail-only feed |
| Chicago | CTA | `https://www.transitchicago.com/downloads/sch_data/google_transit.zip` | 2026-09-20 | |
| New York | MTA subway + Staten Island Railway | `https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip` | 2026-09-21 | The `web.mta.info/developers/data/nyct/subway/google_transit.zip` path is **dead** |

## Boundary layers

Used to scope stations and businesses to the city. Not optional: San Diego's
Trolley serves six other cities, and 54 of Los Angeles' 110 rail stations lie
in 23 other municipalities.

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| San Diego | SANDAG regional municipal boundaries | `https://geo.sandag.org/server/rest/directories/downloads/Municipal_Boundaries.geojson` | `SAN DIEGO` |
| San Francisco | County boundary | **NOT RECORDED** — see Gaps | `San Francisco` |
| Los Angeles | LA County Planning, incorporated cities | `https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/admin_dist_SDE_DIST_DRP_CITY_COMM_BDY/FeatureServer/0/query` (`JURISDICTION='INCORPORATED CITY'`, `outSR=4326`, `f=geojson`) | `LOS ANGELES` |
| Chicago | Socrata "Boundaries - City" (`qqq8-j68g`) | `https://data.cityofchicago.org/resource/qqq8-j68g.geojson?$limit=10` | whole city |
| New York | Borough Boundaries (`gthc-hcne`) | `https://data.cityofnewyork.us/resource/gthc-hcne.geojson?$limit=10` | all five boroughs = the city |

Chicago note: the sibling asset `ewy2-6yfk` ("Boundaries - City - Map") has
null geometry; `qqq8-j68g` is the usable one.
New York note: `tqmj-j8zm`, the borough-boundary ID still in wide circulation,
now returns 404.

## Geocoding

| Service | Used by | Endpoint | Note |
|---|---|---|---|
| US Census Bureau bulk geocoder | Los Angeles, New York | `https://geocoding.geo.census.gov/geocoder/locations/addressbatch` | Free, no API key, US addresses only. Benchmark `Public_AR_Current`. Responses cached by batch content hash, so re-runs and drift checks stay offline and deterministic |

## Basemap tiles

Rendered maps use Folium's default OpenStreetMap tiles. Attribution is in the
rendered HTML. Choosing a tile provider deliberately is still open in
`PLAN.md`.

## Licences and terms of use — OPEN

**This is the one part of this document that is not yet done, and it is
deliberately not papered over.** No source's licence or terms of use has been
read. Every dataset above is published by a government agency on an open-data
portal, which is a reason to expect permissive terms, not evidence of them.

What is already settled is a separate question: what is *appropriate* to
publish, independent of what is *permitted*. That work is complete and written
up in `docs/excluded_categories.md`.

To close this, each source needs: its licence name, a link to the licence text,
whether attribution is required and in what form, and whether redistribution of
derived data is permitted. Socrata portals usually state terms per dataset;
`data.ny.gov` and `data.cityofnewyork.us` have site-wide terms as well.

## Gaps

- **San Francisco's boundary layer endpoint is not recorded anywhere.** The
  file (`sf_county_boundary.geojson`) is in the gitignored raw folder, so it
  cannot currently be re-fetched from scratch. Needs identifying and adding.
- Retrieval dates marked ≈ are inferred from commit history, not recorded at
  download time. Dates for cities added from now on are recorded exactly.
- Licences, as above.
