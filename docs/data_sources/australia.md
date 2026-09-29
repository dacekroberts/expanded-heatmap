# Data sources — Australia

Part of [`data_sources.md`](../data_sources.md), the project's provenance
record, split by country. This file holds the Australia rows of the tables
there. The numbered notices this project must display, the removal-request
commitment and the deploy gate are in the entry point, not here. Sydney's brief
is [`build_briefs/sydney.md`](../build_briefs/sydney.md); Melbourne's is
[`build_briefs/melbourne.md`](../build_briefs/melbourne.md).

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Sydney | **The City of Sydney's Floor Space and Employment Survey (FES), "Industry of occupation"** - one point per business establishment the City's surveyors counted, with an ANZSIC 2006 class, a survey every five years (2007, 2012, 2017, 2022 in one layer) | All three buckets via `pipeline/taxonomies/anzsic_fes.py`, an explicit list of ANZSIC classes (`ClassificationCode`). **No names or addresses**: the publisher strips them, so a pin is titled by its class. **7,328 storefronts** built 2026-09-28 from the 2022 survey's 21,618 establishments: Retail 3,095, Food service 3,256, Personal services 1,004 before the boundary cut | `https://services1.arcgis.com/cNVyNtjGVZybOQWZ/arcgis/rest/services/FES_Industry_of_occupation/FeatureServer/0`, `where=Year='2022'`, paged 2,000 at a time in WGS84 (`outSR=4326`), keyless; the count asserted against the survey's 21,618. Item `https://www.arcgis.com/sharing/rest/content/items/77ac8aa96bd34bacb881cfe8e5358ba0` (licence fields recorded in `outputs/sydney/provenance.json`; layer last edited 2025-02-12) | `Year='2022'` server-side. Excluded by class: religious services 144, interest-group associations 137, professional associations 89, parking 72, licensed members' clubs 27 (owner), brothels 27 (owner), labour associations 23, catering 21 (owner), non-store retail 14, funeral services 7 (owner), commission-based retail 1. 27 points outside OSM's LGA polygon dropped. Points stack per building: 5,218 distinct points, the largest 140. Licence **CC BY 4.0**, credit "City of Sydney" - notice **64** | 2026-09-28 |

## Transit feeds

| City | Agency / system | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Sydney | **OpenStreetMap route relations** for Sydney Trains (`route=train`, `network=Sydney Trains`: T1, T2, T3, T4, T8, T9, 20 relations) and Sydney Metro (`route=subway`, `network=Sydney Metro`: M1, 2 relations). Transport for NSW's GTFS needs an API key (a free account) and is not needed | The Overpass mirrors in `pipeline/osm.py`, bbox -33.925,151.170,-33.855,151.235 | 2026-09-28 | Each line's relations merged by London's branch rule and clipped to the LGA; drawn in each hue's nearest feasible colour (`line_colour_search.py`: closest pair within 500 m 19.2). Stations from every stop role, with OSM's three platform-suffix spellings normalised ("Central, Platform 16", "Campbelltown Platform 2", "Gadigal 1"): **16 inside the LGA**, gate 3 exact against the brief's list (OSM's station nodes inside relation 1251066); 157 outside listed in `outputs/sydney/excluded_stations.csv`. **Light rail L1-L3 left out (owner)**, disclosed with its effect. OpenStreetMap, ODbL 1.0 - notice 1 |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Sydney | **OpenStreetMap relation 1251066** (City of Sydney LGA, admin_level 6, Wikidata Q1094194), polygonised from its outer ways | The Overpass mirrors in `pipeline/osm.py`, `rel(1251066);out geom;` | **City of Sydney - 26.5 km²** in UTM 56S, gated at 24-29. Scopes businesses (27 survey points fall just outside OSM's polygon) and stations (157 outside). OpenStreetMap, ODbL 1.0 - notice 1 |
