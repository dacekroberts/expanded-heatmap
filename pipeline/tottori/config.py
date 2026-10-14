"""Tottori-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/tottori.md (7/7 checks, 2026-10-11). Part of the A/B build
plan's Regional-2 batch, on the shared modules (pipeline/countries/japan*.py)
with every shared rule on. Food only (Band B, owner 2026-10-06), in Kurume's
and Okayama's shape: ONE source.

Business leg: MHLW's 食品衛生申請等システム open data for 31201 alone (every
permit and notification the city's health center entered since 2021-06;
opt-in, field by field). The health center also licenses the four eastern
towns (岩美町, 八頭町, 若桜町, 智頭町) and files them under 鳥取市: the shared
other-municipality rule cuts them by ADDRESS, never by a bounding box. Neither
the city nor the prefecture publishes a barber, beauty-salon or laundry list,
so there are no personal services. Placed by a JOIN to MLIT's 位置参照情報 (one
municipality, no wards); where the block join misses, MHLW's own point
(OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03). JR West's San'in and Inbi lines; no Shinkansen, tram or subway.
English station names from OpenStreetMap's name:en.
"""

import re
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "tottori" / "raw"
DATA_PROCESSED = ROOT / "data" / "tottori" / "processed"
OUTPUTS = ROOT / "outputs" / "tottori"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Tottori"
SLUG = "tottori"
MUNICIPALITY = "鳥取市"
PREFECTURE = "鳥取県"

# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2,
# termsofuse.htm; read 2026-09-24 for Fukuoka, re-read 2026-10-02). A plain
# GET. Credit links the top page only, as the site asks.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    "mhlw": ("31201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=31201_food_business_all.csv",
             MHLW_TOP),
}
# MHLW's monthly file states no date: its newest 許可年月日 is 2026-08-26 and
# its closures run 2026-08-18 to 2026-08-31 (Step 0, 2026-10-06: 1,629,218 B,
# 4,782 rows), and the page dates it by download (provenance.json).
SOURCE_AS_OF = {"mhlw": None}
FOOD_AS_OF = None
# The file carries each permit's 許可満了日 and 許可開始日: the term rules
# (calls 161 and 172) read them against the file's last day (its latest
# 廃業年月日, 2026-08-31), never today. No restaurant permit past its expiry
# is listed (the brief, 0).
TERM_AS_OF = {"mhlw": "2026-08-31"}
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: UTF-8 with a BOM, CRLF.
SOURCE_ENCODING = {"mhlw": "utf-8-sig"}
# The columns the file must carry; fetch_sources.py and step 2 stop on a
# header without them. MHLW's 法人名 holds a sole trader's own name as well
# as a company's (filled on 4,404 of 4,782 rows, 2,154 with no company
# marker; the brief, 2026-10-06), so it is REQUIRED and read IN MEMORY by the
# name rule only, never kept (owner 2026-10-05). Never selected: 法人番号,
# 法人住所 and 営業施設電話番号.
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's): a
# row without one is counted apart for the page's disclosure. A blank-address
# row cannot be split between the city and the four towns (the brief: 650
# rows, 34 of them open restaurants).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses, MHLW's own point places it (call 127c; the
# brief's check: a median 39 m from the block point, 96.1% within 250 m over
# 2,121 rows). The four towns' rows never reach it: the shared
# other-municipality rule sets them aside by address first (370 of them carry
# a point inside the city's box).
OWN_POINT_FALLBACK = {"mhlw"}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# The health center writes a prefecture-wide permit (a stall or vehicle
# licensed across the prefecture, Kobe's trap 6) AFTER the city's name:
# 鳥取県鳥取市鳥取県内 (226 rows), 鳥取県鳥取市鳥取県東部 (4),
# 鳥取県鳥取市鳥取県 (3) and 鳥取県鳥取市県内 (3). The shared area-wide rule
# tests the address again after the city cut and sets them aside (call S19,
# japan_register.permits_from_rows, 2026-10-12; a city-local hook did it
# until then). Measured without either, 208 such rows reached the map at
# MHLW's own point. The shared rule does not stop on an unknown spelling:
# re-read the addresses naming the prefecture when the file is refreshed.


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 31201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Tottori.
# S, W, N, E: the city's N03 extent (S 35.272, W 133.946, N 35.573,
# E 134.441; the 2004 mergers brought in 国府, 福部, 河原, 用瀬, 佐治, 気高, 鹿野
# and 青谷) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.27, 133.94, 35.58, 134.45)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30), as Shimonoseki's and Kurume's:
# no macrons, 前 as -mae, lowercase after a hyphen for a common word. The
# other 11 are OSM's as they stand (26 objects, all with name:en, 2026-10-11;
# Inaba-Yashiro keeps its hyphen before a place name).
OSM_NAME_EN_OVERRIDES = {
    "宝木": "Hogi",                                  # Hōgi
    "鳥取大学前": "Tottori-daigaku-mae",             # Tottoridaigaku-Mae
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the N03 centroid (~134.158) and the whole extent (133.946 to
# 134.441) fall in the 132 to 138 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings on the spacing rule
# (docs/ring_rules.md): step 1 measured a median nearest-station gap of
# 2,924 m (minimum 1,237 m) over the 13 drawn stations (2026-10-11; the brief
# read the same), far over the halving line (about 550 m). Re-measure if the
# drawn stations change.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25, reproduced by step 1 2026-10-11: 2 lines, 14 station records, 13
# groups; no Shinkansen runs in Tottori). Both are cut at the city line (owner
# 2026-09-24): the San'in Line keeps 8 of 161 station records, the Inbi Line
# 6 of 19; neither is cut to one station. 鳥取 is one N02 group on both lines
# (0 m). Both are heavy rail (N02 class 11); no tram or light rail.
# THE INBI LINE IS INSIDE THE CITY IN TWO PIECES (鳥取 and 津ノ井; then 国英,
# 鷹狩, 用瀬 and 因幡社), either side of 八頭町 (東郡家, 郡家, 河原): drawn as cut,
# two pieces with a gap of about 10 km, labelled on each (owner, 2026-10-06,
# call 180).
# No frequency floor (owner, 2026-10-06, calls 46 and 86): the Inbi Line's
# southern piece sees about 12 trains a day out of 鳥取 (10 locals to 智頭 and
# 2 to 上郡; JR West's station timetable for 2026-10-07, read 2026-10-06 for
# the brief; the 14 limited expresses are not known to stop there), drawn and
# named on the page as low-frequency. 津ノ井 sees 18 locals; the San'in Line
# runs 18 or more a day each way.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), a starting hue for scripts/line_colour_search.py (hue) and the
# project's colour. Line names carry no macrons and no "Main" for JR, as
# Matsue's and Shimonoseki's JR San'in Line (the same line).
_JW = "西日本旅客鉄道"
LINES = {
    "SN": {"n02": [(_JW, "山陰線")], "name": "JR San'in Line", "name_ja": "山陰本線", "short": "JR",
           "hue": "#E60012"},
    "IB": {"n02": [(_JW, "因美線")], "name": "JR Inbi Line", "name_ja": "因美線", "short": "JR",
           "hue": "#009944"},
}
# Colours. SHARED LINE: JR West's San'in Line is also on Matsue's and
# Shimonoseki's maps; its colour, #E80010, is read from
# pipeline/line_registry.py (owner, 2026-10-07: one colour per line on every
# map). The Inbi Line is on this map alone: the project's own colour, from
# scripts/line_colour_search.py tottori (2026-10-11, defaults: >= 18 within
# 500 m, >= 10 city-wide), the feasible colour nearest its starting hue (a
# green, chosen to stand apart from the San'in Line's red; not claimed as the
# operator's) that reads 3:1 on both map pages and clears CIE76 45 from every
# pin. Margins from the pins: San'in 51.6, Inbi 45.6 (none between 20 and
# 45). Closest pair 134.7 (the two meet at 鳥取); the dark-mode labels
# separate, 2 of 2.
_COLOURS = {"SN": line_registry.colour("jr-west-sanin-line"), "IB": "#28A800"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3 has no in-city count to compare: both lines run on past the city
# line (Aomori's and Fukui's shape). JR West's station timetable pages
# (timetable.jr-odekake.net) were read for 鳥取 and 鳥取大学前 (2026-10-06, the
# brief); the operator's per-line station list was not read, so N02's
# whole-line totals (San'in Line 161 records, Inbi Line 19) stand unchecked
# against the operator. Step 1 reproduced the brief's in-city counts
# 2026-10-11 (8 and 6; 13 stations).
GATE3 = {"source": "none: no line is wholly inside the city (JR West's station timetable pages, "
                   "timetable.jr-odekake.net, read for two of the 13 stations)", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
TOTTORI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = TOTTORI_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3604110890)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/tottori.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # Worship named only by its body or chain (owner, 2026-10-13)
    "node/11416571301": "'MOAインターナショナル': the name is only the religious body (MOA International); no branch or place name, no religion tag",
    # A bare type word (owner, 2026-10-13)
    "way/1074679293": "'テニス場': \"tennis ground\", a type word; a court inside the Fuse sports park tagged a stadium",
    "way/399683910": "'野球場': \"baseball ground\", a type word; a facility of the Fuse sports park",
    "way/358227005": "'陸上競技場': \"athletics stadium\", a type word; a facility of the Fuse sports park",
    "way/602204728": "'投てき練習場': \"throwing practice ground\", a facility type, not a name",
    "way/602426553": "'中央広場': \"central plaza\", a type word; a square inside the Fuse sports park",
    "node/5725877481": "'親水広場': \"waterside plaza\", a type word; a point inside the Fuse sports park",
    "node/4265566627": "'親水公園': \"waterside park\", a park type with no place name",
    "node/4489250849": "'緑地公園': \"green-space park\", two type words and no place name",
    "node/11262433345": "'御神燈': \"sacred lantern\", the object's type; tagged a monument",
    # A description standing in for a name (owner, 2026-10-13)
    "way/399712885": "'第一補助競技場': \"first auxiliary field\", a numbered facility of the sports park, not a name",
    "way/454856539": "'第二補助競技場': \"second auxiliary field\", a numbered facility of the sports park, not a name",
    "way/729336309": "'小さい公園': \"small park\", a mapper's description",
    "node/13063048596": "'火山灰露出地': \"volcanic ash exposure\", a description of the ground in the dunes; two rows carry it",
    "node/13063105320": "'火山灰露出地': \"volcanic ash exposure\", the second row of the same description, 600 m from the first",
    # A second row of one object (owner, 2026-10-13)
    "way/391990007": "'犬山神社祈祷殿': the prayer hall of 犬山神社 (way/391990005, 155 m), a part of the shrine with a row of its own",
    # Unsure rows a ruling drops: a park named only by a category and a lot or inventory number (ruling 1) (owner, 2026-10-13)
    "way/377421649": "'１号公園': a park named only by a category and a lot or inventory number",
    # Unsure rows a ruling drops: a religious body's meeting hall or branch tagged a place of worship (ruling 2) (owner, 2026-10-13)
    "way/423955062": "'真如苑 鳥取布教所': a religious body's meeting hall or branch tagged a place of worship",
}
