"""Busan-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/busan.md.

Business leg: fourteen of the national LOCALDATA permit registers, served by
the city's keyless LocalDataService Open API on Big-데이터웨이브
(data.busan.go.kr), citywide across all 16 구·군, frozen at 2026-04-15 (the
rows agree). Seoul's register under Seoul's rules, read through
pipeline/countries/korea.py.

Rail: Busan Metro Lines 1-4 and the Busan-Gimhae LRT from OpenStreetMap, as
Seoul's and Daegu's. No GTFS is published.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "busan" / "raw"
DATA_PROCESSED = ROOT / "data" / "busan" / "processed"
OUTPUTS = ROOT / "outputs" / "busan"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Step 1 writes the drawn lines here, one OSM-shaped relation per line.
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

API_URL = "https://data.busan.go.kr/open/services/LocalDataService/{op}"
PAGE_SIZE = 1000
# The feed is frozen: every operation's newest updatedt is 2026-04-15 and the
# rows agree (restaurant permits every month to 2026-04). Stated on the page.
SNAPSHOT = "2026-04-15"

# file key -> (permit type, API operation, opnSvcId).
# 🚨 NEVER pass `state`: rows permitted after 2025-01-31 carry no status code,
# so state=01 drops every one of them (8,804 open premises). Every type is
# pulled IN FULL and step 2 keeps trdstatenm == 영업/정상 itself; the closed
# rows are the donor join's.
# 🚨 ALWAYS pass opnSvcId: LocalDstrb's default answer never includes
# 대규모점포. (The brief, "Two parameter traps".)
REGISTERS = {
    "ilban": ("일반음식점", "LocalRstrn", "07_24_04_P"),
    "hyuge": ("휴게음식점", "LocalRstrn", "07_24_05_P"),
    "danran": ("단란주점영업", "LocalBar", "07_23_01_P"),
    "miyong": ("미용업", "LocalBtyIndst", "05_18_01_P"),
    "iyong": ("이용업", "LocalSrvcIndst", "05_19_01_P"),
    "setak": ("세탁업", "LocalLndry", "06_20_01_P"),
    "mogyok": ("목욕장업", "LocalBths", "11_44_01_P"),
    "dambae": ("담배소매업", "LocalTobaco", "11_43_02_P"),
    "chuksan": ("축산판매업", "LocalStore", "07_22_04_P"),
    "geongi": ("건강기능식품일반판매업", "LocalStore", "07_22_03_P"),
    "daegyumo": ("대규모점포", "LocalDstrb", "08_25_01_P"),
    "jegwa": ("제과점영업", "LocalStore", "07_22_18_P"),
    "jeuksuk": ("즉석판매제조가공업", "LocalStore", "07_22_19_P"),
    "sikpum": ("식품판매업(기타)", "LocalStore", "07_22_13_P"),
}


def register_json(key):
    _, op, svc = REGISTERS[key]
    return DATA_RAW / f"{op}_{svc}_all.json"


# The files whose rows (open or closed) lend a building point to an active row
# that has none - Seoul's donor rule, as Daegu's.
COORD_DONORS = ("ilban", "hyuge", "miyong", "iyong", "setak", "mogyok")

# NEVER READ. Busan's telephone field is `sitetel`; korea.read_register refuses
# a phone column NEVER_READ does not name. Also never selected: the rights
# holder's serial (LocalStore), building tenure and rent.
NEVER_READ = ("sitetel", "rgtmbdsno", "bdngownsenm", "monam")

# The API's lowercase field codes, under the names korea.FIELDS resolves.
FIELD_RENAME = {
    "mgtno": "관리번호", "trdstatenm": "영업상태명", "bplcnm": "사업장명",
    "rdnwhladdr": "도로명전체주소", "sitewhladdr": "소재지전체주소",
    "x": "좌표정보X(EPSG5174)", "y": "좌표정보Y(EPSG5174)",
    "uptaenm": "업태구분명", "sntuptaenm": "위생업태명",
}

# Registers whose addresses the PUBLISHER masks with * - every house number in
# the health-food register (6,263 of 6,263 open rows), as Daegu's.
MASKED_ADDRESS_FILES = ("geongi",)

# The address prefix every in-city row carries; 기장군 is a 군.
CITY_PREFIX = "부산광역시"

# Overpass is fetched through pipeline/osm.py (its hosts and its three checks).
# Busan with the Yangsan end of Line 2 and the Gimhae end of the LRT (the
# brief's box, taken south to the islands).
OSM_BBOX = (34.85, 128.75, 35.45, 129.35)       # S, W, N, E
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 부산광역시, admin_level 4, resolved by name 2026-09-27 and checked by the
# brief. Its polygon holds territorial water: ~2,020 km2 against ~770 of land.
BOUNDARY_RELATION = 2396450
BOUNDARY_NAME = "부산광역시"
BOUNDARY_AREA_KM2 = (1990, 2050)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# The API's x/y: Korea's Bessel-based central belt (EPSG:5174), as Seoul's and
# Daegu's (the brief: 97,260 open points inside Busan, 2 outside).
CRS_REGISTER = "EPSG:5174"

# UTM zone 52N: the longitude (~129.08) falls in the 126 to 132 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# The owner's calls (2026-09-27): Lines 1-4 and the Busan-Gimhae LRT; 동해선
# (Korail's 부전-태화강 commuter line) out on spacing - 16 stops in Busan at a
# mean 2.29 km against the city lines' 0.86-1.09 km. Stations inside Busan only
# (Line 2's 5 in Yangsan and the LRT's 12 in Gimhae excluded); lines drawn to
# their ends.
#
# Matched on the RELATION's route type and ref, NEVER on network: 동해선
# (Korail-run) is tagged 부산 도시철도 like the city's lines.
# key -> (OSM ref, colour, public name, label end). Operator colours.
LINES = {
    "L1": ("1", "#F06A00", "Line 1", None),
    "L2": ("2", "#81BF48", "Line 2", None),
    "L3": ("3", "#BB8C00", "Line 3", None),
    # The operator's #217DCB darkened, hue kept: Delta-E 10.8 -> 31.8 from
    # Retail's blue (linecolour.py; 10.8 clears the floor of 10 but reads as the
    # same blue - Calgary's lesson). Daegu's Line 2 was settled at 32.3.
    "L4": ("4", "#144B7A", "Line 4", None),
    "BGL": ("BGL", "#8652A1", "Busan–Gimhae LRT", None),
}
# Where the drawn colour differs from the one OSM carries, OSM's (step 1 checks
# every relation still carries it).
OSM_COLOUR = {"L4": "#217DCB"}
# Line 4 is a MONORAIL (route=monorail), as Daegu's Line 3.
LINES_ROUTE_TYPES = {"subway", "monorail", "light_rail", "train", "tram"}
# Gate 3: each WHOLE line's station count, termini to termini (inside Busan and
# out). Korean Wikipedia's 부산 도시철도 and 부산김해경전철 articles, read
# 2026-09-27 - a SECONDARY source, as Daegu's: Humetro's own pages were not
# read. (Wikipedia's Busan/Gimhae split of the LRT sums to 19, not 21, so it
# cannot decide scope; the boundary polygon does.)
LINE_STATION_COUNTS = {"Line 1": 40, "Line 2": 43, "Line 3": 17, "Line 4": 14,
                       "Busan–Gimhae LRT": 21}
NOT_DRAWN = {"동해": "동해선 (Donghae Line)"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
KEY_ALIASES = {}
# Which tag carries the English name, in order (cjk-text: print the coverage).
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
# Stop nodes of one Korean name are one station when they chain within this
# distance; further apart they are separate stations that share a name.
COLLAPSE_LINK_M = 500.0
# A line is drawn from its longest relation plus the track another relation adds
# further than this from what is already drawn (Hong Kong's rule).
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "korea_localdata"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"
ACTIVE_STATUS = "영업/정상"

# Sanity bounds for the projected points: the query box.
BUSAN_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
