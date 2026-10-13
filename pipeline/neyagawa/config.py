"""Neyagawa-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/neyagawa.md. Japan A/B batch (Kansai-2, 2026-10-11), on
the shared modules (pipeline/countries/japan*.py) and the Japan foundation's
rules (ALL_RULES).

Business leg: the city's own three lists on BODIK (organization 272159; a
core city licenses its own premises): 理容所確認施設一覧, 美容所確認施設一覧 and
クリーニング所確認施設一覧, each one full list as of 2026-08-31. One bucket,
Personal services (owner, 2026-10-06, call 114): the city publishes no food
permit list. Placed by a JOIN to MLIT's 位置参照情報 for the one municipality
(27215, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Keihan's Main Line, cut at the city line, and JR West's Gakkentoshi
Line, a one-station stub kept as cut (owner, 2026-10-06, the band row).
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "neyagawa" / "raw"
DATA_PROCESSED = ROOT / "data" / "neyagawa" / "processed"
OUTPUTS = ROOT / "outputs" / "neyagawa"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Neyagawa"
SLUG = "neyagawa"
MUNICIPALITY = "寝屋川市"
PREFECTURE = "大阪府"

# The city's three BODIK packages, CC BY 4.0 by 寝屋川市オープンデータ利用規約 and
# BODIK's terms 第1条 (DECISIONS.md, "Licence reads for the Japan builds").
# Each package keeps one FULL list per month, never an additions file: the
# newest edition is the register, and a new month is a new resource under a
# new file name (re-measure then).
_BODIK = "https://data.bodik.jp/dataset/"
SOURCE_FILES = {
    "barber": ("272159_barber_20260831.csv",
               _BODIK + "d7f05be4-01d8-4150-8b9b-c5146a906187/resource/1eea6cda-ffbd-4d7a-9b3b-f740ad231aca/"
               "download/272159_barber_20260831.csv",
               "https://data.bodik.jp/dataset/272159_barber"),
    "beauty": ("272159_hair_dressing_20260831.csv",
               _BODIK + "aa79fd70-d439-4bbf-b393-b94e2f7fa385/resource/19110291-e84f-44fe-814f-d26f1cd70cd9/"
               "download/272159_hair_dressing_20260831.csv",
               "https://data.bodik.jp/dataset/272159_hair_dressing"),
    "laundry": ("272159_cleaning_20260831.csv",
                _BODIK + "71f93e97-3a93-479c-a634-106367c70b85/resource/3824bb1f-7b7b-4fba-9481-cf954a955caf/"
                "download/272159_cleaning_20260831.csv",
                "https://data.bodik.jp/dataset/272159_cleaning"),
}
# The resource names' own date (令和8年8月31日時点), never the download's. The
# lists shrink as well as grow between editions, so each is a snapshot.
REGISTERS_AS_OF = "2026-08-31"
SOURCE_AS_OF = {k: REGISTERS_AS_OF for k in SOURCE_FILES}
FOOD_AS_OF = None  # no food leg: the city publishes no food permit list
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: cp932, comma-separated, one header row.
SOURCE_ENCODING = {k: "cp932" for k in SOURCE_FILES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 営業者名称（法人の場合は代表者氏名） (a sole trader's own
# name, or a company's representative) and 法人営業者名称 are REQUIRED so the
# name rule (japan_register.name_is_operator; owner 2026-09-27) cannot
# silently compare nothing; they are read IN MEMORY by that rule only, never
# kept. Never selected: 施設電話番号, 営業者所在地（法人のみ）.
REQUIRED_COLUMNS = {k: ("施設名称", "施設所在地", "営業種別", "営業者名称（法人の場合は代表者氏名）", "法人営業者名称")
                    for k in SOURCE_FILES}


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 27215.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Neyagawa.
# S, W, N, E: the city's N03 extent (S 34.728, W 135.587, N 34.792, E 135.663)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.72, 135.58, 34.80, 135.67)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word.
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.63) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the four
# stations stand 2.0 to 3.1 km from their nearest neighbour (the brief).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# the brief: 2 lines, no Shinkansen), each cut at the city line (owner
# 2026-09-24): Keihan's 京阪本線 (3 of 41) and JR West's 片町線, signed the JR
# Gakkentoshi Line (1 of 24: 寝屋川公園). A JR one-station stub stays as cut
# (owner 2026-09-27; the band row, 2026-10-06): no other line serves it.
LEFT_OUT_LINES = {}
# The Gakkentoshi Line and Keihan run on into Kyoto Prefecture: its N03 names
# the stations beyond the prefecture line (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("26",)
# No interchange: four stations, four groups.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the JR line as 片町線; JR West
# signs it the Gakkentoshi Line (学研都市線), as on Hirakata's map.
_KH, _JR = "京阪電気鉄道", "西日本旅客鉄道"
LINES = {
    "KM": {"n02": [(_KH, "京阪本線")], "name": "Keihan Main Line", "name_ja": "京阪本線", "short": "Keihan",
           "hue": "#7B7B5A"},
    "JG": {"n02": [(_JR, "片町線")], "name": "JR Gakkentoshi Line", "name_ja": "学研都市線", "short": "JR",
           "hue": "#C000A8"},
}
# Colours: both lines are drawn on another city's map too, so each takes its
# one site-wide colour from pipeline/line_registry.py (owner, 2026-10-07: one
# colour per line on every map), never a value of this city's own.
_COLOURS = {
    "KM": line_registry.colour("keihan-main-line"),
    "JG": line_registry.colour("jr-west-gakkentoshi-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station lists inside the city (the brief: Keihan
# 萱島, 寝屋川市, 香里園; JR 寝屋川公園).
GATE3 = {"source": "Keihan's line timetable and JR West's station timetable pages, read 2026-10-06",
         "lines": {"KM": 3, "JG": 1}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
NEYAGAWA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = NEYAGAWA_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600358691)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
PLACE_DROPPED = {}
