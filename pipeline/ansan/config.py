"""Ansan-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; copied from Bucheon's (the Korean
pattern: SEMAS's register, OSM rail on Busan's step 1), via Namyangju's. One of the Gyeonggi
satellites' second round (owner, 2026-09-29: Namyangju, Ansan and Uijeongbu,
one page each; docs/build_briefs/gyeonggi.md, "The next satellites").
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "ansan" / "raw"
DATA_PROCESSED = ROOT / "data" / "ansan" / "processed"
OUTPUTS = ROOT / "outputs" / "ansan"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- The register ----------------------------------------------------------
#
# SEMAS's 상가(상권)정보 (data.go.kr 15083033), read through
# pipeline/countries/korea_sbiz.py from the country cache (owner, 2026-09-29,
# for Incheon and the Gyeonggi satellites): the national LOCALDATA API needs a
# Korean identity check, and the city's own files are not a register
# (docs/build_briefs/gyeonggi.md).
SEMAS_SIDO = "경기도"
SEMAS_SIGUNGU = ("안산시",)   # 시군구명 prefix: the city and its two 구 (상록구, 단원구; the brief)

# --- Rail ------------------------------------------------------------------

# S, W, N, E: the city plus about 2 km (Ansan, Daebudo included, spans about 37.18-37.38 N, 126.52-126.93 E; step 1 checks the boundary lies inside).
OSM_BBOX = (37.16, 126.50, 37.40, 126.95)
# The Korail lines the metropolitan subway signs (route=train), queried by ref
# beside every subway, light-rail and monorail relation in the box.
OSM_TRAIN_REFS = ('수인·분당', '경의·중앙', '경강', '서해', 'GTX-A', '경춘')
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 안산시, admin_level 6 (the brief, 2026-09-29).
BOUNDARY_RELATION = 2409159
BOUNDARY_NAME = "안산시"
# 486 km2 measured 2026-09-29 (the brief), Daebudo and its sea included.
BOUNDARY_AREA_KM2 = (470, 500)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~127.2) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# Standard: the brief's median gap is 1,417 m (Daebudo and the sea widen it).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Seoul's precedent applied to a satellite (2026-09-29): every metropolitan
# subway, Korail metro and light-rail line with stations in the city is drawn,
# in the operators' colours (Seoul's drawn ones where Seoul draws the line);
# GTX-A (an express) and lines that never enter the city are not. Stations
# inside the city only; lines drawn to their ends.
# key -> (OSM ref, colour, public name, label end).
# Seoul's colour for Line 4, Seongnam's and Suwon's for the Suin–Bundang Line;
# the Seohae Line is drawn on Bucheon's precedent (owner, 2026-09-29): in Ansan
# it runs on its own track through Wonsi, Siu, Seonbu and Dalmi and meets the
# other lines only at Choji - Bucheon's shape, not Goyang's - in Bucheon's
# colour, OSM's tag.
LINES = {
    "L4": ("4", "#009BCE", "Line 4", None),
    "SB": ("수인·분당", "#ECA300", "Suin–Bundang Line", None),
    "SH": ("서해", "#5EAC41", "Seohae Line", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train"}
# Gate 3: each WHOLE line's station count, English Wikipedia's line infoboxes
# (a SECONDARY source, as Busan's): the Suin–Bundang Line's 63, as Seongnam,
# Suwon and Yongin read it. Line 4 is left out (the query brings only its service
# relations that touch the box, as in Namyangju), and the Seohae Line is not
# gated whole, as in Bucheon.
LINE_STATION_COUNTS = {"Suin–Bundang Line": 63}
NOT_DRAWN = {"GTX-A": "GTX-A", "1": "Line 1", "인천1": "Incheon Line 1"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
# OSM's English name, where the operator signs it otherwise (Suwon's
# precedent: a compound run together, spaced as signed).
OSM_NAME_EN_OVERRIDES = {
    "신길온천": "Singil Oncheon",   # OSM name:en "Singiloncheon"
}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

CITY_PREFIX = "경기도 안산시"
TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"
