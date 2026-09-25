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
TAICHUNG_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
