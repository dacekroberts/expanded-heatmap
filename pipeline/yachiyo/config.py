"""Yachiyo-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/yachiyo.md (11/11 checks, 2026-10-11). Yachiyo City (八千代市,
12221), one municipality with no wards. Japan's A/B batch (East-2), one of
the six Chiba pages on the shared Chiba leg
(pipeline/countries/chiba_pref.py), in Matsudo's shape: personal services only
(Band B, owner 2026-10-06), a full list per kind plus the months since.

Business leg: Chiba Prefecture's open-data lists of barbers, beauty salons and
laundries (dataset 6 on opendata.pref.chiba.lg.jp, PDL 1.0), the 習志野 health
center's sheet cut to the city by address. Barbers as of 2025-03-31, built as
published with their own date (owner, call 33); beauty salons and laundries
the 2026-03-31 lists plus the months to 2026-08-31, an upper bound (owner,
call 34). The lists hold only premises whose operators agreed to open
publication, disclosed with no number. No food layer and no MHLW source.
Placed by a JOIN to MLIT's 位置参照情報 for the one municipality.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): the Toyo Rapid Railway Line (4 of N02's 9 stations, its eastern
end) and the Keisei Main Line (3 of 42). English station names from
OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import chiba_pref

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "yachiyo" / "raw"
DATA_PROCESSED = ROOT / "data" / "yachiyo" / "processed"
OUTPUTS = ROOT / "outputs" / "yachiyo"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Yachiyo"
SLUG = "yachiyo"
MUNICIPALITY = "八千代市"
PREFECTURE = chiba_pref.PREFECTURE
# Yachiyo is in the 習志野健康福祉センター's area (習志野市, 八千代市, 鎌ケ谷市):
# its sheet in each of the prefecture's workbooks (chiba_pref.SHEET_AREAS)
HEALTH_CENTER = "習志野"

# Chiba Prefecture's files, shared by the six Chiba pages in
# data/chiba_pref/raw/ (chiba_pref.SOURCE_FILES; never re-pulled from a
# branch, the shared data/ rule)
SOURCE_FILES = chiba_pref.SOURCE_FILES
SOURCES = chiba_pref.SOURCES
SOURCE_KIND = chiba_pref.SOURCE_KIND
SOURCE_AS_OF = chiba_pref.SOURCE_AS_OF
SOURCE_ENCODING = chiba_pref.SOURCE_ENCODING
REGISTERS_AS_OF = chiba_pref.REGISTERS_AS_OF
FOOD_AS_OF = None  # no food leg (Band B: personal services only)
# The operator columns (開設者名, the laundry list's 営業者名) are REQUIRED so
# the name rule cannot compare nothing; read IN MEMORY by that rule only.
REQUIRED_COLUMNS = chiba_pref.REQUIRED_COLUMNS
# The city's rows of each register as the brief measured them on these files
# (2026-10-06): barbers 130 (the 2025-03-31 list), beauty salons 344 listed
# + 9 from the months, laundries 77 + 0 (7 of them 無店舗取次店, not
# premises; the sheet's one row naming no municipality stays out, and the May
# laundry month's one 習志野 row is Narashino's). A different count stops step
# 2: a new edition is re-measured and the brief corrected, never passed
# silently.
EXPECTED_ROWS = {"barber": 130, "beauty": 353, "laundry": 77}


def source_csv(key):
    """A file in the shared Chiba cache, by file key or step-2 source key."""
    return chiba_pref.source_path(key)


def source_rows(key):
    """The city's rows of each register: the 習志野 sheet of the base list and
    of each approved month, cut by address at 八千代市 (chiba_pref.city_rows),
    as MLIT's 市区町村名 and the lists' addresses write it; the step stops
    naming fetch_sources.py where a file is missing."""
    from pipeline.countries.japan_step2 import need
    for k in SOURCE_FILES:
        need(source_csv(k), SLUG)
    return chiba_pref.city_rows(key, MUNICIPALITY, HEALTH_CENTER, expect=EXPECTED_ROWS[key])


def file_rows(key):
    """One file's rows as it stands, for fetch_sources.py's count and column check."""
    return chiba_pref.file_rows(key)


# MLIT 位置参照情報, block (24.0a) and town-chome (19.0b), for 12221 alone
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.6924, W 140.0629, N 35.7840,
# E 140.1519) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.69, 140.06, 35.79, 140.16)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons). None:
# the seven names were read 2026-10-11 and none is translated or carries a
# macron (八千代緑が丘 reads Yachiyo-midorigaoka, 東葉勝田台 Toyo-Katsutadai).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (140.105) and the whole extent (140.063 to
# 140.152) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-station gap is 1,459 m (7 stations), over the 550 m
# that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-11: 2 lines, 7 station records, 7 station groups): the Toyo Rapid
# Railway Line 4 of 9 (八千代緑が丘 to 東葉勝田台, its eastern terminus) and
# the Keisei Main Line 3 of 42 (八千代台, 京成大和田, 勝田台), both commuter
# railways (N02 class 12) cut at the city line (owner 2026-09-24). No N02
# group joins two lines: N02 keeps Keisei's 勝田台 and the Toyo Rapid's
# 東葉勝田台 apart (149 m, a walking interchange under two names), and so does
# step 1 (trap 1); their rings overlap almost wholly. No Shinkansen, JR,
# subway, tram or light rail in the city, and no stub.
#
# No frequency floor (owner, 2026-10-06, calls 46 and 86), and no
# low-frequency stretch: Keisei runs 6 to 10 trains an hour at the three
# stations (its timetable service, read 2026-10-06); the Toyo Rapid about
# every 10 to 12 minutes off-peak (asserted: its station timetables are
# image-only PDFs, the 2026-03-14 edition).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
# No N03_NEIGHBOR_PREFS: every station step 1 reads beyond the line (within
# 3 km: 6, in Funabashi, Narashino and Sakura) is in Chiba Prefecture.

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, and the same
# as on every other map that draws the line: Tokyo's and Funabashi's Keisei
# Main Line; Funabashi's Toyo Rapid Railway Line (N02's 東葉高速鉄道
# 東葉高速線), under the same key there. The Toyo Rapid's trains run through
# onto the Tokyo Metro Tozai Line at 西船橋, outside the city: N02 files the
# Toyo Rapid as its own line and it is drawn under its own name.
LINES = {
    "TR": {"n02": [("東葉高速鉄道", "東葉高速線")], "name": "Toyo Rapid Railway Line", "name_ja": "東葉高速線",
           "short": "Toyo Rapid", "hue": "#00A650"},
    "KS": {"n02": [("京成電鉄", "本線")], "name": "Keisei Main Line", "name_ja": "京成本線", "short": "Keisei",
           "hue": "#005AAA"},
}
# SHARED LINES: both lines are drawn on another map and take that map's
# colour (owner, 2026-10-07: one colour per line on every map), never a value
# of this city's own: the Keisei Main Line from pipeline/line_registry.py
# (Tokyo's value), the Toyo Rapid Railway Line the #20A800 Funabashi's map
# draws it in (Funabashi's search, 2026-10-11), a literal here until the
# registry holds it: it must equal Funabashi's.
# Measured 2026-10-11: the Toyo Rapid Railway Line 45.7 (CIE76) from the
# Personal services pin, its nearest and the one pin this map draws (5.94 on
# the dark page, 3.15 on the light); the Keisei Main Line 72.0 from that pin
# and 51.0 from its nearest of the taxonomy's pins (3.03, 6.19). The two
# lines, which meet at 勝田台 (tracks 23 m apart), are 102.3 apart. No
# accepted trade under 45.
_COLOURS = {
    "KS": line_registry.colour("keisei-main-line"),
    "TR": line_registry.colour("toyo-rapid-railway-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS[_k]
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own stations. The Toyo Rapid Railway's station guide
# links nine station pages (西船橋 to 東葉勝田台, as N02's 9), the first five
# inside Funabashi and the last four (八千代緑が丘, 八千代中央, 村上,
# 東葉勝田台) inside this city (toyokosoku.co.jp/station, read for Funabashi's
# gate 3, 2026-10-11). The Keisei Main Line is cut at the city line and has
# no independent count here.
GATE3 = {"source": "The Toyo Rapid Railway's station guide (9 station pages, the last 4 inside the city), read "
                   "against the city line: Toyo Rapid Railway Line 4",
         "lines": {"TR": 4}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
YACHIYO_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = YACHIYO_BBOX
