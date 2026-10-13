"""Ichikawa-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/ichikawa.md (12/12 checks, 2026-10-11). Ichikawa City
(市川市, 12203), one municipality with no wards. Japan's A/B batch (East-2),
one of the six Chiba pages on the shared Chiba leg
(pipeline/countries/chiba_pref.py), in Kochi's shape as Matsudo built it:
personal services only (Band B, owner 2026-10-04), a full list per kind plus
the months since.

Business leg: Chiba Prefecture's open-data lists of barbers, beauty salons and
laundries (dataset 6 on opendata.pref.chiba.lg.jp, PDL 1.0), the 市川 health
center's sheet (市川市 and 浦安市) cut to the city by address. Barbers as of
2025-03-31, built as published with their own date (owner, call 33); beauty
salons and laundries the 2026-03-31 lists plus the months to 2026-08-31, an
upper bound (owner, call 34). The lists hold only premises whose operators
agreed to open publication, disclosed with no number. Laundries are about 80%
of a census-based estimate (148 against about 186; the brief, 2026-10-05),
built and the share stated on the page with its own date (owner, call 32). No
food layer (the prefecture's food set is old-law only; MHLW's prefecture file
is 62.7% addressed) and no MHLW source. Placed by a JOIN to MLIT's
位置参照情報 for the one municipality.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): the Keisei Main Line (5 of N02's 42 stations), JR East's 総武線 (2
of 48, drawn as its two services, the Chuo-Sobu local and the Sobu Rapid),
Keiyo Line (2 of 19) and Musashino Line (1 of 27, a one-station stub kept as
cut), the Tokyo Metro Tozai Line (3 of 23, drawn cut at the city line; owner,
call 31) and the Hokuso Line (2 of 15). The Toei Shinjuku Line (1 of 21, its
terminus 本八幡) is left out, the station kept through JR (owner, 2026-10-06).
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import chiba_pref

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "ichikawa" / "raw"
DATA_PROCESSED = ROOT / "data" / "ichikawa" / "processed"
OUTPUTS = ROOT / "outputs" / "ichikawa"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Ichikawa"
SLUG = "ichikawa"
MUNICIPALITY = "市川市"
PREFECTURE = chiba_pref.PREFECTURE
# Ichikawa is in the 市川健康福祉センター's area (市川市, 浦安市): its sheet in
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
# (2026-10-05 and 06): barbers 223 (the 2025-03-31 list), beauty salons 638
# listed + 8 from the months, laundries 148 + 0 (none a 無店舗取次店). A
# different count stops step 2: a new edition is re-measured and the brief
# corrected, never passed silently.
EXPECTED_ROWS = {"barber": 223, "beauty": 646, "laundry": 148}


def source_csv(key):
    """A file in the shared Chiba cache, by file key or step-2 source key."""
    return chiba_pref.source_path(key)


def source_rows(key):
    """The city's rows of each register: the 市川 sheet of the base list and
    of each approved month, cut by address at 市川市 (chiba_pref.city_rows), as
    MLIT's 市区町村名 and the lists' addresses write it; the step stops naming
    fetch_sources.py where a file is missing."""
    from pipeline.countries.japan_step2 import need
    for k in SOURCE_FILES:
        need(source_csv(k), SLUG)
    return chiba_pref.city_rows(key, MUNICIPALITY, HEALTH_CENTER, expect=EXPECTED_ROWS[key])


def file_rows(key):
    """One file's rows as it stands, for fetch_sources.py's count and column check."""
    return chiba_pref.file_rows(key)


# MLIT 位置参照情報, block (24.0a) and town-chome (19.0b), for 12203 alone
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.6555, W 139.8855, N 35.7757,
# E 139.9768) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.65, 139.88, 35.78, 139.98)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
# 本八幡 has two OSM objects in range: JR East's reads Moto-Yawata, Toei's
# Motoyawata (each operator's own signage). The station is drawn on JR's line
# and the Toei line is left out, so JR's spelling is taken.
OSM_NAME_EN_TIES = {"本八幡": "Moto-Yawata"}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons). None:
# the 15 names were read 2026-10-11 and none is translated or carries a
# macron (国府台 reads Konodai, 市川真間 Ichikawamama and 京成八幡 Keisei Yawata
# as Keisei signs them, 南行徳 Minami-gyotoku as Tokyo Metro signs it).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (139.933) and the whole extent (139.886 to
# 139.977) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-station gap is 1,305 m (15 stations), over the 550 m
# that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-11: 7 lines, 16 station records, 15 station groups; no Shinkansen,
# tram or light rail). Cut at the city line (owner 2026-09-24):
#   * Keisei Main Line 5 of 42;
#   * JR East's 総武線 2 of 48, 京葉線 2 of 19;
#   * the Tokyo Metro Tozai Line 3 of 23 (南行徳, 行徳, 妙典): an urban line
#     DRAWN cut at the city line on Sakai's and Higashiosaka's precedent
#     (owner, 2026-10-06, call 31; two or more stations are drawn cut, one is
#     left out);
#   * the Hokuso Line 2 of 15 (北国分, 大町). The Keisei Narita Sky Access
#     runs over the Hokuso track without stopping at either; N02 has no Sky
#     Access station inside the city;
#   * JR East's Musashino Line 1 of 27 (市川大野): a commuter railway, a
#     one-station stub kept as cut by the standing call (2026-09-27).
# N02 groups JR's and Toei's 本八幡 (one interchange); it keeps Keisei's
# 京成八幡 and 本八幡, and Keisei's 市川真間 and JR's 市川, apart, each a walking
# interchange under two names, and so does step 1 (trap 1). No frequency floor
# (owner, 2026-10-06, calls 46 and 86); the brief asserts, without reading a
# timetable, that every line here runs several trains an hour.
LEFT_OUT_LINES = {
    # An urban line cut to ONE station, whose place another line serves
    # (owner, 2026-10-06; calls 54 and 92 the rule): 本八幡, 1 of 21, the Toei
    # Shinjuku Line's eastern terminus, in the same N02 group as JR's 本八幡,
    # which keeps the ring.
    ("東京都", "10号線新宿線"): "an urban line with one station inside, 本八幡, its terminus, served by the JR "
                         "Chuo-Sobu Line (owner 2026-10-06)",
}
COLLAPSE_MAX_SPREAD_M = 300
# The lines run on into Tokyo (小岩, 江戸川, 篠崎: 江戸川区; 新柴又: 葛飾区): its
# N03 file names those excluded stations (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("13",)

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, and the same
# as on Tokyo's and Funabashi's maps, which draw every line here (Keisei Main
# Line, JR Chuo-Sobu Line, JR Yokosuka / Sobu Rapid Line, JR Keiyo Line, Tozai
# Line, Hokuso Line), and on the six maps that draw the JR Musashino Line.
#
# JR EAST'S 総武線 carries two public services here, drawn as Tokyo and
# Funabashi draw them (`route`, japan_step1.route_sections; trap 2): the
# Chuo-Sobu local stops at 市川 and 本八幡, the Sobu Rapid at 市川 only. Each
# route's first and last entry is the next station beyond the city line (小岩
# in Tokyo's Edogawa, 下総中山 in Funabashi); the rapid passes all three but
# 市川 ("~").
#
# N02's 京葉線 (trap 3) is the main line through 市川塩浜 plus the Futamata
# branch through 二俣新町 to 西船橋 that the Musashino Line's through trains
# use. JR East lists 二俣新町 as a Keiyo Line station, so the legal line is
# drawn whole under the one public name, as Funabashi's map draws it; the
# through trains need no line of their own.
_JR, _KS = "東日本旅客鉄道", "京成電鉄"
_SOBU = (_JR, "総武線")
LINES = {
    "KS": {"n02": [(_KS, "本線")], "name": "Keisei Main Line", "name_ja": "京成本線", "short": "Keisei",
           "hue": "#005AAA"},
    "JB": {"route": [(*_SOBU, ["小岩", "市川", "本八幡", "下総中山"])],
           "name": "JR Chuo-Sobu Line", "name_ja": "中央・総武線各駅停車", "short": "JR", "hue": "#FFD400"},
    "JO": {"route": [(*_SOBU, ["~小岩", "市川", "~本八幡", "~下総中山"])],
           "name": "JR Yokosuka / Sobu Rapid Line", "name_ja": "横須賀・総武快速線", "short": "JR",
           "hue": "#0067C0"},
    "JM": {"n02": [(_JR, "武蔵野線")], "name": "JR Musashino Line", "name_ja": "武蔵野線", "short": "JR",
           "hue": "#F15A22"},
    "JE": {"n02": [(_JR, "京葉線")], "name": "JR Keiyo Line", "name_ja": "京葉線", "short": "JR",
           "hue": "#C9242F"},
    "T": {"n02": [("東京地下鉄", "5号線東西線")], "name": "Tozai Line", "name_ja": "東西線", "short": "Metro",
          "hue": "#009BBF"},
    "HS": {"n02": [("北総鉄道", "北総線")], "name": "Hokuso Line", "name_ja": "北総線", "short": "Hokuso",
           "hue": "#3A9AD9"},
}
# ONE COLOUR PER LINE, SITE-WIDE (owner, 2026-10-07). All seven lines are
# drawn on another map (Tokyo's, Funabashi's, Matsudo's) and take their one
# colour from pipeline/line_registry.py, never a value of this city's own.
# No line is new to the site, so no colour was searched for.
# Measured 2026-10-11, all seven: every line 50.0 or more from the Personal
# services pin, the one pin this map draws (Tozai 50.0, Hokuso 53.7). Closest
# pair within 500 m 11.8, the JR Musashino Line against the JR Keiyo Line,
# which share track into 西船橋: both are registry colours, so neither moves
# here (the parked call recorded with Funabashi; re-measure if either is
# re-registered). Next within 500 m 18.9 (Keisei Main and Hokuso, which meet
# only at 京成高砂, beyond the city line), then 31.6 (Keisei Main and Tozai,
# 407 m apart at their nearest). The Tozai and Hokuso lines are 17.6 apart
# and never nearer than 6.4 km.
_COLOURS = {
    "KS": line_registry.colour("keisei-main-line"),
    "JB": line_registry.colour("jr-east-chuo-sobu-line"),
    "JO": line_registry.colour("jr-east-yokosuka-line"),
    "JM": line_registry.colour("jr-east-musashino-line"),
    "JE": line_registry.colour("jr-east-keiyo-line"),
    "T": line_registry.colour("tokyo-metro-tozai-line"),
    "HS": line_registry.colour("hokuso-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS[_k]
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own stations inside the city line, for the one line
# with a count independent of N02. Tokyo Metro numbers the Tozai Line T01 to
# T23: T18 浦安 is Urayasu's, T19 南行徳, T20 行徳 and T21 妙典 are inside, T22
# and T23 are Funabashi's (its station numbering, as Tokyo's and Funabashi's
# gate 3 read it). JR East's two services are the route lists above; the
# Keisei, Hokuso, Keiyo and Musashino lines are cut at the city line and no
# operator's page was read for them here.
GATE3 = {"source": "Tokyo Metro's station numbering (T01 to T23; T19, T20 and T21 inside), read against the city "
                   "line",
         "lines": {"T": 3}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
ICHIKAWA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = ICHIKAWA_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602679915)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
PLACE_DROPPED = {}
