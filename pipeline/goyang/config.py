"""Goyang-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; generated from Incheon's config (the
Korean pattern: SEMAS's register, OSM rail on Busan's step 1). One of the
Gyeonggi satellites (owner, 2026-09-28: Goyang, Seongnam and Yongin first; one
page each, 2026-09-29).
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "goyang" / "raw"
DATA_PROCESSED = ROOT / "data" / "goyang" / "processed"
OUTPUTS = ROOT / "outputs" / "goyang"

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
SEMAS_SIGUNGU = ("고양시",)   # 시군구명 prefix: the city and its 구

# --- Rail ------------------------------------------------------------------

OSM_BBOX = (37.55, 126.65, 37.77, 127.01)       # S, W, N, E: the city plus about 2 km
# The Korail lines the metropolitan subway signs (route=train), queried by ref
# beside every subway, light-rail and monorail relation in the box.
OSM_TRAIN_REFS = ('수인·분당', '경의·중앙', '경강', '서해', 'GTX-A', '경춘')
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 고양시, admin_level 6, resolved by name 2026-09-29.
BOUNDARY_RELATION = 2409166
BOUNDARY_NAME = "고양시"
# 266 km2 measured 2026-09-29.
BOUNDARY_AREA_KM2 = (260, 272)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude falls in the 126 to 132 band. Derived per city,
# not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
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
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
LINES = {
    "L3": ("3", line_registry.colour("seoul-subway-line-3"), "Line 3", None),
    "GJ": ("경의·중앙", line_registry.colour("gyeongui-jungang-line"), "Gyeongui–Jungang Line", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train"}
# Gate 3: each WHOLE line's station count, English Wikipedia's line infoboxes
# read 2026-09-29 (a SECONDARY source, as Busan's).
# The Gyeongui–Jungang Line is left out of the whole-line gate: OSM carries 55
# names (Ichon twice) against the infobox's 57, none of the gap in Goyang.
LINE_STATION_COUNTS = {"Line 3": 44}
# The Seohae Line runs on the Gyeongui–Jungang Line's track through the same
# stations in Goyang (Neunggok, Daegok, Goksan, Baengma, Pungsan, Ilsan), so
# drawing it would draw that track twice.
NOT_DRAWN = {"서해": "Seohae Line", "GTX-A": "GTX-A", "1": "Line 1", "2": "Line 2", "4": "Line 4",
             "5": "Line 5", "6": "Line 6", "9": "Line 9", "I2": "Incheon Line 2", "W": "Ui LRT",
             "김포 골드라인": "Gimpo Goldline", "인천1": "Incheon Line 1"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

CITY_PREFIX = "경기도 고양시"
TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"
