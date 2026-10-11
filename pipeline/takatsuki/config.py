"""Takatsuki-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/takatsuki.md. Japan A/B batch (Kansai-2, 2026-10-11), on the shared modules
(pipeline/countries/japan*.py) and the Japan foundation's rules (ALL_RULES).

Business leg: ONE source, MHLW's 食品衛生申請等システム open data for the city's
own health center (27207; a core city licenses its own food premises), in
Kurume's shape: food only (owner, 2026-10-06, call 137). It holds the permits
granted since 2021-06 and its notifications, and publishes an address only
where the filer agreed. The city publishes no food list and no barber,
beauty-salon or laundry list. Placed by a JOIN to MLIT's 位置参照情報 for the
one municipality (no wards), with MHLW's own point where the join misses
(OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR West's Kyoto Line and Hankyu's Kyoto Line, cut at the city line;
the Tokaido Shinkansen crosses the city with no station. English station
names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "takatsuki" / "raw"
DATA_PROCESSED = ROOT / "data" / "takatsuki" / "processed"
OUTPUTS = ROOT / "outputs" / "takatsuki"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Takatsuki"
SLUG = "takatsuki"
MUNICIPALITY = "高槻市"
PREFECTURE = "大阪府"

# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2,
# termsofuse.htm; read 2026-09-24 for Fukuoka, re-read 2026-10-02). A plain
# GET. Credit links the top page only, as the site asks.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    "mhlw": ("27207_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27207_food_business_all.csv",
             MHLW_TOP),
}
# MHLW's monthly file states no date: its newest 許可年月日 is 2026-08-31, and
# the page dates it by download (provenance.json).
SOURCE_AS_OF = {"mhlw": None}
FOOD_AS_OF = None
# The file carries each permit's 許可満了日: the term rules (calls 161 and 172)
# read it against the last day the file covers, never today.
TERM_AS_OF = {"mhlw": "2026-08-31"}
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: UTF-8 with a BOM.
SOURCE_ENCODING = {"mhlw": "utf-8-sig"}
# The columns the file must carry; fetch_sources.py and step 2 stop on a
# header without them. MHLW's 法人名 holds a sole trader's own name as well
# as a company's, so it is REQUIRED and read IN MEMORY by the name rule only,
# never kept (owner 2026-10-05). Never selected: 法人番号, 法人住所 and
# 営業施設電話番号.
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's): a
# row without one is counted apart for the page's disclosure. The rows that
# read only 高槻市内一円 or 高槻市全域 (vehicles and stalls licensed citywide,
# on shared points) are not premises (japan_register's 一円 and area-wide
# tests).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses, MHLW's own point places it (the brief's check:
# a median 30 m from the block point, 99.0% within 250 m; owner, call 127c).
OWN_POINT_FALLBACK = {"mhlw"}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 27207.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Takatsuki.
# S, W, N, E: the city's N03 extent (S 34.781, W 135.557, N 34.977, E 135.673)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.78, 135.55, 34.98, 135.68)
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

# UTM zone 53N: the longitude (~135.61) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: step 1's
# median nearest-station gap is 574 m, above the rule's 550 m
# (docs/ring_rules.md). Re-measure if N02's edition changes.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# the brief: 2 lines, no Shinkansen station), each cut at the city line
# (owner 2026-09-24): JR West's 東海道線, signed the JR Kyoto Line (2 of 59),
# and Hankyu's 京都線 (3 of 27). No line is cut to one station.
LEFT_OUT_LINES = {}
# Both lines run on into Kyoto Prefecture: its N03 names the stations beyond
# the prefecture line (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("26",)
# Two close pairs are separate stations of different names and operators,
# kept apart as N02 keeps them (trap 1): 摂津富田 (JR) and 富田 (Hankyu) 285 m,
# 高槻 (JR) and 高槻市 (Hankyu) 574 m.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02's 東海道線 is signed the JR Kyoto Line
# here, as on Osaka's, Kyoto's and Suita's maps.
_HK, _JR = "阪急電鉄", "西日本旅客鉄道"
LINES = {
    "JY": {"n02": [(_JR, "東海道線")], "name": "JR Kyoto Line", "name_ja": "JR京都線", "short": "JR",
           "hue": "#0072BC"},
    "HY": {"n02": [(_HK, "京都線")], "name": "Hankyu Kyoto Line", "name_ja": "阪急京都線", "short": "Hankyu",
           "hue": "#87544B"},
}
# Colours: both lines are drawn on another city's map too, so each takes its
# one site-wide colour from pipeline/line_registry.py (owner, 2026-10-07: one
# colour per line on every map), never a value of this city's own.
_COLOURS = {
    "JY": line_registry.colour("jr-west-kyoto-line"),
    "HY": line_registry.colour("hankyu-kyoto-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station lists inside the city (the brief: JR
# 摂津富田, 高槻; Hankyu 富田, 高槻市, 上牧).
GATE3 = {"source": "JR West's and Hankyu's station timetable pages, read 2026-10-06",
         "lines": {"JY": 2, "HY": 3}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
TAKATSUKI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = TAKATSUKI_BBOX
