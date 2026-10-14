"""Aomori-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/aomori.md (8/8 checks, 2026-10-11). Part of the A/B build
plan's Regional-2 batch, on the shared modules (pipeline/countries/japan*.py)
with every shared rule on. Food only (Band B, owner 2026-10-06: Hiroshima's
page shape): the city publishes no barber, beauty-salon or laundry list.

Business leg: the city's own 食品営業許可施設一覧 (保健所 生活衛生課, CC BY 4.0
through 青森市オープンデータ利用規約), ONE file of every food permit in term on
2026-08-31, republished whole each month, so nothing is rebuilt (Akita's
shape). MHLW's open data for 02201 is a control only, read by no step (the
brief: 119 of its 120 permits are in the city's list; Gifu's and Toyama's
precedent). Everything placed by a JOIN to MLIT's 位置参照情報 (one
municipality, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR East's Ou and Tsugaru lines and the Aoimori Railway Line. English
station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "aomori" / "raw"
DATA_PROCESSED = ROOT / "data" / "aomori" / "processed"
OUTPUTS = ROOT / "outputs" / "aomori"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Aomori"
SLUG = "aomori"
MUNICIPALITY = "青森市"
PREFECTURE = "青森県"

# The city's own CMS (no catalogue API); the file is a plain GET under
# /_res/projects/default_project/_page_/001/006/184/. The dataset page carries
# 「この作品はクリエイティブ・コモンズ 表示 4.0 国際 ライセンスの下に提供されています」;
# the city's 青森市オープンデータ利用規約 prescribes the credit (clause 3(2)).
# Read 2026-10-07 by staging (licence-read): permitted with conditions,
# fault-based cost clauses (DECISIONS.md, "Licence reads for the Japan
# builds").
_HOST = "https://www.city.aomori.aomori.jp"
# 保健所 生活衛生課: 食品営業許可施設一覧（オープンデータ）, page 1006184 (更新日
# 2026-09-15; refreshed monthly, on the 15th).
FOOD_PAGE = _HOST + "/shisei/jouhokoukai/opendata/1006170/1006184.html"
# source key -> (file, URL of the edition this build read, the page that
# carries its licence). One file (Step 0, 2026-10-06, HTTP 200 from the city's
# own host, 929,390 B). The file is RENAMED each month (r0808zendate is the
# list to the end of R8-08), so a refresh reads the page for the new name and
# re-measures; the pinned URL records which edition this build read.
SOURCE_FILES = {
    "food": ("r0808zendate.csv", _HOST + "/_res/projects/default_project/_page_/001/006/184/r0808zendate.csv",
             FOOD_PAGE),
}
# Kyoto's rule: the date the list states, never the download's. The page
# names the file 食品営業許可施設一覧（8月末時点全件）.
FOOD_AS_OF = "2026-08-31"
SOURCE_AS_OF = {"food": FOOD_AS_OF}
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. The list holds every permit in
# term on its date (every 許可満了日 is on or after 2026-08-31, the brief).
TERM_AS_OF = {"food": FOOD_AS_OF}

SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: UTF-8 with a BOM, CRLF, the header on line 1.
SOURCE_ENCODING = {"food": "utf-8-sig"}
# The columns the file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns (申請者氏名, on every row, with no
# company marker on 3,080 of 5,289, the shape of a sole trader's own name, and
# 代表者氏名) are REQUIRED so the name rule (japan_register.name_is_operator;
# owner 2026-09-27) cannot silently compare nothing; read IN MEMORY by that
# rule only, never kept. Never selected: 施設の電話番号, 申請者住所1 and 住所２ (an
# operator's own address).
REQUIRED_COLUMNS = {
    "food": ("施設の名称、屋号", "施設の所在地１", "営業許可業種", "許可番号", "許可年月日", "許可満了日", "申請者氏名",
             "代表者氏名"),
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 02201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Aomori.
# S, W, N, E: the city's N03 extent (S 40.606, W 140.520, N 40.970,
# E 140.981; the 2005 merger brought in 浪岡町) rounded out; step 1 stops if
# the city leaves it.
OSM_BBOX = (40.60, 140.51, 40.98, 140.99)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}). None is needed: OSM's 18 names
# stand as they are (31 objects, all with name:en, 2026-10-11; no macron, a
# hyphen before a place name or 温泉: Shin-Aomori, Tsugaru-Shinjo,
# Asamushi-Onsen; 鶴ヶ坂 reads Tsurugasaka, 中沢 Nakasawa as JR East signs it).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (~140.754) and the whole extent (140.520 to
# 140.981) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings on the spacing rule
# (docs/ring_rules.md): step 1 measured a median nearest-station gap of 1,819 m
# (minimum 1,289 m) over the 18 drawn stations (2026-10-11; the brief read
# 1,844 m), far over the halving line (about 550 m). Re-measure if the drawn
# stations change.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25: 3 lines; the Shinkansen's 新青森 dropped, JR's conventional 新青森
# kept on the Ou Line). Every line is cut at the city line (owner
# 2026-09-24): the Ou Line keeps 6 of 105 station records, the Tsugaru Line 7
# of 18, the Aoimori Railway Line 7 of 27; none is cut to one station. 青森 is
# one N02 group for all three lines (0 m). No frequency floor (owner,
# 2026-10-06, calls 46 and 86): the Tsugaru Line runs 9 trains a weekday
# toward 蟹田 and 8 toward 青森 (JR East's weekday timetables at 油川 and 中沢,
# read 2026-10-06 for the brief), drawn and named on the page as
# low-frequency.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), a starting hue for scripts/line_colour_search.py (`hue`) and the
# project's colour. Line names carry no macrons and no "Main" for JR, as
# Akita's and Fukushima's JR Ou Line (the same line).
_JR, _AO = "東日本旅客鉄道", "青い森鉄道"
LINES = {
    "OU": {"n02": [(_JR, "奥羽線")], "name": "JR Ou Line", "name_ja": "奥羽本線", "short": "JR",
           "hue": "#E07800"},
    "TS": {"n02": [(_JR, "津軽線")], "name": "JR Tsugaru Line", "name_ja": "津軽線", "short": "JR",
           "hue": "#3CB371"},
    "AO": {"n02": [(_AO, "青い森鉄道線")], "name": "Aoimori Railway Line", "name_ja": "青い森鉄道線",
           "short": "Aoimori", "hue": "#00A0E9"},
}
# Colours: JR East's Ou Line takes its one site-wide colour from
# pipeline/line_registry.py (owner, 2026-10-07: one colour per line on every
# map; Akita's and Fukushima's maps draw it). The Tsugaru Line and the Aoimori
# Railway Line are on this map alone: the project's own colours, from `python
# scripts/line_colour_search.py aomori` (2026-10-11, defaults: >= 18 within
# 500 m, >= 10 city-wide), each the feasible colour nearest its starting hue
# (a JR East green; the Aoimori Railway's sky blue) that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Margins from the pins: Ou 53.6,
# Tsugaru 45.6, Aoimori 75.4 (none between 20 and 45). Closest pair 94.2 (Ou,
# Tsugaru; all three meet at 青森); the dark-mode labels separate, 3 of 3.
_COLOURS = {"OU": line_registry.colour("jr-east-ou-line"), "TS": "#28A800", "AO": "#0098E0"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3 has no in-city count to compare: every line runs on past the city
# line (Fukui's shape). JR East's station timetable pages
# (timetables.jreast.co.jp) were read for six of the 18 stations (青森, 新青森,
# 鶴ケ坂, 浪岡, 油川, 中沢; 2026-10-06, the brief); neither operator's per-line
# station list was read, so N02's whole-line totals (Ou Line 105 records,
# Tsugaru Line 18, Aoimori Railway Line 27) stand unchecked against the
# operators. Step 1 reproduced the brief's in-city counts 2026-10-11 (6, 7,
# 7; 18 stations).
GATE3 = {"source": "none: no line is wholly inside the city (JR East's station timetable pages, "
                   "timetables.jreast.co.jp, read for six of the 18 stations)", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
AOMORI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = AOMORI_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3604107337)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
PLACE_DROPPED = {}
