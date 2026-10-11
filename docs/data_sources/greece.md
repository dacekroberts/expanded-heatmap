# Data sources — Greece

<!-- internal -->The Greece part of the project's provenance record,
[`data_sources.md`](../data_sources.md), split out by country. The numbered
notices this project must display, the removal-request commitment and the
deploy gate apply to every country and are kept in that record. Thessaloniki's
build brief is in the project's repository (`docs/build_briefs/thessaloniki.md`).<!-- /internal -->

## The country, in brief<!-- internal --> (the Thessaloniki build, 2026-10-07)<!-- /internal -->

Greece's first city is Thessaloniki, so these are the facts one build
established. They are not a screen of other Greek cities.

| Question | Answer for Greece | Evidence |
|---|---|---|
| Where commerce is recorded | **Municipally, by license.** The City of Thessaloniki publishes the shops holding an active license (food premises, hairdressers, beauty salons and the venues the same law licenses); no general-retail register was found | the layer's 79 activity values, read in full 2026-10-04 |
| Portal | The City's **GeoServer WFS** (`sdi.thessaloniki.gr`), harvested to data.gov.gr. The City's map portal (`maps.thessaloniki.gr`) carries a no-redistribution splash, read as the web app's own terms (owner, 2026-10-04): never read from it | the City's WFS and map portal, read 2026-10-04 |
| License | **CC BY 4.0**, set on the layer's data.gov.gr record | the record, read 2026-10-04 |
| Personal information | **No name field of any kind**; a point, an activity, a municipal community, a shop code and address fields, which the build never reads | DescribeFeatureType |
| Coordinates | **EPSG:2100** (GGRS87 / Greek Grid), reprojected on read; the build projects in UTM 34N (EPSG:32634) | step 2, 2026-10-07 |
| Rail | **The Thessaloniki Metro, from OpenStreetMap**; gate 3 from Elliniko Metro's station pages and the operator's (THEMA's) station list | step 1, 2026-10-07 |
| Boundaries | **OpenStreetMap's municipality relations** (admin_level 7) | the boundary fetch |

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Thessaloniki | City of Thessaloniki (Δήμος Θεσσαλονίκης), **Ενεργές Άδειες Καταστημάτων** (active shop licenses), GeoServer layer `saloniki:tsp_poi_energes_adeies_katastimaton`; EPSG:2100; a point, a licensed activity (79 values), a municipal community and a shop code per row - **no name field** | All three buckets, Food shops as food retail only, by `antikeimeno` (`pipeline/taxonomies/thessaloniki_adeies.py`, a closed list): **7,132 storefronts** (Food service 3,682, Food shops 2,430, Personal services 1,020) of 8,103 rows; 5 rows just outside the OSM boundary dropped | `https://sdi.thessaloniki.gr/geoserver/wfs?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=saloniki:tsp_poi_energes_adeies_katastimaton&OUTPUTFORMAT=application/json&SORTBY=gid` (one request, every row; never the copy on maps.thessaloniki.gr); the WFS endpoint `https://sdi.thessaloniki.gr/geoserver/wfs`; record `https://data.gov.gr/dataset/gis-thessaloniki-wms-saloniki-tsp_poi_energes_adeies_katastimaton` | none at download; step 2 keeps 7,137 of 8,103 by activity, 7,132 inside the municipality; address fields never read. License **CC BY 4.0** (`https://creativecommons.org/licenses/by/4.0/`) - notice 155 | 2026-10-04 |

### Thessaloniki's license: CC BY 4.0, read 2026-10-04

- **PERMITTED WITH CONDITIONS.** The layer's data.gov.gr record sets CC BY
  4.0 on each resource (a harvester default under the City's organization,
  matching the City portal's default and Decision 11654/2026, Art. 8(3)).
- **Not governing:** the map portal's splash ("in no case are modification
  and/or redistribution permitted"), read as the web app's own terms (owner,
  2026-10-04). The build reads the GeoServer WFS only.
- **MUST DISPLAY:** the credit, the dataset's title linked, the license
  linked, and that the data was changed (notice 155). **MUST NOT:** imply the
  City's endorsement; call the layer current, complete or official. The layer
  carries no date, so the page gives the retrieval date.

## Transit feeds

### Rail geometry that is not a GTFS feed

| City | System / operator | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Thessaloniki | **Thessaloniki Metro Line 1, from OpenStreetMap** - relations 6152448 and 7885077 (ref 1, `#ff0000`) and 7898293 and 7898294 (ref 2, the Kalamaria branch), operator THEMA; drawn as one line, Line 1 (the operator's name), cut at the city line | The Overpass mirrors in `pipeline/osm.py`, bbox `40.54,22.87,40.68,23.02`, one query with the station objects and the boundaries, `out geom` | 2026-10-07 | 36 stop positions -> 18 stations; **gate 3 exact** (18 on the line, 13 in the city) against Elliniko Metro's station pages and THEMA's station list; 13 in the municipality (573 m median, standard rings); the branch's 5 in Kalamaria not ringed (owner). Headways from THEMA's FAQ. OSM's color, 62.3 from Food service's pin. OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Thessaloniki | **OpenStreetMap relation 1770680** ("Δήμος Θεσσαλονίκης", admin_level 7), polygonised from its ways, with the other municipalities in the box (Kalamaria, relation 2348442, names the branch's outside stations) | The city's one Overpass query, administrative relations at admin_level 7 and 8 in the rail box | The municipality: **20.82 km²** (19.307 official), gated at 17.5-21.5; scopes stations (5 outside) and businesses (5 just outside dropped). ODbL 1.0, notice 1 |
