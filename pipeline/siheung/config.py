"""Siheung-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/siheung.md): Ansan's rail (its three lines, colours and
gate 3) with Gimhae's register config, keyed on 시군구코드.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "siheung" / "raw"
DATA_PROCESSED = ROOT / "data" / "siheung" / "processed"
OUTPUTS = ROOT / "outputs" / "siheung"

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
# (data/korea/raw/), as every built SEMAS city (owner, 2026-09-29; Siheung
# Band A, 2026-10-04).
SEMAS_SIDO = "경기도"
SEMAS_SIGUNGU = None
# 시흥시: one 시, no 구. The code and the prefix 시흥시 pick the identical 25,119
# rows of the 2026-06-30 edition (the brief, measured 2026-10-04).
SEMAS_SIGUNGU_CODES = ("41390",)

# --- Rail ------------------------------------------------------------------

# The register's extent plus about 2 km (the brief); step 1 checks the
# boundary lies inside.
OSM_BBOX = (37.29, 126.65, 37.49, 126.90)       # S, W, N, E
# The Korail lines the metropolitan subway signs (route=train), queried by ref
# beside every subway, light-rail and monorail relation in the box (Ansan's).
OSM_TRAIN_REFS = ('수인·분당', '경의·중앙', '경강', '서해', 'GTX-A', '경춘')
# One Overpass query for the city (osm-rail), split by fetch_sources.py into
# the three files below.
OSM_ALL_JSON = DATA_RAW / "osm_all.json"
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 시흥시, admin_level 6 in 경기도, resolved by name 2026-10-07.
BOUNDARY_RELATION = 2409181
BOUNDARY_NAME = "시흥시"
BOUNDARY_ADMIN_LEVEL = "6"
# 166 km2 measured 2026-10-07 (the brief's general-knowledge 139 is land
# only; the polygon takes in tidal flats, as Ansan's does).
BOUNDARY_AREA_KM2 = (158, 174)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~126.80, the register 126.67-126.88) falls in
# the 126 to 132 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# Standard: the brief's median gap is 1,316 m, above the spacing rule's ~550 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Seoul's precedent applied to a satellite (2026-09-29): every metropolitan
# subway, Korail metro and light-rail line with stations in the city is drawn,
# in the operators' colours; GTX-A (an express) and lines that never enter the
# city are not. Stations inside the city only; lines drawn to their ends.
# Ansan's three lines, its colours: Line 4 in Seoul's, the Suin–Bundang Line in
# Seongnam's and Suwon's, the Seohae Line on Bucheon's precedent (owner,
# 2026-09-29) in OSM's. The Suin–Bundang and Seohae lines run every 15 minutes
# at midday, borderline, drawn on Ansan's and Bucheon's precedent (owner,
# 2026-10-04; the page states the wait).
# key -> (OSM ref, colour, public name, label end).
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
LINES = {
    "L4": ("4", line_registry.colour("seoul-subway-line-4"), "Line 4", None),
    "SB": ("수인·분당", line_registry.colour("suin-bundang-line"), "Suin–Bundang Line", None),
    "SH": ("서해", line_registry.colour("seohae-line"), "Seohae Line", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train", "tram"}
# Gate 3: Ansan's. The Suin–Bundang Line's whole 63, English Wikipedia's
# infobox (a SECONDARY source, as Seongnam, Suwon, Yongin and Ansan read it).
# Line 4 is left out (the query brings only its service relations that touch
# the box) and the Seohae Line is not gated whole, as in Bucheon and Ansan.
LINE_STATION_COUNTS = {"Suin–Bundang Line": 63}
# Every relation the box brings in that is not drawn: none has a station in
# Siheung (step 1 prints any that does).
NOT_DRAWN = {"GTX-A": "GTX-A", "1": "Line 1", "2": "Line 2", "7": "Line 7",
             "인천1": "Incheon Line 1", "I2": "Incheon Line 2"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
# OSM's English name, where the operator signs it otherwise.
OSM_NAME_EN_OVERRIDES = {}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602409181)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ko",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "MTV동양파라곤아파트앞": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "동보아파트삼거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "동원아파트삼거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "유천아파트앞삼거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "유통상가사거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "이마트사거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "중심상가로": "a street's own name on tertiary and residential ways ('central shopping district road'), a public road; tags read 2026-10-13",
}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read of this
# index (rule passes 5 and 6), each id read with its cached name and its index
# row; grouped by the reader's class.
PLACE_DROPPED = {
    # A bare type word standing alone (reader's drop; owner, 2026-10-13)
    "node/4640011427": "'자판기'",
    "node/4634867188": "'사각정'",
    "node/4640011481": "'사각정'",
    "node/4640175682": "'사각정'",
    "node/4650409325": "'사각정'",
    "node/4640057105": "'소공연장'",
    "node/4650409326": "'건축비'",
    "way/478860911": "'공원 무대'",
    "way/631442844": "'농구장'",
    "way/667714296": "'중앙광장'",
    "way/545670593": "'중심광장'",
    "way/545670586": "'진입광장'",
    "way/545670584": "'휴게광장'",
    # A description standing in for a name (reader's drop; owner, 2026-10-13)
    "node/4640175680": "'운동기구집합소'",
    "node/4642314537": "'둥굴둥굴동상'",
    "node/4640011423": "'생각하는 동상'",
    "node/4640080473": "'옥구공원 입구'",
    "node/4642270072": "'송운중학교 입구'",
    "node/4642270071": "'송운초등학교 입구'",
    # An estate's own facility or marketing name (reader's drop; owner, 2026-10-13)
    "way/472440125": "'우남퍼스트빌 놀이터'",
    # A second row for one object (the surviving row named in each note) (reader's drop; owner, 2026-10-13)
    "way/648191529": "'신천성당 성전': \"Sincheon church, sanctuary\": the building inside way/648014412 신천성당, 14 m away; one church, two rows",
}
