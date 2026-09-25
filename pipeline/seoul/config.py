"""Seoul-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/seoul.md.

Business leg: seventeen of Seoul's citywide 인허가 (permit) registers - the
national LOCALDATA licensing records, republished per permit type by the
Seoul Metropolitan Government on data.seoul.go.kr under KOGL Type 1. Every
file covers all 25 gu and carries the permit holder's building point.

Rail: the Seoul Metropolitan Subway from OpenStreetMap. The ground (osm-rail):
Korea's national urban-railway station standard dataset has station points
and NO line geometry (1,099 stations, no lines), and no agency GTFS is
published; OSM's subway relations are complete, named and coloured.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "seoul" / "raw"
DATA_PROCESSED = ROOT / "data" / "seoul" / "processed"
OUTPUTS = ROOT / "outputs" / "seoul"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# The light map for phones (mobile mode on page 43): no business dots.
HEATMAP_LITE_HTML = OUTPUTS / "heatmap_lite.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Step 1 writes the drawn lines here, one OSM-shaped relation per line.
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

# The dataset page's own SHEET export, as the page sends it when nobody is
# signed in (ssUserId=SAMPLE_VIEW is that anonymous identity, not a bypass).
# cp949 CSV, one per permit type, citywide.
SHEET_EXPORT_URL = "https://datafile.seoul.go.kr/bigfile/iot/sheet/csv/download.do"
DATASET_PAGE = "https://data.seoul.go.kr/dataList/{oa}/S/1/datasetView.do"
REGISTER_ENCODING = "cp949"

# OA id -> permit type, as the file names it. FOUND BY OA ID, NEVER BY SEARCH:
# the portal's search parameter is inert (a real term and zzzzqqq return
# byte-identical pages).
REGISTERS = {
    "OA-16094": "일반음식점",             # restaurants
    "OA-16095": "휴게음식점",             # cafés, snack bars, convenience stores
    "OA-16063": "미용업",                 # hair and beauty
    "OA-16064": "이용업",                 # barbers
    "OA-16065": "세탁업",                 # laundries
    "OA-16146": "목욕장업",               # public baths, 찜질방
    "OA-16044": "숙박업",                 # lodging - coordinate donor only
    "OA-16007": "동물병원",               # veterinary - coordinate donor only
    "OA-16084": "제과점영업",             # bakeries
    "OA-16085": "즉석판매제조가공업",      # made-on-premises food shops (delis, side dishes)
    "OA-16080": "식품판매업(기타)",        # other food sellers
    "OA-16071": "축산판매업",             # meat and livestock products
    "OA-16144": "담배소매업",             # tobacco retail
    "OA-16096": "대규모점포",             # department stores, marts, markets
    "OA-16070": "건강기능식품일반판매업",  # health-food sellers
    "OA-16089": "단란주점영업",           # karaoke bars licensed for alcohol
    "OA-16090": "유흥주점영업",           # hostess bars and cabarets - excluded
}
# The files whose rows (open or closed) lend a building point to an active row
# that has none - the brief's measured join (median 0 m on the control).
COORD_DONORS = ("OA-16094", "OA-16095", "OA-16063", "OA-16064", "OA-16065",
                "OA-16146", "OA-16044", "OA-16007")


def register_csv(oa):
    return DATA_RAW / f"{oa}.csv"


# NEVER READ. The registers carry the premises' telephone number; step 2 reads
# every other column by name and asserts this one never arrives.
NEVER_READ = ("전화번호",)

OVERPASS_URLS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
)
# Every name search bounded (osm-rail: an unbounded one is a GLOBAL search).
# The query box is Seoul plus its rim, so every drawn line's relations are
# caught; lines are drawn to their ends from the relations' own geometry.
OSM_BBOX = (37.40, 126.75, 37.73, 127.20)       # S, W, N, E
# The metropolitan network as OSM tags it on the RELATION (osm-rail: relation-
# level network filtering is safe; node-level is not).
METRO_NETWORK = "수도권 전철"
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# Seoul's own relation (서울특별시, admin_level 4), resolved by name on
# 2026-09-24 and checked by the brief; its area is gated below.
BOUNDARY_RELATION = 2297418
BOUNDARY_NAME = "서울특별시"
BOUNDARY_AREA_KM2 = (595, 615)                  # Seoul is ~605 km2

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# The registers' 좌표정보(X)/(Y): Korea's Bessel-based central belt (EPSG:5174),
# as LOCALDATA publishes it.
CRS_REGISTER = "EPSG:5174"

# UTM zone 52N: the longitude (~126.98) falls in the 126 to 132 band. Derived per city, not copied - see docs/project_context.md's
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
# The owner's call (2026-09-24): Lines 1-9, the Shinbundang Line, the Ui LRT and
# the Sillim Line, plus three Korail lines Seoul signs as subway - Gyeongui-
# Jungang, Suin-Bundang and Gyeongchun (their spacing inside Seoul, 1.25-1.39 km,
# sits within the subway's own). NOT drawn: AREX (all-stop and express), GTX-A,
# the Seohae Line and the Gimpo Goldline (one-station stubs in Seoul), and lines
# that never enter Seoul. Stations inside Seoul only; lines drawn to their ends.
#
# Matched on the RELATION's ref (osm-rail: relation-level filtering is safe),
# after printing the table. key -> (OSM ref, colour, public name, label end).
# The colours are the operators' own, as every relation carries them.
LINES = {
    "L1": ("1", "#004A85", "Line 1", None),
    "L2": ("2", "#00A23F", "Line 2", None),
    "L3": ("3", "#ED6C00", "Line 3", None),
    "L4": ("4", "#009BCE", "Line 4", None),
    "L5": ("5", "#794698", "Line 5", None),
    "L6": ("6", "#7C4932", "Line 6", None),
    "L7": ("7", "#6E7E31", "Line 7", None),
    # Seoul Metro's #D11D70 darkened, hue kept: Delta-E 9.2 -> 18.0 from Food
    # service's magenta, the nearest colour drawn over it (linecolour.py).
    "L8": ("8", "#92144E", "Line 8", None),
    "L9": ("9", "#A49D87", "Line 9", None),
    "SBD": ("신분당", "#B81B30", "Shinbundang Line", None),
    "UI": ("W", "#BACC50", "Ui LRT", None),
    "SL": ("Silim", "#6789CA", "Sillim Line", None),
    "GJ": ("경의·중앙", "#6AC2B3", "Gyeongui–Jungang Line", None),
    "SB": ("수인·분당", "#ECA300", "Suin–Bundang Line", None),
    "GC": ("경춘", "#007A62", "Gyeongchun Line", None),
}
# Where the drawn colour differs from the one OSM carries, OSM's (step 1 checks
# every relation still carries it).
OSM_COLOUR = {"L8": "#D11D70"}
LINES_ROUTE_TYPES = {"subway", "light_rail", "train"}
NOT_DRAWN = {
    "공항철도": "AREX", "GTX-A": "GTX-A", "서해": "Seohae Line",
    "김포 골드라인": "Gimpo Goldline", "경강": "Gyeonggang Line",
    "U": "Uijeongbu LRT", "I2": "Incheon Line 2",
}
# Undrawn relations that carry no ref, placed by their name's prefix.
NOT_DRAWN_BY_NAME = {"의정부경전철": "U"}
# Stop nodes whose OSM name is wrong, corrected BY NODE ID with the evidence.
# 9459739637 (Ui LRT, southbound) is tagged 삼양 but stands at 삼양사거리: the
# northbound stop node there (4852989066) and the station object (9459739612)
# both say 삼양사거리, 6 m away, while 삼양 is 680 m north (2026-09-24).
STOP_NAME_FIX = {9459739637: "삼양사거리"}
# One interchange under two names: Line 4 signs it 총신대입구(이수), Line 7 이수;
# the two stop groups are 191 m apart and share the transfer (2026-09-24).
KEY_ALIASES = {"이수": "총신대입구"}
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

# Sanity bounds for the projected points: Seoul's extent plus a margin.
SEOUL_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
