"""Ichihara-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/ichihara.md (13/13 checks, 2026-10-11). Ichihara City (市原市,
12219), one municipality with no wards. Japan's A/B batch (East-2), one of
the six Chiba pages on the shared Chiba leg
(pipeline/countries/chiba_pref.py), in Matsudo's shape: personal services
only (Band B, owner 2026-10-06), a full list per kind plus the months since.

Business leg: Chiba Prefecture's open-data lists of barbers, beauty salons and
laundries (dataset 6 on opendata.pref.chiba.lg.jp, PDL 1.0), the 市原 health
center's sheet (Ichihara alone) cut to the city by address. Barbers as of
2025-03-31, built as published with their own date (owner, call 33); beauty
salons and laundries the 2026-03-31 lists plus the months to 2026-08-31, an
upper bound (owner, call 34). The lists hold only premises whose operators
agreed to open publication, disclosed with no number. The laundry list is
about four in five of a census-based estimate, built and the share stated on
the page (owner, call 123, in the shape of Ichikawa's call 32). No food layer
(the prefecture's food set is old-law only) and no MHLW source. Placed by a
JOIN to MLIT's 位置参照情報 for the one municipality; about half the addresses
are 地番, and the rural south's 大字 carry no block points, so the block tier
is lower than the other Chiba pages' (the brief: 93.2%).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): the Kominato Railway Line (17 of N02's 18 stations), JR East's
Uchibo Line (3 of 30) and a one-station stub kept as cut (the standing call),
the Keisei Chihara Line at its terminus ちはら台 (1 of 6). English station
names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline.countries import chiba_pref

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "ichihara" / "raw"
DATA_PROCESSED = ROOT / "data" / "ichihara" / "processed"
OUTPUTS = ROOT / "outputs" / "ichihara"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Ichihara"
SLUG = "ichihara"
MUNICIPALITY = "市原市"
PREFECTURE = chiba_pref.PREFECTURE
# Ichihara is the 市原健康福祉センター's whole area: its sheet in each of the
# prefecture's workbooks holds Ichihara alone (chiba_pref.SHEET_AREAS). The
# barber sheet's header is written with a half-width digit (施設名称1,
# 施設所在地1) and the 2026-08 beauty month's with none (施設名称); the module
# reads both through chiba_pref.HEADER_ALIASES.
HEALTH_CENTER = "市原"

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
# (2026-10-06): barbers 218 (the 2025-03-31 list), beauty salons 414 listed +
# 9 from the months, laundries 75 + 1 (none a 無店舗取次店). A different count
# stops step 2: a new edition is re-measured and the brief corrected, never
# passed silently. A read that skipped the barber sheet (the half-width
# header) would stop here at 0 of 218.
EXPECTED_ROWS = {"barber": 218, "beauty": 423, "laundry": 76}


def source_csv(key):
    """A file in the shared Chiba cache, by file key or step-2 source key."""
    return chiba_pref.source_path(key)


def source_rows(key):
    """The city's rows of each register: the 市原 sheet of the base list and
    of each approved month, cut by address at 市原市 (chiba_pref.city_rows), as
    MLIT's 市区町村名 and the lists' addresses write it; the step stops naming
    fetch_sources.py where a file is missing."""
    from pipeline.countries.japan_step2 import need
    for k in SOURCE_FILES:
        need(source_csv(k), SLUG)
    return chiba_pref.city_rows(key, MUNICIPALITY, HEALTH_CENTER, expect=EXPECTED_ROWS[key])


def file_rows(key):
    """One file's rows as it stands, for fetch_sources.py's count and column check."""
    return chiba_pref.file_rows(key)


# MLIT 位置参照情報, block (24.0a) and town-chome (19.0b), for 12219 alone
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.2312, W 140.0098, N 35.5618,
# E 140.2602) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.23, 140.0, 35.57, 140.27)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
# N02 writes JR's 姉ヶ崎 with the small ヶ; OSM's object (as JR East's own
# station name) writes 姉ケ崎. The alias reads OSM's name:en, Anegasaki.
OSM_NAME_ALIASES = {"姉ヶ崎": "姉ケ崎"}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (140.137) and the whole extent (140.010 to
# 140.260) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-station gap is 1,811 m (20 stations; closest pair
# 1,312 m), over the 550 m that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-11: 3 lines, 21 station records, 20 station groups; no Shinkansen,
# subway, tram or light rail, every line a railway of N02 class 11 or 12):
#   * the Kominato Railway's 小湊鐵道線 17 of 18 (五井 to 養老渓谷; the 18th,
#     上総中野, is Otaki's), drawn (owner, 2026-10-06, call 46). The 房総里山
#     トロッコ, a sightseeing train on specified days, runs on the same track
#     and needs no line of its own;
#   * JR East's 内房線 3 of 30 (八幡宿, 五井, 姉ヶ崎), cut at the city line both
#     ways (owner 2026-09-24);
#   * Keisei's 千原線 1 of 6, its terminus ちはら台: a one-station stub kept as
#     cut (the standing call of 2026-09-27, and the owner for this city,
#     2026-10-06). A commuter railway (class 12), so the urban-stub rule of
#     calls 54 and 92 does not reach it, and it is not in LEFT_OUT_LINES.
# N02 groups 五井 (JR and the Kominato Railway, one interchange); no other
# group holds two operators.
#
# No frequency floor (owner, 2026-10-06, calls 46 and 86). ONE LOW-FREQUENCY
# STRETCH, drawn and named on the page with its reason: the Kominato Railway
# south of 上総牛久 (上総川間 to 養老渓谷, 9 stations): 10 trains each way on a
# weekday, 9 of them running the whole way to or from 養老渓谷 and 1 turning
# at 里見, against 26 a day (one every 40 minutes at midday) between 五井 and
# 上総牛久. Counted by train number from the weekday rows of the railway's own
# timetable page (kominato.co.jp/timetable/, the 2026-03-14 revision, read
# 2026-10-11): one more train each way (617, 628) and the 房総里山トロッコ
# (501, 502) run on specified days only, which is how the brief's column
# count read 11 to 12. Re-count if the revision changes (the brief's check
# pins it). JR's Uchibo Line runs about 3 an hour at 五井 (JR East's
# timetable page, the brief).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
# Every line runs on inside Chiba Prefecture (千葉市, 袖ケ浦市, 大多喜町), whose
# N03 file step 1 already reads for the city: no neighbor prefecture.
N03_NEIGHBOR_PREFS = ()

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons. No built map
# draws any of the three (pipeline/line_registry.py has no entry for them,
# 2026-10-11), so each is new to the site. JR East's line colour for the
# Uchibo Line is a blue; Keisei signs the Chihara Line in its own blue
# (Funabashi's seed for the Keisei Main Line). The Kominato Railway's hue is a
# seed, not read from the operator (its trains wear cream and vermilion, no
# line colour; Matsudo's Ryutetsu the precedent): a vermilion, clear of the
# two blues.
LINES = {
    "KR": {"n02": [("小湊鐵道", "小湊鐵道線")], "name": "Kominato Railway Line", "name_ja": "小湊鉄道線",
           "short": "Kominato", "hue": "#D9432A"},
    "JU": {"n02": [("東日本旅客鉄道", "内房線")], "name": "JR Uchibo Line", "name_ja": "内房線", "short": "JR",
           "hue": "#00B2E5"},
    "KC": {"n02": [("京成電鉄", "千原線")], "name": "Keisei Chihara Line", "name_ja": "京成千原線", "short": "Keisei",
           "hue": "#005AAA"},
}
# All three are the project's own colours, by scripts/line_colour_search.py's
# rule (2026-10-11; >= 18 within 500 m, >= 10 city-wide, 3:1 on both map
# pages, CIE76 45 from every japan_eigyo pin), each the feasible colour
# nearest its hue: the Kominato Railway Line a vermilion (45.0 from Food
# service, the nearest pin; 6.01 on the dark page, 3.12 on the light), the JR
# Uchibo Line a blue (60.2 from Personal services; 6.19, 3.03), the Keisei
# Chihara Line a deeper blue (78.1 from Food service; 3.02, 6.19). No line
# sits between 20 and 45 from a pin. The one pair within 500 m, the Kominato
# Railway and JR Uchibo lines (they meet at 五井), 110.7; closest pair
# anywhere 37.4 (JR Uchibo and Keisei Chihara, whose tracks stay more than
# 500 m apart). Dark-mode labels, 3 distinct of 3.
# The vermilion is the value the registry holds for the JR Keiyo Line
# (#F86040), a line no nearer than Soga, in Chiba City, and on no map within
# the neighbor rule's 2 km: two lines, one colour by the search, not an
# identity.
_COLOURS = {"KR": "#F86040", "JU": "#00A0D0", "KC": "#2860B0"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own stations. The Kominato Railway's station pages
# list 18 stations on the line, 五井 to 上総中野 (as N02's 18; its menu adds
# 安房小湊, a bus connection, not on the line), 17 of them inside the city
# line (the brief, 2026-10-06). JR East's Uchibo Line and Keisei's Chihara
# Line are cut at the city line and have no independent count here.
GATE3 = {"source": "The Kominato Railway's own station pages (kominato.co.jp), 18 stations from Goi to "
                   "Kazusa-Nakano, read against the city line: Kominato Railway Line 17",
         "lines": {"KR": 17}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
ICHIHARA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = ICHIHARA_BBOX
