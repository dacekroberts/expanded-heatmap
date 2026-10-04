"""Daejeon-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/daejeon.md) on Incheon's config (the same SEMAS module and
the same OSM rail route).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "daejeon" / "raw"
DATA_PROCESSED = ROOT / "data" / "daejeon" / "processed"
OUTPUTS = ROOT / "outputs" / "daejeon"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- The register ----------------------------------------------------------
#
# SEMAS's 상가(상권)정보 (data.go.kr 15083033), the national storefront register,
# read through pipeline/countries/korea_sbiz.py from the country cache
# (data/korea/raw/), as every built SEMAS city (owner, 2026-09-29; Band A
# 2026-10-03).
SEMAS_SIDO = "대전광역시"
SEMAS_SIGUNGU = None
# Daejeon's five 구 and no 군: 동구, 중구, 서구, 유성구, 대덕구. On the 2026-06-30
# edition these five are the whole member (80,704 rows, the brief); the codes
# make a sixth district or a merger stop step 2 instead of widening the page.
SEMAS_SIGUNGU_CODES = ("30110", "30140", "30170", "30200", "30230")

# --- Rail ------------------------------------------------------------------

OSM_BBOX = (36.17, 127.22, 36.52, 127.57)       # S, W, N, E: the placed extent plus about 2 km
# One Overpass query for the city (osm-rail), split by fetch_sources.py into
# the three files below.
OSM_ALL_JSON = DATA_RAW / "osm_all.json"
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 대전광역시, admin_level 4 (ISO KR-30), resolved by name 2026-10-04.
BOUNDARY_RELATION = 2349984
BOUNDARY_NAME = "대전광역시"
BOUNDARY_ADMIN_LEVEL = "4"
# An inland city, so no territorial sea: 536 km2 measured 2026-10-04.
BOUNDARY_AREA_KM2 = (525, 545)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~127.39) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Daejeon Metro Line 1, all 22 stations inside the city. NOT drawn: Line 2 (a
# tram under construction, not open) and Korail/KTX (intercity, as everywhere
# in Korea; the query never asks for route=train).
# key -> (OSM ref, colour, public name, label end).
# The operator's green, as OSM tags it on both direction relations.
LINES = {
    "L1": ("1", "#007448", "Line 1", None),
}
OSM_COLOUR = {}
# tram: Line 2's relation, placed as NOT drawn.
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train", "tram"}
# Gate 3: the operator's own count (djtc.kr 시설현황, 22 정거장; brief check
# daejeon-line1-operator-facts).
LINE_STATION_COUNTS = {"Line 1": 22}
# Line 2's relation (route=tram, no stop members on 2026-10-04) is the line
# under construction.
NOT_DRAWN = {"2": "Line 2 (a tram under construction)"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

CITY_PREFIX = "대전광역시"
TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

DAEJEON_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
