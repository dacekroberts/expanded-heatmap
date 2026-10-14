"""Matsudo-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/matsudo.md (13/13 checks, 2026-10-11). Matsudo City (松戸市,
12207), one municipality with no wards. Japan's A/B batch (East-2), the first
of the six Chiba pages on the shared Chiba leg
(pipeline/countries/chiba_pref.py), in Kochi's shape: personal services only
(Band B, owner 2026-10-04), a full list per kind plus the months since.

Business leg: Chiba Prefecture's open-data lists of barbers, beauty salons and
laundries (dataset 6 on opendata.pref.chiba.lg.jp, PDL 1.0), the 松戸 health
center's sheet cut to the city by address. Barbers as of 2025-03-31, built as
published with their own date (owner, call 33); beauty salons and laundries
the 2026-03-31 lists plus the months to 2026-08-31, an upper bound (owner,
call 34). The lists hold only premises whose operators agreed to open
publication, disclosed with no number. No food layer (the prefecture's food
set is old-law only; MHLW's prefecture file is 62.7% addressed) and no MHLW
source. Placed by a JOIN to MLIT's 位置参照情報 for the one municipality.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): the Keisei Matsudo Line (8 of N02's 24 stations), JR East's Joban
Line (5 of 81) and Musashino Line (3 of 27), the Hokuso Line (4 of 15), the
Ryutetsu Nagareyama Line (3 of 6), and two one-station stubs kept as cut (the
standing call): the Keisei Narita Sky Access Line (東松戸, 1 of 8) and the
Tobu Urban Park Line (六実, 1 of 35). English station names from
OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import chiba_pref

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "matsudo" / "raw"
DATA_PROCESSED = ROOT / "data" / "matsudo" / "processed"
OUTPUTS = ROOT / "outputs" / "matsudo"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Matsudo"
SLUG = "matsudo"
MUNICIPALITY = "松戸市"
PREFECTURE = chiba_pref.PREFECTURE
# Matsudo is in the 松戸健康福祉センター's area (松戸市, 流山市, 我孫子市): its
# sheet in each of the prefecture's workbooks (chiba_pref.SHEET_AREAS)
HEALTH_CENTER = "松戸"

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
# (2026-10-05 and 06): barbers 304 (the 2025-03-31 list), beauty salons 759
# listed + 15 from the months, laundries 186 + 0 (2 of them 無店舗取次店, not
# premises). A different count stops step 2: a new edition is re-measured and
# the brief corrected, never passed silently.
EXPECTED_ROWS = {"barber": 304, "beauty": 774, "laundry": 186}


def source_csv(key):
    """A file in the shared Chiba cache, by file key or step-2 source key."""
    return chiba_pref.source_path(key)


def source_rows(key):
    """The city's rows of each register: the 松戸 sheet of the base list and
    of each approved month, cut by address at 松戸市 (chiba_pref.city_rows), as
    MLIT's 市区町村名 and the lists' addresses write it; the step stops naming
    fetch_sources.py where a file is missing."""
    from pipeline.countries.japan_step2 import need
    for k in SOURCE_FILES:
        need(source_csv(k), SLUG)
    return chiba_pref.city_rows(key, MUNICIPALITY, HEALTH_CENTER, expect=EXPECTED_ROWS[key])


def file_rows(key):
    """One file's rows as it stands, for fetch_sources.py's count and column check."""
    return chiba_pref.file_rows(key)


# MLIT 位置参照情報, block (24.0a) and town-chome (19.0b), for 12207 alone
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.7467, W 139.8794, N 35.8498,
# E 140.0014) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.74, 139.87, 35.85, 140.01)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (139.929) and the whole extent (139.879 to
# 140.001) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-station gap is 1,182 m (20 stations), over the 550 m
# that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-11: 7 lines, 25 station records, 20 station groups). N02 groups 松戸
# (JR, Keisei), 馬橋 (JR, Ryutetsu), 新松戸 (JR's two lines) and 東松戸 (JR,
# Hokuso, Keisei); it keeps 新松戸 and Ryutetsu's 幸谷, and Keisei's 八柱 and
# JR's 新八柱, apart, each a walking interchange under two names, and so does
# step 1 (trap 1). No Shinkansen, subway, tram or light rail in the city.
#
# Two one-station stubs are kept as cut (the standing call of 2026-09-27;
# both commuter railways, N02 class 12, so the urban-stub rule of calls 54
# and 92 does not reach them): the Tobu Urban Park Line at 六実 and the Keisei
# Narita Sky Access Line at 東松戸. N02 files 成田空港線 as its own line; it
# runs on the Hokuso Line's track through the city and passes 矢切, 秋山 and
# 松飛台 without a stop, so it is drawn over that track under its own name
# (Tokyo's overlapping services), and 東松戸 keeps its ring through three
# lines either way.
#
# No frequency floor (owner, 2026-10-06, calls 46 and 86). The Ryutetsu, the
# line most likely to raise the question, runs 64 weekday departures from 流山
# (every 20 minutes at midday; its own timetable page, 2024-03-16 revision,
# read 2026-10-05): not a low-frequency stretch.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
# The lines run on into Tokyo (金町 and 新柴又, 葛飾区) and, on the Musashino
# Line, toward Saitama: their N03 files name those excluded stations
# (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("13", "11")

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, and the same
# as on every other map that draws the line: Tokyo's, Mito's and Iwaki's JR
# Joban Line (one line, as Tokyo draws it: N02's 常磐線 carries the rapid,
# which stops at 松戸 alone here, and the local, which stops at all five);
# the JR Musashino Line of five maps; Tokyo's and Funabashi's Hokuso Line;
# Kasukabe's and Funabashi's Tobu Urban Park Line (N02's 野田線); Funabashi's
# Keisei Matsudo Line, the former Shin-Keisei Line (Keisei's since
# 2025-04-01), which N02-25 already files as 京成電鉄 松戸線. Keisei signs
# N02's 成田空港線 the Narita Sky Access Line (成田スカイアクセス線). The
# Ryutetsu's hue is a seed, not read from the operator (each of its trains
# wears its own colour, none the line's): a blue, clear of the green and the
# orange it runs beside. Seeded with a red (#C0392B) the search gives #E06840,
# 19.3 from the JR Musashino Line where the two cross.
_JR, _KS = "東日本旅客鉄道", "京成電鉄"
LINES = {
    "KM": {"n02": [(_KS, "松戸線")], "name": "Keisei Matsudo Line", "name_ja": "京成松戸線", "short": "Keisei",
           "hue": "#EF59A1"},
    "JJ": {"n02": [(_JR, "常磐線")], "name": "JR Joban Line", "name_ja": "常磐線", "short": "JR",
           "hue": "#00B261"},
    "JM": {"n02": [(_JR, "武蔵野線")], "name": "JR Musashino Line", "name_ja": "武蔵野線", "short": "JR",
           "hue": "#F15A22"},
    "HS": {"n02": [("北総鉄道", "北総線")], "name": "Hokuso Line", "name_ja": "北総線", "short": "Hokuso",
           "hue": "#3A9AD9"},
    "RN": {"n02": [("流鉄", "流山線")], "name": "Ryutetsu Nagareyama Line", "name_ja": "流鉄流山線",
           "short": "Ryutetsu", "hue": "#1E50A2"},
    "KA": {"n02": [(_KS, "成田空港線")], "name": "Keisei Narita Sky Access Line", "name_ja": "成田スカイアクセス線",
           "short": "Keisei", "hue": "#F18C1F"},
    "TD": {"n02": [("東武鉄道", "野田線")], "name": "Tobu Urban Park Line", "name_ja": "東武アーバンパークライン",
           "short": "Tobu", "hue": "#7FBE26"},
}
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own: the JR Joban and JR
# Musashino lines, the Hokuso Line (the grey Tokyo's map draws it in) and the
# Tobu Urban Park Line (the green Kasukabe's map draws it in).
#
# The other three are the project's own, by scripts/line_colour_search.py's
# rule with those four held fixed (2026-10-11; >= 18 within 500 m, >= 10
# city-wide, 3:1 on both map pages, CIE76 45 from every japan_eigyo pin): the
# Keisei Matsudo Line a pink-violet nearest Keisei's pink (45.8 from Food
# service, the nearest pin; 6.02 on the dark page, 3.11 on the light), the
# Ryutetsu a blue (77.8; 3.11, 6.02), the Narita Sky Access Line an orange
# nearest Keisei's (50.0 from Retail; 5.89, 3.18). Funabashi's map draws the
# Keisei Matsudo Line too, in the same #E060D0 (the same search from the same
# hue): a value for the registry.
# Measured with all seven (2026-10-11): every line 45.3 or more from its
# nearest pin (JR Joban 45.7, JR Musashino 54.7, Hokuso 53.7), except the
# Tobu Urban Park Line's shared green, 29.1 from the olive Food shops pin, AN
# ACCEPTED TRADE between 20 and 45: the shared colour is kept, and it is 45.3
# from Personal services, the one pin this map draws. Closest pair within
# 500 m 18.8 (JR Joban and Tobu Urban Park, both shared colours; their tracks
# come within 500 m only beyond the city line, toward 柏), then 26.1 (JR
# Musashino and the Sky Access Line, which meet at 東松戸); the Sky Access
# Line and the Hokuso Line, drawn over one track, 74.5. Dark-mode labels, 7
# distinct of 7.
_COLOURS = {
    "JJ": line_registry.colour("jr-east-joban-line"),
    "JM": line_registry.colour("jr-east-musashino-line"),
    "HS": line_registry.colour("hokuso-line"),
    "TD": line_registry.colour("tobu-urban-park-line"),
    "KM": line_registry.colour("keisei-matsudo-line"), "RN": "#3060B8", "KA": "#D87800",
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own stations. The Ryutetsu's timetable page links one
# timetable per station, six in all (流山 to 馬橋, as N02's 6); 馬橋, 幸谷 and
# 小金城趾 are inside the city line (the brief, 2026-10-05).
GATE3 = {"source": "Ryutetsu's own timetable page (ryutetsu.jp/timetable.html), six stations, read against the "
                   "city line: Nagareyama Line 3",
         "lines": {"RN": 3}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
MATSUDO_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = MATSUDO_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602679924)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "日本大学松戸歯学部附属歯科衛生専門学校": "a college (amenity=college, Wikipedia); 歯科 is its field, not a clinic (the Tokyo precedent); tags read 2026-10-13",
}
PLACE_DROPPED = {}
