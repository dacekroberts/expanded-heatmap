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
| San Francisco | Socrata "Bay Area County Polygons" (`wamw-vt4s`) | `https://data.sfgov.org/resource/wamw-vt4s.geojson?$where=county='San Francisco'&$limit=10` | `San Francisco` |
| Los Angeles | LA County Planning, incorporated cities | `https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/admin_dist_SDE_DIST_DRP_CITY_COMM_BDY/FeatureServer/0/query` (`JURISDICTION='INCORPORATED CITY'`, `outSR=4326`, `f=geojson`) | `LOS ANGELES` |
| Chicago | Socrata "Boundaries - City" (`qqq8-j68g`) | `https://data.cityofchicago.org/resource/qqq8-j68g.geojson?$limit=10` | whole city |
| New York | Borough Boundaries (`gthc-hcne`) | `https://data.cityofnewyork.us/resource/gthc-hcne.geojson?$limit=10` | all five boroughs = the city |

Chicago note: the sibling asset `ewy2-6yfk` ("Boundaries - City - Map") has
null geometry; `qqq8-j68g` is the usable one.
New York note: `tqmj-j8zm`, the borough-boundary ID still in wide circulation,
now returns 404.
San Francisco note: `wamw-vt4s` is a **nine-county** Bay Area layer, so the
`county` filter is not optional — unfiltered it would scope the city to the
whole region. This endpoint was recovered on 2026-09-21 (it had been recorded
nowhere) by identifying the raw file from its own fields, `objectid` /
`fipsstco` / `county` with FIPS `06075`; the endpoint reproduces the file
byte-for-byte at 38,822 bytes with identical geometry, so it is the confirmed
original source and not a lookalike.

## Geocoding

| Service | Used by | Endpoint | Note |
|---|---|---|---|
| US Census Bureau bulk geocoder | Los Angeles, New York | `https://geocoding.geo.census.gov/geocoder/locations/addressbatch` | Free, no API key, US addresses only. Benchmark `Public_AR_Current`. Responses cached by batch content hash, so re-runs and drift checks stay offline and deterministic |

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

| **NYC DOHMH (`43nn-pn8j`), NYC DCWP (`w7w3-xahh`), NYC boroughs (`gthc-hcne`)** | **The absent licence field is required by law, not an oversight.** NYC's Open Data Technical Standards Manual states that Local Law 11 of 2012 "requires that data sets must be available **without registration requirement, license requirement, or usage restrictions**". The city therefore cannot attach a licence to these datasets. The "All Rights Reserved" notice in the nyc.gov footer covers nyc.gov's own website content, not datasets published under the Open Data Law. One condition does attach — see the notice below. |

### Still not established

| Source | Status |
|---|---|
| **US Census bulk geocoder** | Terms page not read. A US federal government work, used only to derive coordinates stored in this project's own outputs. Low priority, and the only item left unread.

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
| **MTA** (New York) | "Our data feeds are free to use." No API key needed for the static subway feed | Not specified for the GTFS data | Logos, maps and symbols need a separate licence application (free of charge but must be applied for) |

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
- **CTA**'s licence is granted for assisting riders or promoting public
  transport. **Decided: the project falls within that purpose.** It shows
  people in the city what businesses are near their station, which is
  rider-facing information about using the system, not merely an abstract
  analysis. It is also not sold, not advertising, and claims no affiliation —
  the clauses the purpose limitation sits beside.

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

This is the operative output of the licence review: three sources require
specific text, and one of the three is already satisfied. These are
obligations, not courtesies. They belong with the app work that surfaces this
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
6. **Display the required notices** (above) — the one thing that still blocks
   publishing, and part of the same app job as surfacing this page.
7. **Decide the tile provider deliberately**, given that OSM's tile service is
   explicitly best-effort with no SLA.
8. Optionally, read the Census geocoder's terms — the only source left unread.

**Where this leaves the project:** every source's position is now established
except the Census geocoder, and nothing found forbids what this project does.
What remains is not a permission question but an implementation one — four
notices to display before the site goes public.

## Gaps

- ~~San Francisco's boundary layer endpoint is not recorded anywhere.~~
  **Closed 2026-09-21:** identified as `wamw-vt4s` and confirmed byte-for-byte
  against the raw file. All five cities can now be rebuilt from scratch from
  this document alone.
- Retrieval dates marked ≈ are inferred from commit history, not recorded at
  download time. Dates for cities added from now on are recorded exactly.
- Licences, as above — the one substantive gap left.
