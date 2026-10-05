"""Shimonoseki-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/shimonoseki.md
(6/6 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py): food only, Okayama's shape, from ONE source.

Business leg: MHLW's 食品衛生申請等システム open data for Shimonoseki City alone
(every permit and notification the city entered since 2021-06; opt-in,
field by field). The city publishes no food list of its own and no barber,
beauty or laundry list (its pages carry notification forms only; no BODIK
catalogue), so there are no personal services (Band B, food only). No source
names an individual operator, so the name rule cannot run anywhere (owner,
2026-10-02, Okayama's call). Placed by a JOIN to MLIT's 位置参照情報 for the one
municipality (35201, no wards), through the shared 大字 rule; where the block
join misses, MHLW's own point (OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), the Shinkansen left out, stations kept
only inside the city line (N03). JR West's Sanyo and San'in lines, and JR
Kyushu's Sanyo Line stub to Moji. English station names from
OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "shimonoseki" / "raw"
DATA_PROCESSED = ROOT / "data" / "shimonoseki" / "processed"
OUTPUTS = ROOT / "outputs" / "shimonoseki"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Shimonoseki"
SLUG = "shimonoseki"
MUNICIPALITY = "下関市"
PREFECTURE = "山口県"

# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2,
# termsofuse.htm; read 2026-09-24 for Fukuoka, re-read 2026-10-02). A plain
# GET. Credit links the top page only, as the site asks.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    "mhlw": ("35201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=35201_food_business_all.csv",
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
# never kept (owner 2026-10-05, reversing Okayama's position of 2026-10-02). Never selected: 法人番号, 法人住所 and
# 営業施設電話番号.
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's): a
# row without one is counted apart for the page's disclosure.
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses, MHLW's own point places it (the brief's check:
# a median 38 m from the block point, 98.1% within 250 m; 2,504 rows).
OWN_POINT_FALLBACK = {"mhlw"}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 35201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Shimonoseki.
# S, W, N, E: the city's N03 extent (S 33.911, W 130.775, N 34.376, E 131.173;
# 角島 included), rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (33.9, 130.76, 34.39, 131.19)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word (Kitakyushu's Abeyama-koen). OSM's
# macrons are removed; the other 10 are OSM's as they stand.
OSM_NAME_EN_OVERRIDES = {
    "長府": "Chofu",                                 # Chōfu
    "梶栗郷台地": "Kajikuri-Godaichi",               # Kajikuri-Gōdaichi
    "川棚温泉": "Kawatana-onsen",                    # Kawatana-Onsen
    "梅ヶ峠": "Umegato",                             # Umegatō
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 52N: the longitude (~130.94) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-station gap is 2,745 m, the widest of any Japanese
# city so far.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-03: 3 lines; 新下関 stays as a JR station, the Shinkansen dropped):
# JR West's Sanyo Line (5 of 131) and San'in Line (17 of 161), and JR Kyushu's
# Sanyo Line (1 of 2: 下関, which is JR West's too; the Kanmon Tunnel to 門司),
# cut at the city line (owner 2026-09-24).
LEFT_OUT_LINES = {}
# JR Kyushu's track runs on under the strait to 門司 in Kitakyushu: Fukuoka's
# N03 names it (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("40",)
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. JR Kyushu's 山陽線 (下関 to 門司, one station
# inside, which JR West's line shares: a one-station stub, kept as cut) is
# drawn as part of the one JR Sanyo Line, under that public name and its one
# label and legend entry: the same line, its operator changing at 下関.
# Line names without macrons, as JR West's signs.
_JW, _JK = "西日本旅客鉄道", "九州旅客鉄道"
LINES = {
    "JS": {"n02": [(_JW, "山陽線"), (_JK, "山陽線")], "name": "JR Sanyo Line", "name_ja": "山陽本線", "short": "JR",
           "hue": "#0068B7"},
    "JN": {"n02": [(_JW, "山陰線")], "name": "JR San'in Line", "name_ja": "山陰本線", "short": "JR",
           "hue": "#E60012"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# shimonoseki` (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its operator's hue that reads 3:1 on both
# map pages and clears CIE76 45 from every pin (the Sanyo Line's teal is
# Okayama's). The pair separates by 122.7; the dark-mode labels, 2 of 2.
_COLOURS = {"JS": "#007890", "JN": "#E80010"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
# The San'in Line beyond 小串 is LEFT OUT (owner, 2026-10-02): its 7 stations
# in the city (湯玉, 宇賀本郷, 長門二見, 滝部, 特牛, 阿川, 長門粟野) see about 8 to
# 10 trains a day. N02 files the whole line as one 山陰線, so the stretch is
# split off by walking the track from the far end to 小串 and left out
# (draw_as None, Osaka's Umekita-Fukushima track); the line is drawn to 小串.
# 伊上 (Nagato, next beyond 長門粟野) lies on the same undrawn stretch, so it
# is listed too: it is not a station of a drawn line cut by the city line.
# Measured 2026-10-03 (scratch probe on step 1's functions): 17 N02 sections,
# 36,624 m left out; 20 sections, 23,525 m drawn; every drawn San'in station
# on the drawn track (2 m at most).
BRANCHES = {
    "JN_BEYOND_KOGUSHI": {"line": (_JW, "山陰線"), "terminus": "長門粟野", "junction": "小串",
                          "stations": ["湯玉", "宇賀本郷", "長門二見", "滝部", "特牛", "阿川", "長門粟野", "伊上"],
                          "length_m": (33000, 40000), "draw_as": None,
                          "label": "San'in Line beyond Kogushi",
                          # its 7 in-city stations go to excluded_stations.csv
                          # (japan_step1; the 15-minute words file them as too
                          # infrequent in What Is Excluded). JR West's station
                          # timetables (revised 2026-10-03): 11 trains each way
                          # on weekdays at 小串, 滝部 and 阿川, 12 at weekends.
                          "excluded_reason": "left out: the San'in Line beyond Kogushi runs 11 trains a day each "
                                             "way on weekdays, far below the 15-minute test (owner, 2026-10-02)",
                          "excluded_lines": "JN"},
}

# Gate 3: no line lies wholly inside the city; step 1 lists each line's
# in-city stations.
GATE3 = {"source": "no line wholly inside the city", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
SHIMONOSEKI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = SHIMONOSEKI_BBOX
