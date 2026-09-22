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
| 8 | Boston | MBTA rapid transit: Red, Orange, Blue, Green (4 branches) and the Mattapan Trolley, drawn as 5 line groups (**57 in-city stations**; Regional Rail and ferries not included) | **Three** registries: ISD Food Establishment Inspections (CKAN `4582bec6`, 902,651 rows collapsed in SQL to ~2,900 active premises), Licensing Board `04dc653b` for package stores, Cannabis `e395fd88` | `boston_licensecat` (dispatches per source) | **Built 2026-09-21.** The second **two-bucket** city and the thinnest map here: 3,164 premises, 2,410 within a ring. **Personal services is absent, not thin** — Massachusetts licenses cosmetology at state level with no address-bearing export, verified three ways — and Retail is narrow (retail food, package stores, cannabis only), so this is food-and-drink density rather than commercial density, said plainly on the city page. Two station rules at once, as in Philadelphia: heavy rail keeps every in-city station, the Green Line's street-running branches are thinned. All sources **ODC-PDDL**, the cleanest licensing of any city here; MassDOT requires one acknowledgement notice, now active |
| 9 | Washington D.C. | WMATA Metrorail, 6 lines, 98 stations — **40 inside the District (40.8%)**, 32 in Virginia and 26 in Maryland; grade-separated throughout, so no thinning | Basic Business Licenses (`maps2.dcgis.dc.gov/.../FEEDS/DCRA/FeatureServer/0`): 278,747 rows, **76,107 Active**, 61,329 also in the District, 40 fields. `BUSINESSACTIVITY` (95 values in scope), `ENTITYTRADENAME`, `ENTITYNAME`, `ENTITYTYPE`, `PREMISEINDC`, `MAR_ID`, `SSL`, `X_COORDINATE`/`Y_COORDINATE` | `dc_businessactivity` (verified, all 95 values) | **Built 2026-09-21.** The **first non-NAICS registry here to cover all three buckets on its own** — no assembly, no `source` column, unlike New York's four sources and Boston's three. 5,230 premises, 3,860 within a ring (**73.8%, the highest ring coverage in the project**). Three Step 0 findings needed correcting on contact with the real data: the trade-name gap is **26.9% not 49%** on the rows that reach the map (the 49% was measured before excluding `General Business`), `MAR_ID` does **not** recover the missing coordinates (the same 452 rows lack both, so a geocoding step was needed after all), and the residual privacy exposure is **14 pins / 0.36%** rather than "the LA trap at half severity". `General Business` (11,074) and the five residential rental types (37,195) are excluded — 61% of the in-District register is somebody's home being let. Only feed in the project **behind an API key**, and the only one with a **ten-day validity window**, so `fetch_sources.py` re-checks `feed_end_date` on every run. WMATA requires **no notice**, so the mandatory count stays at five |
| - | Seattle | Sound Transit Link (1 Line + 2 Line) | "Seattle Business License" (ArcGIS `services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Seattle_Business_License/FeatureServer/0`, layer "Business Locations (Active)"): **54,604 rows**, point geometry, `BUSLIC_NAICS_CODE` + `BUSLIC_NAICS_DESC`, `BUSLIC_SIC_CODE` + `BUSLIC_SIC_DESC`, `BUSLIC_TRADE_NAME`, `BUSLIC_LEGAL_NAME`, `BUSLIC_LOCATION_ADRS_TEXT` | `naics` (already built) | **DEFERRED by the owner 2026-09-21 — to be implemented later, not excluded.** Findings kept so returning to it costs nothing. On the evidence it is the **best-equipped candidate found**: an official nightly export from Finance & Administrative Services that is **active-only by construction**, carries real NAICS (so no new taxonomy module), a trade name, and point geometry — no geocoding step. Not on Socrata, which is why earlier screens missed it; it lives on ArcGIS under owner `SeattleData`. Still to do: the category distribution, the in-city check, `BUSLIC_LOCATION_TYPE` (values include "HEADER QUARTER" — headquarters vs branch needs a verdict), and the licence, whose `licenseInfo` is an as-is accuracy disclaimer rather than a grant. Privacy flags: `BUSLIC_CONTACT_NAME` is a person and `BUSLIC_PHONE_NUM` a phone number — both must stay unpublished (`drop_contact_details()` already covers the phone). Note this project's original prototype was Seattle's Link light rail |
| 7 | Miami | **Metrorail + both Metromover loops, 42 stations across SIX municipalities** (23 Metrorail, 19 Metromover; MIA Airport People Mover and Tri-Rail not drawn) | Miami-Dade County Local Business Tax (ArcGIS `Local_Business_Tax_Feature_Layer_View`): 194,099 rows all `YEAR`=2026, 175,982 Active, `CATGRYNAME` (150 values), `LAT`/`LON`, `FOLIO`, `MUNBUSLOC` | `miami_catgryname` (verified, all 150 values) | **Built 2026-09-21.** The project's first **REGIONAL** city and the first proof of the multi-jurisdiction idea: Metrorail leaves the City of Miami, and the county licenses all 34 of its municipalities in ONE file with one schema and one publisher, so full-line coverage needed no extra sources, no cross-source dedup and no second licence review. **Its `BUSNAICSCD` is NULL on all 194,099 rows**, so NAICS was unusable despite being in the schema. Best coordinate quality in the project (100% present, zero placeholders) and the only registry whose trade name is never blank. First city to need a PREMISES dedup: `RECEIPTNO` is per row, `ACCOUNTNO` per account and `FOLIO` per *parcel*, so 1,944 premises holding several category licences collapse on name-plus-address |
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

## Canada - live-verified 2026-09-21 (rail first, then business data)

Screened in the order that kills candidates cheapest: urban rail, then
business data. `routes.txt` was read from each agency's live GTFS via the
Mobility Database catalogue, counting route_type 0/1/5/7/12 and **excluding 2
(commuter rail)**, as every built city does.

**Viable - five cities:**

| City | Rail | Business data | Cost to build |
|---|---|---|---|
| **Montreal** | Metro, 4 lines | `locaux-commerciaux`: 28,621 surveyed premises, 100% coords, `SCIAN` (NAICS) 99.6%, trade name 100%, vacancy flag. CC-BY 4.0 | Lowest - may need **no new taxonomy module**, since SCIAN 72/44+45/81 are the prefixes `naics.py` already uses |
| **Vancouver - BUILT 2026-09-21, regionally with Surrey** | SkyTrain, 3 lines | `business-licences`: 205,943 rows, `geo_point_2d`, `businesstype`/`businesssubtype`, legal + trade name. OGL-Vancouver | Low - needs a local taxonomy module |
| **Calgary - BUILT 2026-09-21** | CTrain, 2 lines | `vdjc-pybd`: `point`, `tradename`, `licencetypes`, `jobstatusdesc`, and **`homeoccind`** - a home-occupation flag handed over directly, as Chicago's `business_activity` is | Low |
| **Edmonton - BUILT 2026-09-21** | LRT, 3 lines | `qhi4-bdpu`: `latitude`/`longitude`, `business_licence_category`, `business_name` | Low |
| **Toronto - BUILT 2026-09-21** | 17 rail routes | 159,872 rows, `Category`, `Operating Name` - but **no coordinates at all** | **Highest.** Needs a geocoding pass like D.C.; licence field reads "not specified" so the terms must be read; and `Client Name` is a person or company, so LA's privacy discipline applies from the start |

**CORRECTED 2026-09-21 - an earlier version of this section said Toronto
"codes its subway as `route_type 0`, not 1". That is false**, and the cause
matters more than the error: the Mobility Database mirror of the TTC feed was
**three months expired** (`feed_end_date 20260606`) and contained **no subway
at all** - 209 bus, 17 tram, 2 ferry, zero `route_type 1`, with the only
subway-named entries being shuttle *buses*. The agency's own feed (Toronto CKAN
`ttc-routes-and-schedules`) has **3 subway lines as `route_type 1`** - Line 1
Yonge-University, Line 2 Bloor-Danforth, Line 4 Sheppard - plus **Line 5
Eglinton and Line 6 Finch West** LRT among 20 type-0 routes. Separating rail
from streetcar is trivial, not the San Francisco problem described here.
`scripts/screen_rail.py` now flags stale feeds.

**Toronto was also measured after geocoding, and it is the WEAKEST of the six,
not the strongest.** 37,563 active licences (23.5% of 159,872), of which 71.4%
geocode against the City's own address repository. Across 234 stations that is
**41 storefront sites per station - Boston's 39**, because **Toronto is a
two-bucket city**: within a ring, Food service 7,249, Personal services 1,973,
**Retail 357**. The city licenses food, personal services and specific trades,
not general retail; its largest categories are Taxicab Owner, Public Garage and
Building Renovator. `bodysafe` and `dinesafe` do not help - they are inspection
programmes over the same premises, not a retail source. Full measurements and
every endpoint are in `docs/canada_step0_endpoints.md`.

**Ruled out on data:** Ottawa has 6 LRT routes but **no general business
register** - 697 catalogue entries scanned on a wide net, and the only
address-level commercial data is food-safety inspections.

**Ruled out on rail (live-verified, bus-only in their own `routes.txt`):**
Winnipeg, Hamilton, Quebec City (tramway under construction), Halifax
(bus + 2 ferries), Mississauga, Brampton.

### Brampton - blocked on rail, NOT on data. Revisit ~mid-2027.

Do not re-screen Brampton's data; it was checked on 2026-09-21 and is
**better than most US cities in this project**: 6,059 businesses, **X/Y on
100%**, **`NAICS_DETAIL` on 97.3%** with 614 distinct six-digit codes already
split into `NAIC_2/3/4/6`, an `OPERATIONAL` flag, employee bands and gross
floor area - and described as "an employer census of all brick and mortar
businesses", so a census rather than a sample.

The only blocker is that **no urban rail reaches it**. The Miami regional
precedent does *not* apply: Metrorail physically extends into Hialeah and
Coral Gables, whereas TTC Line 2 terminates at Kipling inside Toronto, and the
only rail serving Brampton is GO commuter rail, which this project excludes
everywhere.

That changes when the **Hurontario LRT (Hazel McCallion Line)** opens.
Per the project owner 2026-09-21, from a web search and **not independently
verified here**: repeated delays put civil infrastructure completion at
2027-2028, with passenger service following testing and commissioning.

**Revisit trigger: mid-2027, and the question is "has an opening date been
announced?", not "is it open?"** - an announced date is actionable months
ahead, whereas checking for service in mid-2027 would likely just return
"still building". If it opens, both Brampton *and* Mississauga come into
scope together, since the line runs between them - though Mississauga needs a
different source than Brampton: its Business Directory lists **only businesses
that agreed to be included** (opt-in, so it would map who filled in a form,
not where commerce is - the Boston survey problem in a purer form), and its
Licensed Eateries set is food-only, 2,225 rows, with no coordinates.

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
