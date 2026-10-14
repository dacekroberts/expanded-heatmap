"""Kure-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/kure.md (8/8 checks, 2026-10-11). Part of the A/B build
plan's Regional-2 batch, on the shared modules (pipeline/countries/japan*.py)
with every shared rule on. Food only (Band B with the food share stated,
owner 2026-10-06, call 185), in Kurume's and Okayama's shape: ONE source.

Business leg: MHLW's 食品衛生申請等システム open data for 34202 alone (every
permit and notification the city's health center entered since 2021-06;
opt-in, field by field). The city publishes no food list of its own and no
barber, beauty-salon or laundry list, so there are no personal services.
Placed by a JOIN to MLIT's 位置参照情報 (one municipality, no wards); where
the block join misses, MHLW's own point (OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03). JR West's Kure Line alone; no Shinkansen, tram or subway.
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kure" / "raw"
DATA_PROCESSED = ROOT / "data" / "kure" / "processed"
OUTPUTS = ROOT / "outputs" / "kure"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kure"
SLUG = "kure"
MUNICIPALITY = "呉市"
PREFECTURE = "広島県"

# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2,
# termsofuse.htm; read 2026-09-24 for Fukuoka, re-read 2026-10-02). A plain
# GET. Credit links the top page only, as the site asks.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    "mhlw": ("34202_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=34202_food_business_all.csv",
             MHLW_TOP),
}
# MHLW's monthly file states no date: its newest 許可年月日 is 2026-08-28 and
# its closures are dated 2026-08-20 and 2026-08-31 (Step 0, 2026-10-06:
# 1,149,444 B, 3,538 rows), and the page dates it by download
# (provenance.json).
SOURCE_AS_OF = {"mhlw": None}
FOOD_AS_OF = None
# The file carries each permit's 許可満了日 and 許可開始日: the term rules
# (calls 161 and 172) read them against the file's last day (its latest
# 廃業年月日, 2026-08-31), never today. No restaurant permit past its expiry
# is listed; 3 restaurant permits start on 2026-09-01 or 2026-10-01 and wait
# (the brief, 2026-10-06).
TERM_AS_OF = {"mhlw": "2026-08-31"}
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: UTF-8 with a BOM, CRLF.
SOURCE_ENCODING = {"mhlw": "utf-8-sig"}
# The columns the file must carry; fetch_sources.py and step 2 stop on a
# header without them. MHLW's 法人名 holds a sole trader's own name as well
# as a company's (filled on 907 of the 1,768 storefront rows, 126 with no
# company marker; the brief, 2026-10-06), so it is REQUIRED and read IN
# MEMORY by the name rule only, never kept (owner 2026-10-05). Never
# selected: 法人番号, 法人住所 and 営業施設電話番号.
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's): a
# row without one is counted apart for the page's disclosure (the brief:
# 1,169 open rows with a blank address).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses, MHLW's own point places it (call 127c; the
# brief's check: a median 34 m from the block point, 96.1% within 250 m over
# 1,557 rows).
OWN_POINT_FALLBACK = {"mhlw"}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 34202.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Kure.
# S, W, N, E: the city's N03 extent (S 34.028, W 132.446, N 34.333,
# E 132.869; the islands of 倉橋, 蒲刈, 豊 and 豊浜 to the south and east carry
# no rail) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.02, 132.44, 34.34, 132.87)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Every name:en read 2026-10-11 (20 objects, all with name:en): Hepburn
# without macrons throughout (Tenno, Ato), as Hiroshima's map writes its
# stations; no override needed.
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the city runs 132.446 to 132.869 E, inside the 132 to 138
# band. Derived per city, not copied - see docs/project_context.md's CRS
# lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings on the spacing rule
# (docs/ring_rules.md): step 1 measured a median nearest-station gap of
# 1,442 m over the 13 drawn stations (2026-10-11, minimum 1,170 m; the brief
# read the same), far above the ~550 m halving threshold. Re-measure if the
# drawn stations change.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25, 2026-10-06: 1 line, 13 station records in 13 groups; no
# Shinkansen runs in Kure). The Kure Line keeps 13 of 28, cut at the city
# line (owner 2026-09-24), one contiguous stretch along the coast from
# 呉ポートピア to 安浦 (step 1 reproduced 13 on 2026-10-11; within 3 km beyond
# the line it names 小屋浦 and 水尻 in 坂町 and 風早 in 東広島市). Heavy rail (N02
# class 11); no tram or light rail.
# No frequency floor (owner, 2026-10-06, calls 46 and 86): the fewest trains
# read is 20 a day (安浦 toward 三原; JR West's station timetables for
# 2026-10-07, read 2026-10-06 for the brief), so no stretch is low-frequency.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue and the project's colour. The name is as
# Hiroshima's map writes the same line.
_JW = "西日本旅客鉄道"
LINES = {
    "JY": {"n02": [(_JW, "呉線")], "name": "JR Kure Line", "name_ja": "呉線", "short": "JR", "hue": "#F39800"},
}
# Colour. SHARED LINE: Hiroshima's map draws the Kure Line too (its one
# station 矢野, key JY), so the colour, #D08000, is read from
# pipeline/line_registry.py, where the line was registered with this build
# (owner, 2026-10-07: one colour per line on every map).
# Margins from the pins (step 3, 2026-10-11, CIE76): 43.0 from Food shops
# olive #737a00, the nearer pin; between 20 and 45, an accepted trade, as on
# Hiroshima's map, since the colour is the line's own site-wide. One line, so
# no pair to separate.
_COLOURS = {"JY": line_registry.colour("jr-west-kure-line")}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3 has no in-city count to compare: the line runs on past the city line
# at both ends (Aomori's and Tottori's shape). JR West's station timetable
# pages (timetable.jr-odekake.net) were read for 11 of the 13 stations
# (2026-10-06, the brief; 安登 and かるが浜 not read); the operator's per-line
# station list was not read, so N02's whole-line total (28 records) stands
# unchecked against the operator.
GATE3 = {"source": "none: no line is wholly inside the city (JR West's station timetable pages, "
                   "timetable.jr-odekake.net, read for 11 of the 13 stations)", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KURE_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KURE_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3604089279)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "焼山南ハイツ入口": "a signed junction (highway=traffic_signals) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
}
PLACE_DROPPED = {}
