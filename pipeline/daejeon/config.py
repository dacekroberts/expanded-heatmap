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

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602349984)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ko",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "계룡아파트삼거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "롯데마트삼거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "리베라호텔네거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
}
# Dropped by id on the full read of 2026-10-13 under the owner's rulings of the
# same day, each id read with its cached name (docs/decisions_drafts/search-rollout.md).
PLACE_DROPPED = {
    # glitched: dropped in the full read (owner, 2026-10-13)
    "node/462083659": "'(... Fortress)': a name cut down to an ellipsis and one English word (full read, glitched)",
    # bare type: dropped in the full read (owner, 2026-10-13)
    "way/687287292": "'sadang': \"sadang\" is the Korean word for a shrine, romanised (full read, bare type)",
    "node/4631163316": "'절': \"temple\" (full read, bare type)",
    "way/496707703": "'본당': \"main hall\" (full read, bare type)",
    "way/1533010772": "'워쉽센터': \"worship center\", no congregation named (full read, bare type)",
    "way/840863353": "'기념광장': \"memorial plaza\" (full read, bare type)",
    "way/840863355": "'진입광장': \"entrance plaza\", 213 m from 기념광장 (full read, bare type)",
    "way/472045058": "'원형광장': \"circular plaza\" (full read, bare type)",
    "way/1212175831": "'중정': \"courtyard\" (full read, bare type)",
    "way/1149063414": "'캠핑장': \"campsite\" (full read, bare type)",
    "way/472143829": "'유수지': \"retention basin\" (full read, bare type)",
    "way/499258562": "'유수지': \"retention basin\" (full read, bare type)",
    # description: dropped in the full read (owner, 2026-10-13)
    "way/1346324317": "'도서관 앞 마당': \"yard in front of the library\" (full read, description)",
    "way/1316464421": "'고려시대 건물터': \"building site of the Goryeo period\": a caption, no site name (full read, description)",
    "node/4902307746": "'고려시대 도로': \"road of the Goryeo period\": a caption (full read, description)",
    "node/4912416078": "'청동기시대 집자리 유적': \"Bronze Age dwelling remains\": a caption (full read, description)",
    "node/4643402883": "'구봉중 농구장': \"Gubong Middle School basketball court\": a school's court tagged a stadium (full read, description)",
    # estate facility: dropped in the full read (owner, 2026-10-13)
    "way/469676883": "'4단지 광장': \"complex 4 plaza\": named only by an apartment block number (full read, estate facility)",
    "way/469664013": "'5단지 공원': \"complex 5 park\": named only by an apartment block number (full read, estate facility)",
    # duplicate: dropped in the full read (owner, 2026-10-13)
    "way/499318498": "'자광사 본당': the main hall of 자광사, 11 m from the temple's own row (full read, duplicate)",
    "way/499318499": "'자광사 일주문': the gate of 자광사, 38 m from the temple's own row (full read, duplicate)",
    # religious education hall: dropped in the full read (owner, 2026-10-13)
    "way/584945724": "'증산도교육문화회관': the Jeungsando education and culture hall (full read, religious education hall)",
    # worship by denomination: dropped in the full read (owner, 2026-10-13)
    "way/584742321": "'예수 그리스도 후기 성도 교회': the Church of Jesus Christ of Latter-day Saints, the body's name alone (full read, worship by denomination)",
    # article of its kind: dropped in the full read (owner, 2026-10-13)
    "node/8395631086": "'평화의 소녀상': a local copy carrying the article of the Seoul original; public art with no article of its own (full read, article of its kind)",
    # unsure in the full read, dropped by ruling 2: a religious body's meeting hall or branch tagged a place of worship (owner, 2026-10-13)
    "node/6085773378": "'대철회관': 대철회관, a diocese's hall (회관) tagged a place of worship (my reading: a diocese is a body) (unsure in the full read; ruling 2)",
    # Twin round 1 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/584742322": "'예수 그리스도 후기 성도 교회': the twin of way/584742321; worship by denomination: dropped in the full read (owner, 2026-10-13)",
    "way/472148695": "'유수지': the twin of way/472143829; bare type: dropped in the full read (owner, 2026-10-13)",
    "way/840863360": "'진입광장': the twin of way/840863355; bare type: dropped in the full read (owner, 2026-10-13)",
    # Twin round 2 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/584742323": "'예수 그리스도 후기 성도 교회': the twin of way/584742321; worship by denomination: dropped in the full read (owner, 2026-10-13)",
}
# Kept by the owner's word (place_index, PLACE_KEPT; owner, 2026-10-13): a famous
# place the rules pass over for want of a tag, the id read with its cached name
# (docs/decisions_drafts/search-rollout.md). Not yet confirmed by a rebuild.
PLACE_KEPT = {
    "way/30614864": "'한밭수목원동', Hanbat Arboretum, east garden (leisure=garden, no Wikidata or Wikipedia tag): a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "way/30614866": "'한밭수목원서', Hanbat Arboretum, west garden (leisure=garden, no Wikidata or Wikipedia tag): a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "way/68169809": "'대전오월드', O-World (tourism=theme_park, no Wikidata or Wikipedia tag): a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
}
