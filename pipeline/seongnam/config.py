"""Seongnam-specific settings, scoped to one city per this project's
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
DATA_RAW = ROOT / "data" / "seongnam" / "raw"
DATA_PROCESSED = ROOT / "data" / "seongnam" / "processed"
OUTPUTS = ROOT / "outputs" / "seongnam"

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
SEMAS_SIGUNGU = ("성남시",)   # 시군구명 prefix: the city and its 구

# --- Rail ------------------------------------------------------------------

OSM_BBOX = (37.31, 127.01, 37.49, 127.22)       # S, W, N, E: the city plus about 2 km
# The Korail lines the metropolitan subway signs (route=train), queried by ref
# beside every subway, light-rail and monorail relation in the box.
OSM_TRAIN_REFS = ('수인·분당', '경의·중앙', '경강', '서해', 'GTX-A', '경춘')
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 성남시, admin_level 6, resolved by name 2026-09-29.
BOUNDARY_RELATION = 2409180
BOUNDARY_NAME = "성남시"
# 142 km2 measured 2026-09-29.
BOUNDARY_AREA_KM2 = (138, 146)

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
    # Seoul Metro's #D11D70 darkened, hue kept, as Seoul draws it (Delta-E 9.2 ->
    # 18.0 from Food service's magenta).
    "L8": ("8", line_registry.colour("seoul-subway-line-8"), "Line 8", None),
    "SB": ("수인·분당", line_registry.colour("suin-bundang-line"), "Suin–Bundang Line", None),
    "SBD": ("신분당", line_registry.colour("shinbundang-line"), "Shinbundang Line", None),
    "GG": ("경강", "#0B318F", "Gyeonggang Line", None),
}
OSM_COLOUR = {"L8": "#D11D70"}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train"}
# Gate 3: each WHOLE line's station count, English Wikipedia's line infoboxes
# read 2026-09-29 (a SECONDARY source, as Busan's).
# The Gyeonggang Line is left out of the whole-line gate: its infobox counts 18
# stations, more than the metropolitan section Pangyo-Yeoju OSM carries (11).
# Line 8 is left out too: OSM carries its 24 stations (Amsa-Moran and the
# Byeollae extension), the infobox reads 25.
LINE_STATION_COUNTS = {"Suin–Bundang Line": 63, "Shinbundang Line": 16}
NOT_DRAWN = {"GTX-A": "GTX-A", "3": "Line 3"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

CITY_PREFIX = "경기도 성남시"
TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602409180)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ko",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "두산아파트앞삼거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "한신아파트삼거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "환승주차장삼거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
}
# Dropped by id on the full read of 2026-10-13 under the owner's rulings of the
# same day, each id read with its cached name (docs/decisions_drafts/search-rollout.md).
PLACE_DROPPED = {
    # estate facility: dropped in the full read (owner, 2026-10-13)
    "way/850079175": "'12단지 주공공원': the park of an apartment estate's block 12 (Jugong), tagged park (full read, estate facility)",
    "way/842276167": "'3단지 관리사무소 앞 공원': describes a spot inside an apartment estate (the park in front of block 3's management office) (full read, estate facility)",
    "way/842276653": "'3단지 테니스장 공터': describes a spot inside an apartment estate (the empty lot by block 3's tennis court) (full read, estate facility)",
    "way/842499612": "'건영 3단지 공원': the park of one apartment estate block (Geonyeong block 3) (full read, estate facility)",
    "way/472844688": "'매화1단지 놀이터': the playground of one apartment estate block (Maehwa block 1) (full read, estate facility)",
    "way/471318610": "'하얀마을 놀이터': the playground of an apartment village (Hayan maeul), tagged park (full read, estate facility)",
    "way/890919704": "'청구 5단지 테니스장': the tennis court of one apartment estate block (Cheonggu block 5), tagged park (full read, estate facility)",
    "way/1352026618": "'봇들마을 5단지 광장': the square of one apartment estate block (Botdeul maeul block 5) (full read, estate facility)",
    "way/850136104": "'주공 소공원': small park named only for the estate builder (Jugong) (full read, estate facility)",
    "way/1493282006": "'진경산수원': a garden whose operator tag is an apartment complex (full read, estate facility)",
    # business: dropped in the full read (owner, 2026-10-13)
    "node/4648779486": "'NAVER': a company's name on a node tagged monument (full read, business)",
    # bare type: dropped in the full read (owner, 2026-10-13)
    "way/468337416": "'부처석상': whole name is a type (stone Buddha statue), tagged place of worship (full read, bare type)",
    "way/437236113": "'잔디광장': whole name is a type (lawn plaza) (full read, bare type)",
    "way/429223452": "'저류지': whole name is a type (retention basin), tagged park (full read, bare type)",
    "way/882707364": "'가로공원': whole name is a type (street park) (full read, bare type)",
    # glitch: dropped in the full read (owner, 2026-10-13)
    "node/4652816469": "'연정교회(예전이름)': mapper's note (former name) glued to the name (full read, glitch)",
    "way/1180292474": "'판교 꿈꾸는교': name cut one syllable short of the word for church (full read, glitch)",
    # religious residence: dropped in the full read (owner, 2026-10-13)
    "node/11942351602": "'정토사 요사채 염불원': the monks' quarters and chanting hall of a temple that has its own row, tagged place of worship (full read, religious residence)",
    # religious office: dropped in the full read (owner, 2026-10-13)
    "node/8116836672": "'금광교회 비전센터': a church's vision centre (an education and office hall), tagged place of worship (full read, religious office)",
    "node/13440336213": "'하나님의교회 세계복음선교협회 총회': a denomination's general assembly office (office=religion); the wikidata is the body's (full read, religious office)",
    # estate: dropped in the full read (owner, 2026-10-13)
    "node/9174471900": "'남서울파크힐': one gated housing estate under its marketing name, mapped as a hamlet (full read, estate)",
    # unsure in the full read, dropped by ruling 5: a stock plaza or rest-area name with no place in it (owner, 2026-10-13)
    "way/1059805491": "'종합광장': 종합광장, general plaza, no place in it (unsure in the full read; ruling 5)",
}
