"""Taichung-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/taichung.md,
and the national argument is in taipei.md and pipeline/countries/taiwan.py.

Business leg: the national business tax register (FIA, daily), the rows whose
address is in Taichung, placed by a JOIN to Taichung's own door-plate file -
the only Taiwanese door-plate file that carries WGS84 as well as TWD97.

Rail: the Taichung Metro Green Line - its stations from the operator's own
table (coordinates, Chinese and English names), its route from OpenStreetMap,
because the operator's table has no geometry (ODbL, the Toulouse/Rennes
precedent). TDX is not used (key-gated; taipei.md).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "taichung" / "raw"
DATA_PROCESSED = ROOT / "data" / "taichung" / "processed"
OUTPUTS = ROOT / "outputs" / "taichung"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

PORTAL = "https://newdatacenter.taichung.gov.tw/api/v1/no-auth/resource.download?rid="
# The door-plate INDEX: one row per monthly file, each a Google Drive link.
# Read it for the newest month; never pin one file id (the brief).
DOORPLATE_INDEX_RID = "03d9c01c-4a7c-4bd8-ae88-12ed011391b3"
DOORPLATE_INDEX_CSV = DATA_RAW / "doorplate_index.csv"
DOORPLATE_CSV = DATA_RAW / "taichung_doorplate.csv"
# Taichung Metro's own Green Line station table (data.gov.tw 144164).
STATIONS_RID = "f9511cc5-4799-4df9-98b7-0b0f89fc2be9"
STATIONS_RAW_CSV = DATA_RAW / "green_line_stations.csv"

# The door-plate file's columns (read 2026-09-23 by the screen).
PLATE_COLS = {"street": "街、路段", "lane": "巷", "alley": "弄", "num": "號",
              "lon": "WGS84經度", "lat": "WGS84緯度"}
# The district, as a CODE (the register names it); step 2 learns code -> name.
PLATE_DISTRICT_COL = "鄉鎮市區代碼"
# The register's address prefixes for Taichung, including the pre-2010
# county's (checked absent 2026-09-23, cheap to keep).
ADDRESS_PREFIXES = ("臺中市", "台中市", "臺中縣", "台中縣")

OVERPASS_URLS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
)
# Every name search bounded (osm-rail): the whole special municipality.
OSM_BBOX = (23.99, 120.46, 24.45, 121.46)       # S, W, N, E
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
# No boundary polygon: the whole line is in the city, and the check is the
# operator's own station addresses (every one must start with the city's name).
# Overpass 504ed on the boundary from all three mirrors on 2026-09-25, and the
# build does not need it - the register is scoped by address prefix.

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 51N: the longitude (~120.67) falls in the 120 to 126 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32651"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# One line, the Green Line, Beitun Main Station to HSR Taichung Station, all
# inside the city; every station kept (owner 2026-09-25: a full page).
LINE_KEY = "G"
LINE_NAME = "Green Line"
# The line's two OSM relations (one per direction, 18 stops each) are named
# 臺中捷運綠線…方向; matched on that name within route=subway.
LINE_MATCH = "臺中捷運綠線"
# Neither the operator's table nor OSM carries a colour (2026-09-25), and the
# licence read found none on the dataset pages. A green of this project's own,
# Delta-E 31 from the Personal services pins (owner 2026-09-25, Riga's
# precedent: the project palette); the page says so.
LINE_COLOUR = "#3B7D23"

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "taiwan_fia"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "industry"

# The head-office rule (owner 2026-09-25, as measured on Taipei): a COMPANY
# head-office or single-site row on the 3rd floor or higher, or with a room
# number (室), looks like an office - dropped, unless its address holds this
# many storefront rows or more (a market or a mall).
OFFICE_FLOOR_MIN = 3
OFFICE_EXEMPT_ROWS_AT_ADDRESS = 20

# Sanity bounds for the joined points.
CITY_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602921154)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("zh",)
PLACE_FOLD = None
PLACE_REVIEWED = {}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "way/584486672": "an estate courtyard tagged a park, English description for a name",
    "way/447947694": "an estate garden tagged a park, stray characters glued on the name",
    "way/596748585": "an estate courtyard tagged a park",
    "node/12608938544": "an estate's name stone tagged a monument",
    "way/873107595": "a religious order's residence with no article",
    "way/255784429": "a seminary with no article, a bare type word for a name",
    "node/9467644899": "a religious residence with no article",
    "way/315710452": "a religious residence with no article",
    "node/2771942345": "a religious residence with no article",
    "node/3993477568": "a religious residence with no article",
    "way/235082930": "a religious residence with no article",
    "way/1177121867": "a religious residence with no article",
    "way/1064302069": "a religious residence with no article",
    "node/13529262392": "a private family graveyard hall with no article",
    "node/8012733550": "a fortune-telling shop tagged a place of worship",
    "node/13307324001": "a temple-supplies shop tagged a place of worship",
    "node/6275626560": "a club's name sign tagged a monument",
    "way/652853354": "a theme park's ride; the article and wikidata are the park's",
    "way/1202342705": "a land-management contract and its dates standing in for a name",
    "way/1111663477": "a description standing in for a name",
    "node/13812682720": "a description standing in for a name",
    "way/472434989": "a description standing in for a name",
    "way/677269927": "a school's tennis court tagged a park",
    "way/1051186692": "a school's sports ground tagged a park",
    "way/313817354": "a school's practice field tagged a park",
    "way/1177185588": "a croquet court tagged a park",
    "way/316490599": "a description of an abandoned building standing in for a name",
    "node/11622474587": "a description of an abandoned farmhouse standing in for a name",
    "node/7913261874": "a description of an abandoned lookout standing in for a name",
    "way/355264470": "museum contents, a description for a name",
    "way/355264472": "museum contents, a description for a name",
    "node/4560301918": "a display train car with no wikidata, misspelled name",
    "node/14111447403": "a bare English type word, an exhibit with no article",
    "node/14111427565": "a plaque with no article, a bare English type word",
    "node/13608966396": "a campsite's name sign tagged a monument",
    "node/13463177463": "a park's name sign tagged a monument",
    "node/13341560911": "a survey mark, a type word for a name",
    "node/2651899973": "a survey mark, a type word and code for a name",
    "node/12541185954": "a description of a trial dig standing in for a name",
    "node/11425383092": "a teaching traffic signal, a description for a name, not a junction",
    "node/14188067111": "a vandalised name",
    "node/13729110241": "a joke entry tagged a place of worship",
    "node/8124716274": "a joke entry tagged a place of worship",
    "way/568973023": "a cut name",
    "node/6033486093": "an address number glued on the name",
    "node/3876397374": "a heritage grade glued on the name",
    "node/10605756630": "a joke name on a locality",
    "relation/4870087": "a name that says the thing is gone",
    "node/5095177073": "public art with no Wikipedia article of its own",
    "way/506832155": "a duplicate station row, the station building beside the station node",
    "way/1145589752": "a route name with a date and a contributor note glued on",
    "way/897246263": "a route name with a date and a contributor note glued on",
    "way/897246264": "a route name with a date and a contributor note glued on",
    "way/1192688584": "a facility's own road",
    "way/1192688585": "a facility's own road",
    "way/603953115": "a facility's own road",
    "way/877354323": "a facility's own road",
    "way/877354324": "a facility's own road",
    "way/1068481135": "a facility's own road",
    "way/874959784": "a facility's own road",
    "way/877354316": "a facility's own road",
    "way/874982890": "a facility's own road",
    "way/877354321": "a facility's own road",
    "way/1373253556": "a facility's own road",
    "way/513509678": "a facility's own road",
    "way/513509681": "a facility's own road",
    "way/1307191263": "a facility's own road",
    "way/1068195024": "a facility's own road",
    "way/177524023": "a facility's own road",
    "way/1047453150": "a facility's own road",
    "way/515714956": "a facility's own road",
    "way/886577656": "a facility's own road",
    "way/1329443890": "a facility's own road",
    "way/1329566412": "a facility's own road",
    "way/659704405": "a facility's own road",
    "way/1330423345": "a facility's own road",
    "way/1338928888": "a facility's own road",
    "way/1426611540": "a facility's own road",
    "way/1514602987": "a facility's own road",
    "way/1531872009": "a facility's own road",
    "way/920149793": "a facility's own road",
    "way/951232482": "a facility's own road",
    "way/959922673": "a facility's own road",
    "way/979849819": "a facility's own road",
    "way/1136248904": "a facility's own road",
    "way/877354328": "a facility's own road",
    "way/877354329": "a facility's own road",
    "way/406143321": "a facility's own road",
    "way/578229562": "a facility's own road",
    "way/1013479900": "a facility's own road",
    "way/926268032": "a facility's own road",
    "way/382892404": "a direction label standing in for a name",
    "way/382892405": "a direction label standing in for a name",
    "way/382892406": "a direction label standing in for a name",
    "way/405699737": "a direction label standing in for a name",
    "way/1075773997": "a direction label standing in for a name",
    "way/958562782": "an address number standing in for a name",
    "way/609207480": "an address number standing in for a name",
    "way/303906307": "an address number standing in for a name",
    "way/313373000": "an address number standing in for a name",
    "way/292862853": "an address number standing in for a name",
    "way/1182155269": "an address number standing in for a name",
    "way/1014958006": "an address number standing in for a name",
    "way/1119998037": "a name that says the thing is gone",
    "way/1119998039": "a name that says the thing is gone",
    "way/1119998041": "a name that says the thing is gone",
    "way/1119998044": "a name that says the thing is gone",
    "way/415752087": "a name that says the thing is gone",
    "way/1163005581": "a temporary way",
    "way/1163005611": "a temporary way",
    "way/1222030824": "a temporary way",
    "way/1222030825": "a temporary way",
    "way/1232537321": "a temporary way",
    "way/433775844": "a description standing in for a name",
    "way/331774727": "a description standing in for a name",
    "way/919998793": "a description standing in for a name",
    "way/573463470": "a description standing in for a name",
    "way/1432522662": "a description standing in for a name",
    "way/1138184912": "a description standing in for a name",
    "way/1308066511": "a description standing in for a name",
    "way/617142815": "a description standing in for a name",
    "way/1182627693": "a description standing in for a name",
    "way/1182627694": "a description standing in for a name",
    "way/1182627696": "a description standing in for a name",
    "way/1182627697": "a description standing in for a name",
    "way/1182627698": "a description standing in for a name",
    "way/1182627699": "a description standing in for a name",
    "way/1182627700": "a description standing in for a name",
    "way/1182627701": "a description standing in for a name",
    "way/1182627702": "a description standing in for a name",
    "way/1182627703": "a description standing in for a name",
    "way/1182629977": "a description standing in for a name",
    "way/1182629978": "a description standing in for a name",
    "way/1182629982": "a description standing in for a name",
    "way/1363515652": "a description standing in for a name",
    "way/1363515654": "a description standing in for a name",
    "way/1125558064": "a glitched name: code or cut name",
    "way/638737207": "a glitched name: code or cut name",
    "way/320974574": "a glitched name: code or cut name",
    "way/241896777": "a glitched name: code or cut name",
    "way/577637244": "a glitched name: English or a second name glued on",
    "way/216648103": "a glitched name: English or a second name glued on",
    "way/240795026": "a glitched name: English or a second name glued on",
}
