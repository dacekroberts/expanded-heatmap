# Data sources — Switzerland

The Switzerland part of the project's provenance record,
[`data_sources.md`](../data_sources.md), split out by country. The numbered
notices this project must display, the removal-request commitment and the
deploy gate apply to every country and are kept in that record. Zurich's
build brief is in the project's repository (`docs/build_briefs/zurich.md`).

## The country, in brief (`add-country`, 2026-09-30)

Switzerland's first city is Zurich, so these are the national facts one build
established, each with what it rests on. They are not a screen of other Swiss
cities: none has been probed.

| Question | Answer for Switzerland | Evidence |
|---|---|---|
| Where commerce is recorded | **Municipally, by trade.** The Stadt Zürich publishes its own register of the food-and-drink and alcohol-retail premises it licenses (Stadtpolizei, Fachgruppe Bewilligung Gastro). No general-retail or personal-services register was found for the city, and the national business statistics (STATENT) are aggregate | the register, read 2026-09-30; the Zurich catalogue sweep in the project's master-list evidence (`docs/city_master_list_evidence.md`; control `zzqqxxnonsense` -> 0, 2026-09-23) |
| Portal | **CKAN** at `data.stadt-zuerich.ch`. 🚨 **Its geodata download URLs return an Angular page, not data**: use the city's **WFS** (`ogd.stadt-zuerich.ch/wfs/geoportal/<Dataset>`), which serves GeoJSON with no key | the brief; re-checked 2026-09-30 |
| Licence | **CC0** on the Stadt's open data, "with few exceptions"; the city recommends "Quelle: Stadt Zürich" but does not require it | the dataset's CKAN record and the city's legal notice (below) |
| Personal information | **The register publishes the premises' trade name, never a holder column** (19 columns, none a person). Some trade names are a person's own name, so the project's name rule applies (Kansas City's and New Orleans's). The Swiss data-protection act itself was not read: the publisher's choice of columns did the first part of the work (`read-licence` step 6b) | the register's columns, 2026-09-30 |
| Home signal | **None in the register.** No home-based flag; the name rule is the only guard | the register's columns |
| Geocoder | **Not needed for Zurich**: every row carries its own LV95 point | 3,487 of 3,487 rows, 2026-09-30 |
| Coordinates | **CH1903+ / LV95, EPSG:2056, in metres** - the national grid, used as the build's projected CRS instead of a UTM zone (the tram-city skill). The WFS's GeoJSON also carries WGS84 points; the two agree to 0.07 m at most | step 2's control, 2026-09-30 |
| Classification | The register's own `betriebsart`, **single-valued**, 14 values (the publisher's documentation lists 11; three more appear in the data) | `pipeline/taxonomies/zurich_gastwirtschaft.py` |
| Encoding | UTF-8 GeoJSON; German names with umlauts read cleanly | the fetch |
| Rail | **Trams, from OpenStreetMap.** Zurich has no metro; VBZ's tram relations all carry a `colour`, and the Swiss national GTFS (`gtfs:feed` CH-Alle on the relations) was not needed and was not fetched or read | step 1, 2026-09-30 |
| Boundaries | **OpenStreetMap's Gemeinde relations** (admin_level 8), each tagged with its BFS number (`swisstopo:BFS_NUMMER`; source swissBOUNDARIES3D) | the boundary fetch |

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Zurich | **Stadt Zürich, `Gastwirtschaftsbetriebe`** (Stadtpolizei Zürich, Fachgruppe Bewilligung Gastro; Open Data Zürich, GIS-Zentrum), one row per licensed premises. The publisher: published rows are always `Offen` (open) - all 3,487 were, every one `jahr` 2026; last updated 28.09.2026, "laufende Nachführung" | Food service and **partial retail** (`pipeline/taxonomies/zurich_gastwirtschaft.py`): Food service 2,335 (Gastwirtschaft 2,099, Nebenwirtschaft 192, Kleinwirtschaft 30, Dancing / Disco 10, Take Away 3, Aussenliegende Saisonwirtschaft 1); **Licensed shops** 1,028 - the shops, kiosks and petrol stations licensed to sell alcohol (Kleinverkaufsstelle 954, Kiosk 53, Tankstelle 21), on the tobacco-retail precedent of Seoul and Gyeonggi (owner, 2026-09-30). Out by type (124): Ausgabestelle 56 (food stands, caterers, food trucks), Kantine / Mensa 31, Patentbefreit 25, Cabaret / Nachtclub 6, Veranstaltungsraum 6. **3,363 storefronts placed, all inside the Stadt**; 12 trade names that are a person's own name show the street address (`config.PERSON_NAMED`) | `https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Gastwirtschaftsbetriebe?SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&typeName=gastwirtschaftsbetriebe&outputFormat=application/vnd.geo+json` (layer name lower-case), keyless, 1.8 MB; dates and licence from `https://data.stadt-zuerich.ch/api/3/action/package_show?id=geo_gastwirtschaftsbetriebe` | none: every row and column. `fetch_sources.py` exits on a non-JSON answer (the CKAN page's Angular shell), on fewer than 3,000 rows, on a changed column list, or on a CKAN licence other than `cc-zero`. Step 2 exits on any row not `Offen` and places each row by its LV95 `ekoord`/`nkoord`. The opening hours (`oeffnungszeit`) are never shown. Licence **CC0**, no notice required - see below | 2026-09-30 |

⚠️ **The second CKAN hit is not a second source.** `sid_wipo_gastwirtschaftsbetriebe_od1111`,
"Historisierte Bestände der Gastwirtschaftsbetriebe", is the same register's
year-end counts since 2012 (one CSV, CC0, updated 19.02.2026). Not used.

### Zurich's licence: PERMITTED (CC0), read 2026-09-30

| Document | Says |
|---|---|
| The dataset's CKAN record (`package_show`) | `license_id` **cc-zero**, "Creative Commons CCZero" |
| The WFS capabilities | `Fees` None, `AccessConstraints` None |
| The portal's front page, `data.stadt-zuerich.ch` | "Die hier veröffentlichten Daten stehen kostenlos und zur freien – auch kommerziellen - Weiterverwendung zur Verfügung." |
| The city's legal notice, `stadt-zuerich.ch/de/service/rechtliche-hinweise.html` (dated 31 March 2026) | Written for the **website** (texts, images, logos), whose reuse needs consent, with **Open Government Data excepted**: datasets published on `data.stadt-zuerich.ch` are provided under the rules of the Reglement über offene Verwaltungsdaten (AS 170.410), and "Für bestimmte Datensätze bezeichnet die Stadt Zürich separate Nutzungsbedingungen, die eine uneingeschränkte Nutzung explizit erlauben." |
| The city's open-data guidance | CC0 on all but a few datasets; "Quelle: Stadt Zürich" **recommended**, not required |

Nothing is incorporated by reference that narrows the CC0 grant, and no act is
owed to the publisher. **No notice is required.** The page credits "Stadt
Zürich" in its data caption as the city asks. The Reglement's own text was not
read beyond the legal notice's summary of it.

## Transit feeds

### Rail geometry that is not a GTFS feed

| City | System / operator | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Zurich | **OpenStreetMap** - VBZ's trams: **36 `route=tram` relations kept, refs 2-11, 13-15, 17, 50 and 51**, every one coloured; and 8 relations judged and left out (`config.NOT_DRAWN`): tram 12 (1299849, 2799200; Glattalbahn, 1 of 18 stops in the Stadt, a stub, owner call 19), tram 20 (14987051, 14987052; Limmattalbahn, AVA, 4 of 26, a stub, call 25) and the Forchbahn S18 (`route=light_rail`: 2727252, 2727409, 20153407, 20153408; a suburban railway, call 18) | The Overpass mirrors in `pipeline/osm.py`, bbox `47.32,8.40,47.47,8.65`: tram and light-rail relations `out geom`, `node(r)` and every `railway=tram_stop` in the box | 2026-09-30 | On the shared `pipeline/osm_tram.py`: 417 stop positions -> **195 stations** by name (Waffenplatzstrasse's two directions 233 m apart under one stop code, so the collapse limit is 240 m) -> **180 in the Stadt**, 15 outside (trams 2, 4, 10 and 50, listed in `outputs/zurich/excluded_stations.csv`). No gate 3. **282 m median gap: the halved rings.** ⚠️ **Trams 50 and 51 are the 2026 timetable's construction lines** (VBZ, 14 Dec 2025 to 12 Dec 2026, Bahnhofquai/HB rebuilt): they replace the northern halves of 4, 11, 13 and 14, so the map must be rebuilt when the Bahnhofquai reopens. Colours: OSM's (VBZ's), with 9, 11, 15, 50 and 51 moved off a shared colour, 10 darkened off the Food service pins and 7's black drawn `#262626` (`config.LINE_COLOURS`). OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Zurich | **OpenStreetMap relation 1682248**, the Stadt Zürich (admin_level 8, BFS 261, source swissBOUNDARIES3D), polygonised from its outer ways - 91.9 km² in LV95, gated at 85-95 | The Overpass mirrors in `pipeline/osm.py`, `relation["boundary"="administrative"]["admin_level"="8"](47.32,8.40,47.47,8.65);out geom;` (54 Gemeinden) | The Stadt Zürich: scopes stations (15 outside) and businesses (none outside). ODbL 1.0, notice 1 |
| Zurich | **The other 53 Gemeinde relations** in the same answer, the NAMING layer | as above | Names the Gemeinde of each excluded station (Schlieren, Zollikon, Opfikon, Kloten, Rümlang); step 1 exits if a station lies in none. ODbL 1.0, notice 1 |
