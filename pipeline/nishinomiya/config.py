"""Nishinomiya-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/nishinomiya.md
(13/13 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py), in Kawasaki's shape: the city's own lists, all
three buckets.

Business leg: the city's own portal (にしのみやオープンデータ, PDL 1.0;
生活衛生課): the full food-permit list as of 2026-08-31 and the barber,
beauty-salon and laundry registers of 2026-09, placed by a JOIN to MLIT's
位置参照情報 for the one municipality (no wards). The laundry register holds
62% of the official count, kept and disclosed (owner, 2026-10-02). MHLW's
open data for Nishinomiya holds only the opt-in online filings (3% of the
official restaurant count): not used.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03). Hanshin's Main and Mukogawa Lines, Hankyu's Kobe, Imazu and Koyo
Lines and JR West's Kobe and Takarazuka Lines; no Shinkansen station inside.
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "nishinomiya" / "raw"
DATA_PROCESSED = ROOT / "data" / "nishinomiya" / "processed"
OUTPUTS = ROOT / "outputs" / "nishinomiya"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Nishinomiya"
SLUG = "nishinomiya"
MUNICIPALITY = "西宮市"
PREFECTURE = "兵庫県"

# The city's portal (no CKAN): each dataset is a detail page whose download
# buttons name files under /opendata/files/<id>/. The portal's terms
# (西宮市オープンデータ利用規約 第2.0版, kiyaku.pdf, revised 2026-06-15) 第1 apply
# PDL 1.0, which needs the source, that it was processed and by whom (read
# 2026-10-02). The file names change each month, so they are pinned here and
# a later edition is a brief to correct.
PORTAL = "https://opendata.nishi.or.jp/opendata"
TERMS = PORTAL + "/kiyaku.pdf"


def _page(n):
    return f"{PORTAL}/ResultDetail.php?id={n}"


# source key -> (file, URL, the dataset page that carries its licence). Ids 49
# and 50 serve ONE workbook (sheets 理容 and 美容) and ids 67 and 68 another
# (sheets 一般 and 取次); each copy is cached under its own name, and
# source_rows reads its own sheet, so the key still decides the bucket.
SOURCE_FILES = {
    "food": ("R8.8ichiran_syokuhin.xlsx", f"{PORTAL}/files/9/R8.8ichiran_syokuhin.xlsx", _page(9)),
    "barber": ("riyo_2026.9.xlsx", f"{PORTAL}/files/49/2026.9.xlsx", _page(49)),
    "beauty": ("biyo_2026.9.xlsx", f"{PORTAL}/files/50/2026.9.xlsx", _page(50)),
    "laundry_general": ("cleaning_ippan_2026.9.xlsx", f"{PORTAL}/files/67/2026.9cleaning.xlsx", _page(67)),
    "laundry_pickup": ("cleaning_toritsugi_2026.9.xlsx", f"{PORTAL}/files/68/2026.9cleaning.xlsx", _page(68)),
}
SHEETS = {"barber": "理容", "beauty": "美容", "laundry_general": "一般", "laundry_pickup": "取次"}
# The dates the lists state (Kyoto's rule, never the download's): the food
# list's 「令和8年8月末　施設一覧」; the registers' month in their names
# (2026.9), read as its last day (newest 確認年月日 2026-09-29). No food row's
# 有効期限 has passed on 2026-08-31 (the earliest is 2026-11-30).
SOURCE_AS_OF = {"food": "2026-08-31", "barber": "2026-09-30", "beauty": "2026-09-30",
                "laundry_general": "2026-09-30", "laundry_pickup": "2026-09-30"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
REGISTERS_AS_OF = "2026-09-30"
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# The two laundry sheets are one kind (japan_step2.kind): the key names the
# sheet, the kind decides the bucket.
SOURCE_KIND = {"laundry_general": "laundry", "laundry_pickup": "laundry"}
# Declared, never inferred: XLSX; the food list opens with two title rows
# above its header (xlsx_rows finds the header by its address column).
SOURCE_ENCODING = {}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns (the food list's 申請者氏名, the
# registers' 開設者氏名, an individual or a company's representative) are
# REQUIRED so the name rule (japan_register.name_is_operator; owner
# 2026-09-27) cannot silently compare nothing; they are read IN MEMORY by
# that rule only, never kept. Never selected: 開設者住所 and 開設者電話番号 (an
# operator's own address and phone), 開設者法人名称, 開設者役職, every
# premises phone. The 市内一円 rows' addresses carry vehicle plates; they are
# not premises and never reach the map.
_REGISTER = ("施設所在地", "施設名称", "業種", "開設者氏名")
REQUIRED_COLUMNS = {
    "food": ("営業所所在地", "営業所名称", "業種", "申請者氏名"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry_general": _REGISTER,
    "laundry_pickup": _REGISTER,
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    the food list as it is, each register from its own sheet of the shared
    workbook (japan_register.city_rows' `sheet`, Fukui's)."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    yield from jr.city_rows(path, sheet=SHEETS.get(key))


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 28204.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Nishinomiya.
# S, W, N, E: the city's N03 extent (S 34.672, W 135.230, N 34.861, E 135.384)
# rounded out; step 1 stops if the city leaves it. The box the OSM query used
# (2026-10-03).
OSM_BBOX = (34.66, 135.21, 34.88, 135.4)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style as Kitakyushu's config describes (no
# macrons, 前 as -mae, lowercase after a hyphen). OSM carries macrons on
# three names and writes 前 as "-Mae" on two; the other 17 are OSM's as they
# stand. JR's and Hanshin's 西宮 are different stations (separate N02 groups),
# so step 1 appends their operators.
OSM_NAME_EN_OVERRIDES = {
    "阪神国道": "Hanshin-Kokudo",                         # Hanshin-Kokudō
    "甲子園口": "Koshienguchi",                           # Kōshienguchi
    "甲東園": "Kotoen",                                   # Kōtōen
    "武庫川団地前": "Mukogawa-danchi-mae",                # Mukogawadanchi-Mae
    "鳴尾・武庫川女子大前": "Naruo-Mukogawajoshidai-mae",   # Naruo / Mukogawajoshidai-Mae
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.34) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median gap to the nearest station
# is 684 m (closest 427 m): standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25:
# 7 lines, no Shinkansen station inside). Hanshin's Mukogawa Line (4 of 4)
# and Hankyu's Koyo Line (3 of 3) lie wholly inside; Hanshin's Main Line
# keeps 7 of 33 and Hankyu's Imazu Line 5 stations of 11 records, cut at the
# city line. The city is a narrow strip between Amagasaki and Ashiya, so the
# Hankyu Kobe Line (2 of 17), the JR Kobe Line (3 of 59) and the JR
# Takarazuka Line (2 of 30) are cut short: drawn as cut (owner 2026-10-02,
# Sakai's Midosuji precedent). N02 files the Imazu Line's two services
# (宝塚-西宮北口 and 西宮北口-今津) as one line, drawn as the one public line.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour.
_HS, _HK, _JR = "阪神電気鉄道", "阪急電鉄", "西日本旅客鉄道"
LINES = {
    "HS": {"n02": [(_HS, "本線")], "name": "Hanshin Main Line", "name_ja": "阪神本線", "short": "Hanshin",
           "hue": "#0062B3"},
    "HM": {"n02": [(_HS, "武庫川線")], "name": "Hanshin Mukogawa Line", "name_ja": "武庫川線", "short": "Hanshin",
           "hue": "#0062B3"},
    "HQ": {"n02": [(_HK, "神戸線")], "name": "Hankyu Kobe Line", "name_ja": "阪急神戸線", "short": "Hankyu",
           "hue": "#8C1C2D"},
    "HI": {"n02": [(_HK, "今津線")], "name": "Hankyu Imazu Line", "name_ja": "今津線", "short": "Hankyu",
           "hue": "#8C1C2D"},
    "HY": {"n02": [(_HK, "甲陽線")], "name": "Hankyu Koyo Line", "name_ja": "甲陽線", "short": "Hankyu",
           "hue": "#8C1C2D"},
    "JK": {"n02": [(_JR, "東海道線")], "name": "JR Kobe Line", "name_ja": "JR神戸線", "short": "JR",
           "hue": "#0072BC"},
    "JT": {"n02": [(_JR, "福知山線")], "name": "JR Takarazuka Line", "name_ja": "JR宝塚線", "short": "JR",
           "hue": "#F7A800"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# nishinomiya` (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its operator's hue that reads 3:1 on both
# map pages and clears CIE76 45 from every pin. Hanshin's and JR's blues go to
# teal and slates, Hankyu's maroon to three browns and corals, JR's
# Takarazuka yellow to ochre. Closest pair within 500 m 19.0 (Hanshin Main /
# JR Kobe), anywhere 15.6 (Hanshin Mukogawa / JR Kobe); the dark-mode labels
# separate, 7 of 7.
_COLOURS = {"HS": "#007890", "HM": "#586878", "HQ": "#985030", "HI": "#D08068", "HY": "#D06840", "JK": "#7090A0",
            "JT": "#C88800"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station indexes for the two lines wholly inside
# the city (read 2026-10-03, brief_check's checks): Hanshin's
# (hanshin.co.jp/station/) gives the Mukogawa Line 武庫川, 東鳴尾, 洲先 and
# 武庫川団地前 (4); Hankyu's (hankyu.co.jp/station/) the Koyo Line 夙川,
# 苦楽園口 and 甲陽園 (3).
GATE3 = {"source": "Hanshin's (hanshin.co.jp/station/) and Hankyu's (hankyu.co.jp/station/) station indexes: "
                   "Mukogawa Line 4, Koyo Line 3",
         "lines": {"HM": 4, "HY": 3}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
NISHINOMIYA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = NISHINOMIYA_BBOX
