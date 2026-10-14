"""Fuji-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/fuji.md (9/9 checks, 2026-10-11). Part of the A/B build
plan's Regional-2 batch, on the shared modules (pipeline/countries/japan*.py)
with every shared rule on. Personal services only (Band B, owner 2026-10-06:
Kochi's page shape): MHLW's food file for the prefecture's jurisdiction
(22000) places about 41% of the city's estimated restaurants, at most 67%,
under the placement bar.

Business leg: Shizuoka Prefecture's three 生活衛生 registers on its open-data
portal (opendata.pref.shizuoka.jp, author 衛生課, CC BY): barbers, beauty
salons and laundries, each a full list as of 2026-03-31 plus the monthly
files of new premises since (April to August 2026). The lists cover the
prefecture less 静岡市 and 浜松市; Fuji's rows are cut by address. Closures
after 2026-03-31 are not published, so each register is an UPPER BOUND on its
last month (Kyoto's call: pinned to the last month read). Everything placed
by a JOIN to MLIT's 位置参照情報 (one municipality, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR Central's Tokaido and Minobu lines, cut at the city line, and the
Gakunan Railway Line, whole. English station names from OpenStreetMap's
name:en.
"""

import unicodedata
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "fuji" / "raw"
DATA_PROCESSED = ROOT / "data" / "fuji" / "processed"
OUTPUTS = ROOT / "outputs" / "fuji"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Fuji"
SLUG = "fuji"
MUNICIPALITY = "富士市"
PREFECTURE = "静岡県"

# Shizuoka Prefecture's open-data portal (静岡県オープンデータ): one dataset per
# trade, author 衛生課, every resource marked 表示（CC BY）. Each holds the full
# list as of 31 March (all premises on the 開設届出台帳, 廃止 and みなし廃止 out,
# 政令市 excluded) and one file per month of the previous month's new
# premises. Licence: CC BY 4.0 by the portal's terms, with its prescribed
# modified-use credit (read by staging, 2026-10-06; DECISIONS.md).
PORTAL = "https://opendata.pref.shizuoka.jp"
_DATASET = {"barber": 11261, "beauty": 11262, "laundry": 11263}
_PAGE = {t: f"{PORTAL}/dataset/{n}.html" for t, n in _DATASET.items()}
# key -> (trade, resource id, the resource's own name, the portal's file
# path after /fs/<id digits>/_/, the last day the file covers). The resource
# ids and paths are the dataset pages' own links (read 2026-10-11). A new
# month is a new resource id and a re-measure; the 2027 full list (about
# 2027-04-30) replaces the March one.
# July's beauty file exists twice on the portal (857848 and 857854, 11 rows
# each, Fuji's one row identical in both; the brief, 2026-10-06): the dataset
# page links only 857854, which is the one pinned. April's beauty file is the
# portal's 2026-07-02 replacement (a phone-number correction; phones are
# never read).
_LISTS = {
    "barber": ("barber", 855060, "理容所施設一覧（令和８年３月31日時点）.csv", "__________8_3_31____.csv", "2026-03-31"),
    "barber_04": ("barber", 854471, "令和８年４月新規開設理容所施設一覧.csv", "__8_4__________.csv", "2026-04-30"),
    "barber_05": ("barber", 855027, "令和８年５月新規開設理容所施設一覧.csv", "__8_5__________.csv", "2026-05-31"),
    "barber_06": ("barber", 857430, "令和８年６月新規理容所施設一覧.csv", "__8_6__________.csv", "2026-06-30"),
    "barber_07": ("barber", 857849, "令和８年７月新規理容所施設一覧.csv", "__8_7__________.csv", "2026-07-31"),
    "barber_08": ("barber", 859043, "令和８年８月新規理容所施設一覧.csv", "__8_8__________.csv", "2026-08-31"),
    "beauty": ("beauty", 855063, "美容所施設一覧（令和８年３月31日時点）.csv", "__________8_3_31____.csv", "2026-03-31"),
    "beauty_04": ("beauty", 855979, "令和８年４月新規美容所施設一覧（0702差替え版）.csv", "__8_4___________0702_____.csv",
                  "2026-04-30"),
    "beauty_05": ("beauty", 855036, "令和８年５月新規美容所施設一覧.csv", "__8_5__________.csv", "2026-05-31"),
    "beauty_06": ("beauty", 857434, "令和８年６月新規美容所施設一覧.csv", "__8_6__________.csv", "2026-06-30"),
    "beauty_07": ("beauty", 857854, "令和８年７月新規美容所施設一覧.csv", "__8_7__________.csv", "2026-07-31"),
    "beauty_08": ("beauty", 859045, "令和８年８月新規美容所施設一覧.csv", "__8_8__________.csv", "2026-08-31"),
    "laundry": ("laundry", 855059, "クリーニング所施設一覧（令和８年３月31日時点）.csv", "______________8_3_31____.csv",
                "2026-03-31"),
    "laundry_04": ("laundry", 854473, "令和８年４月新規クリーニング所施設一覧.csv", "__8_4______________.csv", "2026-04-30"),
    "laundry_05": ("laundry", 855025, "令和８年５月新規クリーニング所施設一覧.csv", "__8_5______________.csv", "2026-05-31"),
    "laundry_06": ("laundry", 857432, "令和８年６月新規クリーニング所施設一覧.csv", "__8_6______________.csv", "2026-06-30"),
    "laundry_07": ("laundry", 857850, "令和８年７月新規クリーニング所施設一覧.csv", "__8_7______________.csv", "2026-07-31"),
    "laundry_08": ("laundry", 859042, "令和８年８月新規クリーニング所施設一覧.csv", "__8_8______________.csv", "2026-08-31"),
}
# source key -> (file, URL, the page that carries its licence). The file name
# is Step 0's: <dataset>_<resource id>_<the resource's own name>.
SOURCE_FILES = {
    k: (f"{_DATASET[t]}_{rid}_{name}", f"{PORTAL}/fs/{'/'.join(str(rid))}/_/{path}", _PAGE[t])
    for k, (t, rid, name, path, _) in _LISTS.items()}
SOURCE_AS_OF = {k: d for k, (_, _, _, _, d) in _LISTS.items()}
# What step 2 reads: each trade's full list plus its monthly additions
# (source_rows); the monthly files are read inside it only.
SOURCES = {k: SOURCE_FILES[k][0] for k in ("barber", "beauty", "laundry")}
MONTHLY = {t: tuple(k for k, v in _LISTS.items() if v[0] == t and k != t) for t in SOURCES}
# Each register's date, PINNED to the last month read (never the download's):
# an upper bound, openings added, closures not.
TRADE_AS_OF = {t: SOURCE_AS_OF[MONTHLY[t][-1]] for t in SOURCES}
REGISTERS_AS_OF = max(TRADE_AS_OF.values())
FOOD_AS_OF = None  # no food leg (owner, 2026-10-06)
# Declared, never inferred: every file is cp932 (a title row and a blank row
# above the header; city_rows finds the header by its address column).
SOURCE_ENCODING = {k: "cp932" for k in _LISTS}
# The premises columns, by trade. The months are not one shape (June's files
# put 確認年月日 before 業種; the June and July files pad each row to 248
# columns; May's laundry file names its kind 業種, its date 届出年月日): every
# column is read by NAME, never by position.
_NAME = {"barber": "理容所名称", "beauty": "美容所名称", "laundry": "クリーニング所名称"}
_ADDR = {"barber": "理容所所在地", "beauty": "美容所所在地", "laundry": "クリーニング所所在地"}
_OPERATOR = "開設者氏名"
# The kind column: 業種 on the barber and beauty files (the trade's own name
# on every row), 種別 on the laundry files (取次所, クリーニング所（一般）,
# 無店舗取次所), except May's laundry file, which names it 業種.
_KIND = {"barber": "業種", "beauty": "業種", "laundry": "種別"}
_KIND_BY_KEY = {"laundry_05": "業種"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator column (開設者氏名: a company's name where
# the operator is a company, by the dataset pages; no company or cooperative
# marker on 196 of 211 barber rows, 427 of 534 beauty rows and 33 of 93
# laundry rows, the shape of a sole trader's own name; the brief, 2026-10-06)
# is REQUIRED so the name rule (japan_register.name_is_operator; owner
# 2026-09-27) cannot silently compare nothing; it is read IN MEMORY by that
# rule only, never kept. Never selected: the phone column (…電話番号).
REQUIRED_COLUMNS = {k: (_NAME[t], _ADDR[t], _OPERATOR, _KIND_BY_KEY.get(k, _KIND[t]))
                    for k, (t, *_) in _LISTS.items()}
# The columns carried into step 2: the premises' own, the kind (a 無店舗
# laundry agent is not a premises) and the operator column for the name rule
# (in memory). No file carries a permit term (確認年月日 is the confirmation
# date; 開設確認 has no expiry), so no TERM_AS_OF is needed.
_KEEP = (*_NAME.values(), *_ADDR.values(), _OPERATOR, "業種", "種別")
# Fuji's rows per file, as this build measured them (2026-10-11, equal to the
# brief's of 2026-10-06): a file that changes shape or is replaced stops the
# build instead of passing silently. Barbers 211 + 1, beauty salons 534 + 5,
# laundries 93 + 0 (31 general, 61 pick-up counters, 1 storeless agent).
FUJI_ROWS = {
    "barber": 211, "barber_04": 0, "barber_05": 0, "barber_06": 0, "barber_07": 0, "barber_08": 1,
    "beauty": 534, "beauty_04": 0, "beauty_05": 0, "beauty_06": 3, "beauty_07": 1, "beauty_08": 1,
    "laundry": 93, "laundry_04": 0, "laundry_05": 0, "laundry_06": 0, "laundry_07": 0, "laundry_08": 0,
}


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def _address(r, trade):
    a = unicodedata.normalize("NFKC", (r.get(_ADDR[trade]) or "")).replace(" ", "").replace("　", "")
    return a[len(PREFECTURE):] if a.startswith(PREFECTURE) else a


def source_rows(key):
    """A register's rows (japan_step2 reads this hook where a city defines it):
    the prefecture's full list (2026-03-31) and every monthly addition since,
    in one stream (Shizuoka's and Ichinomiya's shape, call 126), cut to the
    rows whose address begins 富士市 once 静岡県 is cut (Kakogawa's
    prefecture-list filter), the premises and name-rule columns only.

    The cut is by ADDRESS, never by health center: 富士保健所 covers 富士市 and
    富士宮市 (the brief, 2026-10-06: 312 barbers, 831 salons and 133 laundries
    in all, one beauty row writing 富士宮 with no 市). A row that names 富士市
    anywhere after its start stops the build (Tsu's rule): its municipality
    would be a guess. A month with nothing new holds one row reading 該当なし
    and no address, which the cut passes over.

    No file carries a unique key (確認番号 repeats and is sometimes empty);
    the brief measured 0 repeats by (address, trade name) in any list, and
    step 2 keeps one pin per address, name and bucket anyway. The counts are
    checked against FUJI_ROWS."""
    from pipeline.countries import japan_register as jr

    for k in (key, *MONTHLY[key]):
        path = source_csv(k)
        if not path.exists():
            raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
        n = 0
        for r in jr.city_rows(path):
            a = _address(r, key)
            if a.startswith(MUNICIPALITY):
                n += 1
                yield {c: r.get(c) for c in _KEEP if c in r}
            elif MUNICIPALITY in a:
                raise SystemExit(f"{path.name}: a row names {MUNICIPALITY} after its start - assign it by hand")
        if n != FUJI_ROWS[k]:
            raise SystemExit(f"{path.name}: {n} rows begin {MUNICIPALITY}, the build measured {FUJI_ROWS[k]} - "
                             f"a new edition? Re-measure (config.FUJI_ROWS).")


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 22210.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Fuji.
# S, W, N, E: the city's N03 extent (S 35.116, W 138.558, N 35.359,
# E 138.812; the 2008 merger brought in 富士川町) rounded out; step 1 stops if
# the city leaves it. The box reaches the slopes of Mount Fuji; every drawn
# station lies south of 35.21 N.
OSM_BBOX = (35.11, 138.55, 35.36, 138.82)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the whole extent (138.558 to 138.812, centroid 138.699) falls
# in the 138 to 144 band. Derived per city, not copied (Hamamatsu, west of
# 138 E, is 53N) - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25: 3 lines; the Shinkansen's 新富士 dropped). JR's Tokaido Line keeps
# 4 of 89 and its Minobu Line 5 of 39, cut at the city line (owner
# 2026-09-24); the Gakunan Railway Line lies wholly inside (10 of 10). 富士 is
# one group on both JR lines, 吉原 one group on JR and Gakunan (142 m).
_JR, _GK = "東海旅客鉄道", "岳南電車"
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names carry no macrons.
LINES = {
    "JT": {"n02": [(_JR, "東海道線")], "name": "JR Tokaido Line", "name_ja": "東海道線", "short": "JR",
           "hue": "#F68B1E"},
    "MN": {"n02": [(_JR, "身延線")], "name": "JR Minobu Line", "name_ja": "身延線", "short": "JR",
           "hue": "#A8518A"},
    "GK": {"n02": [(_GK, "岳南鉄道線")], "name": "Gakunan Railway Line", "name_ja": "岳南鉄道線",
           "short": "Gakunan", "hue": "#E8380D"},
}
# Colours: JR Central's Tokaido Line takes its one site-wide colour from
# pipeline/line_registry.py (owner, 2026-10-07: one colour per line on every
# map). The Minobu and Gakunan lines are on this map alone: each is the
# feasible colour nearest its operator's hue by scripts/line_colour_search.py's
# rule with the Tokaido colour held fixed (3:1 on both basemaps, CIE76 >= 45
# from every pin, >= 18 from a line within 500 m; measured 2026-10-11).
# Margins: pins >= 62.6 (JT), 45.3 (MN), 53.2 (GK), so no accepted trade
# under 45; lines JT/GK 21.1 (they share 吉原, 12 m apart at the nearest),
# JT/MN 89.0, MN/GK 88.8. Against Shizuoka's Shizuoka-Shimizu Line (#0068B8,
# the neighbouring map): 41.1 or more. Re-measure if a pin colour, the
# registry colour or a drawn line changes.
_COLOURS = {"JT": line_registry.colour("jr-central-tokaido-line"), "MN": "#B070B0", "GK": "#E83810"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the Gakunan Railway's weekday timetable (gakutetsu.jp/timetable,
# 2026heijitsu.pdf, the 2026-03-14 revision; read by staging 2026-10-06) lists
# 10 stations, 吉原 to 岳南江尾, as N02 has 10. JR is cut at the city line.
GATE3 = {"source": "The Gakunan Railway's weekday timetable (gakutetsu.jp/timetable, revised 2026-03-14): "
                   "10 stations, 吉原 to 岳南江尾",
         "lines": {"GK": 10}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
FUJI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = FUJI_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3604674651)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/fuji.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # A description standing in for a name (owner, 2026-10-13)
    "way/1272406197": "'Old electric locomotives and cars': an English description of rolling stock on display, tagged a monument; no wikidata",
    # A bare type word (owner, 2026-10-13)
    "way/1208746160": "'児童遊び場': 'children's play area' alone",
    # A duplicate of one object (owner, 2026-10-13)
    "way/445137992": "'石坂川(暗渠)': the culverted section of 石坂川 (way/445137991, about 600 m upstream), named with '(culvert)' in brackets",
}
