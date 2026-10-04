"""Gimhae-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/gimhae.md) on Daejeon's config (Incheon's SEMAS module and
OSM rail route, keyed on 시군구코드), with the LRT drawn as Busan draws it.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "gimhae" / "raw"
DATA_PROCESSED = ROOT / "data" / "gimhae" / "processed"
OUTPUTS = ROOT / "outputs" / "gimhae"

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
# (data/korea/raw/), as every built SEMAS city (owner, 2026-09-29; Band A and
# its own page, 2026-10-03). Busan's businesses come from a different source
# (its permit API), so the two pages never sum.
SEMAS_SIDO = "경상남도"
SEMAS_SIGUNGU = None
# 김해시: one 시, no 구 (the brief: the prefix 김해시 selects the same rows).
SEMAS_SIGUNGU_CODES = ("48250",)

# --- Rail ------------------------------------------------------------------

# Gimhae plus about 2 km, taken east to 사상 so the whole line arrives.
OSM_BBOX = (35.13, 128.68, 35.41, 129.03)       # S, W, N, E
# One Overpass query for the city (osm-rail), split by fetch_sources.py into
# the three files below. Busan's cached BGL relation is never read or written.
OSM_ALL_JSON = DATA_RAW / "osm_all.json"
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 김해시, admin_level 6 in 경상남도, resolved by name 2026-10-04.
BOUNDARY_RELATION = 7224485
BOUNDARY_NAME = "김해시"
BOUNDARY_ADMIN_LEVEL = "6"
# 460 km2 measured 2026-10-04.
BOUNDARY_AREA_KM2 = (450, 470)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~128.89) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# The Busan-Gimhae LRT, drawn as Busan's map draws it (pipeline/busan/config.py:
# ref BGL, its color and name), to both ends. The 12 stations inside Gimhae
# are kept; the 9 in Busan are recorded as outside (Busan's page counts them).
# The light-rail test passes: grade-separated, every 5-6 minutes all day, a
# median spacing measured at step 1. NOT drawn: Busan's lines that reach the
# box with no station in Gimhae, and Korail (never queried).
# key -> (OSM ref, colour, public name, label end).
LINES = {
    "BGL": ("BGL", "#8652A1", "Busan–Gimhae LRT", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train", "tram"}
# Gate 3: the whole line, termini to termini: the operator's station list (21
# names on its 부원 page) and Busan's LINE_STATION_COUNTS agree.
LINE_STATION_COUNTS = {"Busan–Gimhae LRT": 21}
NOT_DRAWN = {"2": "Busan Line 2", "3": "Busan Line 3"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

GIMHAE_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
