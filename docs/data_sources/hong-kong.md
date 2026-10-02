# Data sources — Hong Kong

<!-- internal -->The Hong Kong part of the project's provenance record,
[`data_sources.md`](../data_sources.md), split out by country on 2026-09-27.
The numbered notices this project must display, the removal-request
commitment and the deploy gate apply to every country and are kept in
that record.<!-- /internal -->

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Hong Kong | **FEHD's license registers** (Food and Environmental Hygiene Department, via DATA.GOV.HK) - restaurants, other food premises and non-food premises, one XML each, regenerated daily with their own `GENERATION_DATE` and code lists; each license placed at **FEHD's own point** from the same registers on the **CSDI Portal**, joined by license number (the brief's ALS geocode was replaced, owner 2026-09-24) | Food service 17,254, food shops 3,846, bathhouses 35: **21,135** storefronts, each named by the shop sign on its license (no licensee name exists in the data); 28 licenses with no CSDI point yet left off | `https://www.fehd.gov.hk/english/licensing/license/text/LP_{Restaurants,OtherFood,NonFood}_EN.XML`; `https://portal.csdi.gov.hk/csdi-webpage/file-api?dataset_id=<id>&format=geojson&layer_name=FEHD_{RL,FL,TL}` (ids in `pipeline/hong_kong/config.py`) | none server-side; storefront license types kept in step 2 (35,830 licenses generated 2026-09-25; 17,266 / 16,519 / 2,032 CSDI points, latest record update 2026-09-23) | 2026-09-25 |

## Transit feeds

### Rail geometry that is not a GTFS feed

| City | System / operator | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Hong Kong | **OpenStreetMap** - MTR's Island, Tsuen Wan, Kwun Tong, Tseung Kwan O, South Island, Tung Chung, Tuen Ma and East Rail lines (relations matched on network `港鐵 MTR` and `ref`), and the Light Rail's twelve routes (network `輕鐵 Light Rail`) merged into ONE drawn line (owner) | every rail route relation in the SAR's bbox, via `https://overpass-api.de/api/interpreter`, `https://overpass.kumi.systems/api/interpreter` or `https://maps.mail.ru/osm/tools/overpass/api/interpreter` (tried in that order) | 2026-09-25 | **Why not the agency:** MTR's open data (`https://opendata.mtr.com.hk/data/` - `mtr_lines_and_stations.csv` and `light_rail_routes_and_stops.csv`, on DATA.GOV.HK, no license declared) is station LISTS with no coordinates and no geometry - read for gate 3 only, not published; and the Transport Department's GTFS (`static.data.gov.hk/td/pt-headway-en/gtfs.zip`) carries no MTR rail - its agency.txt holds buses, minibuses, ferries, the trams, the Peak Tram and MTR Bus. Gate 3 exact on all nine lines after two recorded corrections: Racecourse (race days only, absent from MTR's list) left out, and Light Rail stop 250 given MTR's current name Hoi Wong Road (OSM still Tuen Mun Swimming Pool). Airport Express and Disneyland Resort Line not drawn (owner). OpenStreetMap, ODbL 1.0 - notice 1 |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Hong Kong | **OpenStreetMap relation 913110** (`ISO3166-1`=HK, found by a bbox-bounded search), polygonised from outer ways and area-gated at its measured 2,759 km2 - the SAR's waters included, not its ~1,110 km2 of land | The Overpass mirrors in `pipeline/hong_kong/config.py` | The SAR; every drawn station falls inside it. OpenStreetMap, ODbL 1.0 - notice 1 |

## Geocoding

| Service | Used by | Endpoint | Note |
|---|---|---|---|
| Hong Kong Address Lookup Service (ALS) | Hong Kong - **a cross-check only, not published** | `https://www.als.gov.hk/lookup` | About 2,000 lookups of a planned 21,162 were made before the build switched to FEHD's own CSDI points (owner 2026-09-24); kept in `data/hong_kong/raw/als_cache.jsonl` as the record of the check that justified the switch (accepted ALS hits a median 12 m from FEHD's point, 89% within 50 m). Terms: DATA.GOV.HK's Terms of Use v1.2 by the service's own redirect<!-- internal --> (read 2026-09-24 by the license-read agent)<!-- /internal -->, with an unresolved reading under which no terms grant use at all - moot for an unpublished check, and the reason ALS is not a published source |
