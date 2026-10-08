"""Yokosuka-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/yokosuka.md
(12/12 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py), in Kawasaki's shape: the city's own lists, all
three buckets.

Business leg: the city's CC BY 4.0 lists on BODIK (民生局健康部保健所生活衛生課):
every food permit in force at 2026-08-31, and full barber, beauty and two
laundry lists (general and pick-up) of 2026-08, placed by a JOIN to MLIT's
位置参照情報 for the one municipality (no wards). MHLW's open data for
Yokosuka holds only the opt-in online filings (3.8% of the official
restaurant count): a control, never a source.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03). Keikyu's Main and Kurihama Lines and JR East's Yokosuka Line;
no Shinkansen. English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "yokosuka" / "raw"
DATA_PROCESSED = ROOT / "data" / "yokosuka" / "processed"
OUTPUTS = ROOT / "outputs" / "yokosuka"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Yokosuka"
SLUG = "yokosuka"
MUNICIPALITY = "横須賀市"
PREFECTURE = "神奈川県"

# The city's two BODIK datasets (organization 142018), both license_id
# cc-by-40-intl; the catalogue's terms (odcs.bodik.jp/142018/tos/) 第１条
# grant CC BY 4.0 International. The city's own page says the licence covers
# the catalogue's copies only, so every file comes from data.bodik.jp, never
# the city's site (read 2026-10-02).
BODIK = "https://data.bodik.jp"
BODIK_API = BODIK + "/api/3/action"
FOOD_PAGE = BODIK + "/dataset/142018_00_18_syokuhin_all"
ENV_PAGE = BODIK + "/dataset/142018_00_19_environmental_sanitation_facilities"
_FOOD_DS = BODIK + "/dataset/3a1aaf46-e6ca-41fa-8977-3388f3b7e3ba/resource/"
_ENV_DS = BODIK + "/dataset/76f9d975-d773-486b-b7ad-48d046a4a696/resource/"
# source key -> (file, URL of the edition this build read, the dataset page
# that carries its licence). Every file is RENAMED each month (syoku08.csv,
# ..._202608.xlsx) under a stable resource id, so fetch_sources.py reads each
# resource's current URL from CKAN (SOURCE_RESOURCES) and the pinned URL
# records which edition the build read.
SOURCE_FILES = {
    "food": ("syoku08.csv", _FOOD_DS + "4c06c4b1-84de-4c4c-af65-fff85a7963e4/download/syoku08.csv", FOOD_PAGE),
    "barber": ("riyouzyo_202608.xlsx",
               _ENV_DS + "d888225b-47f9-431a-9fcd-de53153e6eb9/download/riyouzyo_202608.xlsx", ENV_PAGE),
    "beauty": ("biyouzyo_202608.xlsx",
               _ENV_DS + "0e4a4287-f846-4ba2-aa09-1cbbd554ddba/download/biyouzyo_202608.xlsx", ENV_PAGE),
    "laundry_general": ("kuri-ninngu_ippann_202608.xlsx",
                        _ENV_DS + "bed0a6b2-683a-46b7-8f39-5ccd9552a97f/download/kuri-ninngu_ippann_202608.xlsx",
                        ENV_PAGE),
    "laundry_pickup": ("kuri-ninngu_toritugi_202608.xlsx",
                       _ENV_DS + "26c5d72d-91ba-4128-938c-8695f008e54c/download/kuri-ninngu_toritugi_202608.xlsx",
                       ENV_PAGE),
}
SOURCE_RESOURCES = {
    "food": (BODIK_API, "4c06c4b1-84de-4c4c-af65-fff85a7963e4"),
    "barber": (BODIK_API, "d888225b-47f9-431a-9fcd-de53153e6eb9"),
    "beauty": (BODIK_API, "0e4a4287-f846-4ba2-aa09-1cbbd554ddba"),
    "laundry_general": (BODIK_API, "bed0a6b2-683a-46b7-8f39-5ccd9552a97f"),
    "laundry_pickup": (BODIK_API, "26c5d72d-91ba-4128-938c-8695f008e54c"),
}
# The dates the lists state (Kyoto's rule, never the download's): the food
# resource's 「営業許可を取得している全施設　2026年8月末現在」; the registers'
# month in their names (202608).
SOURCE_AS_OF = {k: "2026-08-31" for k in SOURCE_FILES}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# The two laundry lists are one kind (japan_step2.kind): the key names the
# file, the kind decides the bucket.
SOURCE_KIND = {"laundry_general": "laundry", "laundry_pickup": "laundry"}
# Declared, never inferred: the food list is UTF-8 with a BOM, comma CSV; the
# four registers XLSX, one sheet each, header on row 1.
SOURCE_ENCODING = {"food": "utf-8-sig"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 詳細業種 is the food list's form of business (業態),
# read as the form by the city's "form_cols" rule (japan_register.FORM_COLS).
# The operator columns (the food list's 申請者氏名, filled for companies only
# beside 申請者法人名称; the registers' 営業者氏名・法人名称, a sole trader's own
# name or a company's) are REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; they are read IN MEMORY by that rule only, never kept. Never
# selected: 申請者住所 (an operator's own address), 申請者役職, 法人代表者, every
# 電話番号.
_REGISTER = ("営業所名称", "営業所所在地", "営業者氏名・法人名称")
REQUIRED_COLUMNS = {
    "food": ("営業所名称", "営業所所在地", "業種", "詳細業種", "申請者氏名"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry_general": _REGISTER,
    "laundry_pickup": _REGISTER,
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 14201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Yokosuka.
# S, W, N, E: the city's N03 extent (S 35.168, W 139.576, N 35.330, E 139.747;
# 猿島 included) rounded out; step 1 stops if the city leaves it. The box the
# OSM query used (2026-10-03).
OSM_BBOX = (35.15, 139.56, 35.35, 139.76)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment). Station names follow the operators' signs, as Tokyo's, Yokohama's
# and Kawasaki's do (owner 2026-09-28: signage style, OSM's names as they
# stand, no macrons).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~139.67) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median gap to the nearest station
# group is 840 m: standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25:
# 3 lines, no Shinkansen). Keikyu's Main Line keeps 11 of its 50 stations
# (追浜 to 浦賀), its Kurihama Line 7 of 9 (三浦海岸 and 三崎口 in Miura), JR's
# Yokosuka Line 4 of 9 (田浦 to 久里浜), each cut at the city line (owner
# 2026-09-24). No line is cut to a stub. 堀ノ内 is one station of both Keikyu
# lines (one N02 group); 京急久里浜 and JR's 久里浜, 224 m apart (the closest pair), are
# separate N02 groups of different names and stay apart.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02's JR 横須賀線 is the Yokosuka Line
# itself here (大船 to 久里浜), so no route is needed.
_KQ, _JR = "京浜急行電鉄", "東日本旅客鉄道"
LINES = {
    "KK": {"n02": [(_KQ, "本線")], "name": "Keikyu Main Line", "name_ja": "京急本線", "short": "Keikyu",
           "hue": "#E5171F"},
    "KU": {"n02": [(_KQ, "久里浜線")], "name": "Keikyu Kurihama Line", "name_ja": "京急久里浜線", "short": "Keikyu",
           "hue": "#E5171F"},
    "JO": {"n02": [(_JR, "横須賀線")], "name": "JR Yokosuka Line", "name_ja": "横須賀線", "short": "JR",
           "hue": "#0070B9"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# yokosuka` (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Keikyu's two lines share one red,
# so the Kurihama Line takes the nearest red-orange 18.1 from the Main Line
# (the closest pair, within 500 m at 堀ノ内); JR's blue goes to teal. The
# dark-mode labels separate, 3 of 3.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "KK": line_registry.colour("keikyu-main-line"), "KU": "#F05830",
    "JO": line_registry.colour("jr-east-yokosuka-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station lists. Keikyu's (keikyu.co.jp/ride/kakueki/,
# read 2026-10-03) lists the Main Line's 追浜 to 浦賀, 11 stations inside the
# city, and the Kurihama Line's 堀ノ内 to 津久井浜, 7 (三浦海岸 and 三崎口 lie in
# Miura).
GATE3 = {"source": "Keikyu's station list (keikyu.co.jp/ride/kakueki/): Main Line 追浜-浦賀 11, "
                   "Kurihama Line 堀ノ内-津久井浜 7, inside the city",
         "lines": {"KK": 11, "KU": 7}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
YOKOSUKA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = YOKOSUKA_BBOX
