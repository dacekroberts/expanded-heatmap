# Data sources — Belgium

<!-- internal -->The Belgium part of the project's provenance record,
[`data_sources.md`](../data_sources.md), opened 2026-10-04 with Belgium's
first cities. The numbered notices this project must display, the
removal-request commitment and the deploy gate apply to every country and are
kept in that record.<!-- /internal -->

Belgium has no single business register that maps shops the way this project
needs, so each region's cities use a different source: the City of Brussels a
street survey of its shops, Antwerp and Ghent the federal food-safety agency's
list of food businesses placed on Flanders' business-register points, Charleroi
and Liège Wallonia's survey of shops in their commercial districts, and the
other 18 communes of the Brussels-Capital Region the national business
register's company locations. Rail comes from each operator's own open data on
the Belgian Mobility Company's portal, under CC BY 4.0.

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| Brussels | **"Commerces recensés par hub.brussels situés sur le territoire de la Ville de Bruxelles"** (published by the City of Brussels, Ville de Bruxelles/Data Management, on opendata.brussels.be; source hub.brussels; listed contributors hub.brussels and Google Maps) - hub.brussels's field survey of the City's ground-floor commercial units, one survey dated **October 17, 2025**, every unit with a point, empty units included | All three categories: 6,880 units, every one inside the City of Brussels; 1,068 empty units and 743 units of types this map leaves out (hotels, offices, banks, repairs, gyms, cinemas and the like) removed; **5,069 storefronts: Food service 1,930, Retail 2,623, Personal services 516**. A unit with several types takes the highest of Food service, Retail and Personal services. The shop sign is the dot's name | `https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/commerces-recenses-par-hubbrussels-vbx/exports/json` (dataset page `https://opendata.brussels.be/explore/dataset/commerces-recenses-par-hubbrussels-vbx/`) | Fields named in the request (`select`): the Google Maps and Street View link columns are never downloaded, and nothing on the map links to Google. **License: CC BY 4.0** (the portal adopts the producer's license): credit, license link, a statement of changes, no endorsement implied; no City of Brussels logo or "BXL" mark (the portal's terms). Notice 144 | 2026-10-04 |
| Charleroi | **"Offre commerciale en Wallonie (LoGIC 2024)"** (Service public de Wallonie, with SEGEFA, ULiège) - a field survey of the region's shops, done in **August 2024** in Charleroi, each a point with its sign and one of four classes (retail, horeca, services, vacant). Complete inside the city's 18 commercial districts; outside them only shops over 200 m² of sales area | Two categories: 2,653 points in the City of Charleroi (INS 52011), all inside the commune; services (454) and vacant units (769) left out; **1,430 storefronts: Retail 980, Food service 450** (horeca, hotels included). The shop sign is the dot's name; 33 signs that read as a person's own name show the category instead | `https://geoservices.wallonie.be/geotraitement/spwdatadownload/results/5f56d784-2fd7-47eb-a62a-991d4741a67d/LOGIC_2024_GEOPACKAGE_3812.zip` (3,172,940 bytes, files dated 2025-04-09; catalogue record `https://metawal.wallonie.be/geonetwork/srv/api/records/5f56d784-2fd7-47eb-a62a-991d4741a67d`) | INS 52011 and the classes Commerce de détail and HoReCa, in step 2. Layer `LOGIC_2024__POINTS_VENTE`, EPSG:3812; the street and house number are never read. **License: CC BY 4.0**, the downloaded GeoPackage only (the map service's terms forbid altering what it serves, so it is not used): the SPW citation verbatim, the catalogue link, a statement of changes, no endorsement. Notice 147 | 2026-10-03 |
| Liège | **LoGIC 2024**, Charleroi's file, surveyed **July and August 2024** in Liège; complete inside the city's 20 commercial districts, only shops over 200 m² outside them | Two categories: 3,761 points in the City of Liège (INS 62063), all inside the commune; services (623) and vacant units (793) left out; **2,345 storefronts: Retail 1,477, Food service 868** (horeca, hotels included). 39 signs that read as a person's own name show the category instead | Charleroi's row | INS 62063, as Charleroi. Notice 147 | 2026-10-03 |

## Transit feeds

| City | Agency / system | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Brussels | **STIB-MIVB**, its static GTFS on the Belgian Mobility Company's open-data portal (`data.belgianmobility.io`): metro 1, 2, 5 and 6 (`route_type` 1) and the trams that enter the City (4, 7, 8, 9, 10, 19, 25, 35, 51, 55, 62, 81, 82, 92, 93; `route_type` 0) | `https://api-management-discovery-production.azure-api.net/api/gtfs/feed/stibmivb/static` (19,837,741 bytes; feed version 2_21_20261002_143730, valid 2026-09-28 to 2026-10-25) | 2026-10-04 | **CC BY 4.0** under the portal's Terms of Use (`https://data.belgianmobility.io/en/terms.html`, December 2025, effective January 1, 2026; the portal `https://data.belgianmobility.io/`), STIB-MIVB the sole licensor: "Source: STIB-MIVB – Open Data – [date of dataset update]", the modified-data line, the portal named. Downloading is accepting those terms (accepted by the owner for this build; a change of terms is the owner's again). Nothing is taken from stib-mivb.be itself (its website terms are for private use): no logo, network map or brand material. Station names in French and Dutch from the feed's `translations.txt`. Notice 148 |
| Charleroi | **LETEC**, its static GTFS on the Belgian Mobility Company's open-data portal: the light-metro lines M2, M3 and M4 (`route_type` 1); M1 runs as a bus in this timetable (`M1ab`, `route_type` 3) and is not drawn | `https://api-management-discovery-production.azure-api.net/api/gtfs/feed/tec/static` (84,926,285 bytes; feed version 20261002, valid 2026-10-02 to 2026-12-25) | 2026-10-04 | **CC BY 4.0** under the portal's Terms of Use (the operator's national-access-point entry says CC0; CC BY satisfies both): "Source: LETEC – Open Data – [date of dataset update]", the modified-data line, the portal named; no logo, and the operator credited as LETEC (owner). Stations collapsed on `parent_station`, Tirou's two parents merged (owner); 48 stations, 38 in the commune, M2 drawn to Anderlues (owner) with 10 outside. Colors this project's own: the feed gives the three lines one color (owner). One copy of the feed serves both cities. Notice 150 |
| Liège | **LETEC**, the same feed: tram T1 (`route_type` 0), Coronmeuse and Liège Expo to Standard | Charleroi's row | 2026-10-04 | As Charleroi. 23 stops, every one in the commune; Liège Expo's two parent stops merged (owner). The feed's own color. Stop count checked against the City of Liège's "Tram - Stations" (row below). Notice 150 |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Brussels | **"Limites administratives des communes en Région de Bruxelles-Capitale"** (PARADIGM, on opendata.brussels.be), the Region's 19 communes | `https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/limites-administratives-des-communes-en-region-de-bruxelles-capitale/exports/geojson` (dataset page `https://opendata.brussels.be/explore/dataset/limites-administratives-des-communes-en-region-de-bruxelles-capitale/`; retrieved 2026-10-04) | The City of Brussels (national code 21004), 33.1 km2: it scopes the stations and confirms every unit inside; the other 18 communes name the stations left out. **CC0 1.0**: nothing to display |
| Charleroi | **OpenStreetMap**, every municipality relation (`admin_level` 8, keyed on `ref:INS`) in the box 50.36,4.22,50.51,4.56: 22 communes | The Overpass mirrors in `pipeline/osm.py`, `out geom` (retrieved 2026-10-04) | The City of Charleroi (INS 52011), 102.8 km2: it scopes the stations and confirms every point inside; Anderlues and Fontaine-l'Évêque name M2's stations left out. OpenStreetMap, ODbL 1.0 - notice 1 |
| Liège | **OpenStreetMap**, as Charleroi, box 50.56,5.48,50.71,5.68: 18 communes | As Charleroi (retrieved 2026-10-04) | The City of Liège (INS 62063), 68.5 km2. OpenStreetMap, ODbL 1.0 - notice 1 |

## Other sources

| City | Source | Used for | Endpoint | Terms |
|---|---|---|---|---|
| Liège | **"Tram - Stations"** (Ville de Liège, opendata.liege.be), 23 stations, 2022 | Counting T1's stops against the feed's (each of the 23 within 87 m of one of the feed's 23 stops); read for the count, never shown | `https://opendata.liege.be/explore/dataset/tram-stations/` (retrieved 2026-10-04) | CC BY: nothing of it is published, so nothing to display |
