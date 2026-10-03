"""Yokkaichi-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/yokkaichi.md
(14/14 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py), in Kobe's shape: the city's own lists, all
three buckets.

Business leg: the city's five CC BY 4.0 lists on BODIK as of 2026-08-31: every
food permit (the city's full export from the national 食品衛生申請等システム,
業態 beside 業種), every food notification (届出), and the barber, beauty and
laundry lists, placed by a JOIN to MLIT's 位置参照情報 (one municipality, no
wards). The notification list is the city's complete list, so its food-retail
types count as Food shops (japan_eigyo's rule). MHLW's open data for 24202
holds only the opt-in online filings: not used (Toyama's precedent).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Kintetsu's Nagoya and Yunoyama lines, the Yokkaichi Asunarou Railway's
two narrow-gauge lines, the Sangi Line, JR's Kansai Line and the Ise Railway's
one station. English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "yokkaichi" / "raw"
DATA_PROCESSED = ROOT / "data" / "yokkaichi" / "processed"
OUTPUTS = ROOT / "outputs" / "yokkaichi"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Yokkaichi"
SLUG = "yokkaichi"
MUNICIPALITY = "四日市市"
PREFECTURE = "三重県"

# The city's lists on BODIK (data.bodik.jp, the city's catalogue,
# odcs.bodik.jp/242021), each package license_id cc-by-40-intl, under the
# catalogue's terms (四日市市オープンデータ利用規約 第1条: CC BY 4.0; read
# 2026-10-02). The files are the editions this build read, pinned, each named
# with its as-of date.
BODIK = "https://data.bodik.jp/dataset"
CATALOGUE = "https://odcs.bodik.jp/242021/"
# source key -> (file, URL, the dataset page that carries its licence)
SOURCE_FILES = {
    "food": ("242021_food_business_all_20260831.xlsx",
             f"{BODIK}/e5809d89-173d-40ea-9ee7-5bc4a61678a6/resource/ee120d14-40b8-4161-a650-9e8a3307dbeb/"
             "download/242021_food_business_all_20260831.xlsx",
             f"{BODIK}/242021_00131"),
    "notify": ("242021_eigyoutodokede_20260831.xlsx",
               f"{BODIK}/f6ff9f86-e225-4f53-982c-156f6d5be2c4/resource/c047f8a3-2602-4a81-8bfa-e7c6cdbc03f8/"
               "download/242021_eigyoutodokede_20260831.xlsx",
               f"{BODIK}/242021_00136"),
    "barber": ("242021_barber_20260831.xlsx",
               f"{BODIK}/9fac6464-fcdc-45f0-91a8-fd766c1b3f39/resource/bb0550ed-b532-43f7-8e7e-3e14015496d0/"
               "download/242021_barber_20260831.xlsx",
               f"{BODIK}/242021_00111"),
    "beauty": ("242021_beauty_20260831.xlsx",
               f"{BODIK}/fb1ba35c-5541-4801-a63b-898b162a6ea1/resource/d90b0082-d04b-4fd7-8cfb-35d0c17dc3e8/"
               "download/242021_beauty_20260831.xlsx",
               f"{BODIK}/242021_00112"),
    "laundry": ("242021_cleaning_20260831.xlsx",
                f"{BODIK}/158b7658-dbe4-4d91-96b6-06d334fac978/resource/f40a0050-cb84-4b29-89d7-dc12b76f4516/"
                "download/242021_cleaning_20260831.xlsx",
                f"{BODIK}/242021_00113"),
}
# The dates the lists state (Kyoto's rule, never the download's): each
# resource is named with its month-end, 20260831.
SOURCE_AS_OF = {k: "2026-08-31" for k in SOURCE_FILES}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# The notification list is a food list too: japan_eigyo reads its types
# (その他の食料・飲料販売業, 乳類販売業, コンビニエンスストア ...) as food ones.
SOURCE_KIND = {"notify": "food"}
# Declared, never inferred: five XLSX workbooks, one sheet each, the header on
# row 1 (its first cell blank).
SOURCE_ENCODING = {k: "xlsx" for k in SOURCES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns (the food lists' 申請者氏名 and
# 申請者代表者名, the registers' 開設者氏名 and 代表者氏名) are REQUIRED so the
# name rule (japan_register.name_is_operator; owner 2026-09-27) cannot
# silently compare nothing; they are read IN MEMORY by that rule only, never
# kept. Never selected: 申請者住所 / 開設者住所 (operators' own addresses),
# 申請者電話番号 / 開設者電話番号 and the premises' phones.
_REGISTER = ("施設屋号", "施設住所", "開設者氏名", "代表者氏名")
REQUIRED_COLUMNS = {
    "food": ("営業施設屋号", "営業施設住所", "業種", "業態", "有効期間終了日", "申請者氏名", "申請者代表者名"),
    "notify": ("営業施設屋号", "営業施設住所", "業種", "申請者氏名", "申請者代表者名"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry": (*_REGISTER, "区分"),
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one municipality.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Yokkaichi.
# S, W, N, E: the city's N03 extent (S 34.901, W 136.414, N 35.071, E 136.689)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.89, 136.40, 35.09, 136.70)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen. 近鉄富田 takes Kintetsu's hyphen, as OSM's own
# Kintetsu-Yokkaichi; the other 28 are OSM's as they stand. 近鉄四日市 and
# あすなろう四日市 are separate N02 groups 33 m apart, separate stations of
# different names (Kobe's Tarumi / Sanyo Tarumi): kept apart.
OSM_NAME_EN_OVERRIDES = {
    "暁学園前": "Akatsuki-gakuen-mae",              # Akatsukigakuenmae
    "北勢中央公園口": "Hokusei-chuo-koenguchi",      # Hokusei Chūō Kōenguchi
    "近鉄富田": "Kintetsu-Tomida",                   # Kintetsu Tomida
    "南日永": "Minami-Hinaga",                       # Minami hinaga
    "新正": "Shinsho",                               # Shinshyo
    "山城": "Yamajo",                                # Yamajō
    "大矢知": "Oyachi",                              # Ōyachi
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~136.62) falls in the 132 to 138 band. Derived
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
# 2026-10-03: 8 legal lines, no Shinkansen). Asunarou's 内部線 (8 of 8) and
# 八王子線 (2 of 2) lie wholly inside; Kintetsu's 名古屋線 (10 of 44) and
# 湯の山線 (6 of 10), the Sangi Line (7 of 15) and JR's 関西線 (6 of 19) are
# cut at the city line (owner 2026-09-24). The Ise Railway keeps one station
# (河原田, of 10, also JR's): a one-station stub of a regional line stays as
# cut (Kobe's JR Takarazuka Line, owner 2026-09-27).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the Sangi Line's approach to
# 近鉄富田 as a legal line of its own (近鉄連絡線, trap 2): one public line.
_KT, _AS, _SG = "近畿日本鉄道", "四日市あすなろう鉄道", "三岐鉄道"
LINES = {
    "KN": {"n02": [(_KT, "名古屋線")], "name": "Kintetsu Nagoya Line", "name_ja": "近鉄名古屋線",
           "short": "Kintetsu", "hue": "#E2001A"},
    "KY": {"n02": [(_KT, "湯の山線")], "name": "Kintetsu Yunoyama Line", "name_ja": "近鉄湯の山線",
           "short": "Kintetsu", "hue": "#E2001A"},
    "AU": {"n02": [(_AS, "内部線")], "name": "Asunarou Utsube Line", "name_ja": "内部線",
           "short": "Asunarou", "hue": "#00A0E9"},
    "AH": {"n02": [(_AS, "八王子線")], "name": "Asunarou Hachioji Line", "name_ja": "八王子線",
           "short": "Asunarou", "hue": "#00A0E9"},
    "SG": {"n02": [(_SG, "三岐線"), (_SG, "近鉄連絡線")], "name": "Sangi Line", "name_ja": "三岐線",
           "short": "Sangi", "hue": "#F39800"},
    "JK": {"n02": [("東海旅客鉄道", "関西線")], "name": "JR Kansai Line", "name_ja": "関西本線",
           "short": "JR", "hue": "#00A23E"},
    "IS": {"n02": [("伊勢鉄道", "伊勢線")], "name": "Ise Railway Ise Line", "name_ja": "伊勢線",
           "short": "Ise Railway", "hue": "#004EA2"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# yokkaichi` (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its operator's hue that reads 3:1 on both
# map pages and clears CIE76 45 from every pin. The Ise Railway's blue, which
# no blue clears Retail's pin in, goes purple. Closest pair within 500 m and
# anywhere 18.2 (Asunarou's two lines); the dark-mode labels separate, 7 of 7.
_COLOURS = {"KN": "#E00018", "KY": "#F85838", "AU": "#08A0C0", "AH": "#488090", "SG": "#D08000", "JK": "#20A800",
            "IS": "#9840A0"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own station count for the lines wholly inside the
# city: the Yokkaichi Asunarou Railway's route map (yar.co.jp/route/, read
# 2026-10-03) gives the Utsube Line あすなろう四日市 to 内部, 8 stations, and the
# Hachioji Line 日永 and 西日野, 2. The lines the city line cuts have no
# in-city count of their own; step 1 lists them.
GATE3 = {"source": "the Yokkaichi Asunarou Railway's route map (yar.co.jp/route/)", "lines": {"AU": 8, "AH": 2}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
YOKKAICHI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = YOKKAICHI_BBOX
