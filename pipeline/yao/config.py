"""Yao-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/yao.md.
Japan A/B batch (Kansai-2, 2026-10-11), on the shared modules
(pipeline/countries/japan*.py) and the Japan foundation's rules (ALL_RULES).

Business leg: ONE source, MHLW's 食品衛生申請等システム open data for the city's
own health center (27212; a core city licenses its own food premises), in
Kurume's shape: food only (owner, 2026-10-06, call 137). It holds the permits
granted since 2021-06 and its notifications, and publishes an address only
where the filer agreed. The city publishes no food list and no barber,
beauty-salon or laundry list. Placed by a JOIN to MLIT's 位置参照情報 for the
one municipality (no wards), with MHLW's own point where the join misses
(OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Kintetsu's Osaka Line and Shigi Line, JR West's Yamatoji Line and
Osaka Higashi Line (one station, its terminus, kept as cut), and Osaka
Metro's Tanimachi Line drawn cut at its one station, its terminus 八尾南
(owner, calls 54 and 92). The Nishi-Shigi Cable, a sightseeing funicular, is
left out. English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "yao" / "raw"
DATA_PROCESSED = ROOT / "data" / "yao" / "processed"
OUTPUTS = ROOT / "outputs" / "yao"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Yao"
SLUG = "yao"
MUNICIPALITY = "八尾市"
PREFECTURE = "大阪府"

# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2,
# termsofuse.htm; read 2026-09-24 for Fukuoka, re-read 2026-10-02). A plain
# GET. Credit links the top page only, as the site asks.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    "mhlw": ("27212_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27212_food_business_all.csv",
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
# read only 八尾市内一円 (vehicles and stalls licensed citywide, on shared
# points) are not premises (japan_register's 一円 test).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses, MHLW's own point places it (the brief's check:
# a median 41 m from the block point, 97.3% within 250 m; owner, call 127c).
OWN_POINT_FALLBACK = {"mhlw"}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 27212.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Yao.
# S, W, N, E: the city's N03 extent (S 34.583, W 135.562, N 34.651, E 135.664)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.58, 135.56, 34.66, 135.67)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word.
OSM_NAME_EN_OVERRIDES = {
    "久宝寺口": "Kyuhojiguchi",                      # Kyūhōjiguchi
    "八尾南": "Yao-minami",                          # Yao-Minami
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.62) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-group gap is 1,283 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# the brief: 6 lines, no Shinkansen), each cut at the city line (owner
# 2026-09-24): Kintetsu's 大阪線 (5 of 49) and 信貴線 (3 of 3, wholly inside),
# JR West's 関西線, signed the JR Yamatoji Line (3 of 34), and おおさか東線 (1 of
# 14: its terminus 久宝寺, shared with the Yamatoji Line; a JR one-station stub
# stays as cut, owner 2026-09-27). Osaka Metro's 谷町線 is an urban line cut to
# one station, its terminus 八尾南, which no other line serves: DRAWN cut
# (owner, 2026-10-06, calls 54 and 92). The 西信貴鋼索線 is a sightseeing
# funicular, left out (Kobe's rule, owner 2026-09-27); its lower station
# 信貴山口 stays on the Shigi Line.
LEFT_OUT_LINES = {
    ("近畿日本鉄道", "西信貴鋼索線"): "sightseeing funicular, the Nishi-Shigi Cable (Kobe's rule, owner 2026-09-27)",
}
# Kintetsu and the Yamatoji Line run on into Nara Prefecture: its N03 names
# the stations beyond the prefecture line (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("29",)
# 河内山本 (Kintetsu's two lines) and 久宝寺 (JR's two lines) are the
# interchange groups; 近鉄八尾 and JR 八尾 are separate stations, kept apart as
# N02 keeps them.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the JR Yamatoji Line as 関西線,
# as on Osaka's and Nara's maps.
_KT, _JR, _OM = "近畿日本鉄道", "西日本旅客鉄道", "大阪市高速電気軌道"
LINES = {
    "KO": {"n02": [(_KT, "大阪線")], "name": "Kintetsu Osaka Line", "name_ja": "近鉄大阪線", "short": "Kintetsu",
           "hue": "#F85838"},
    "KS": {"n02": [(_KT, "信貴線")], "name": "Kintetsu Shigi Line", "name_ja": "近鉄信貴線", "short": "Kintetsu",
           "hue": "#A03020"},
    "JQ": {"n02": [(_JR, "関西線")], "name": "JR Yamatoji Line", "name_ja": "大和路線", "short": "JR",
           "hue": "#12A500"},
    "OH": {"n02": [(_JR, "おおさか東線")], "name": "JR Osaka Higashi Line", "name_ja": "おおさか東線", "short": "JR",
           "hue": "#A088A0"},
    "T": {"n02": [(_OM, "2号線(谷町線)")], "name": "Tanimachi Line", "name_ja": "谷町線",
          "short": "Osaka Metro", "hue": "#933CA5"},
}
# Colours: four of the five lines are drawn on another city's map too, so each
# takes its one site-wide colour from pipeline/line_registry.py (owner,
# 2026-10-07: one colour per line on every map), never a value of this city's
# own. The Shigi Line is on no other map: its colour is this project's own
# (2026-10-11), the colour nearest a dark Kintetsu red that reads 3:1 on both
# map pages, clears CIE76 45 from every pin (48.1) and stands 32.0 or more
# from the four other lines here (the Osaka Line, which it meets at 河内山本,
# included).
_COLOURS = {
    "KO": line_registry.colour("kintetsu-osaka-line"),
    "KS": "#A04818",
    "JQ": line_registry.colour("jr-west-yamatoji-line"),
    "OH": line_registry.colour("jr-west-osaka-higashi-line"),
    "T": line_registry.colour("osaka-metro-tanimachi-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station lists inside the city (the brief:
# Kintetsu's Osaka Line 久宝寺口, 近鉄八尾, 河内山本, 高安, 恩智; Shigi Line
# 河内山本, 服部川, 信貴山口; JR's Yamatoji Line 久宝寺, 八尾, 志紀; the Osaka
# Higashi Line's terminus 久宝寺; the Tanimachi Line's terminus 八尾南).
GATE3 = {"source": "Kintetsu's, JR West's and Osaka Metro's station lists and timetable pages, read 2026-10-06",
         "lines": {"KO": 5, "KS": 3, "JQ": 3, "OH": 1, "T": 1}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
YAO_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = YAO_BBOX
