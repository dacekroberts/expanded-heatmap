"""Gimpo-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/gimpo.md) on Gimhae's config (Incheon's SEMAS module and
OSM rail route, keyed on 시군구코드, one light metro as the city's line).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "gimpo" / "raw"
DATA_PROCESSED = ROOT / "data" / "gimpo" / "processed"
OUTPUTS = ROOT / "outputs" / "gimpo"

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
# (data/korea/raw/), as every built SEMAS city (owner, 2026-09-29; Gimpo back
# from the Gyeonggi scope, Band A, 2026-10-04).
SEMAS_SIDO = "경기도"
SEMAS_SIGUNGU = None
# 김포시: one 시, no 구. The code and the prefix 김포시 pick the identical 25,160
# rows of the 2026-06-30 edition (the brief, measured 2026-10-04).
SEMAS_SIGUNGU_CODES = ("41570",)

# --- Rail ------------------------------------------------------------------

# The register's extent plus about 2 km, taken east to 김포공항 (Seoul) so the
# whole line arrives (the brief).
OSM_BBOX = (37.54, 126.50, 37.80, 126.83)       # S, W, N, E
# One Overpass query for the city (osm-rail), split by fetch_sources.py into
# the three files below.
OSM_ALL_JSON = DATA_RAW / "osm_all.json"
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 김포시, admin_level 6 in 경기도, resolved by name 2026-10-07.
BOUNDARY_RELATION = 2409165
BOUNDARY_NAME = "김포시"
BOUNDARY_ADMIN_LEVEL = "6"
# 295 km2 measured 2026-10-07 (the brief's 277, general knowledge, is the land
# figure; the OSM polygon reaches into the Han estuary).
BOUNDARY_AREA_KM2 = (285, 305)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~126.72, the western edge 126.52) falls in the
# 126 to 132 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# The Gimpo Goldline, drawn to both ends; its stations inside Gimpo are kept
# and 김포공항 (Seoul's 강서구) is recorded as outside. The light-rail test
# passes (the brief): its own underground track, every 6 minutes all day,
# median spacing measured at step 1. NOT drawn: the lines that meet it at
# 김포공항 and Incheon's lines in the box, none with a station in Gimpo.
# The colour is OSM's tag on both relations (#957326).
# key -> (OSM ref, colour, public name, label end).
LINES = {
    "GOLD": ("김포 골드라인", "#957326", "Gimpo Goldline", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train", "tram"}
# Gate 3: the whole line, 양촌 to 김포공항: 10 stations, English Wikipedia's
# infobox (a SECONDARY source, as Ansan's and Uijeongbu's), read 2026-10-07.
LINE_STATION_COUNTS = {"Gimpo Goldline": 10}
# Every relation the box brings in that is not drawn: none has a station in
# Gimpo (step 1 prints any that does).
NOT_DRAWN = {"3": "Line 3", "5": "Line 5", "9": "Line 9", "I2": "Incheon Line 2",
             "인천1": "Incheon Line 1"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602409165)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ko",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "건영아파트앞": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "삼환아파트앞": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "신화아파트앞": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "청구아파트앞": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "효성아파트앞": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
}
# Dropped by id on the leak-word read of 2026-10-13, each id read with its cached
# name and tags (docs/decisions_drafts/search-rollout.md).
PLACE_DROPPED = {
    "node/414915406": "a glitched name (stray brackets around both the Korean and the English name), never repaired ((동변연립앞) (( Dongbyeonyeollipap ))); tags read 2026-10-13",
    # The entries below: the full read of 2026-10-13 under the owner's rulings of the
    # same day, each id read with its cached name (docs/decisions_drafts/search-rollout.md).
    # bare type: dropped in the full read (owner, 2026-10-13)
    "way/1312053620": "'게이트볼 경기장': \"gateball ground\" (full read, bare type)",
    # coded type: dropped in the full read (owner, 2026-10-13)
    "way/1120568149": "'주제공원8호': \"theme park no. 8\": a planning lot number with no district name; the type comes before the number, so the numbered-lot rule did not see it (full read, coded type)",
    # estate facility: dropped in the full read (owner, 2026-10-13)
    "way/301855864": "'삼환어린이공원': its description tag reads \"the park of the Samhwan apartments\"; no operator tag for the estate rule to read (full read, estate facility)",
    # duplicate: dropped in the full read (owner, 2026-10-13)
    "node/11274048445": "'김포장릉': a node for the royal tomb 장릉, 11 m from the tomb own row (way/480156330, which holds the article) (full read, duplicate)",
}
# Kept by the owner's word (place_index, PLACE_KEPT; owner, 2026-10-13): a famous
# place the rules pass over for want of a tag, the id read with its cached name
# (docs/decisions_drafts/search-rollout.md). Not yet confirmed by a rebuild.
PLACE_KEPT = {
    "node/4388665489": "'김포 문수산성', Munsusanseong fortress (tourism=attraction node, no Wikidata or Wikipedia tag): a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "way/1153659203": "'김포조각공원', Gimpo Sculpture Park (leisure=park that also carries tourism=theme_park): a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
}
