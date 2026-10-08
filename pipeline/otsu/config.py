"""Ōtsu-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/otsu.md
(12/12 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py), in Toyama's shape: one complete city food list
plus three registers.

Business leg: the city's monthly food-permit list (every permit in force on
2026-08-31, old and new law in one list) on its own site, catalogued CC BY on
its BODIK portal (owner, 2026-10-02: accepted as CC BY 4.0), and its barber,
beauty and laundry lists of the same date on BODIK, placed by a JOIN to MLIT's
位置参照情報 (one municipality, no wards). MHLW's open data for 25201 holds
only the opt-in online filings: not used (Toyama's precedent).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Keihan's Ishiyama-Sakamoto and Keishin lines and JR West's Kosei and
Biwako lines; the Sakamoto Cable, a sightseeing funicular, left out. English
station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "otsu" / "raw"
DATA_PROCESSED = ROOT / "data" / "otsu" / "processed"
OUTPUTS = ROOT / "outputs" / "otsu"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Ōtsu"
SLUG = "otsu"
MUNICIPALITY = "大津市"
PREFECTURE = "滋賀県"

# The food list is served from the city's 衛生課 open-data page and catalogued
# on the city's BODIK portal (data.bodik.jp, organisation 252018, license_id
# cc-by, a record whose only content is that page); the three registers are
# BODIK resources. The catalogue's terms (大津市オープンデータ利用規約 ４(1):
# CC BY 4.0; read 2026-10-02) and the city's copyright page exempt the portal.
FOOD_PAGE = "https://www.city.otsu.lg.jp/soshiki/021/1441/od/02594.html"
BODIK = "https://data.bodik.jp/dataset"
CATALOGUE = "https://odcs.bodik.jp/252018/"
# source key -> (file, URL of the edition this build read, the page that links
# it and carries its licence). The food file is RENAMED each month (od_2608 is
# 2026-08), so fetch_sources.py reads the current link from the page
# (SOURCE_LINKS) and the pinned URL records which edition the build read.
SOURCE_FILES = {
    "food": ("od_2608.csv", "https://www.city.otsu.lg.jp/material/files/group/4/od_2608.csv", FOOD_PAGE),
    "barber": ("20260831riyo.csv",
               f"{BODIK}/38908ca8-beaa-45f6-b130-8e9ae9f6d97d/resource/53520e16-5488-4d92-b9a1-a7d1365fe595/"
               "download/20260831riyo.csv",
               f"{BODIK}/38908ca8-beaa-45f6-b130-8e9ae9f6d97d"),
    "beauty": ("20260831biyo.csv",
               f"{BODIK}/cc0d476f-a5cc-429b-9797-8bb84c3df02f/resource/177df3f3-af8b-4619-aa54-337890a95e51/"
               "download/20260831biyo.csv",
               f"{BODIK}/cc0d476f-a5cc-429b-9797-8bb84c3df02f"),
    "laundry": ("20260831cleaning.csv",
                f"{BODIK}/f658266c-2854-4974-8bba-8041a80a391d/resource/8495b105-ce24-4ba7-ab6b-2431f4f60cb1/"
                "download/20260831cleaning.csv",
                f"{BODIK}/f658266c-2854-4974-8bba-8041a80a391d"),
}
SOURCE_LINKS = {"food": r"/od_\d{4}\.csv$"}
# The dates the lists state (Kyoto's rule, never the download's): the food
# list's 「食品営業許可施設一覧（令和8年8月末時点）」, the registers'
# 「2026年8月末現在」.
SOURCE_AS_OF = {k: "2026-08-31" for k in SOURCE_FILES}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: all four UTF-8 with a BOM, comma CSV.
SOURCE_ENCODING = {k: "utf-8-sig" for k in SOURCES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns (the food list's 申請者名, the
# registers' 営業者氏名) are REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; they are read IN MEMORY by that rule only, never kept. Never
# selected: 施設電話番号.
_REGISTER = ("施設名称", "施設所在地", "営業者氏名")
REQUIRED_COLUMNS = {
    "food": ("施設名", "施設所在地", "業種", "許可満了年月日", "申請者名"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry": _REGISTER,
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one municipality.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (S 34.871, W 135.815, N 35.285, E 136.043)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.86, 135.80, 35.30, 136.06)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen, as OSM writes Keihan's stops (Keihan-ishiyama,
# Biwako-hamaotsu, its signs' style). The other 36 are OSM's as they stand.
# 京阪膳所 / 膳所 (54 m) and 京阪石山 / 石山 (95 m) are separate N02 groups of
# different names, Keihan's and JR's stations: kept apart (Kobe's Tarumi /
# Sanyo Tarumi). No Keihan stop is mapped as a tram_stop (all 24 matched in
# the station file), so no TRAM_OSM_JSON.
OSM_NAME_EN_OVERRIDES = {
    "蓬莱": "Horai",                     # Hōrai
    "近江舞子": "Omi-Maiko",             # Ōmi-Maiko
    "大津": "Otsu",                      # Ōtsu
    "おごと温泉": "Ogoto-onsen",         # Ogotoonsen
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.87) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-03: 5 lines, no Shinkansen). Keihan's 石山坂本線 lies wholly inside
# (21 of 21); its 京津線 keeps 4 of 7 (Kyoto draws the other 3), JR's 湖西線 12
# of 21 and 東海道線 4 of 59, each cut at the city line (owner 2026-09-24).
LEFT_OUT_LINES = {
    # A sightseeing funicular up Mt Hiei (Kobe's Maya and Rokko, owner
    # 2026-09-27): never in excluded_stations.csv; the page says so.
    ("比叡山鉄道", "比叡山鉄道線"): "a sightseeing funicular, the Sakamoto Cable (Kobe's rule)",
}
# The lines run on into Kyoto (Keihan's Keishin Line, JR's Biwako and Kosei
# lines to 山科): Kyoto's N03 names the stations beyond the prefecture line
# (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("26",)
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. JR West signs N02's 東海道線 here as the
# Biwako Line (琵琶湖線), as Kyoto's config names it east of 京都 (trap 2).
_KH, _JR = "京阪電気鉄道", "西日本旅客鉄道"
LINES = {
    "KI": {"n02": [(_KH, "石山坂本線")], "name": "Keihan Ishiyama-Sakamoto Line", "name_ja": "石山坂本線",
           "short": "Keihan", "hue": "#00A040"},
    "KK": {"n02": [(_KH, "京津線")], "name": "Keihan Keishin Line", "name_ja": "京津線",
           "short": "Keihan", "hue": "#949054"},
    "JC": {"n02": [(_JR, "湖西線")], "name": "JR Kosei Line", "name_ja": "湖西線", "short": "JR", "hue": "#00B2E5"},
    "JB": {"n02": [(_JR, "東海道線")], "name": "JR Biwako Line", "name_ja": "琵琶湖線", "short": "JR",
           "hue": "#0072BC"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py otsu`
# (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide): each the
# feasible colour nearest its operator's hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. The Keishin and Biwako lines come out
# as Kyoto's own colours for them. Closest pair within 500 m and anywhere
# 26.7 (the Kosei and Biwako lines); the dark-mode labels separate, 4 of 4.
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search: the
# Keishin Line's #909040 sat 16.0 from it, under the owner's floor of 20
# (2026-10-07), and takes Kyoto's new colour for the same line, #949054
# (olive 25.2, between 20 and 45: an accepted trade). Its start hue follows.
_COLOURS = {"KI": "#28A800", "KK": "#949054", "JC": "#08A0C0", "JB": "#406878"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own station count for the line wholly inside the
# city: Keihan's station index (keihan.co.jp/traffic/station/, read
# 2026-10-03; brief_check proves it) numbers the Ishiyama-Sakamoto Line OT01
# 石山寺 to OT21 坂本比叡山口: 21. The lines the city line cuts have no in-city
# count of their own; step 1 lists them.
GATE3 = {"source": "Keihan's station index (keihan.co.jp/traffic/station/)", "lines": {"KI": 21}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
OTSU_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = OTSU_BBOX
