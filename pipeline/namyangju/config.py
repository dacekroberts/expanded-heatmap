"""Namyangju-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; copied from Bucheon's (the Korean
pattern: SEMAS's register, OSM rail on Busan's step 1). One of the Gyeonggi
satellites' second round (owner, 2026-09-29: Namyangju, Ansan and Uijeongbu,
one page each; docs/build_briefs/gyeonggi.md, "The next satellites").
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "namyangju" / "raw"
DATA_PROCESSED = ROOT / "data" / "namyangju" / "processed"
OUTPUTS = ROOT / "outputs" / "namyangju"

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
SEMAS_SIGUNGU = ("남양주시",)   # 시군구명 prefix: the city has no 구 (the brief)

# --- Rail ------------------------------------------------------------------

# S, W, N, E: the city plus about 2 km (Namyangju spans about 37.55-37.79 N,
# 127.13-127.42 E; step 1 checks the boundary lies inside).
OSM_BBOX = (37.52, 127.10, 37.81, 127.45)
# The Korail lines the metropolitan subway signs (route=train), queried by ref
# beside every subway, light-rail and monorail relation in the box.
OSM_TRAIN_REFS = ('수인·분당', '경의·중앙', '경강', '서해', 'GTX-A', '경춘')
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 남양주시, admin_level 6 (the brief, 2026-09-29).
BOUNDARY_RELATION = 2409175
BOUNDARY_NAME = "남양주시"
# 457 km2 measured 2026-09-29 (the brief).
BOUNDARY_AREA_KM2 = (440, 475)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~127.2) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# Standard: the brief's median gap is 2,294 m (a sprawling city, 457 km2).
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
# Seoul's colours (pipeline/seoul/config.py): Line 4, the Gyeongui–Jungang and
# Gyeongchun lines; Line 8 as Seoul and Seongnam draw it (Seoul Metro's
# #D11D70 darkened, hue kept, clear of Food service's magenta).
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
LINES = {
    "L4": ("4", line_registry.colour("seoul-subway-line-4"), "Line 4", None),
    "L8": ("8", line_registry.colour("seoul-subway-line-8"), "Line 8", None),
    "GJ": ("경의·중앙", line_registry.colour("gyeongui-jungang-line"), "Gyeongui–Jungang Line", None),
    "GC": ("경춘", line_registry.colour("gyeongchun-line"), "Gyeongchun Line", None),
}
OSM_COLOUR = {"L8": "#D11D70"}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train"}
# Gate 3: each WHOLE line's station count, English Wikipedia's line infoboxes
# (a SECONDARY source, as Busan's). None of the four lines can take it here,
# each for a reason an earlier city recorded:
#   * Line 4: the query brings only its service relations that touch the box
#     (29 stations, of 51), as Line 1 in Incheon and Suwon;
#   * Line 8: OSM carries 24 stations, the infobox 25 (Seongnam's note);
#   * the Gyeongui–Jungang Line: OSM 55, the infobox 57 (Goyang's note);
#   * the Gyeongchun Line: OSM's relations carry 25 with the Cheongnyangni and
#     Kwangwoon University branches, the infobox 20, its own table 21
#     Sangbong-Chuncheon (read 2026-09-30).
# In their place, the IN-CITY stations of each line read against the line
# tables (English Wikipedia, 2026-09-30): Gyeongchun Byeollae, Toegyewon,
# Sareung, Geumgok, Pyeongnaehopyeong, Cheonmasan and Maseok (7);
# Gyeongui–Jungang Donong, Yangjeong, Deokso, Dosim, Paldang and Ungilsan (6);
# Line 4's Jinjeop extension Byeollae Byeolgaram, Onam and Jinjeop (3); Line 8's
# Byeollae extension Dasan and Byeollae (2). Step 1's 17 agree, line by line.
LINE_STATION_COUNTS = {}
NOT_DRAWN = {"GTX-A": "GTX-A", "2": "Line 2", "5": "Line 5", "6": "Line 6", "9": "Line 9"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
# OSM's English name, where the operator signs it otherwise (Suwon's
# precedent: a compound run together, hyphenated or spaced as signed).
OSM_NAME_EN_OVERRIDES = {
    "별내별가람": "Byeollae Byeolgaram",     # OSM name:en "Byeollaebyeolgaram"
    "평내호평": "Pyeongnae-Hopyeong",        # OSM name:en "PyeongnaeHopyeong"
}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

CITY_PREFIX = "경기도 남양주시"
TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"
