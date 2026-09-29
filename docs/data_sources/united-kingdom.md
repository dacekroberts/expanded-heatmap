# Data sources — United Kingdom

Part of [`data_sources.md`](../data_sources.md), the project's provenance
record, split by country. This file holds the United Kingdom rows of the tables
there. The numbered notices this project must display, the removal-request
commitment and the deploy gate are in the entry point, not here. London's brief
is [`build_briefs/london.md`](../build_briefs/london.md); the United Kingdom's
screen is its row in `docs/global_country_shortlist.md`, Tier 4.

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| London | **The Food Standards Agency's Food Hygiene Rating Scheme** (FSA, with the 33 London local authorities) — one bulk XML per authority, every food premises a borough inspects, with the FSA's own point where the premises is not a private address | **Food only**: Food service (Restaurant/Cafe/Canteen, Takeaway/sandwich shop, Pub/bar/nightclub) and food retail, shown as "Food shops" (Retailers - other, supermarkets), via `pipeline/taxonomies/fsa_businesstype.py`. **54,241 storefronts** built 2026-09-28 from 81,529 rows | The authority list `https://api.ratings.food.gov.uk/Authorities` (header `x-api-version: 2`), filtered to `RegionName == "London"` (33, asserted), then each authority's `FileName`, e.g. `https://ratings.food.gov.uk/OpenDataFiles/FHRS501en-GB.xml` (33 files, 80,367,855 bytes, keyless). Each file's `<ExtractDate>` is recorded in `outputs/london/provenance.json` (2026-09-09 to 2026-09-16). The list is cached: the API returned HTTP 500 the same evening | None server-side. Step 2 reads only FHRSID, name, type, postcode, authority and point - never the rating, scores or phone. 5,350 storefront rows (9.0%) have no FSA point and are not placed (26% in Richmond to 2% in Brent); a private address is never placed. 186 trading-as names show the trade name. Licence **OGL v3** with the FSA's conditions — notice **57** | 2026-09-28 |

## Transit feeds

| City | Agency / system | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| London | **OpenStreetMap route relations** for the Underground (11 lines, `network=London Underground`), the DLR (`network=Docklands Light Railway`, five route refs drawn as one line), the Elizabeth line and the six Overground lines (both `route=train`, selected by NAME: OSM tags most of them `network=National Rail`) | The Overpass mirrors in `pipeline/osm.py`: one bounded query for the relations with geometry (`config.OSM_ROUTES_QUERY`, 173 relations), one for their stop nodes (1,035), one for eight station nodes the relations omit (`config.STATION_ADDITIONS`) | 2026-09-28 | **TfL publishes no GTFS.** Its Unified API (`api.tfl.gov.uk`) lists the 19 lines' stops, but its line strings are station-to-station straight lines, so track is OSM's regardless; TfL's stop lists served only a scratch cross-check (nothing stored or published), and its terms' `licence-read` stalled on tfl.gov.uk's Cloudflare challenge and was stopped. Gate 3 exact on 14 counts (Wikipedia, secondary; the Overground against TfL's own stop lists). OSM, **ODbL 1.0** — notice 1 covers the rail data as well as the basemap |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| London | **OpenStreetMap relation 175342** (Greater London, admin_level 5), polygonised from its outer ways | The Overpass mirrors in `pipeline/osm.py`, `rel(175342);out geom;` | **Greater London - 1,595.5 km²** in UTM 30N, gated at 1,560-1,620. It is exactly the FSA's 33 "London" authorities. Scopes businesses (3 points outside) and stations (32 outside -> `outputs/london/excluded_stations.csv`). OpenStreetMap, ODbL 1.0 — notice 1 |
