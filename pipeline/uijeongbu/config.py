"""Uijeongbu-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; copied from Bucheon's (the Korean
pattern: SEMAS's register, OSM rail on Busan's step 1), via Namyangju's. One of the Gyeonggi
satellites' second round (owner, 2026-09-29: Namyangju, Ansan and Uijeongbu,
one page each; docs/build_briefs/gyeonggi.md, "The next satellites").
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "uijeongbu" / "raw"
DATA_PROCESSED = ROOT / "data" / "uijeongbu" / "processed"
OUTPUTS = ROOT / "outputs" / "uijeongbu"

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
SEMAS_SIGUNGU = ("의정부시",)   # 시군구명 prefix: the city has no 구 (the brief)

# --- Rail ------------------------------------------------------------------

# S, W, N, E: the city plus about 2 km (Uijeongbu spans about 37.69-37.77 N, 127.01-127.13 E; step 1 checks the boundary lies inside).
OSM_BBOX = (37.67, 126.99, 37.79, 127.15)
# The Korail lines the metropolitan subway signs (route=train), queried by ref
# beside every subway, light-rail and monorail relation in the box.
OSM_TRAIN_REFS = ('수인·분당', '경의·중앙', '경강', '서해', 'GTX-A', '경춘')
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 의정부시, admin_level 6 (the brief, 2026-09-29).
BOUNDARY_RELATION = 2409183
BOUNDARY_NAME = "의정부시"
# 82 km2 measured 2026-09-29 (the brief).
BOUNDARY_AREA_KM2 = (78, 86)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~127.2) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# Standard: the brief's median gap is 622 m, just above the spacing rule's ~550 m (docs/ring_rules.md).
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
# The U Line (Uijeongbu LRT) in OSM's colour, Line 1 and Line 7 in Seoul's.
# Line 7's one station (Jangam) is drawn by the satellites' rule (every line
# with a station in the city, to its ends).
LINES = {
    "U": ("U", "#F0831E", "U Line", None),
    "L1": ("1", "#004A85", "Line 1", None),
    "L7": ("7", "#6E7E31", "Line 7", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train"}
# Gate 3: each WHOLE line's station count, English Wikipedia's line infoboxes
# (a SECONDARY source, as Busan's): the U Line's 15 (Balgok to Tapseok) and
# Line 7's 53 (Bucheon's). Line 1 is left out, as in Incheon and Suwon.
LINE_STATION_COUNTS = {"U Line": 15, "Line 7": 53}
NOT_DRAWN = {"GTX-A": "GTX-A", "4": "Line 4",
             "U-DEPOT": "the U Line's depot-shuttle trips (the U relation carries the whole line)"}
# OSM carries the U Line as three relations: the main one, ref U, and two
# depot-shuttle trips with no ref (the brief). They are placed by name, and only
# as not drawn - a drawn line is never matched on text (Incheon's pattern).
NOT_DRAWN_BY_NAME = {"의정부경전철: 발곡 → 차량기지임시승강장": "U-DEPOT",
                     "의정부경전철: 차량기지임시승강장 → 탑석": "U-DEPOT"}
STOP_NAME_FIX = {}
# OSM's English name, where the operator signs it otherwise.
OSM_NAME_EN_OVERRIDES = {}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

CITY_PREFIX = "경기도 의정부시"
TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"
