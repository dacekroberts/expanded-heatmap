"""Yokohama-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/yokohama.md.
The seventh Japanese city on the shared modules (pipeline/countries/japan*.py),
and the first page NOT built on food (owner, 2026-09-29: Band B, personal
services only): Yokohama publishes no food-permit list, so the page says so.

Business leg: the city's 環境衛生関係施設一覧 - the barber (理容所), beauty
(美容所) and laundry (クリーニング所) registers as of 2026-04-01, one CSV per
ward inside one zip per register - placed by a JOIN to MLIT's 位置参照情報 for
the 18 wards.

Rail: MLIT N02 (not GTFS, not OSM), the Shinkansen left out, stations kept only
inside the city line (N03). English station names from OpenStreetMap's name:en.
"""

import csv
import io
import zipfile
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "yokohama" / "raw"
DATA_PROCESSED = ROOT / "data" / "yokohama" / "processed"
OUTPUTS = ROOT / "outputs" / "yokohama"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Yokohama"
SLUG = "yokohama"
MUNICIPALITY = "横浜市"
PREFECTURE = "神奈川県"

# The city's 環境衛生関係施設一覧 (page last updated 2026-09-20). One zip per
# register, each holding 18 ward CSVs (UTF-16 LE with a BOM, TAB-separated,
# named .csv). The page's other six zips (bathhouses, inns, entertainment
# venues, pools, building sanitation, openings) are not personal-services
# storefronts or not a complete list, so they are not read.
DATASET_PAGE = "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/seikatsu/kaiteki/kankyodata.html"
FILE_BASE = "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/seikatsu/kaiteki/kankyodata.files/"
# The registers' own date (令和８年４月１日現在). No closure field: the date is
# the one clock (the one-clock rule's snapshot case). The page also publishes
# each month's OPENINGS since (新規, 2026-05 to 2026-09, about 170 barbers,
# salons and laundries) but no closures, so they are not added: a snapshot
# stays a snapshot.
REGISTERS_AS_OF = "2026-04-01"
FOOD_AS_OF = None  # no food list is published
SOURCE_ENCODING = {"barber": "utf-16", "beauty": "utf-16", "laundry": "utf-16"}
SOURCES = {
    "barber": "life/20260401riyou.zip",
    "beauty": "life/20260401biyou.zip",
    "laundry": "life/20260401cleaning.zip",
}
SOURCE_FILES = {k: (f, FILE_BASE + f.split("/")[-1], DATASET_PAGE) for k, f in SOURCES.items()}
# The columns step 2 reads. The operator columns 申請者氏名 (a person's name)
# and 申請者役職 are read ONLY by japan_register.name_is_operator, in memory,
# for the owner's name rule (2026-09-27); nothing keeps them. The phone column
# 施設電話番号 is never read.
_REGISTER_COLUMNS = ("施設名称", "施設所在地", "業種", "詳細業種")
REQUIRED_COLUMNS = {k: _REGISTER_COLUMNS for k in SOURCES}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A register's rows: every ward CSV inside its zip (japan_register.city_rows
    reads only .xlsx members of a zip, so the members are read here, city-local).
    The kind of premises is in 詳細業種 (美容所(移動), a salon in a vehicle;
    無店舗取次店, a storeless laundry pick-up), while 業種 repeats the register's
    name - so 詳細業種 is the type the taxonomy reads."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if not jr.zip_member_name(info).lower().endswith(".csv"):
                continue
            text = jr.decode(zf.read(info))
            head = text.split("\n", 1)[0]
            delim = "\t" if head.count("\t") > head.count(",") else ","
            for r in csv.DictReader(io.StringIO(text), delimiter=delim):
                r["業種"] = (r.get("詳細業種") or "").strip() or r.get("業種", "")
                yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent, rounded out; step 1 stops if the city
# leaves it.
OSM_BBOX = (35.28, 139.44, 35.62, 139.74)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-09-30): OSM writes ケ where N02 writes ヶ (Tokyo's
# finding too) - Sotetsu's 鶴ヶ峰 is OSM's 鶴ケ峰 (ref SO09).
OSM_NAME_ALIASES = {"鶴ヶ峰": "鶴ケ峰"}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment). Station names follow the operators' signs, as Tokyo's do (owner
# 2026-09-28: signage style, no macrons; Tokyu's and the subway's lowercase
# after a hyphen, Higashi-hakuraku, Kita-yamata, kept). One OSM object breaks
# that style: 大船 "Ōfuna" (the only macron in the city) -> "Ofuna".
OSM_NAME_EN_OVERRIDES = {"大船": "Ofuna"}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~139.64) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median gap, 836 m, keeps the
# standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (Japan's standing rule:
# JR, the subway and the private railways; the Shinkansen left out, so
# Shin-Yokohama stays as a JR, subway, Tokyu and Sotetsu station). Lines
# running on beyond the city are cut at the line (owner 2026-09-24), including
# the one-station stub of the JR Nambu Line (矢向, 1 of 30; Kobe's JR Takarazuka
# Line precedent, owner 2026-09-27: keep as cut). The Kanazawa Seaside Line is an
# automated guideway (N02 class 24), drawn as Kobe's Port Liner is.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's own hue (`hue`, which scripts/line_colour_search.py
# starts from) and the project's colour.
#
# JR EAST as Tokyo's (owner 2026-09-28): N02 files JR East under its LEGAL
# lines, and one of them, 東海道線, carries four public services here - the
# Keihin-Tohoku Line (to 横浜, then 根岸線 as the Negishi Line), the Tokaido
# Line, the Yokosuka Line (over the Hinkaku track via 新川崎) and the
# Sotetsu-JR Link Line (羽沢横浜国大 to 武蔵小杉 over the freight track). Each is
# a `route` over the legal lines it runs on, stops as JR East's route maps give
# them; the first and last entry of a service running on past the city is its
# next station outside. The other JR lines are one service each (n02).
_JR = "東日本旅客鉄道"
_TOKAIDO = (_JR, "東海道線")
LINES = {
    # --- Yokohama Municipal Subway (横浜市): the Blue Line is N02's 1号線
    # (関内 to 湘南台) plus 3号線 (関内 to あざみ野)
    "B": {"n02": [("横浜市", "1号線"), ("横浜市", "3号線")],
          "name": "Blue Line", "name_ja": "ブルーライン", "short": "Subway", "hue": "#0070C0"},
    "G": {"n02": [("横浜市", "4号線")],
          "name": "Green Line", "name_ja": "グリーンライン", "short": "Subway", "hue": "#009944"},
    # --- JR East
    "JK": {"route": [(*_TOKAIDO, ["川崎", "鶴見", "新子安", "東神奈川", "横浜"]),
                     (_JR, "根岸線", ["横浜", "桜木町", "関内", "石川町", "山手", "根岸", "磯子", "新杉田", "洋光台",
                                   "港南台", "本郷台", "大船"])],
           "name": "JR Keihin-Tohoku / Negishi Line", "name_ja": "京浜東北・根岸線", "short": "JR", "hue": "#00B2E5"},
    "JT": {"route": [(*_TOKAIDO, ["川崎", "横浜", "戸塚", "大船", "藤沢"])],
           "name": "JR Tokaido Line", "name_ja": "東海道線", "short": "JR", "hue": "#F68B1E"},
    "JO": {"route": [(*_TOKAIDO, ["新川崎", "~鶴見", "横浜", "保土ヶ谷", "東戸塚", "戸塚", "大船"])],
           "name": "JR Yokosuka Line", "name_ja": "横須賀線", "short": "JR", "hue": "#0070B9"},
    "SJ": {"route": [(*_TOKAIDO, ["羽沢横浜国大", "武蔵小杉"])],
           "name": "Sotetsu-JR Link Line", "name_ja": "相鉄・JR直通線", "short": "JR", "hue": "#1D2F6F"},
    "JH": {"n02": [(_JR, "横浜線")],
           "name": "JR Yokohama Line", "name_ja": "横浜線", "short": "JR", "hue": "#7AC143"},
    "JN": {"n02": [(_JR, "南武線")],
           "name": "JR Nambu Line", "name_ja": "南武線", "short": "JR", "hue": "#FFD400"},
    "JI": {"n02": [(_JR, "鶴見線")],
           "name": "JR Tsurumi Line", "name_ja": "鶴見線", "short": "JR", "hue": "#FFDD00"},
    # --- Keikyu (京浜急行電鉄)
    "KK": {"n02": [("京浜急行電鉄", "本線")],
           "name": "Keikyu Main Line", "name_ja": "京急本線", "short": "Keikyu", "hue": "#E5171F"},
    "KZ": {"n02": [("京浜急行電鉄", "逗子線")],
           "name": "Keikyu Zushi Line", "name_ja": "京急逗子線", "short": "Keikyu", "hue": "#E5171F"},
    # --- Tokyu (東急電鉄)
    "TY": {"n02": [("東急電鉄", "東横線")],
           "name": "Tokyu Toyoko Line", "name_ja": "東横線", "short": "Tokyu", "hue": "#DA0442"},
    "DT": {"n02": [("東急電鉄", "田園都市線")],
           "name": "Tokyu Den-en-toshi Line", "name_ja": "田園都市線", "short": "Tokyu", "hue": "#20A288"},
    "KD": {"n02": [("東急電鉄", "こどもの国線")],
           "name": "Tokyu Kodomonokuni Line", "name_ja": "こどもの国線", "short": "Tokyu", "hue": "#0068B7"},
    "SH": {"n02": [("東急電鉄", "東急新横浜線")],
           "name": "Tokyu Shin-yokohama Line", "name_ja": "東急新横浜線", "short": "Tokyu", "hue": "#6C5BA7"},
    # --- Minatomirai (横浜高速鉄道)
    "MM": {"n02": [("横浜高速鉄道", "みなとみらい21線")],
           "name": "Minatomirai Line", "name_ja": "みなとみらい線", "short": "Minatomirai", "hue": "#09357F"},
    # --- Sotetsu (相模鉄道)
    "SO": {"n02": [("相模鉄道", "相鉄本線")],
           "name": "Sotetsu Main Line", "name_ja": "相鉄本線", "short": "Sotetsu", "hue": "#004098"},
    "SI": {"n02": [("相模鉄道", "相鉄いずみ野線")],
           "name": "Sotetsu Izumino Line", "name_ja": "相鉄いずみ野線", "short": "Sotetsu", "hue": "#004098"},
    "SS": {"n02": [("相模鉄道", "相鉄新横浜線")],
           "name": "Sotetsu Shin-yokohama Line", "name_ja": "相鉄新横浜線", "short": "Sotetsu", "hue": "#004098"},
    # --- Yokohama Seaside Line (横浜シーサイドライン), an automated guideway
    "SL": {"n02": [("横浜シーサイドライン", "金沢シーサイドライン")],
           "name": "Kanazawa Seaside Line", "name_ja": "金沢シーサイドライン", "short": "Seaside Line",
           "hue": "#00A5DE"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# yokohama` (2026-09-30, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Closest pair within 500 m 18.0
# (Blue Line / Keihin-Tohoku), anywhere 12.4 (Kodomonokuni / Seaside Line,
# 17 km apart); the dark-mode labels separate, 20 of 20.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
# Moved so the shared colours fit (2026-10-07), hue kept as far as they allow:
# the Blue Line #08A0C0 to #007088 (pins 53.2, nearest line Tokyu Kodomonokuni
# Line 13.4, nearest beside it 19.1); the Tokyu Kodomonokuni Line #688898 to
# #486878 (pins 55.7, nearest line Blue Line 13.4, nearest beside it 18.6).
# docs/decisions_drafts/line-registry.md.
_COLOURS = {
    "B": "#007088", "G": "#30A800", "JK": line_registry.colour("jr-east-keihin-tohoku-line"),
    "JT": line_registry.colour("jr-east-tokaido-line"), "JO": line_registry.colour("jr-east-yokosuka-line"),
    "SJ": line_registry.colour("sotetsu-jr-link-line"), "JH": "#68A008",
    "JN": line_registry.colour("jr-east-nambu-line"), "JI": line_registry.colour("jr-east-tsurumi-line"),
    "KK": line_registry.colour("keikyu-main-line"), "KZ": "#F05830",
    "TY": line_registry.colour("tokyu-toyoko-line"), "DT": line_registry.colour("tokyu-den-en-toshi-line"),
    "KD": "#486878", "SH": "#C870C8", "MM": "#9840A0", "SO": "#9040C0", "SI": "#6048E0", "SS": "#C070F8",
    "SL": "#9090A0",
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station counts for the lines inside the city,
# against the collapsed set: Yokohama Municipal Subway's numbering - Blue Line
# B02-B32 (B01 湘南台 is in Fujisawa), Green Line G01-G10; Yokohama Seaside
# Line 1-14; Minatomirai Line MM01-MM06; Tokyu Kodomonokuni Line (3) and Tokyu
# Shin-yokohama Line SH01-SH03 (新横浜, 新綱島, 日吉); Sotetsu Shin-yokohama Line
# SO51-SO52 plus 西谷 (SO11). The lines the city line cuts have no published
# in-city count; their stations are listed by step 1.
GATE3 = {"source": "operators' station numbering (Yokohama Municipal Subway, Yokohama Seaside Line, "
                   "Yokohama Minatomirai Railway, Tokyu, Sotetsu)",
         "lines": {"B": 31, "G": 10, "SL": 14, "MM": 6, "KD": 3, "SH": 3, "SS": 3}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
YOKOHAMA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = YOKOHAMA_BBOX
