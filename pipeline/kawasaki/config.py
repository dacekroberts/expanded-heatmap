"""Kawasaki-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/kawasaki.md
(10/10 checks, 2026-10-03). Japan wave 2's pilot, on the shared modules
(pipeline/countries/japan*.py), in Kobe's shape: the city's own lists, all
three buckets.

Business leg: the city's monthly CC BY lists (健康福祉局保健医療政策部生活衛生課):
every food permit in force at 2026-08-31, and full barber, beauty and laundry
lists of the same date, placed by a JOIN to MLIT's 位置参照情報 for the 7
wards. MHLW's open data for Kawasaki holds only the opt-in online filings
(10% of the official restaurant count): a control, never a source.

Rail: MLIT N02-25 (not GTFS, not OSM), the Shinkansen left out, stations kept
only inside the city line (N03). JR East and four private railways, every line
a radial the long, narrow city cuts. English station names from
OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kawasaki" / "raw"
DATA_PROCESSED = ROOT / "data" / "kawasaki" / "processed"
OUTPUTS = ROOT / "outputs" / "kawasaki"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kawasaki"
SLUG = "kawasaki"
MUNICIPALITY = "川崎市"
PREFECTURE = "神奈川県"

# The city's two pages, each under a CC BY licence block (the 2.1 JP of the
# city's 利用規約 §2 and the 4.0 the pages' badge links; the credit names both,
# owner 2026-10-02). No catalogue API.
FOOD_PAGE = "https://www.city.kawasaki.jp/350/page/0000093741.html"
ENV_PAGE = "https://www.city.kawasaki.jp/350/page/0000120745.html"
_FILES = "https://www.city.kawasaki.jp/350/cmsfiles/contents/"
# source key -> (file, URL of the edition this build read, the page that links
# it and carries its licence). Every file is RENAMED each month (080803 is R8,
# month 08; …202608), so fetch_sources.py reads the current link from the page
# (SOURCE_LINKS) and the pinned URL records which edition the build read.
SOURCE_FILES = {
    "food": ("food_202608.csv", _FILES + "0000093/93741/080803(UTF-8).csv", FOOD_PAGE),
    "barber": ("riyoujo202608.csv", _FILES + "0000120/120745/01riyoujo202608.csv", ENV_PAGE),
    "beauty": ("biyoujo202608.csv", _FILES + "0000120/120745/02biyoujo202608.csv", ENV_PAGE),
    "laundry": ("cleaning202608.csv", _FILES + "0000120/120745/03cleaning202608.csv", ENV_PAGE),
}
# The food page also links twelve monthly NEW-permit files (…0800(UTF-8).csv,
# ending 00); the full list is the one link that does not end 00.
SOURCE_LINKS = {
    "food": r"/0000093/93741/\d{4}(?!00)\d\d\(UTF-8\)\.csv$",
    "barber": r"/01riyoujo\d{6}\.csv$",
    "beauty": r"/02biyoujo\d{6}\.csv$",
    "laundry": r"/03cleaning\d{6}\.csv$",
}
# The dates the lists state (Kyoto's rule, never the download's): the food
# list's 「令和8年8月末時点」; the registers' month in their names.
SOURCE_AS_OF = {"food": "2026-08-31", "barber": "2026-08-31", "beauty": "2026-08-31", "laundry": "2026-08-31"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: all four UTF-8 with a BOM, comma CSV.
SOURCE_ENCODING = {k: "utf-8-sig" for k in SOURCES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns (the food list's
# 営業者氏名（法人のみ） and 代表者氏名（法人のみ）, companies only: the city does
# not publish a sole trader's name; the registers' 開設者名 / 営業者名 and
# 代表者名) are REQUIRED so the name rule (japan_register.name_is_operator;
# owner 2026-09-27) cannot silently compare nothing; they are read IN MEMORY
# by that rule only, never kept. Never selected: 開設者住所 / 営業者住所 and
# 営業者住所（法人のみ） (operators' own addresses), every 電話番号.
_REGISTER = ("施設名称", "施設所在地", "開設者名", "代表者名")
REQUIRED_COLUMNS = {
    "food": ("営業所の名称", "営業所の所在地", "営業種目", "営業者氏名（法人のみ）", "代表者氏名（法人のみ）"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry": ("施設名称", "施設所在地", "施設（種別）", "営業者名", "代表者名"),
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Kawasaki.
# S, W, N, E: the city's N03 extent (S 35.470, W 139.449, N 35.643, E 139.836)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.46, 139.44, 35.66, 139.85)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment). Station names follow the operators' signs, as Tokyo's and
# Yokohama's do (owner 2026-09-28: signage style, no macrons).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~139.70) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-03: 10 lines, no Shinkansen station inside). The city is a strip
# along the Tama River, so every line is a radial the city line cuts (owner
# 2026-09-24); the Keikyu Main Line (2 of 50: 京急川崎, 八丁畷) and the Keio
# Sagamihara Line (2 of 12: 京王稲田堤, 若葉台), urban lines cut to two
# stations, are drawn as cut (owner 2026-10-02, Sakai's Midosuji precedent).
# 尻手's platform lies inside the city line, so it is ringed.
LEFT_OUT_LINES = {}
# The lines run on into Tokyo as well as Yokohama: Tokyo's N03 names the
# stations beyond the Tama River (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("13",)
# 武蔵小杉: N02 files the JR Yokosuka Line platform (its 東海道線, the 品鶴線
# track) as its own group, about 377 m from the Nambu Line and Tokyu group;
# it is one station by name and by passage (Tokyo's Keiyo platforms at 東京,
# 424 m), so GROUP_JOIN joins it and the spread allows it.
GROUP_JOIN = {("東日本旅客鉄道", "東海道線", "武蔵小杉"): "one Musashi-Kosugi, 377 m (the Yokosuka Line platform)"}
COLLAPSE_MAX_SPREAD_M = 450

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour.
#
# JR EAST as Yokohama's (owner 2026-09-28, Tokyo's services): N02's 東海道線
# here carries four public services, each a `route` over it with its stops in
# Kawasaki and its next station outside: the Keihin-Tohoku Line and the Tokaido
# Line (川崎), the Yokosuka Line (武蔵小杉, 新川崎, over the 品鶴線 track) and the
# Sotetsu-JR Link Line (武蔵小杉). "~名" passes a station without stopping.
# Tokyu's Meguro and Oimachi Lines are drawn the same way: Meguro trains run
# on their own pair of 東横線 tracks from 田園調布 to 日吉, Oimachi trains on
# 田園都市線's from 二子玉川 to 溝の口, stopping at every station.
_JR, _TK = "東日本旅客鉄道", "東急電鉄"
_TOKAIDO = (_JR, "東海道線")
LINES = {
    # --- JR East
    "JN": {"n02": [(_JR, "南武線")], "name": "JR Nambu Line", "name_ja": "南武線", "short": "JR", "hue": "#FFD400"},
    "JB": {"n02": [], "name": "JR Nambu Branch Line", "name_ja": "南武支線", "short": "JR", "hue": "#FFD400"},
    "JI": {"n02": [(_JR, "鶴見線")], "name": "JR Tsurumi Line", "name_ja": "鶴見線", "short": "JR", "hue": "#FFDD00"},
    "JK": {"route": [(*_TOKAIDO, ["蒲田", "川崎", "鶴見"])],
           "name": "JR Keihin-Tohoku Line", "name_ja": "京浜東北線", "short": "JR", "hue": "#00B2E5"},
    "JT": {"route": [(*_TOKAIDO, ["~蒲田", "川崎", "~鶴見"])],
           "name": "JR Tokaido Line", "name_ja": "東海道線", "short": "JR", "hue": "#F68B1E"},
    "JO": {"route": [(*_TOKAIDO, ["武蔵小杉", "新川崎", "~鶴見"])],
           "name": "JR Yokosuka Line", "name_ja": "横須賀線", "short": "JR", "hue": "#0070B9"},
    "SJ": {"route": [(*_TOKAIDO, ["武蔵小杉", "~鶴見"])],
           "name": "Sotetsu-JR Link Line", "name_ja": "相鉄・JR直通線", "short": "JR", "hue": "#1D2F6F"},
    # --- Keikyu (京浜急行電鉄)
    "KK": {"n02": [("京浜急行電鉄", "本線")],
           "name": "Keikyu Main Line", "name_ja": "京急本線", "short": "Keikyu", "hue": "#E5171F"},
    "KD": {"n02": [("京浜急行電鉄", "大師線")],
           "name": "Keikyu Daishi Line", "name_ja": "京急大師線", "short": "Keikyu", "hue": "#E5171F"},
    # --- Tokyu (東急電鉄)
    "TY": {"n02": [(_TK, "東横線")],
           "name": "Tokyu Toyoko Line", "name_ja": "東横線", "short": "Tokyu", "hue": "#DA0442"},
    "MG": {"route": [(_TK, "東横線", ["多摩川", "新丸子", "武蔵小杉", "元住吉", "日吉"])],
           "name": "Tokyu Meguro Line", "name_ja": "目黒線", "short": "Tokyu", "hue": "#009CD2"},
    "DT": {"n02": [(_TK, "田園都市線")],
           "name": "Tokyu Den-en-toshi Line", "name_ja": "田園都市線", "short": "Tokyu", "hue": "#20A288"},
    "OM": {"route": [(_TK, "田園都市線", ["二子玉川", "二子新地", "高津", "溝の口"])],
           "name": "Tokyu Oimachi Line", "name_ja": "大井町線", "short": "Tokyu", "hue": "#F18C43"},
    # --- Odakyu (小田急電鉄)
    "OH": {"n02": [("小田急電鉄", "小田原線")],
           "name": "Odakyu Odawara Line", "name_ja": "小田原線", "short": "Odakyu", "hue": "#2288CC"},
    "OT": {"n02": [("小田急電鉄", "多摩線")],
           "name": "Odakyu Tama Line", "name_ja": "多摩線", "short": "Odakyu", "hue": "#2288CC"},
    # --- Keio (京王電鉄)
    "KO": {"n02": [("京王電鉄", "相模原線")],
           "name": "Keio Sagamihara Line", "name_ja": "相模原線", "short": "Keio", "hue": "#DD0077"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# kawasaki` (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Closest pair within 500 m 18.1
# (Keikyu Daishi / Main), anywhere 10.0 (Keihin-Tohoku / Meguro); the
# dark-mode labels separate, 16 of 16.
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search: the Nambu
# Branch Line's #909800 sat 14.9 from it, under the owner's floor of 20
# (2026-10-07). It moved to #B88C3C, an ochre: the colour nearest JR's yellow
# #FFD400, held to a yellow-orange hue (LCh 80-100 degrees), that reads 3:1 on
# both pages and clears 25 from every pin and 18 from every other line (olive
# 27.6, nearest line JR Tsurumi 18.5). Three of 16 lines sit between 20 and
# 45 from olive (JR Nambu #B09000 23.2, the Branch 27.6, JR Tsurumi 32.5), an
# accepted trade (owner, 2026-10-07). DECISIONS, "Lines within 20 of the
# olive and violet pins recoloured".
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "JN": line_registry.colour("jr-east-nambu-line"), "JB": "#B88C3C",
    "JI": line_registry.colour("jr-east-tsurumi-line"),
    "JK": line_registry.colour("jr-east-keihin-tohoku-line"),
    "JT": line_registry.colour("jr-east-tokaido-line"), "JO": line_registry.colour("jr-east-yokosuka-line"),
    "SJ": line_registry.colour("sotetsu-jr-link-line"), "KK": line_registry.colour("keikyu-main-line"),
    "KD": "#F05830", "TY": line_registry.colour("tokyu-toyoko-line"),
    "MG": line_registry.colour("tokyu-meguro-line"), "DT": line_registry.colour("tokyu-den-en-toshi-line"),
    "OM": line_registry.colour("tokyu-oimachi-line"), "OH": line_registry.colour("odakyu-odawara-line"),
    "OT": line_registry.colour("odakyu-tama-line"), "KO": line_registry.colour("keio-sagamihara-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
# N02 files the Nambu Branch (尻手 to 浜川崎, JR East's 浜川崎支線, signed
# 南武支線) inside its 南武線. Split off by walking the track from 浜川崎 to 尻手.
BRANCHES = {
    "JB": {"line": (_JR, "南武線"), "terminus": "浜川崎", "junction": "尻手",
           "stations": ["八丁畷", "川崎新町", "小田栄", "浜川崎"], "length_m": (3000, 5500)},
}

# Gate 3: the operator's own station count for the line wholly inside the
# city: Keikyu's station list (read 2026-10-03) gives the Daishi Line 港町,
# 鈴木町, 川崎大師, 東門前, 大師橋 and 小島新田 beyond 京急川崎: 7. The lines the
# city line cuts have no in-city count of their own; step 1 lists them.
GATE3 = {"source": "Keikyu's station list (keikyu.co.jp/ride/kakueki/)", "lines": {"KD": 7}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KAWASAKI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KAWASAKI_BBOX
