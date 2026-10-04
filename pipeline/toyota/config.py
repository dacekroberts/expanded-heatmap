"""Toyota-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/toyota.md
(14/14 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py), in Kawasaki's shape: the city's own lists, all
three buckets.

Business leg: the city's CC BY 4.0 lists on BODIK (organisation 232114): the
standing food-permit list as of 2026-08-31 (temporary and stall permits left
out by the city, so 75% of the official restaurant count) and the standing
barber, beauty-salon and laundry registers of the same date, placed by a JOIN
to MLIT's 位置参照情報 for the one municipality (no wards). MHLW's open data
for Toyota holds only the opt-in online filings: not used.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03). The Aichi Loop Line, Meitetsu's Mikawa and Toyota Lines and
Linimo; no JR station and no Shinkansen in the city. English station names
from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "toyota" / "raw"
DATA_PROCESSED = ROOT / "data" / "toyota" / "processed"
OUTPUTS = ROOT / "outputs" / "toyota"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Toyota"
SLUG = "toyota"
MUNICIPALITY = "豊田市"
PREFECTURE = "愛知県"

# The city's two BODIK datasets, both license_id cc-by-40-intl, under the
# 豊田市オープンデータカタログページ利用規約 (odcs.bodik.jp/232114/tos/, the
# city's copy at city.toyota.aichi.jp .../1019046.html), CC BY 4.0
# International; the registers' dataset title lacks the word オープンデータ the
# terms use for their scope, and the permitting reading is accepted (owner,
# 2026-10-02, Hiroshima's precedent).
BODIK = "https://data.bodik.jp"
BODIK_API = BODIK + "/api/3/action"
FOOD_PAGE = BODIK + "/dataset/232114_permit_food_facility"
ENV_PAGE = BODIK + "/dataset/232114_environmental_health_service_facility"
TERMS = "https://odcs.bodik.jp/232114/tos/"
_FOOD_DS = BODIK + "/dataset/385d18b1-7493-4a82-8b0d-b00d2996da69/resource/"
_ENV_DS = BODIK + "/dataset/57c36023-1519-4f73-9bd6-ca6dd4df7493/resource/"
# source key -> (file, URL of the edition this build read, the dataset page
# that carries its licence). Every register resource is named _20268.xlsx, so
# each is saved under its own name; the food file is renamed each month. The
# fetch reads each resource's current URL from CKAN (SOURCE_RESOURCES).
SOURCE_FILES = {
    "food": ("20260907_0800.xlsx", _FOOD_DS + "91fe2bf3-0a1a-4daa-acf4-5737ca31ab83/download/20260907_0800.xlsx",
             FOOD_PAGE),
    "barber": ("riyo_202608.xlsx", _ENV_DS + "cec8cb27-29e7-4b29-8995-36f51ac36abd/download/_20268.xlsx", ENV_PAGE),
    "beauty": ("biyo_202608.xlsx", _ENV_DS + "4019ebe4-d8e2-4bf2-a890-0beba402e732/download/_20268.xlsx", ENV_PAGE),
    "laundry": ("cleaning_202608.xlsx", _ENV_DS + "39c48071-845b-471b-9d10-bebc78a05bfd/download/_20268.xlsx",
                ENV_PAGE),
}
SOURCE_RESOURCES = {
    "food": (BODIK_API, "91fe2bf3-0a1a-4daa-acf4-5737ca31ab83"),
    "barber": (BODIK_API, "cec8cb27-29e7-4b29-8995-36f51ac36abd"),
    "beauty": (BODIK_API, "4019ebe4-d8e2-4bf2-a890-0beba402e732"),
    "laundry": (BODIK_API, "39c48071-845b-471b-9d10-bebc78a05bfd"),
}
# The dates the lists state (Kyoto's rule, never the download's): the food
# dataset's 「（2026年8月31日現在）」; the registers' 「前月末時点」 of their
# 2026-09-14 upload. No food row's 有効期間終期 falls before 2026-08-31.
SOURCE_AS_OF = {k: "2026-08-31" for k in SOURCE_FILES}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: four XLSX; the laundry workbook has two sheets
# (洗場, 取次店), both read (xlsx_rows reads every sheet with an address
# column); the pick-up sheet names its shop 施設名称１.
SOURCE_ENCODING = {}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns (the food list's 営業者氏名, a sole
# trader's own name on 1,800 rows, and 代表者氏名; the registers' 開設者氏名（法人）,
# companies only) are REQUIRED so the name rule (japan_register.name_is_operator;
# owner 2026-09-27) cannot silently compare nothing; they are read IN MEMORY by
# that rule only, never kept. Never selected: 営業者住所 and 営業者住所ビル名 (an
# operator's own address), 代表者肩書き, 開設者住所（法人）, every phone.
_REGISTER = ("施設名称", "施設所在地", "開設者氏名（法人）")
REQUIRED_COLUMNS = {
    "food": ("営業の種類", "施設の名称", "施設所在地", "営業者氏名", "代表者氏名"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry": _REGISTER,
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 23211.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Toyota.
# S, W, N, E: the city's N03 extent (S 34.991, W 137.040, N 35.291, E 137.581;
# the 2005 merger reached the mountains of 足助 and 稲武) rounded out; step 1
# stops if the city leaves it. The box the OSM query used (2026-10-03).
OSM_BBOX = (34.98, 137.02, 35.31, 137.6)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style as Kitakyushu's config describes (no
# macrons, 前 as -mae, lowercase after a hyphen). OSM carries macrons on four
# names and writes three of Meitetsu's apart where its others take a hyphen
# (上挙母 as two words, where the Aichi Loop's 新上挙母 is Shin-Uwagoromo); the
# other 18 are OSM's as they stand.
OSM_NAME_EN_OVERRIDES = {
    "浄水": "Josui",                                   # Jōsui
    "三河上郷": "Mikawa-Kamigo",                        # Mikawa-Kamigō
    "四郷": "Shigo",                                   # Shigō
    "陶磁資料館南": "Toji-shiryokan-minami",            # Tōji-shiryōkan-minami
    "上豊田": "Kami-Toyota",                            # Kami Toyota
    "三河八橋": "Mikawa-Yatsuhashi",                    # Mikawa Yatsuhashi
    "上挙母": "Uwagoromo",                              # Uwa Goromo
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~137.16) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median nearest-station gap is
# 966 m: standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25:
# 4 lines, no JR, no Shinkansen). The Aichi Loop Line keeps 12 of 23 and
# Meitetsu's Mikawa Line 10 of 23, cut at the city line; the Meitetsu Toyota
# Line (3 of 8: 梅坪, 上豊田, 浄水) and Linimo (2 of 9: 八草, 陶磁資料館南),
# urban lines cut short, are drawn as cut (owner 2026-10-02, Sakai's Midosuji
# precedent). 梅坪 (Mikawa and Toyota lines) and 八草 (Aichi Loop and Linimo)
# are one N02 group each; 新豊田 and 豊田市 (255 m) and 新上挙母 and 上挙母
# (319 m) are separate groups of different names and stay apart.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour.
_AK, _MT, _LM = "愛知環状鉄道", "名古屋鉄道", "愛知高速交通"
LINES = {
    "AK": {"n02": [(_AK, "愛知環状鉄道線")], "name": "Aichi Loop Line", "name_ja": "愛知環状鉄道線",
           "short": "Aichi Loop", "hue": "#00A040"},
    "MM": {"n02": [(_MT, "三河線")], "name": "Meitetsu Mikawa Line", "name_ja": "名鉄三河線", "short": "Meitetsu",
           "hue": "#E60012"},
    "MT": {"n02": [(_MT, "豊田線")], "name": "Meitetsu Toyota Line", "name_ja": "名鉄豊田線", "short": "Meitetsu",
           "hue": "#E60012"},
    "LM": {"n02": [(_LM, "東部丘陵線")], "name": "Linimo", "name_ja": "リニモ", "short": "Linimo",
           "hue": "#F39800"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# toyota` (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Meitetsu's one red splits into red
# (Mikawa) and red-orange (Toyota), 18.1 apart at 梅坪, the closest pair;
# Linimo's orange goes to ochre. The dark-mode labels separate, 4 of 4.
_COLOURS = {"AK": "#28A800", "MM": "#E80010", "MT": "#F05030", "LM": "#D08000"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the Aichi Loop Railway's own station index
# (aikanrailway.co.jp/station/, read 2026-10-03) lists its 23 stations in line
# order, 岡崎 to 高蔵寺; 三河上郷 to 八草 (12) lie inside the city.
GATE3 = {"source": "The Aichi Loop Railway's station index (aikanrailway.co.jp/station/): 23 stations, "
                   "三河上郷-八草 12 inside the city",
         "lines": {"AK": 12}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
TOYOTA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = TOYOTA_BBOX
