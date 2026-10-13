"""Urayasu-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/urayasu.md (11/11 checks, 2026-10-11). Urayasu City (浦安市,
12227), one municipality with no wards. Japan's A/B batch (East-2), one of the
six Chiba pages on the shared Chiba leg (pipeline/countries/chiba_pref.py), in
Matsudo's shape: personal services only (Band B, owner 2026-10-06), a full
list per kind plus the months since.

Business leg: Chiba Prefecture's open-data lists of barbers, beauty salons and
laundries (dataset 6 on opendata.pref.chiba.lg.jp, PDL 1.0), the 市川 health
center's sheet cut to the city by address. Barbers as of 2025-03-31, built as
published with their own date (owner, call 33); beauty salons and laundries
the 2026-03-31 lists plus the months to 2026-08-31, an upper bound (owner,
call 34). The lists hold only premises whose operators agreed to open
publication, disclosed with no number. No food layer (the prefecture's food
set is old-law only) and no MHLW source. Placed by a JOIN to MLIT's
位置参照情報 for the one municipality.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): the Disney Resort Line (all 4 of N02's stations, a monorail loop
wholly inside the city, counted as rail by the owner's call 53), JR East's
Keiyo Line (2 of 19) and the Tokyo Metro Tozai Line at 浦安 (1 of 23), drawn
cut by the owner's exception (calls 54 and 92). English station names from
OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import chiba_pref

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "urayasu" / "raw"
DATA_PROCESSED = ROOT / "data" / "urayasu" / "processed"
OUTPUTS = ROOT / "outputs" / "urayasu"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Urayasu"
SLUG = "urayasu"
MUNICIPALITY = "浦安市"
PREFECTURE = chiba_pref.PREFECTURE
# Urayasu is in the 市川健康福祉センター's area (市川市, 浦安市): its sheet in
# each of the prefecture's workbooks (chiba_pref.SHEET_AREAS)
HEALTH_CENTER = "市川"

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
# (2026-10-06): barbers 76 (the 2025-03-31 list), beauty salons 192 listed + 3
# from the months, laundries 58 + 0 (none a 無店舗取次店). A different count
# stops step 2: a new edition is re-measured and the brief corrected, never
# passed silently.
EXPECTED_ROWS = {"barber": 76, "beauty": 195, "laundry": 58}


def source_csv(key):
    """A file in the shared Chiba cache, by file key or step-2 source key."""
    return chiba_pref.source_path(key)


def source_rows(key):
    """The city's rows of each register: the 市川 sheet of the base list and
    of each approved month, cut by address at 浦安市 (chiba_pref.city_rows), as
    MLIT's 市区町村名 and the lists' addresses write it; the step stops naming
    fetch_sources.py where a file is missing."""
    from pipeline.countries.japan_step2 import need
    for k in SOURCE_FILES:
        need(source_csv(k), SLUG)
    return chiba_pref.city_rows(key, MUNICIPALITY, HEALTH_CENTER, expect=EXPECTED_ROWS[key])


def file_rows(key):
    """One file's rows as it stands, for fetch_sources.py's count and column check."""
    return chiba_pref.file_rows(key)


# MLIT 位置参照情報, block (24.0a) and town-chome (19.0b), for 12227 alone
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.6167, W 139.8715, N 35.6727,
# E 139.9395) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.61, 139.87, 35.68, 139.94)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
# N02 writes the monorail's four names with a half-width middle dot
# (リゾートゲートウェイ･ステーション) and OSM with the full-width one; step 1
# compares both under NFKC, which makes them one, so no alias is needed.
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
# None: the one object of the 13 without a name:en (2026-10-11) is a ride
# inside a theme park, not an N02 station, and is not drawn.
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons). None:
# all 7 names were read 2026-10-11 and none carries a macron.
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (139.902) and the whole extent (139.8715 to
# 139.9395) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-station gap is 906 m (7 stations), over the 550 m
# that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-11: 3 lines, 7 station records, 7 station groups; no Shinkansen,
# tram or light rail):
#   * the Disney Resort Line 4 of 4 (舞浜リゾートライン, N02 class 15, a
#     straddle monorail): a loop wholly inside the city, counted as rail
#     (owner, call 53, 2026-10-06, on the Chiba Urban Monorail's precedent);
#   * JR East's 京葉線 2 of 19 (舞浜, 新浦安), cut at the city line (owner
#     2026-09-24). The Musashino Line's through trains run on this track and
#     need no line of their own;
#   * the Tokyo Metro Tozai Line 1 of 23 (浦安): an urban line cut to one
#     station, which the one-station rule would leave out with its station
#     kept through other lines. No other line serves 浦安, so the line is
#     DRAWN CUT (owner, calls 54 and 92, 2026-10-06; Suita's Esaka the other
#     exception) and is not in LEFT_OUT_LINES.
# No group holds two operators. N02 keeps JR's 舞浜 and the monorail's
# リゾートゲートウェイ･ステーション apart (161 m by the brief, the closest
# pair), a walking interchange under two names, and so does step 1 (trap 1).
# No frequency floor (owner, 2026-10-06, calls 46 and 86), and no stretch near
# it: JR Keiyo runs 10 to 11 trains an hour at 新浦安 (JR East's timetable page,
# read 2026-10-06 by the brief).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
# The Keiyo and Tozai lines run on into Tokyo (葛西臨海公園 and 葛西, 江戸川区):
# its N03 file names those excluded stations
# (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("13",)

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, and the same
# as on every other map that draws the line: Tokyo's and Funabashi's JR Keiyo
# Line (N02's 京葉線 drawn whole under the one public name, Funabashi's form)
# and Tozai Line. The monorail's label and legend entry are its real public
# name, the Disney Resort Line (ディズニーリゾートライン, as N02 and the line
# itself write it; owner, call 122), a trade name with no logo or
# brand colour used; Maihama Resort Line is the operator. Its hue is a seed,
# not read from the operator (each of its trains wears its own colour, none
# the line's; Matsudo's Ryutetsu the precedent): a violet, clear of the Keiyo
# Line's red-orange and the Tozai Line's grey-blue.
_JR = "東日本旅客鉄道"
LINES = {
    "DR": {"n02": [("舞浜リゾートライン", "ディズニーリゾートライン")], "name": "Disney Resort Line",
           "name_ja": "ディズニーリゾートライン", "short": "Disney Resort Line", "hue": "#7B4FA0"},
    "JE": {"n02": [(_JR, "京葉線")], "name": "JR Keiyo Line", "name_ja": "京葉線", "short": "JR",
           "hue": "#C9242F"},
    "T": {"n02": [("東京地下鉄", "5号線東西線")], "name": "Tozai Line", "name_ja": "東西線", "short": "Metro",
          "hue": "#009BBF"},
}
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own: the JR Keiyo Line and
# the Tozai Line, in the colours Tokyo's and Funabashi's maps draw them.
#
# The Disney Resort Line is new to the site and the project's own colour, by
# scripts/line_colour_search.py's rule with those two held fixed (2026-10-11;
# >= 18 within 500 m, >= 10 city-wide, 3:1 on both map pages, CIE76 45 from
# every japan_eigyo pin): #7850A0, the feasible colour nearest the violet seed
# (55.4 from Food service, the nearest pin; 3.08 on the dark page, 6.08 on the
# light).
# Measured with all three (2026-10-11): JR Keiyo 45.0 from its nearest pin
# (Food service), the Tozai Line 50.0 (Personal services), so no line sits
# between 20 and 45. The one pair within 500 m, the Disney Resort Line and JR
# Keiyo (they meet at 舞浜), 90.3; closest pair anywhere 51.7 (the Disney
# Resort Line and the Tozai Line). Dark-mode labels, 3 distinct of 3.
_COLOURS = {
    "DR": "#7850A0",
    "JE": line_registry.colour("jr-east-keiyo-line"),
    "T": line_registry.colour("tokyo-metro-tozai-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own stations inside the city line. The Disney Resort
# Line has four stations, all in the city (the brief, 2026-10-06, as N02's 4);
# Tokyo Metro numbers the Tozai Line T01 to T23, T18 浦安 the one inside (its
# station numbering, as Tokyo's and Funabashi's gate 3 read it). JR East's
# Keiyo Line is cut at the city line and has no independent count here.
GATE3 = {"source": "The Disney Resort Line's four stations, all inside the city, and Tokyo Metro's station "
                   "numbering (T01 to T23, T18 inside), read against the city line",
         "lines": {"DR": 4, "T": 1}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
URAYASU_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = URAYASU_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602679929)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
PLACE_DROPPED = {}
