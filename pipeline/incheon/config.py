"""Incheon-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/incheon.md), Busan's config (the Korean rail pattern) and
the SEMAS register (owner, 2026-09-29).
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "incheon" / "raw"
DATA_PROCESSED = ROOT / "data" / "incheon" / "processed"
OUTPUTS = ROOT / "outputs" / "incheon"

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
# (data/korea/raw/). Chosen over the brief's route (owner, 2026-09-29): the
# national LOCALDATA API needs a data.go.kr key, and data.go.kr accounts need a
# Korean identity check (본인인증), closed to this project; Incheon's own permit
# lists place only 73% through KESA's lift-building join and its salons list
# carries lot-number addresses that no keyless file places. SEMAS carries a
# WGS84 point on every row and all three buckets.
SEMAS_SIDO = "인천광역시"
SEMAS_SIGUNGU = None          # the whole city, its ten 구/군

# --- Rail ------------------------------------------------------------------

OSM_BBOX = (37.35, 126.55, 37.62, 126.80)       # S, W, N, E
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 인천광역시, admin_level 4 (ISO KR-28), resolved by name 2026-09-29.
BOUNDARY_RELATION = 2297419
BOUNDARY_NAME = "인천광역시"
# Its polygon holds territorial sea around the Ongjin islands (Busan's shape):
# 9,906 km2 measured 2026-09-29 against about 1,067 of land.
BOUNDARY_AREA_KM2 = (9800, 10000)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~126.71) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Seoul's precedent (the brief's recommendation, applied 2026-09-29): the
# city's own lines and the metropolitan subway lines that serve it, with the
# Korail line Seoul signs as subway. NOT drawn: AREX (Seoul left it out on
# spacing), the airport maglev (suspended), the Wolmi Sea Train (a tourist
# ride), and lines that only touch the bbox. Stations inside Incheon only;
# lines drawn to their ends.
# key -> (OSM ref, colour, public name, label end). Operator colours.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
LINES = {
    "IC1": ("인천1", "#B4C7E7", "Incheon Line 1", None),
    "IC2": ("I2", "#F4A462", "Incheon Line 2", None),
    "L1": ("1", line_registry.colour("seoul-subway-line-1"), "Line 1", None),
    "L7": ("7", line_registry.colour("seoul-subway-line-7"), "Line 7", None),
    "SB": ("수인·분당", line_registry.colour("suin-bundang-line"), "Suin–Bundang Line", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train"}
# Gate 3: each WHOLE line's station count, termini to termini (inside Incheon
# and out). English Wikipedia's line infoboxes, read 2026-09-29 - a SECONDARY
# source, as Busan's and Daegu's. Line 1 (102 stations) is left out of the
# whole-line gate: the query brings only its service relations that touch
# Incheon (65 stations), and its southern branches (Cheonan, Sinchang,
# Seodongtan, Gwangmyeong) never do. Its 11 stations inside Incheon are the
# Gyeongin Line's Incheon section, Bugae to Incheon (Stockholm's precedent).
LINE_STATION_COUNTS = {"Incheon Line 1": 33, "Incheon Line 2": 27, "Line 7": 53,
                       "Suin–Bundang Line": 63}
NOT_DRAWN = {"공항철도": "AREX", "4": "Line 4", "9": "Line 9", "김포 골드라인": "Gimpo Goldline",
             "서해": "Seohae Line", "GTX-A": "GTX-A", "경의·중앙": "Gyeongui–Jungang Line",
             "WOLMI": "Wolmi Sea Train (a tourist ride)"}
# The Wolmi Sea Train's relation carries no ref; placed by its name, as NOT drawn.
NOT_DRAWN_BY_NAME = {"월미바다열차": "WOLMI"}
STOP_NAME_FIX = {}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

CITY_PREFIX = "인천광역시"
TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

INCHEON_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
