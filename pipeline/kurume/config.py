"""Kurume-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/kurume.md
(7/7 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py), in Okayama's shape: food only, from ONE
source.

Business leg: MHLW's 食品衛生申請等システム open data for Kurume City alone
(every permit and notification the city entered since 2021-06; opt-in, field
by field). The city's own new-permit stream stops at 2021-05 and points to
MHLW; its barber and beauty datasets are monthly lists of new premises, not
registers, and it publishes no laundry list, so there are no personal
services (Band B, food only). MHLW names no individual operator, so the name
rule cannot run (Okayama's precedent, owner 2026-10-02). Placed by a JOIN to
MLIT's 位置参照情報 (one municipality, no wards); where the block join misses,
MHLW's own point (OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), the Shinkansen left out, stations kept
only inside the city line (N03). Nishitetsu's Tenjin Omuta and Amagi lines
and JR Kyushu's Kagoshima Main and Kyudai Main lines. English station names
from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kurume" / "raw"
DATA_PROCESSED = ROOT / "data" / "kurume" / "processed"
OUTPUTS = ROOT / "outputs" / "kurume"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kurume"
SLUG = "kurume"
MUNICIPALITY = "久留米市"
PREFECTURE = "福岡県"

# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2,
# termsofuse.htm; read 2026-09-24 for Fukuoka, re-read 2026-10-02). A plain
# GET. Credit links the top page only, as the site asks.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    "mhlw": ("40203_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=40203_food_business_all.csv",
             MHLW_TOP),
}
# MHLW's monthly file states no date: its newest 許可年月日 is 2026-08-31, and
# the page dates it by download (provenance.json).
SOURCE_AS_OF = {"mhlw": None}
FOOD_AS_OF = None
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: UTF-8 with a BOM.
SOURCE_ENCODING = {"mhlw": "utf-8-sig"}
# The columns the file must carry; fetch_sources.py and step 2 stop on a
# header without them. MHLW's 法人名 holds a sole trader's own name as
# well as a company's, so it is REQUIRED and read IN MEMORY by the name rule only,
# never kept (owner 2026-10-05, reversing Okayama's precedent). Never selected: 法人番号, 法人住所 and
# 営業施設電話番号.
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's): a
# row without one is counted apart for the page's disclosure. 1,022 rows read
# only 久留米市内 (vehicles and stalls licensed citywide, on one shared point):
# not premises (japan_register's `citywide` rule, WAVE2_RULES).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses, MHLW's own point places it (the brief's check:
# a median 48 m from the block point, 93.7% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one municipality.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Kurume.
# S, W, N, E: the city's N03 extent (S 33.224, W 130.385, N 33.368, E 130.732)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (33.21, 130.37, 33.38, 130.75)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-10-03): OSM names the Nishitetsu stop with its 駅.
OSM_NAME_ALIASES = {"聖マリア病院前": "聖マリア病院前駅"}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen, no apostrophe before n (Fukuoka's Gannosu). OSM
# TRANSLATED two names rather than romanising them (Fukuoka's Kashii Shrine
# case): romanised here. Nishitetsu's two Kurume stations take its hyphen, as
# Fukuoka's Nishitetsu-Kashii. The other 17 are OSM's as they stand.
OSM_NAME_EN_OVERRIDES = {
    "聖マリア病院前": "Sei-Maria-byoin-mae",       # St. Mary Hospital Station
    "学校前": "Gakko-mae",                         # Elementary School
    "古賀茶屋": "Koganchaya",                      # Kogan'chaya
    "筑後草野": "Chikugo-Kusano",                  # Chikugo Kusano
    "久留米高校前": "Kurume-koko-mae",             # Kurume-Kōkōmae
    "久留米大学前": "Kurume-daigaku-mae",          # Kurume-Daigakumae
    "西鉄久留米": "Nishitetsu-Kurume",             # Nishitetsu Kurume
    "大城": "Oki",                                 # Ohki
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 52N: the longitude (~130.51) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-03: 4 lines; the Kyushu Shinkansen's 久留米 stays a JR station).
# Every line is cut at the city line (owner 2026-09-24): Nishitetsu's
# 天神大牟田線 10 of 50 and 甘木線 7 of 12, JR's 久大線 8 of 37 and 鹿児島線 2
# of 99. No line is cut to one station.
LEFT_OUT_LINES = {}
# JR's Kagoshima Main Line runs on across the Chikugo River into Saga
# Prefecture (肥前旭, Tosu): its N03 names the station beyond the prefecture
# line (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("41",)
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names follow the operators' signs
# with no macrons, as Kitakyushu's.
_NNR, _JR = "西日本鉄道", "九州旅客鉄道"
LINES = {
    "NT": {"n02": [(_NNR, "天神大牟田線")], "name": "Nishitetsu Tenjin Omuta Line", "name_ja": "天神大牟田線",
           "short": "Nishitetsu", "hue": "#E60012"},
    "NA": {"n02": [(_NNR, "甘木線")], "name": "Nishitetsu Amagi Line", "name_ja": "甘木線",
           "short": "Nishitetsu", "hue": "#F39800"},
    "JK": {"n02": [(_JR, "鹿児島線")], "name": "JR Kagoshima Main Line", "name_ja": "鹿児島本線", "short": "JR",
           "hue": "#E60012"},
    "JQ": {"n02": [(_JR, "久大線")], "name": "JR Kyudai Main Line", "name_ja": "久大本線", "short": "JR",
           "hue": "#009944"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# kurume` (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Closest pair within 500 m and
# anywhere 18.1 (the Tenjin Omuta and Kagoshima Main lines, both red); the
# dark-mode labels separate, 4 of 4.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "NT": line_registry.colour("nishitetsu-tenjin-omuta-line"), "NA": "#D08000",
    "JK": line_registry.colour("jr-kyushu-kagoshima-main-line"),
    "JQ": line_registry.colour("jr-kyushu-kyudai-main-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city, so Nishitetsu's own station
# lists (its timetable site, jik.nishitetsu.jp, read 2026-10-03), read against
# the city line, give each cut line's in-city stops: the Tenjin Omuta Line 宮の陣
# to 犬塚 (10) and the Amagi Line 宮の陣 to 金島 (7; 大堰 beyond is Tachiarai's).
# JR's two lines are N02's.
GATE3 = {"source": "Nishitetsu's station lists (jik.nishitetsu.jp), read against the city line",
         "lines": {"NT": 10, "NA": 7}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KURUME_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KURUME_BBOX
