# Data sources — Switzerland

<!-- internal -->The Switzerland part of the project's provenance record,
[`data_sources.md`](../data_sources.md), split out by country. The numbered
notices this project must display, the removal-request commitment and the
deploy gate apply to every country and are kept in that record. Zurich's
build brief is in the project's repository (`docs/build_briefs/zurich.md`).<!-- /internal -->

## The country, in brief<!-- internal --> (`add-country`, 2026-09-30)<!-- /internal -->

Switzerland's first city is Zurich, so these are the national facts one build
established, each with what it rests on. They are not a screen of other Swiss
cities: none has been probed.

| Question | Answer for Switzerland | Evidence |
|---|---|---|
| Where commerce is recorded | **Municipally, by trade.** The Stadt Zürich publishes its own register of the food-and-drink and alcohol-retail premises it licenses (Stadtpolizei, Fachgruppe Bewilligung Gastro). No general-retail or personal-services register was found for the city, and the national business statistics (STATENT) are aggregate | the register, read 2026-09-30; the Zurich catalog sweep<!-- internal --> in the project's master-list evidence<!-- /internal --> (<!-- internal -->`docs/city_master_list_evidence.md`; <!-- /internal -->control `zzqqxxnonsense` -> 0, 2026-09-23) |
| Portal | **CKAN** at `data.stadt-zuerich.ch`. 🚨 **Its geodata download URLs return an Angular page, not data**: use the city's **WFS** (`ogd.stadt-zuerich.ch/wfs/geoportal/<Dataset>`), which serves GeoJSON with no key | <!-- internal -->the brief; <!-- /internal -->re-checked 2026-09-30 |
| License | **CC0** on the Stadt's open data, "with few exceptions"; the city recommends "Quelle: Stadt Zürich" but does not require it | the dataset's CKAN record and the city's legal notice (below) |
| Personal information | **The register publishes the premises' trade name, never a holder column** (19 columns, none a person). Some trade names are a person's own name, so the project's name rule applies (Kansas City's and New Orleans's). The Swiss data-protection act itself was not read: the publisher's choice of columns did the first part of the work | the register's columns, 2026-09-30 |
| Home signal | **None in the register.** No home-based flag; the name rule is the only guard | the register's columns |
| Geocoder | **Not needed for Zurich**: every row carries its own LV95 point | 3,487 of 3,487 rows, 2026-09-30 |
| Coordinates | **CH1903+ / LV95, EPSG:2056, in meters** - the national grid, used as the build's projected CRS instead of a UTM zone<!-- internal --> (the tram-city skill)<!-- /internal -->. The WFS's GeoJSON also carries WGS84 points; the two agree to 0.07 m at most | step 2's control, 2026-09-30 |
| Classification | The register's own `betriebsart`, **single-valued**, 14 values (the publisher's documentation lists 11; three more appear in the data) | `pipeline/taxonomies/zurich_gastwirtschaft.py` |
| Encoding | UTF-8 GeoJSON; German names with umlauts read cleanly | the fetch |
| Rail | **Trams, from OpenStreetMap.** Zurich has no metro; VBZ's tram relations all carry a `colour`, and the Swiss national GTFS (`gtfs:feed` CH-Alle on the relations) was not needed and was not fetched or read | step 1, 2026-09-30 |
| Boundaries | **OpenStreetMap's Gemeinde relations** (admin_level 8), each tagged with its BFS number (`swisstopo:BFS_NUMMER`; source swissBOUNDARIES3D) | the boundary fetch |

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Zurich | **Stadt Zürich, `Gastwirtschaftsbetriebe`** (Stadtpolizei Zürich, Fachgruppe Bewilligung Gastro; Open Data Zürich, GIS-Zentrum), one row per licensed premises. The publisher: published rows are always `Offen` (open) - all 3,487 were, every one `jahr` 2026; last updated 28.09.2026, "laufende Nachführung" | Food service and **partial retail** (`pipeline/taxonomies/zurich_gastwirtschaft.py`): Food service 2,335 (Gastwirtschaft 2,099, Nebenwirtschaft 192, Kleinwirtschaft 30, Dancing / Disco 10, Take Away 3, Aussenliegende Saisonwirtschaft 1); **Licensed shops** 1,028 - the shops, kiosks and petrol stations licensed to sell alcohol (Kleinverkaufsstelle 954, Kiosk 53, Tankstelle 21), on the tobacco-retail precedent of Seoul and Gyeonggi (owner, 2026-09-30). Out by type (124): Ausgabestelle 56 (food stands, caterers, food trucks), Kantine / Mensa 31, Patentbefreit 25, Cabaret / Nachtclub 6, Veranstaltungsraum 6. **3,363 storefronts placed, all inside the Stadt**; 12 trade names that are a person's own name show the street address (`config.PERSON_NAMED`) | `https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Gastwirtschaftsbetriebe?SERVICE=WFS&VERSION=1.1.0&REQUEST=GetFeature&typeName=gastwirtschaftsbetriebe&outputFormat=application/vnd.geo+json` (layer name lower-case), keyless, 1.8 MB; dates and license from `https://data.stadt-zuerich.ch/api/3/action/package_show?id=geo_gastwirtschaftsbetriebe` | none: every row and column. `fetch_sources.py` exits on a non-JSON answer (the CKAN page's Angular shell), on fewer than 3,000 rows, on a changed column list, or on a CKAN license other than `cc-zero`. Step 2 exits on any row not `Offen` and places each row by its LV95 `ekoord`/`nkoord`. The opening hours (`oeffnungszeit`) are never shown. License **CC0**, no notice required - see below | 2026-09-30 |
| Geneva (Regional) | **Répertoire des entreprises du canton de Genève (REG)**, SITG dataset `REG_ENTREPRISE_ETABLISSEMENT` (contributor: Département de l'économie et de l'emploi, OCIRT), the canton's register of active businesses: 100,588 rows (63,224 companies, 37,364 establishments), every one `En activité` and placed on its LV95 `E`/`N`, NOGA 2008 at six digits on every row. Daily; the build uses the zip created 04.10.2026 (extracted from SITG's geodatabase the Friday evening before) | All three buckets (`pipeline/taxonomies/geneva_noga.py`, a closed list keyed on the code): **establishment rows only**, home-based, itinerant and market-stand premises dropped (5,828 canton-wide), then the closed list, then the 12 tram communes by OSM polygon (the register's `PHYS_COMMUNE` agrees on every row): **5,863 storefronts** (Food service 1,862, Retail 2,897, Personal services 1,104). Left out and disclosed (owner, 2026-10-04): 1,847 company rows in the 12 communes with a storefront code and no establishment row (no premises type). 1,311 trade names withheld, the street address shown: 1,130 sole traders' names that are the owner's own, 144 person-shaped names of unknown legal form, and 37 person-shaped names of firms in office-typed premises (owner, 2026-10-07) | `https://ge.ch/sitg/geodata/SITG/OPENDATA/REG_ENTREPRISE_ETABLISSEMENT-CSV.zip` (dataset page `https://sitg.ge.ch/donnees/reg-entreprise-etablissement`), keyless, 11,344,581 bytes; UTF-8 with BOM, `;` | none at download. `fetch_sources.py` keeps the dated zip and stops on a sha256 that differs from its record; step 2 reads 17 columns by name and never writes the phone, fax, e-mail or legal-name columns (the legal name is read in memory only, for the name rule). License **SITG Level A**, conditions linked from `https://sitg.ge.ch/ressources/conditions-utilisation-donnees` - notice 154 | 2026-10-04 |

⚠️ **The second CKAN hit is not a second source.** `sid_wipo_gastwirtschaftsbetriebe_od1111`,
"Historisierte Bestände der Gastwirtschaftsbetriebe", is the same register's
year-end counts since 2012 (one CSV, CC0, updated 19.02.2026). Not used.

### Zurich's license: permitted (CC0), read 2026-09-30

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

### Geneva's license: permitted with conditions (SITG Level A), read 2026-10-04

The canton's REG is a **Level A, "Accès libre"** dataset under SITG's
*Conditions d'utilisation des données du Portail SITG* (version of 19 May
2026; the copy inside the zip is byte-identical): reproduce, publish, adapt
and combine, commercial use included. What it asks, and where this project
does it:

| Condition | Done by |
|---|---|
| CU 5.3.1: the source "de manière clairement visible", at least as "Source : Portail des données SITG (État de Genève), téléchargé et/ou extrait en date du […]." | Notice 154, with the zip's date, 04.10.2026 |
| CU 5.3.2: a derived use stated with its source, on the example "… cartographie … réalisé sur la base de Données du Portail SITG, imprimé et/ou extrait en date du […]." | Notice 154 |
| CU 5.4.2: no re-identification of personal data | REG is never joined to another source; the legal name is read only to withhold a sole trader's own name |
| CU 5.5: third parties told the conditions apply | Notice 154 links the conditions |
| CU 7.2: a narrow indemnity (third-party claims from the user's own infringements) | Accepted by the owner, 2026-10-04 (`docs/data_sources.md`, "Geneva's SITG indemnity") |
| ge.ch's website terms, applied by SITG's footer to its subdomains | Read by the owner as the website's only, not the dataset's (2026-10-04) |

## Transit feeds

### Rail geometry that is not a GTFS feed

| City | System / operator | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Zurich | **OpenStreetMap** - VBZ's trams: **36 `route=tram` relations kept, refs 2-11, 13-15, 17, 50 and 51**, every one colored; and 8 relations judged and left out (`config.NOT_DRAWN`): tram 12 (1299849, 2799200; Glattalbahn, 1 of 18 stops in the Stadt, a stub, owner call 19), tram 20 (14987051, 14987052; Limmattalbahn, AVA, 4 of 26, a stub, call 25) and the Forchbahn S18 (`route=light_rail`: 2727252, 2727409, 20153407, 20153408; a suburban railway, call 18) | The Overpass mirrors in `pipeline/osm.py`, bbox `47.32,8.40,47.47,8.65`: tram and light-rail relations `out geom`, `node(r)` and every `railway=tram_stop` in the box | 2026-09-30 | On the shared `pipeline/osm_tram.py`: 417 stop positions -> **195 stations** by name (Waffenplatzstrasse's two directions 233 m apart under one stop code, so the collapse limit is 240 m) -> **180 in the Stadt**, 15 outside (trams 2, 4, 10 and 50, listed on the city's page). No gate 3. **282 m median gap: the halved rings.** ⚠️ **Trams 50 and 51 are the 2026 timetable's construction lines** (VBZ, 14 Dec 2025 to 12 Dec 2026, Bahnhofquai/HB rebuilt): they replace the northern halves of 4, 11, 13 and 14, so the map must be rebuilt when the Bahnhofquai reopens. Colors: OSM's (VBZ's), with 9, 11, 15, 50 and 51 moved off a shared color, 10 darkened off the Food service pins and 7's black drawn `#262626` (`config.LINE_COLOURS`). OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |
| Geneva (Regional) | **OpenStreetMap** - TPG's trams: **10 `route=tram` relations kept, refs 12, 14, 15, 17 and 18**, two each, every one colored with TPG's color; nothing judged and left out | The Overpass mirrors in `pipeline/osm.py`, bbox `46.15,6.03,46.25,6.26`, ONE query: tram and light-rail relations `out geom`, `node(r)` and every `railway=tram_stop` in the box, and the admin_level 8 communes | 2026-10-07 | On the shared `pipeline/osm_tram.py`: OSM names many stop positions with TPG's platform letter ("Bel-Air (A)"), which step 1 strips for 14 named stops before the collapse: 181 stop positions -> **85 stops**, **gate 3 exact on every line** against TPG's own line pages (12: 25, 14: 30, 15: 22, 17: 26, 18: 31) -> **81 in the 12 communes**, 4 of tram 17's in France (Gaillard 2, Ambilly, Annemasse; listed on the city's page). **330 m median gap: the halved rings.** OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Zurich | **OpenStreetMap relation 1682248**, the Stadt Zürich (admin_level 8, BFS 261, source swissBOUNDARIES3D), polygonised from its outer ways - 91.9 km² in LV95, gated at 85-95 | The Overpass mirrors in `pipeline/osm.py`, `relation["boundary"="administrative"]["admin_level"="8"](47.32,8.40,47.47,8.65);out geom;` (54 Gemeinden) | The Stadt Zürich: scopes stations (15 outside) and businesses (none outside). ODbL 1.0, notice 1 |
| Zurich | **The other 53 Gemeinde relations** in the same answer, the NAMING layer | as above | Names the Gemeinde of each excluded station (Schlieren, Zollikon, Opfikon, Kloten, Rümlang); step 1 exits if a station lies in none. ODbL 1.0, notice 1 |
| Geneva (Regional) | **The 12 Swiss commune relations the trams serve** (admin_level 8, keyed on `swisstopo:BFS_NUMMER`): Genève 6621, Lancy 6628, Meyrin 6630, Carouge 6608, Bernex 6607, Vernier 6643, Plan-les-Ouates 6633, Chêne-Bougeries 6612, Chêne-Bourg 6613, Thônex 6640, Onex 6631, Confignon 6618, polygonised from their outer ways - 77.0 km² in LV95, gated at 74-80 | The Overpass mirrors in `pipeline/osm.py`, the city's one query (50 communes in the box) | The 12 communes: scope stations (4 outside) and businesses (the register's `PHYS_COMMUNE` agrees on every row). ODbL 1.0, notice 1 |
| Geneva (Regional) | **The other 38 commune relations** in the same answer, Swiss by BFS number and French by `ref:INSEE`, the NAMING layer | as above | Names the commune of each excluded stop (Gaillard, Ambilly, Annemasse); step 1 exits if a stop lies in none. ODbL 1.0, notice 1 |
