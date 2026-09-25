"""Taoyuan-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/taoyuan.md,
the national argument taipei.md, and the method the `taiwan-city` skill.

Business leg: the national business tax register (FIA, daily; the shared cache
in data/taiwan/raw/), the rows whose address is in Taoyuan, JOINED to Taoyuan's
door-plate file (TGOS edition, monthly).

Rail: the Taoyuan Airport MRT (Taoyuan Metro's line A). The operator's XML
gives the stations' names and order but no coordinates, so the stations are
the OSM route relation's stop nodes, checked name by name against the
operator's list (gate 3), and the route is the same relation's geometry. The
national 捷運車站 layer says which stations are in Taoyuan. Stations inside
Taoyuan only (owner 2026-09-25); the line is drawn to its ends.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "taoyuan" / "raw"
DATA_PROCESSED = ROOT / "data" / "taoyuan" / "processed"
OUTPUTS = ROOT / "outputs" / "taoyuan"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

TYCG = "https://opendata.tycg.gov.tw/api/dataset/"
# The August 2026 door-plate edition (TGOS_A68000_11508, 94,461,884 bytes in the
# brief). The dataset lists one resource per month: a refresh picks the newest.
DOORPLATE_URL = (TYCG + "ec47dbd5-9ed8-4c8d-8ce1-ccb63b1b72e6/resource/"
                 "d00ecba4-dec2-4a62-bfc7-989a8359cebe/download")
DOORPLATE_EDITION = "TGOS_A68000_11508"
DOORPLATE_CSV = DATA_RAW / "taoyuan_doorplate.csv"
# Taoyuan Metro's own datasets (data.gov.tw 128388, 128390): the network and the
# line's stations in order, names in Chinese and English. No coordinates.
NETWORK_XML_URL = (TYCG + "434a3d9f-ebc1-474b-b8b7-da53eb340b48/resource/"
                   "35cd3ed3-42a4-401d-90bd-7f5b82588169/download")
ROUTE_XML_URL = (TYCG + "8c1fe832-fe4a-4033-a283-25ab39a99d93/resource/"
                 "5535111f-9af5-40b9-9e58-a4d382fb8b2c/download")
NETWORK_XML = DATA_RAW / "metro_network.xml"
ROUTE_XML = DATA_RAW / "metro_route_stations.xml"
# The national 捷運車站 layer (內政部, data.gov.tw 73233): which county each
# station is in.
NATIONAL_STATIONS_URL = ("https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/"
                         "63A7BA62-C429-4F2D-8B73-21AAB9E6EAE0/resource/"
                         "4C11DFAE-ED20-4843-89E7-08D23CADAA16/download")
NATIONAL_STATIONS_ZIP = DATA_RAW / "national_metro_stations.zip"

# The door-plate file's columns (read 2026-09-25): TWD97 TM2 only, so step 2
# reprojects (the shared step reads PLATE_CRS).
PLATE_COLS = {"street": "街路段", "lane": "巷", "alley": "弄", "num": "號",
              "x": "橫座標", "y": "縱座標"}
PLATE_CRS = "EPSG:3826"
PLATE_DISTRICT_COL = "鄉鎮市區代碼"
ADDRESS_PREFIXES = ("桃園市", "桃園縣")
CITY_NAME_ZH = "桃園市"

OVERPASS_URLS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
)
# Bounded (osm-rail): Taoyuan and the line's run to Taipei Main Station.
OSM_BBOX = (24.58, 120.97, 25.13, 121.53)       # S, W, N, E
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
LINE_NAME_MATCH = "機場"                           # 桃園機場捷運 / 機場捷運

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 51N: the longitude (~121.30) falls in the 120 to 126 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32651"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
LINE_KEY = "A"
LINE_NAME = "Airport MRT"
# The all-stop service's relations (普通車) serve every station; the express
# (直達車) skips most. Drawn from the all-stop one, in the colour OSM carries on
# it (step 1 checks the relation still does).
ALL_STOP_MARK = "普通車"
# The operator's XML is dated 2018-10-01 (its own UpdateTime) and lists A1-A21;
# A22 老街溪 opened in 2023, and the national layer (updated 2023-08) and OSM
# both carry it. Added BY ID, with its English name, so gate 3 still compares
# every other station one for one.
OPERATOR_LIST_ADDITIONS = {"A22": "Laojie River"}
LINE_COLOUR = "#2C5AA5"

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "taiwan_fia"
RAW_CLASSIFICATION_COLUMN = "industry"
# The owner's head-office rule, as Taichung (taiwan-city skill).
OFFICE_FLOOR_MIN = 3
OFFICE_EXEMPT_ROWS_AT_ADDRESS = 20

def label_focus(stations):
    """No boundary polygon is read (the stations' own addresses scope them), so
    the line label is focused on the kept stations' extent, 2 km around them."""
    import geopandas as gpd
    pts = gpd.GeoSeries(gpd.points_from_xy(stations.longitude, stations.latitude), crs=CRS_GEOGRAPHIC)
    hull = pts.to_crs(CRS_PROJECTED).union_all().convex_hull.buffer(2000)
    return gpd.GeoSeries([hull], crs=CRS_PROJECTED).to_crs(CRS_GEOGRAPHIC).iloc[0]


CITY_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
