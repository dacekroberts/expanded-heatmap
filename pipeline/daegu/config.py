"""Daegu-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/daegu.md.

Business leg: fourteen of the national LOCALDATA permit registers, republished
monthly by the city on D-데이터허브 (data.daegu.go.kr) as XLSX, citywide across
all 9 authorities. Seoul's register under Seoul's rules, read through
pipeline/countries/korea.py, which refuses the renamed columns and the blank
sub-type column that Seoul's step 2 would read as nothing.

Rail: Daegu Metro Lines 1-3 from OpenStreetMap, as Seoul's. Korea's station
dataset lacks Daegu Metro, and no GTFS is published.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "daegu" / "raw"
DATA_PROCESSED = ROOT / "data" / "daegu" / "processed"
OUTPUTS = ROOT / "outputs" / "daegu"

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

# The dataset page's own download button (no account). The body is the XLSX.
FILE_DOWN_URL = "https://data.daegu.go.kr/cmm/fms/FileDown.do?atchFileId={file_id}&fileSn=0"
DATASET_PAGE = "https://data.daegu.go.kr/open/data/dataView.do?dataSetId={dataset}&provdMethod=FILE"
# The monthly edition. EVERY MONTH IS A NEW SET OF DATASET AND FILE IDS, so the
# edition is pinned here and stated on the page; a new month is a config change.
EDITION = "2026-08"

# file key -> (permit type as the file names it, group dataset, file id).
# FOUND BY ID: the 2026-08 edition is 36 group datasets in four id blocks
# (119500-09, 119560-69, 119600-09, 119690-95), and the personal-services and
# bar files are in the first two (the brief, "Enumerate by id").
REGISTERS = {
    "ilban": ("일반음식점", "DMI_0000119607", "FILE_000000000033041"),       # restaurants
    "hyuge": ("휴게음식점", "DMI_0000119607", "FILE_000000000033040"),       # cafés, snack bars
    "danran": ("단란주점영업", "DMI_0000119565", "FILE_000000000032961"),    # karaoke bars
    "miyong": ("미용업", "DMI_0000119690", "FILE_000000000033054"),          # hair and beauty
    "iyong": ("이용업", "DMI_0000119503", "FILE_000000000032908"),           # barbers
    "setak": ("세탁업", "DMI_0000119502", "FILE_000000000032906"),           # laundries
    "mogyok": ("목욕장업", "DMI_0000119561", "FILE_000000000032951"),        # public baths
    "dambae": ("담배소매업", "DMI_0000119695", "FILE_000000000033094"),      # tobacco retail
    "chuksan": ("축산판매업", "DMI_0000119604", "FILE_000000000033004"),     # meat sellers
    "geongi": ("건강기능식품일반판매업", "DMI_0000119604", "FILE_000000000033013"),  # health food
    "daegyumo": ("대규모점포", "DMI_0000119605", "FILE_000000000033024"),    # large stores
    # Pages 3-4 of 119604's file list, which the portal shows six to a page -
    # missed by the first brief, corrected 2026-09-27 (24dc747).
    "jegwa": ("제과점영업", "DMI_0000119604", "FILE_000000000033020"),       # bakeries
    "jeuksuk": ("즉석판매제조가공업", "DMI_0000119604", "FILE_000000000033002"),  # delis, side dishes
    "sikpum": ("식품판매업(기타)", "DMI_0000119604", "FILE_000000000032999"),  # other food sellers
}


def register_xlsx(key):
    return DATA_RAW / f"dg_{key}_{EDITION.replace('-', '')}.xlsx"


# The files whose rows (open or closed) lend a building point to an active row
# that has none - Seoul's donor rule. Lodging and veterinary clinics were
# Seoul's extra donors; they are not downloaded here.
COORD_DONORS = ("ilban", "hyuge", "miyong", "iyong", "setak", "mogyok")

# NEVER READ. Daegu's telephone column is 소재지전화 (Seoul's is 전화번호);
# korea.read_register refuses a header whose phone column is not named here.
# The rest are never selected: the rights holder's serial (축산판매업), and
# tenure and rent.
NEVER_READ = ("소재지전화", "권리주체일련번호", "건물소유구분명", "보증액", "월세액")

# Registers whose addresses the PUBLISHER masks with * - every house and unit
# number in the health-food file (4,616 of 4,616 open rows, 2026-09-27; 98% of
# them still carry a point). korea.building_keys raises on masking anywhere else.
MASKED_ADDRESS_FILES = ("geongi",)

# The address prefix every in-city row carries. 달성군 and 군위군 are 군, not
# 구: the building-key regex matches [구군] (korea.py raises if it misses).
CITY_PREFIX = "대구광역시"

# Overpass is fetched through pipeline/osm.py (its hosts and its three checks).
# Every name search bounded (osm-rail: an unbounded one is a GLOBAL search).
# Daegu with 군위군 and the Gyeongsan ends of Lines 1 and 2 (the brief's box).
OSM_BBOX = (35.55, 128.35, 36.35, 128.85)       # S, W, N, E
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 대구광역시, admin_level 4, resolved by name on 2026-09-27 and checked by the
# brief; its area is gated below.
BOUNDARY_RELATION = 2395674
BOUNDARY_NAME = "대구광역시"
BOUNDARY_AREA_KM2 = (1480, 1510)                # 1,495 km2 with 군위군

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# The registers' 좌표정보X(EPSG5174)/Y: Korea's Bessel-based central belt, as
# the column names themselves say.
CRS_REGISTER = "EPSG:5174"

# UTM zone 52N: the longitude (~128.60) falls in the 126 to 132 band. Derived per city, not copied - see docs/project_context.md's
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
# The owner's calls (2026-09-27): Lines 1, 2 and 3 only; 대경선 (Korail's
# Gumi-Daegu-Gyeongsan line) out on spacing - 3 stops in Daegu, a mean 4.08 km
# apart against the subway's 0.77-1.07 km, as Seoul's AREX (3.37 km) was.
# Stations inside Daegu only (5 on Lines 1 and 2 are in Gyeongsan); lines
# drawn to their ends.
#
# Matched on the RELATION's route type and ref, NEVER on network: Lines 1-2
# read 대구 도시철도, Line 3 대구도시철도, and 대경선 (Korail-run) is tagged
# 대구 도시철도 too. key -> (OSM ref, colour, public name, label end).
# The colours are the operator's own, as every relation carries them.
LINES = {
    "L1": ("1", "#D93F5C", "Line 1", None),
    # The operator's #00AA80 darkened, hue kept: Delta-E 6.2 -> 32.3 from
    # Personal services' green (linecolour.py; the floor is 10, the preferred
    # 45, which only a near-black #004433 reaches). Line 1's red is kept at
    # 14.7 from Food service, as Seoul's Line 8 was kept at 18.0.
    "L2": ("2", "#00664D", "Line 2", None),
    "L3": ("3", "#FFB100", "Line 3", None),
}
# Where the drawn colour differs from the one OSM carries, OSM's (step 1 checks
# every relation still carries it).
OSM_COLOUR = {"L2": "#00AA80"}
# Line 3 is a MONORAIL (route=monorail). Seoul's query asks for
# subway|light_rail|train and would lose it without an error.
LINES_ROUTE_TYPES = {"subway", "monorail", "light_rail", "train", "tram"}
# Gate 3: each WHOLE line's station count, termini to termini (inside Daegu and
# out). The operator's own sources could not be read from here on 2026-09-27
# (dtro.or.kr's route map renders blank, data.go.kr refuses the connection, and
# the city's own route map is dated 2022, before the Hayang extension), so these
# are Korean Wikipedia's infoboxes read that day - a SECONDARY source, stated as
# one. Wikipedia's table also puts 대구한의대병원 in Gyeongsan; OSM's boundary
# puts it 614 m inside 동구, and the polygon, not a list, decides scope here.
LINE_STATION_COUNTS = {"Line 1": 35, "Line 2": 29, "Line 3": 30}
NOT_DRAWN = {"대경": "대경선 (Daegyeong Line)"}
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

# Sanity bounds for the projected points: the query box (Daegu plus its rim).
DAEGU_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
