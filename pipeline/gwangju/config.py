"""Gwangju-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/gwangju.md) on Daejeon's config (Incheon's SEMAS module and
OSM rail route, keyed on 시군구코드).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "gwangju" / "raw"
DATA_PROCESSED = ROOT / "data" / "gwangju" / "processed"
OUTPUTS = ROOT / "outputs" / "gwangju"

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
# 2026-10-03). The 2026 merger put Gwangju's five 구 in the member
# 전남광주통합특별시 (시도코드 12) with all of South Jeolla, under new codes;
# the old 광주광역시 29xxx codes are gone. Keyed on codes, never names (owner,
# 2026-10-03): 동구, 서구, 남구 and 북구 recur in other cities, and 경기도
# 광주시 is another city.
SEMAS_SIDO = "전남광주통합특별시"
SEMAS_SIGUNGU = None
# 동구 12210, 서구 12240, 남구 12270, 북구 12300, 광산구 12330.
SEMAS_SIGUNGU_CODES = ("12210", "12240", "12270", "12300", "12330")

# --- Rail ------------------------------------------------------------------

OSM_BBOX = (35.03, 126.63, 35.27, 127.04)       # S, W, N, E: the placed extent plus about 2 km
# One Overpass query for the city (osm-rail), split by fetch_sources.py into
# the three files below.
OSM_ALL_JSON = DATA_RAW / "osm_all.json"
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# The boundary may have moved with the merger (the brief): the query asks for
# any relation named 광주광역시 and for the five 구 relations. On 2026-10-04
# no 광주광역시 relation came back, so step 1 takes the UNION of the five 구
# (admin_level 6), each by id and checked by name and by the query box.
BOUNDARY_NAME = "광주광역시"
BOUNDARY_DISTRICTS = ("동구", "서구", "남구", "북구", "광산구")
BOUNDARY_DISTRICT_RELATIONS = {4162635: "동구", 7348759: "서구", 7348741: "남구",
                               7348583: "북구", 7348758: "광산구"}
# The five 구 measured 500 km2 together, 2026-10-04.
BOUNDARY_AREA_KM2 = (490, 510)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~126.85) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Gwangju Metro Line 1, 20 stations, all inside the city (녹동 to 평동). NOT
# drawn: Line 2 (not open; phase 1 reported for 2028-12) and Korail/KTX
# (intercity, as everywhere in Korea; the query never asks for route=train).
# key -> (OSM ref, colour, public name, label end).
# The operator's color as OSM tags it on both direction relations.
LINES = {
    "L1": ("1", "#009088", "Line 1", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train", "tram"}
# Gate 3: the operator's own count (grtc.co.kr 운행현황, 역수 20개역; brief
# check gwangju-line1-operator-facts).
LINE_STATION_COUNTS = {"Line 1": 20}
# Line 2's two circle relations (route=light_rail, 36 planned stops each on
# 2026-10-04) are the line under construction.
NOT_DRAWN = {"2": "Line 2 (under construction)"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
# OSM's English name, where it misspells what the operator signs: OSM gives
# 금남로4가 "Geumnamno 4(sa)-ga" but 금남로5가 "Geumnamro 5-ga"; the
# operator's English station list reads Geumnamno4-ga and Geumnamno5-ga
# (grtc.co.kr/subwayeng, read 2026-10-04), spaced here as OSM spaces 4가.
OSM_NAME_EN_OVERRIDES = {
    "금남로5가": "Geumnamno 5-ga",
}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

GWANGJU_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
