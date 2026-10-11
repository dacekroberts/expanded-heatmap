"""Kobe-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/kobe.md.
The first Japanese city: what every Japanese city shares is in
pipeline/countries/japan.py (rail, city line) and japan_register.py (the
address join), and this file holds only what is Kobe's.

Business leg: Kobe City's 生活衛生関係許可施設等の情報提供 - the food-permit
list (all permits in force at the end of 2026-03) and the barber, beauty and
laundry registers - placed by a JOIN to MLIT's 位置参照情報 for the 9 wards.

Rail: MLIT N02 (not GTFS, not OSM), the Shinkansen and the two funiculars left
out, stations kept only inside the city line (N03). English station names from
OpenStreetMap's name:en, because N02 carries Japanese names only (owner,
2026-09-27).
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kobe" / "raw"
DATA_PROCESSED = ROOT / "data" / "kobe" / "processed"
OUTPUTS = ROOT / "outputs" / "kobe"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kobe"
SLUG = "kobe"
MUNICIPALITY = "神戸市"
PREFECTURE = "兵庫県"

# Kobe City's 生活衛生関係許可施設等の情報提供. The page lists each file; the
# food list is re-issued under a new timestamped name, so FOOD_FILE is the
# edition this build read (end of 2026-03), pinned, never "the newest".
DATASET_PAGE = "https://www.city.kobe.lg.jp/a99427/kenko/health/hygiene/dataset.html"
FILE_BASE = "https://www.city.kobe.lg.jp/documents/6359/"
FOOD_FILE = "20260407150739.csv"
FOOD_AS_OF = "2026-03-31"
# Declared, never inferred (docs/data_sources.md): the food list is Shift-JIS
# (cp932) CSV; the three registers are UTF-16 LE with a BOM, TAB-separated
# despite the .csv name. japan_register.decode() reads both.
SOURCE_ENCODING = {"food": "cp932", "barber": "utf-16", "beauty": "utf-16", "laundry": "utf-16"}
# source key -> file. The key is the taxonomy's `source` column.
SOURCES = {
    "food": FOOD_FILE,
    "barber": "r7_riyousho.csv",
    "beauty": "r7_biyousho.csv",
    "laundry": "r7_cleaning.csv",
}
# source key -> (file, URL, the page that links it and carries its licence),
# the shape japan_fetch reads for every Japanese city; one page covers all four.
SOURCE_FILES = {k: (f, FILE_BASE + f, DATASET_PAGE) for k, f in SOURCES.items()}
# The columns each file must carry; fetch_sources.py stops on a header without
# them. These are the only columns step 2 reads. The operator columns
# (営業者名 / 開設者名) and the phone columns are NEVER read: they carry
# individuals' names and numbers (the brief's privacy trap).
REQUIRED_COLUMNS = {
    "food": ("許可番号", "業種情報公開名称", "営業所所在地", "屋号"),
    "barber": ("施設名称", "施設所在地", "施設（種別）"),
    "beauty": ("施設名称", "施設所在地", "施設（種別）"),
    "laundry": ("施設名称", "施設所在地", "施設（種別）"),
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (34.623-34.891 N, 134.910-135.304 E,
# measured 2026-09-27) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.58, 134.88, 34.92, 135.34)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
# How far an OSM station object may be from N02's group centroid and still name
# it (a large interchange's parts sit up to ~275 m apart; the next station
# along a line is ~1 km).
OSM_NAME_MATCH_M = 600
# Where OSM's objects for one station disagree on name:en, the spelling taken.
# 神戸三宮: Hankyu's object says "Kobe-Sannomiya", Hanshin's "Kobe Sannomiya"
# (2026-09-27); both railways sign the hyphenated form.
OSM_NAME_EN_TIES = {"神戸三宮": "Kobe-Sannomiya"}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.19) falls in the 132 to 138 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line, EXCEPT:
#   * the Shinkansen (owner 2026-09-24, every Japanese city; japan.stations()
#     drops it) - Shin-Kobe stays, as a subway station;
#   * the Maya and Rokkō funiculars (owner 2026-09-27): sightseeing lines whose
#     upper stations are mountain-tops with near-empty rings;
#   * Kobe Electric's Kōen-Toshi Line, whose track crosses the city line with no
#     station inside it.
# JR, Hankyu, Hanshin, Sanyō and Kobe Electric are cut at the city line (owner
# 2026-09-24), including the one-station stub of the JR Takarazuka Line
# (道場; owner 2026-09-27: keep as cut).
#
# Stations collapse on N02's own station-group code (N02_005g), NOT the name:
# the name joins two 長田 1.5 km apart (the subway's and Kobe Electric's) and
# two 御影 1.1 km apart (Hankyu's and Hanshin's), while the group code merges
# only real interchanges (三宮, 新長田, 新開地) - measured 2026-09-27.
LEFT_OUT_LINES = {
    ("こうべ未来都市機構", "摩耶ケーブル線"): "sightseeing funicular (owner 2026-09-27)",
    ("神戸六甲鉄道", "六甲ケーブル線"): "sightseeing funicular (owner 2026-09-27)",
}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 (operator, line) pairs it is drawn from, its real public name
# (English, then Japanese), and its colour. N02 splits one public line into
# its legal sections: the Seishin-Yamate Line is 山手線 + 西神線 + 西神延伸線.
# The Wadamisaki Line is N02's 山陽線 branch south of 兵庫 (step 1 splits it off
# the JR Kobe Line by the track graph). The Kobe Kōsoku Line is the shared
# tunnel Hankyu, Hanshin and Kobe Electric run through (N02 files it under each
# of the three).
#
# COLOURS: the project's own, not the operators' (none is taken from an
# operator's published value), each HUE-matched to the operator's branding
# (subway green, Kaigan blue, JR blue, Hankyu maroon, Sanyō red, Kobe Electric
# orange...). Ten were then moved in lightness and saturation, hue kept, to
# the nearest colour clearing CIE76 Delta-E 45 against every category pin and
# 20 against every other line (2026-09-27; closest line pair 20.5, Kaigan /
# Kobe Kōsoku). With no branding decision behind them, a new city's own
# colours clear the preferred 45 (pipeline/linecolour.py).
#
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after these, and two lines
# sat under the owner's floor of 20 from it (2026-10-07). Each moved to the
# colour nearest its own that reads 3:1 on both pages, clears 20 from every
# pin and 18 from every other line, on every map that draws it: the JR
# Takarazuka Line #9F9504 (16.3) to #A8903C, a mustard held to a yellow hue
# (LCh 87-111 degrees), ONE colour with Amagasaki's and Itami's (olive 20.1,
# nearest line Shintetsu Ao 19.5: the yellows and ochres of the three maps
# leave no more room); the Hokushin Line #7A9C1C (17.5) to #6CA424 (25.6).
# Three of 15 lines sit between 20 and 45 from olive (those two and the
# Shintetsu Ao Line 29.0), an accepted trade (owner, 2026-10-07). DECISIONS,
# "Lines within 20 of the olive and violet pins recoloured".
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
LINES = {
    "SY": {"n02": [("神戸市", "山手線"), ("神戸市", "西神線"), ("神戸市", "西神延伸線")],
           "name": "Seishin-Yamate Line", "name_ja": "西神・山手線", "colour": "#05A904"},
    "HO": {"n02": [("神戸市", "北神線")],
           "name": "Hokushin Line", "name_ja": "北神線", "colour": "#6CA424"},
    "KG": {"n02": [("神戸市", "海岸線")],
           "name": "Kaigan Line", "name_ja": "海岸線", "colour": "#266B73"},
    "PL": {"n02": [("神戸新交通", "ポートアイランド線")],
           "name": "Port Liner", "name_ja": "ポートライナー", "colour": "#8B41C8"},
    "RL": {"n02": [("神戸新交通", "六甲アイランド線")],
           "name": "Rokkō Liner", "name_ja": "六甲ライナー", "colour": "#4198AA"},
    "JK": {"n02": [("西日本旅客鉄道", "東海道線"), ("西日本旅客鉄道", "山陽線")],
           "name": "JR Kobe Line", "name_ja": "JR神戸線", "colour": line_registry.colour("jr-west-kobe-line")},
    "JW": {"n02": [("西日本旅客鉄道", "山陽線")],
           "name": "Wadamisaki Line", "name_ja": "和田岬線", "colour": "#737C8C"},
    "JT": {"n02": [("西日本旅客鉄道", "福知山線")],
           "name": "JR Takarazuka Line", "name_ja": "JR宝塚線", "colour": line_registry.colour("jr-west-takarazuka-line")},
    "HQ": {"n02": [("阪急電鉄", "神戸線")],
           "name": "Hankyu Kobe Line", "name_ja": "阪急神戸線", "colour": line_registry.colour("hankyu-kobe-line")},
    "HS": {"n02": [("阪神電気鉄道", "本線")],
           "name": "Hanshin Main Line", "name_ja": "阪神本線", "colour": line_registry.colour("hanshin-main-line")},
    "SM": {"n02": [("山陽電気鉄道", "本線")],
           "name": "Sanyo Electric Main Line", "name_ja": "山陽電鉄本線", "colour": line_registry.colour("sanyo-electric-main-line")},
    "KK": {"n02": [("阪急電鉄", "神戸高速線"), ("阪神電気鉄道", "神戸高速線"), ("神戸電鉄", "神戸高速線")],
           "name": "Kobe Kōsoku Line", "name_ja": "神戸高速線", "colour": "#705E5C"},
    "KA": {"n02": [("神戸電鉄", "有馬線")],
           "name": "Shintetsu Arima Line", "name_ja": "神鉄有馬線", "colour": "#DB7B06"},
    "KS": {"n02": [("神戸電鉄", "三田線")],
           "name": "Shintetsu Sanda Line", "name_ja": "神鉄三田線", "colour": "#9E522E"},
    "KO": {"n02": [("神戸電鉄", "粟生線")],
           "name": "Shintetsu Ao Line", "name_ja": "神鉄粟生線", "colour": "#B8860A"},
}
# The operator as a station suffix, used only where two stations share an
# English name (Mikage (Hankyu) / Mikage (Hanshin)).
for _k, _short in {"SY": "Subway", "HO": "Subway", "KG": "Subway", "PL": "Port Liner",
                   "RL": "Rokkō Liner", "JK": "JR", "JW": "JR", "JT": "JR", "HQ": "Hankyu",
                   "HS": "Hanshin", "SM": "Sanyō", "KK": "Kōsoku", "KA": "Shintetsu",
                   "KS": "Shintetsu", "KO": "Shintetsu"}.items():
    LINES[_k]["short"] = _short
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
# A branch with its own public name inside one N02 line: the N02 track reachable
# from `terminus` without passing `junction` (japan_step1 walks the section
# graph). `stations` are the branch's own; the junction serves both lines.
# The Wadamisaki Line is 2.7 km (JR West), so a walk outside length_m stops.
BRANCHES = {
    "JW": {"line": ("西日本旅客鉄道", "山陽線"), "terminus": "和田岬", "junction": "兵庫",
           "stations": ("和田岬",), "length_m": (1500, 3500)},
}

# Gate 3: the operators' own station counts for the lines wholly inside the
# city, against the collapsed set (docs: Kobe Municipal Subway S01-S16,
# K01-K10 and the Hokushin Line's two stations; Kobe New Transit P01-P12 and
# R01-R06; Kobe Electric's Arima Line KB02-KB16). The lines the city line cuts
# have no published in-city count; their stations are listed by step 1.
GATE3 = {"source": "operators' station numbering (Kobe Municipal Subway, Kobe New Transit, "
                   "Kobe Electric Railway)",
         "lines": {"SY": 16, "KG": 10, "HO": 2, "PL": 12, "RL": 6, "KA": 15}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"
# This taxonomy also classifies by source: keep those raw column(s) through step 2
# (they are passed to classify() by filter_to_storefront() and the map).

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KOBE_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KOBE_BBOX
