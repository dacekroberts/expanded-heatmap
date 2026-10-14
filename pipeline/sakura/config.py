"""Sakura-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/sakura.md (12/12 checks, 2026-10-11). Sakura City (佐倉市,
12212), one municipality with no wards. Japan's A/B batch (East-2), one of
the six Chiba pages on the shared Chiba leg
(pipeline/countries/chiba_pref.py), in Matsudo's shape: personal services only
(Band B, owner 2026-10-06), a full list per kind plus the months since.

Business leg: Chiba Prefecture's open-data lists of barbers, beauty salons and
laundries (dataset 6 on opendata.pref.chiba.lg.jp, PDL 1.0), the 印旛 health
center's sheet cut to the city by address. Barbers as of 2025-03-31, built as
published with their own date (owner, call 33); beauty salons and laundries
the 2026-03-31 lists plus the months to 2026-08-31, an upper bound (owner,
call 34). The lists hold only premises whose operators agreed to open
publication, disclosed with no number. No food layer and no MHLW source.
Placed by a JOIN to MLIT's 位置参照情報 for the one municipality.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): the Yamaman Yukarigaoka Line, an automated guideway loop wholly
inside the city (6 of N02's 6 stations), the Keisei Main Line (5 of 42), and
JR East's Sobu Main Line (1 of 48) and Narita Line (1 of 27), two one-station
stubs kept as cut (the standing call) that meet at 佐倉. English station names
from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import chiba_pref

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "sakura" / "raw"
DATA_PROCESSED = ROOT / "data" / "sakura" / "processed"
OUTPUTS = ROOT / "outputs" / "sakura"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Sakura"
SLUG = "sakura"
MUNICIPALITY = "佐倉市"
PREFECTURE = chiba_pref.PREFECTURE
# Sakura is in the 印旛健康福祉センター's area (nine municipalities): its sheet
# in each of the prefecture's workbooks (chiba_pref.SHEET_AREAS). The beauty
# workbook's 海匝 sheet is an exact copy of 印旛 and is never read: the rows are
# the 印旛 sheet's alone, cut by address (chiba_pref.city_rows).
HEALTH_CENTER = "印旛"

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
# (2026-10-06) and the shared module re-measured (2026-10-11): barbers 117
# (the 2025-03-31 list), beauty salons 255 listed + 1 from the months (July;
# April's one row repeats a listed confirmation and is dropped by the module),
# laundries 79 + 0 (1 of them a 無店舗取次店, not a premises). A different
# count stops step 2: a new edition is re-measured and the brief corrected,
# never passed silently.
EXPECTED_ROWS = {"barber": 117, "beauty": 256, "laundry": 79}


def source_csv(key):
    """A file in the shared Chiba cache, by file key or step-2 source key."""
    return chiba_pref.source_path(key)


def source_rows(key):
    """The city's rows of each register: the 印旛 sheet of the base list and
    of each approved month, cut by address at 佐倉市 (chiba_pref.city_rows), as
    MLIT's 市区町村名 and the lists' addresses write it; the step stops naming
    fetch_sources.py where a file is missing."""
    from pipeline.countries.japan_step2 import need
    for k in SOURCE_FILES:
        need(source_csv(k), SLUG)
    return chiba_pref.city_rows(key, MUNICIPALITY, HEALTH_CENTER, expect=EXPECTED_ROWS[key])


def file_rows(key):
    """One file's rows as it stands, for fetch_sources.py's count and column check."""
    return chiba_pref.file_rows(key)


# MLIT 位置参照情報, block (24.0a) and town-chome (19.0b), for 12212 alone
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.6246, W 140.1263, N 35.7662,
# E 140.3013) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.62, 140.12, 35.77, 140.31)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
# ユーカリが丘 is two OSM objects, Keisei's reading Yukarigaoka and the
# Yamaman's Yūkarigaoka: the spelling without a macron, the Tokyo-area
# signage style (owner 2026-09-28).
OSM_NAME_EN_TIES = {"ユーカリが丘": "Yukarigaoka"}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons). None:
# all 11 names were read 2026-10-11 and none carries a macron. The Yamaman's
# stations are named for what stands beside them and OSM romanizes them
# rather than translating (公園 Koen, 女子大 Joshidai, 中学校 Chugakko, 地区
# センター Chikucenter); the operator's station page (town.yukarigaoka.jp/
# yukariline/station/, read 2026-10-11) writes the names in Japanese only, so
# OSM's spellings stand.
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (140.213) and the whole extent (140.126 to
# 140.301) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-station gap is 644 m (11 stations), over the 550 m
# that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-11: 4 lines, 13 station records, 11 station groups). N02 groups
# ユーカリが丘 (Keisei and the Yamaman) and 佐倉 (JR's two lines); it keeps
# Keisei's 京成佐倉 and JR's 佐倉 apart, two stations about 1.5 km from each
# other, and so does step 1 (trap 1). No Shinkansen, subway or tram in the
# city.
#
# The Yamaman Yukarigaoka Line is an automated guideway (N02 class 16), an
# urban line, drawn in full: all 6 of its stations are inside, so no stub rule
# reaches it. It is a stem from ユーカリが丘 to 公園 and a one-way loop from
# 公園 through 女子大, 中学校 and 井野, drawn once from N02's sections.
#
# Two one-station stubs are kept as cut (the standing call of 2026-09-27,
# restated for wave 5; both commuter railways, N02 class 11, so the urban-stub
# rule of calls 54 and 92 does not reach them): JR East's Sobu Main Line and
# Narita Line, which meet at 佐倉, the Narita Line's western end.
#
# No frequency floor (owner, 2026-10-06, calls 46 and 86), and no stretch runs
# about 11 trains a day or fewer: the thinnest, Keisei at 大佐倉, has 2 to 4
# trains an hour at midday (Keisei's timetable service), and the Yamaman runs
# every 20 minutes through the day (its timetable of 2026-05-01; the brief,
# 2026-10-06).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, and the same
# as on every other map that draws the line: Tokyo's and Funabashi's Keisei
# Main Line.
#
# N02's 総武線 is JR East's whole legal line from Tokyo to Choshi. West of
# Chiba it carries the Chuo-Sobu local and the Sobu Rapid services that
# Tokyo's and Funabashi's maps draw as routes; the stretch through 佐倉, east
# of Chiba, is neither, and is named as JR East names it, the Sobu Main Line
# (総武本線), a line of its own on this site. The Narita Line (成田線) leaves it
# at 佐倉. No other built map draws either.
#
# The Yamaman's hue is a seed, not read from the operator (its trains wear a
# white livery with stripes, none the line's color): a blue, clear of
# Keisei's mauve, the yellow and the green.
_JR = "東日本旅客鉄道"
LINES = {
    "YU": {"n02": [("山万", "ユーカリが丘線")], "name": "Yamaman Yukarigaoka Line", "name_ja": "山万ユーカリが丘線",
           "short": "Yamaman", "hue": "#0068B7"},
    "KS": {"n02": [("京成電鉄", "本線")], "name": "Keisei Main Line", "name_ja": "京成本線", "short": "Keisei",
           "hue": "#005AAA"},
    "JS": {"n02": [(_JR, "総武線")], "name": "JR Sobu Main Line", "name_ja": "総武本線", "short": "JR",
           "hue": "#FFD400"},
    "JN": {"n02": [(_JR, "成田線")], "name": "JR Narita Line", "name_ja": "成田線", "short": "JR",
           "hue": "#00B261"},
}
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own: the Keisei Main Line
# (the mauve Tokyo's and Funabashi's maps draw it in).
#
# The other three are the project's own, by scripts/line_colour_search.py's
# rule with the Keisei Main Line held fixed (2026-10-11; >= 18 within 500 m,
# >= 10 city-wide, 3:1 on both map pages, CIE76 45 from every japan_eigyo
# pin): the Yamaman a blue (82.3 from Food service, the nearest pin; 3.27 on
# the dark page, 5.72 on the light), the JR Sobu Main Line an amber nearest
# JR East's yellow (46.1 from Retail; 4.66, 4.02), the JR Narita Line JR
# East's green (45.7 from Personal services; 5.94, 3.15). The Sobu Main
# Line's search also held 10 from two colours no line here wears, so the line
# reads apart from them on the neighboring maps: the JR Chuo-Sobu Line's
# #B09000 (30.8) and the Keisei Narita Sky Access Line's #D87800 (10.3; the
# search alone gives #D07800). The Narita Line's #20A800 is the value the
# registry's JR Joban Line and Funabashi's Toyo Rapid Railway Line wear; none
# of the three is drawn within 2 km of another (the Toyo Rapid ends at
# 東葉勝田台, about 9 km west of 佐倉). Re-measure if a map draws the Narita
# Line beside either.
# Measured with all four (2026-10-11): every line 45.7 or more from its
# nearest pin (Keisei Main 51.0). Pairs within 500 m: the Yamaman and Keisei
# Main, which meet at ユーカリが丘, 46.3; the two JR lines, which meet at 佐倉,
# 90.7. Dark-mode labels, 4 distinct of 4.
_COLOURS = {
    "KS": line_registry.colour("keisei-main-line"),
    "YU": "#0068B8", "JS": "#C06808", "JN": "#20A800",
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS[_k]
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own stations. The Yamaman's station page lists six
# stations (ユーカリが丘, 地区センター, 公園, 女子大, 中学校, 井野), as N02's 6,
# all inside the city line (town.yukarigaoka.jp/yukariline/station/, read
# 2026-10-11). Keisei's and JR East's lines are cut at the city line and have
# no independent count here.
GATE3 = {"source": "Yamaman's own station page (town.yukarigaoka.jp/yukariline/station/), six stations, all "
                   "inside the city line: Yukarigaoka Line 6",
         "lines": {"YU": 6}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
SAKURA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = SAKURA_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602679899)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
PLACE_DROPPED = {}
