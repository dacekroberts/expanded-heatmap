"""Matsumoto-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/matsumoto.md (12/13 checks, 2026-10-11: the one failure is
the register work's date, which moved from 2026-07-01 to 2026-10-01 on
2026-10-08; the build reads the new edition). Part of the A/B build plan's
Regional-2 batch, on the shared modules (pipeline/countries/japan*.py) with
every shared rule on. Personal services only (Band B, owner 2026-10-06, call
133: Kochi's page shape): MHLW's food file publishes an address for 35.4% of
the city's open restaurant permits, and the city's old-law ledger lifts the
placed share of fixed premises only to 42.2%, under the placement bar.

Business leg: the city's three 生活衛生 registers on LinkData.org (work
rdf1s8757i, published by 松本市 DX推進本部): barbers, beauty salons and
laundries, as of 2026-10-01. Standing registers that say nothing about closed
premises. Everything placed by a JOIN to MLIT's 位置参照情報 for 20202.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Alpico Kotsu's Kamikochi Line (wholly inside) and JR East's Shinonoi
and Oito lines, cut at the city line. English station names from
OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "matsumoto" / "raw"
DATA_PROCESSED = ROOT / "data" / "matsumoto" / "processed"
OUTPUTS = ROOT / "outputs" / "matsumoto"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Matsumoto"
SLUG = "matsumoto"
MUNICIPALITY = "松本市"
PREFECTURE = "長野県"

# The city's LinkData work 「松本市の生活衛生施設データ」 (rdf1s8757i), linked from
# the city's open-data page (city.matsumoto.nagano.jp/soshiki/5/4172.html).
# LinkData's text format: UTF-8, tab-separated, nine # header lines, which
# japan_register.city_rows reads (a first line of #LINK). Each table's header
# marks CC BY 3.0 and the attribution name 松本市 DX推進本部; the city's page
# and terms say CC BY 4.0 (read 2026-10-07; owner's call 207: both named in
# the credit).
# LinkData overwrites a table in place: the Step 0 files of 2026-10-06 are the
# 2026-07-01 edition (matsumoto_barber.txt and its siblings, kept beside
# these), and the work page moved to 「2026年10月1日現在」 on 2026-10-08. The
# build reads the newer edition, saved under dated names so the two never mix.
WORK_PAGE = "http://linkdata.org/work/rdf1s8757i"
_LINK = "http://linkdata.org/download/rdf1s8757i/link/"
REGISTERS_AS_OF = "2026-10-01"  # the work page's own line, never the download's date
# source key -> (file, URL, the dataset page that links it).
SOURCE_FILES = {
    "barber": ("matsumoto_barber_20261001.txt", _LINK + "matsumoto_barber.txt", WORK_PAGE),
    "beauty": ("matsumoto_beauty_20261001.txt", _LINK + "matsumoto_beauty.txt", WORK_PAGE),
    "laundry": ("matsumoto_cleaning_20261001.txt", _LINK + "matsumoto_cleaning.txt", WORK_PAGE),
}
SOURCE_AS_OF = {k: REGISTERS_AS_OF for k in SOURCE_FILES}
FOOD_AS_OF = None  # no food leg (MHLW's addresses fail placement; call 133)
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: LinkData's .txt is UTF-8 (no BOM), CRLF.
SOURCE_ENCODING = {k: "utf-8" for k in SOURCES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 営業者 (the operator) is REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; it is read IN MEMORY by that rule only, never kept (filled on 277
# of the 992 rows of 2026-10-01, every one with a company marker). Never
# selected: 施設郵便番号, 検査確認日, 検査確認番号 (repeats; never a key).
_REGISTER = ("施設名称", "施設所在地", "営業者")
REQUIRED_COLUMNS = {"barber": _REGISTER, "beauty": _REGISTER, "laundry": (*_REGISTER, "種別")}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 20202.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Matsumoto.
# S, W, N, E: the city's N03 extent (S 36.010, W 137.550, N 36.379,
# E 138.131) rounded out; step 1 stops if the city leaves it. The box reaches
# the Hida mountains; every drawn station lies east of 137.82 E.
OSM_BBOX = (36.00, 137.54, 36.38, 138.14)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# All 20 names read 2026-10-11. One is translated in OSM; the operator's own
# timetable of 2026-03-14 romanizes it in full.
OSM_NAME_EN_OVERRIDES = {
    "北新・松本大学前": "Kitanii-Matsumotodaigakumae",  # OSM: "Kitanii / Matsumoto Univ."
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the city runs 137.550 to 138.131 E (centroid 137.814, 松本
# station about 137.97), in the 132 to 138 band but for its eastern mountain
# edge. Derived per city, not copied - see docs/project_context.md's CRS
# lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings on the spacing rule
# (docs/ring_rules.md): step 1 measured a median nearest-station gap of 950 m
# over the 20 drawn stations (2026-10-11; the brief read 1,021 m; closest pair
# 松本 to 西松本, 417 m), above the ~550 m halving threshold. Re-measure if the
# drawn stations change.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25: 3 lines, no Shinkansen). The Kamikochi Line lies wholly inside
# (14 of 14); JR's Shinonoi Line keeps 4 of 15 and its Oito Line 4 of 33, cut
# at the city line (owner 2026-09-24). 松本 is one group on all three (JR and
# Alpico, 116 m).
_AL, _JR = "アルピコ交通", "東日本旅客鉄道"
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names carry no macrons. N02 files the
# track south of 松本 as 篠ノ井線, the legal line; JR East's Chuo Line trains run
# through over it from 塩尻 (the brief), which the map does not label: a
# parked call in the drafts entry.
LINES = {
    "AK": {"n02": [(_AL, "上高地線")], "name": "Alpico Kotsu Kamikochi Line", "name_ja": "上高地線",
           "short": "Alpico", "hue": "#0090D0"},
    "JS": {"n02": [(_JR, "篠ノ井線")], "name": "JR Shinonoi Line", "name_ja": "篠ノ井線", "short": "JR",
           "hue": "#F08300"},
    "JO": {"n02": [(_JR, "大糸線")], "name": "JR Oito Line", "name_ja": "大糸線", "short": "JR",
           "hue": "#8F4E9C"},
}
# Colours: scripts/line_colour_search.py matsumoto (2026-10-11), each 3:1 on
# both map pages. Against the pins (CIE76; aim 45): AK 71.6, JS 53.6, JO 47.6;
# closest pair of lines 51.2 (AK, JO). No line is under 45, so no accepted
# trade. None of the three is in pipeline/line_registry.py: no other map
# draws the Kamikochi, Shinonoi or Oito line (2026-10-11). The hues are this
# project's starting points, not the operators' own colours.
_COLOURS = {"AK": "#0090D0", "JS": "#E07800", "JO": "#9050A0"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: Alpico Kotsu's Kamikochi Line timetable of 2026-03-14 (the PDF
# linked from alpico.co.jp/traffic/rail/, 137,355 B, read 2026-10-11 with
# pdftotext; owner's call 176, counts only) numbers 14 stations, AK01 松本 to
# AK14 新島々, as N02 has 14, and 25 trains each way a day. JR is cut at the
# city line.
GATE3 = {"source": "Alpico Kotsu's Kamikochi Line timetable of March 14, 2026 (alpico.co.jp/traffic/rail/): "
                   "14 stations, AK01 松本 to AK14 新島々",
         "lines": {"AK": 14}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
MATSUMOTO_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = MATSUMOTO_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3603648972)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/matsumoto.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # A glitched name (owner, 2026-10-13)
    "node/10781534710": "'ｖ': a single stray letter as the name of a peak",
    # A bare type word (owner, 2026-10-13)
    "node/12705583085": "'ピクニック広場': picnic plaza, type words only; a sub-area node tagged a park, operator the prefecture",
    # Unsure rows a ruling drops: a stock plaza or rest-area name with no place in it (ruling 5) (owner, 2026-10-13)
    "node/12697321693": "'ふれあい広場': a stock plaza or rest-area name with no place in it",
    "node/12705616062": "'親しみ広場': a stock plaza or rest-area name with no place in it",
    "way/691453526": "'いこいの広場': a stock plaza or rest-area name with no place in it",
    "way/553893486": "'憩いの広場': a stock plaza or rest-area name with no place in it",
}
