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

## Transit feeds

| City | Agency / system | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| Brussels | **STIB-MIVB**, its static GTFS on the Belgian Mobility Company's open-data portal (`data.belgianmobility.io`): metro 1, 2, 5 and 6 (`route_type` 1) and the trams that enter the City (4, 7, 8, 9, 10, 19, 25, 35, 51, 55, 62, 81, 82, 92, 93; `route_type` 0) | `https://api-management-discovery-production.azure-api.net/api/gtfs/feed/stibmivb/static` (19,837,741 bytes; feed version 2_21_20261002_143730, valid 2026-09-28 to 2026-10-25) | 2026-10-04 | **CC BY 4.0** under the portal's Terms of Use (`https://data.belgianmobility.io/en/terms.html`, December 2025, effective January 1, 2026; the portal `https://data.belgianmobility.io/`), STIB-MIVB the sole licensor: "Source: STIB-MIVB – Open Data – [date of dataset update]", the modified-data line, the portal named. Downloading is accepting those terms (accepted by the owner for this build; a change of terms is the owner's again). Nothing is taken from stib-mivb.be itself (its website terms are for private use): no logo, network map or brand material. Station names in French and Dutch from the feed's `translations.txt`. Notice 148 |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| Brussels | **"Limites administratives des communes en Région de Bruxelles-Capitale"** (PARADIGM, on opendata.brussels.be), the Region's 19 communes | `https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/limites-administratives-des-communes-en-region-de-bruxelles-capitale/exports/geojson` (dataset page `https://opendata.brussels.be/explore/dataset/limites-administratives-des-communes-en-region-de-bruxelles-capitale/`; retrieved 2026-10-04) | The City of Brussels (national code 21004), 33.1 km2: it scopes the stations and confirms every unit inside; the other 18 communes name the stations left out. **CC0 1.0**: nothing to display |
