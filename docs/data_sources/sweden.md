# Data sources — Sweden

Part of [`data_sources.md`](../data_sources.md), the project's provenance
record, split by country. This file holds the Sweden rows of the tables there.
The numbered notices this project must display, the removal-request commitment
and the deploy gate are in the entry point, not here. Stockholm's brief is
[`build_briefs/stockholm.md`](../build_briefs/stockholm.md).

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Stockholm | **Stockholms stad's food inspection register, *Livsmedelstillsyn*** (miljöförvaltningen, from Ecos 2), an ArcGIS FeatureServer layer. ⚠️ **ONE ROW PER INSPECTION, not per premises**: 289,742 rows for 8,146 premises (`ObjektId`). 🚨 **FROZEN**: inspections run 2018-01-02 to **2025-10-21**, the layer last edited 2025-10-22; built on as it stands (owner, 2026-09-28), and the page states the date | **Food only**, via `pipeline/taxonomies/sweden_livsmedel.py`: `VerksamhetsTyp` *Restaurang-, catering- och barverksamhet* -> Food service, *Detaljhandel* -> Food shops; the 19 other types (production, wholesale, transport, water, and the *Övrigt* catch-all, 185 premises of head offices and distributors by name) are excluded. Each premises is its LATEST record by `TillsynsDatum`, its types every type any record carries. Restaurant-typed institutional kitchens (preschools, schools, care homes, home care, day centres, staff canteens; 718) and pharmacies are left out by name (owner, 2026-09-29). The type arrived with the 2024 inspections; untyped premises last inspected in 2022-23 whose name the rules call a storefront (225; 220 once caterers and mobile units left, 2026-09-29) are added, flagged `name_classified` (owner, 2026-09-28); the rules are right 96.5% of the time on typed premises. **5,218 placed storefronts** (4,150 Food service, 1,068 Food shops; 215 from the name) since caterers, event firms, food trucks and prep kitchens were taken out by name on 2026-09-29 (built the same day with 5,262); 85 (1.6%) have no position and are not placed, most of the earlier 209 having been food trucks | `https://services-eu1.arcgis.com/81H0sgjoIWj6WxIM/arcgis/rest/services/Livsmedelstillsyn/FeatureServer/41` — `/query?where=1=1&outFields=*&orderByFields=OBJECTID&outSR=4326`, paged by 2,000 (the layer's `maxRecordCount`), keyless; 75.5 MB as CSV | none: every row and every field (owner, 2026-09-29). `fetch_sources.py` exits if the layer's field list changes or the rows fetched differ from the server's count. Step 2 never reads the inspection text (`Beskrivning`, `Anmarkning`, `Nr`, `Typ`, `Kontrollorsak`, `Kontrollomrade`). The served point equals the register's own SWEREF 99 18 00 position (EPSG:3011) to 0.0 m on all 5,218. No name column other than the premises' own (`AnlaggningsNamn`); no placed storefront's address carries a flat, floor or c/o marker. Licence **SILENT** — notice **66**, see below | 2026-09-29 |

### Stockholm's licence: SILENT, with the pages named

Resolved 2026-09-22 and recorded in the brief; the build re-read nothing new.

| Source | Says |
|---|---|
| `dataportal.se` (a HARVESTER) | `Åtkomsträttigheter: Begränsad` (restricted) |
| The ArcGIS item | `access: public`, serves without credentials, `licenseInfo` empty |
| The publisher's own Hub DCAT feed, `https://open-data-sthlm-miljo.hub.arcgis.com/api/feed/dcat-us/1.1.json` | `accessLevel: public` on all 109 datasets; `license` CC0 on 8, not this one |

A contradiction between a catalogue and its publisher is decided for the
publisher (`read-licence` step 5). The blank licence is a silence, not a
refusal, because the publisher demonstrably uses the licence field elsewhere.
`brief_check.py stockholm` re-reads the feed. The notice credits the publisher
and states the changes without claiming a licence (owner, 2026-09-29).

## Transit feeds

| City | Agency / system | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Stockholm | **OpenStreetMap route relations** for the Tunnelbana (`route=subway` in bbox 59.22,17.75,59.45,18.20): 14 relations, routes 10, 11, 13, 14, 17, 18, 19 in both directions, `colour` tagged as words (blue, red, green). SL's GTFS needs a Trafiklab key, so it is not used | The Overpass mirrors in `pipeline/osm.py`: the relations `out geom`, then their stop AND platform members `out center`, and the station node for Hallonbergen | 2026-09-29 | **Drawn as SL's three lines** (owner, 2026-09-29): Gröna linjen (T17-19), Röda linjen (T13-14), Blå linjen (T10-11), each labelled once with its routes in the legend. Left out: "Gul linje till Älvsjö" (21104772, no ref), under construction. ⚠️ **Mirrors disagree**: the first stops fetch came from a mirror older than the relations and lacked eleven stations' stop nodes; step 1 now stops if any member is missing. ⚠️ **Some stations are platform members only** (Tekniska högskolan). **Hallonbergen (route 11) is in no relation** and is added from its station node; it lies in Sundbyberg. **Gate 3 passes**: 100 stations against 100, and per route 10: 14, 11: 12, 13: 25, 14: 19, 19: 35 (English Wikipedia's table of lines, secondary, read 2026-09-29; 17 and 18 are left out of the per-route gate because OSM's relations run on to Hässelby strand). 82 inside the kommun, 18 outside -> `outputs/stockholm/excluded_stations.csv`; spacing median 745 m. Pendeltåg, Roslagsbanan, Saltsjöbanan and trams not drawn (owner, 2026-09-28). ODbL, notice 1 |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Stockholm | **OpenStreetMap relation 398021** (Stockholms kommun, admin_level 7), polygonised from its outer ways. 🚨 `name=Stockholm` at admin_level 7 matches NOTHING, and widening it finds two US "Stockholm Township" relations: the relation is pinned by id and its name asserted | The Overpass mirrors in `pipeline/osm.py`, `rel(398021);out geom;` | **Stockholms kommun - 215.8 km²** in UTM 34N (water included), gated at 210-222. Scopes businesses (none outside) and stations (18 outside). ODbL 1.0, notice 1 |
| Stockholm | **OpenStreetMap's admin_level 7 kommun relations** in the rail bbox (17), the NAMING layer, not the scoping one | The Overpass mirrors in `pipeline/osm.py`, `rel["boundary"="administrative"]["admin_level"="7"](59.22,17.75,59.45,18.20);out geom;` | Names the kommun of each excluded station (Solna, Sundbyberg, Danderyd, Huddinge, Botkyrka); step 1 exits if a station lies in none. ODbL 1.0, notice 1 |
