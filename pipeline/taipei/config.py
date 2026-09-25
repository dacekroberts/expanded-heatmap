"""Taipei (Regional)-specific settings: Taipei City + New Taipei City, scoped to
one page per this project's per-city folder architecture.

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/taipei.md,
the method the `taiwan-city` skill.

REGIONAL, like Dublin and Lille (owner, 2026-09-23): New Taipei completely
surrounds Taipei, and the metro crosses the boundary on several lines.

Business leg: the national business tax register (FIA; the shared cache), the
rows whose address is in either city, JOINED to each city's own door-plate file
(the shared step 2, run once per city and the two results concatenated).

Rail (owner, 2026-09-25): every metro and light-rail line in the two cities -
Taipei Metro's five lines and their branches, New Taipei's Circular Line and
Danhai and Ankeng light rail, and the Airport MRT's stations in the two cities.
Routes, stations and colours from OpenStreetMap: Taipei's network map carries no colours
and may lack New Taipei's lines (the recorded ground, osm-rail). A station is in
the region when either city's door-plate file has plates within 300 m of it.
Gate 3: Taipei Metro's own station list. NOT drawn: Taiwan Railway, high-speed
rail, the Maokong Gondola.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "taipei" / "raw"
DATA_PROCESSED = ROOT / "data" / "taipei" / "processed"
OUTPUTS = ROOT / "outputs" / "taipei"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

# Taipei's door plates (民政局, data.taipei) - the name is the one the screen's
# control reads (scripts/screen_taiwan_join.py taipei).
TAIPEI_DOORPLATE_URL = ("https://data.taipei/api/dataset/b7c8e724-1e98-45ee-a0bd-f3840623ed97/"
                        "resource/ce76ca0c-7f94-4935-ab47-1d2a41ca2abb/download")
TAIPEI_DOORPLATE_CSV = DATA_RAW / "taipei_doorplate_20260902.csv"
TAIPEI_DOORPLATE_EDITION = "臺北市門牌位置數值資料 20260902"
# New Taipei's (data.ntpc.gov.tw), English-headed. In data/new_taipei/raw/, where
# the screen reads it.
NEW_TAIPEI_DOORPLATE_URL = "https://data.ntpc.gov.tw/api/datasets/d7b568ab-3819-40c8-a6e7-a6b199443101/csv/file"
NEW_TAIPEI_DOORPLATE_CSV = ROOT / "data" / "new_taipei" / "raw" / "new_taipei_doorplate.csv"
# The dataset's own description names the month (ROC 115/09) - read 2026-09-25.
NEW_TAIPEI_DOORPLATE_EDITION = "新北市門牌位置數值資料 11509"
# Taipei Metro's own station list (臺北捷運路線車站資料服務, data.gov.tw 131326): gate 3.
METRO_LIST_URL = ("https://data.taipei/api/dataset/8bf00fa8-86a5-437e-b5c7-9bc0fe0e2971/"
                  "resource/e3c0e67f-5916-405f-ad9a-41f52a65c2d2/download")
METRO_LIST_CSV = DATA_RAW / "taipei_metro_stations.csv"

OVERPASS_URLS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
)
# Bounded (osm-rail): the metro's extent in the two cities. Relations reaching
# beyond it (the Airport MRT to Taoyuan) come back whole, drawn to their ends.
OSM_BBOX = (24.93, 121.36, 25.20, 121.66)       # S, W, N, E
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"

# The two door-plate files' columns (read 2026-09-25): both TWD97 TM2 with a
# district CODE; Taipei's headers are Chinese, New Taipei's English.
PLATE_CRS = "EPSG:3826"
TAIPEI_PLATES = {"cols": {"street": "街路段", "lane": "巷", "alley": "弄", "num": "號",
                          "x": "橫座標", "y": "縱座標"}, "district": "鄉鎮市區代碼"}
NEW_TAIPEI_PLATES = {"cols": {"street": "street、road、section", "lane": "lane", "alley": "alley",
                              "num": "number", "x": "x_3826", "y": "y_3826"}, "district": "areacode"}
TAIPEI_PLATE_XY = ("橫座標", "縱座標")
NEW_TAIPEI_PLATE_XY = ("x_3826", "y_3826")
ADDRESS_PREFIXES = ("臺北市", "台北市", "新北市", "臺北縣", "台北縣")
CITY_PREFIXES = {"Taipei": ("臺北市", "台北市"), "New Taipei": ("新北市", "臺北縣", "台北縣")}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 51N: the longitude (~121.53) falls in the 120 to 126 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32651"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Matched on the RELATION's ref (and, where one ref holds a branch, its name),
# after printing the table. Colours are the ones OSM carries on each line's
# relations (the Seoul / Hong Kong precedent), except the Zhonghe-Xinlu Line,
# whose relations say `colour=orange` - a CSS keyword, resolved through the CSS
# named-colour table to #FFA500 (osm-rail: never invent a shade). The two
# branches carry their own colours in OSM, as on Taipei Metro's own map, so they
# are drawn as lines of their own. operator_lines: the rows of Taipei Metro's
# list each line is checked against (gate 3); New Taipei's lines and the Airport
# MRT are not in that list.
LINES = {
    "BR": {"ref": "BR", "colour": "#A74C00", "name": "Wenhu Line", "operator_lines": ["BR"]},
    "R": {"ref": "R", "colour": "#FF0000", "name": "Tamsui–Xinyi Line", "operator_lines": ["R"]},
    "RB": {"ref": "捷運紅線 (新北投支線)", "colour": "#F890A5", "name": "Xinbeitou Branch",
           "operator_lines": ["R-3"]},
    "G": {"ref": "G", "name_not": ("小碧潭",), "colour": "#1E7B54", "name": "Songshan–Xindian Line",
          "operator_lines": ["G"]},
    "GB": {"ref": "G", "name_has": "小碧潭", "colour": "#CEDC00", "name": "Xiaobitan Branch",
           "operator_lines": ["G-3"]},
    "O": {"ref": "O", "colour": "#FFA500", "name": "Zhonghe–Xinlu Line", "operator_lines": ["O"]},
    "BL": {"ref": "BL", "colour": "#007EC7", "name": "Bannan Line", "operator_lines": ["BL"]},
    "Y": {"ref": "Y", "colour": "#FFD900", "name": "Circular Line"},
    "LB": {"ref": "LB", "colour": "#6DB7D0", "name": "Sanying Line"},
    "V": {"ref": "V", "colour": "#FEBEB5", "name": "Danhai LRT"},
    "K": {"ref": "K", "colour": "#C3B091", "name": "Ankeng LRT"},
    "A": {"ref": "A", "colour": "#2C5AA5", "name": "Airport MRT"},
}
NOT_DRAWN = set()
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0
# A station is in the region when a door plate of either city lies this close.
SCOPE_RADIUS_M = 300.0

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "taiwan_fia"
RAW_CLASSIFICATION_COLUMN = "industry"
OFFICE_FLOOR_MIN = 3
OFFICE_EXEMPT_ROWS_AT_ADDRESS = 20

CITY_BBOX = {"lat_min": 24.60, "lat_max": 25.35, "lon_min": 121.25, "lon_max": 122.05}
