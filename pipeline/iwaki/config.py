"""Iwaki-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/iwaki.md (12/12 checks, 2026-10-07). Japan's A/B batch
(Regional-1), on the shared modules (pipeline/countries/japan*.py) with the
Japan foundation's rules on (2026-10-07), in Fukuyama's shape (a city's own
full food list plus the months since) with Ichinomiya's answered merge
(owner, call 149, Ichinomiya's call 126): the full list kept whole, the
months added, as Fukushima's.

Business leg: food and personal services from the city's own CSVs (保健所
生活衛生課; CC BY 4.0 as each dataset page states, read 2026-10-07 by
staging). Food: the list of permits in term on 2026-03-31 plus the five
monthly lists of NEW permits, April to August 2026 (the months publish no
renewals and the city publishes no closures, so the food leg is an upper
bound, disclosed as Kyoto's is). Personal services: the barber and
beauty-salon list as of 2026-05-31 plus its four monthly lists of new
premises to 2026-09-30. No laundry list is published (disclosed). All
placed by a JOIN to MLIT's 位置参照情報 (one municipality, no wards). MHLW's
file for 07204 was read at Step 0 as a control only (43 permits, every one a
city permit); never a source here (call 150: its notifications too thin for
a partial layer, as Aomori's).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR East's Joban and Ban'etsu East lines. English station names from
OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "iwaki" / "raw"
DATA_PROCESSED = ROOT / "data" / "iwaki" / "processed"
OUTPUTS = ROOT / "outputs" / "iwaki"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Iwaki"
SLUG = "iwaki"
MUNICIPALITY = "いわき市"
PREFECTURE = "福島県"

# The city's own CMS (no catalogue API); every file a plain GET under
# /www/contents/<page id>/simple/. Each dataset page links CC BY 4.0
# (creativecommons.org/licenses/by/4.0/deed.ja): the food page calls it
# 「表示4.0日本」, a port that does not exist, credited as CC BY 4.0 (read
# 2026-10-07 by staging; the city's general open-data page still says CC BY
# 2.1 JP).
HOST = "https://www.city.iwaki.lg.jp"
# 食品営業許可施設 (保健所 生活衛生課), page 1652661537484.
FOOD_PAGE = HOST + "/www/contents/1652661537484/index.html"
# 理容所・美容所, page 1780984436063.
LIFE_PAGE = HOST + "/www/contents/1780984436063/index.html"
_FOOD_FILES = HOST + "/www/contents/1652661537484/simple/"
_LIFE_FILES = HOST + "/www/contents/1780984436063/simple/"

# The monthly lists of new food permits since the full list's date: (month,
# the last day it covers). The 24 months before it (2024-04 to 2026-03,
# cached at Step 0) are already in the full list and are not read (the
# brief: 181 of the 183 permits of 2025-08 to 2026-03 by number and grant
# date).
FOOD_MONTHS = (("04", "2026-04-30"), ("05", "2026-05-31"), ("06", "2026-06-30"), ("07", "2026-07-31"),
               ("08", "2026-08-31"))
_FOOD_MONTH_KEYS = {f"food_{m}": f"Shokuhin_itiran_R08{m}.csv" for m, _ in FOOD_MONTHS}
# The barber and beauty list's months: each month's new premises, June to
# September 2026 (the page: 令和８年６月分から毎月追加していきます).
LIFE_MONTHS = (("6", "2026-06-30"), ("7", "2026-07-31"), ("8", "2026-08-31"), ("9", "2026-09-30"))
_LIFE_MONTH_KEYS = {f"life_{m}": f"ribiyoujo_R8.{m}.csv" for m, _ in LIFE_MONTHS}
# source key -> (file, URL, the page that lists it and carries its licence).
# One entry per file read (Step 0, 2026-10-06, each HTTP 200 from the city's
# own host).
SOURCE_FILES = {
    "food_list": ("Shokuhin_itiran_R08.csv", _FOOD_FILES + "Shokuhin_itiran_R08.csv", FOOD_PAGE),
    **{k: (name, _FOOD_FILES + name, FOOD_PAGE) for k, name in _FOOD_MONTH_KEYS.items()},
    "life_list": ("ribiyoujo_ichiran.csv", _LIFE_FILES + "ribiyoujo_ichiran.csv", LIFE_PAGE),
    **{k: (name, _LIFE_FILES + name, LIFE_PAGE) for k, name in _LIFE_MONTH_KEYS.items()},
}
# Kyoto's rule: the date each list states, never the download's. The full
# food list reads 令和７年度末時点 (2026-03-31), the barber and beauty list
# 令和８年５月31日現在; each month file covers the month it names (the food
# page's 「令和８年8月31日現在」 is the August file's).
FOOD_AS_OF = "2026-03-31"
FOOD_NEW_TO = FOOD_MONTHS[-1][1]
REGISTERS_AS_OF = "2026-05-31"
REGISTERS_NEW_TO = LIFE_MONTHS[-1][1]
SOURCE_AS_OF = {"food_list": FOOD_AS_OF, **{f"food_{m}": end for m, end in FOOD_MONTHS},
                "life_list": REGISTERS_AS_OF, **{f"life_{m}": end for m, end in LIFE_MONTHS}}

# What step 2 reads. The food leg is two sources, each read against its own
# file's date (calls 161 and 172; Fukushima's worked example): "food", the
# full list of permits in term on 2026-03-31, and "food_new", the five
# months' new permits, in term on 2026-08-31. One source rebuilt from all six
# files would read every permit against one date: 2026-08-31 would drop the
# full list's permits ending in May to August that the months never
# republish (Fukuyama's method, merge (b), 134 restaurants, which call 149
# set aside). Every row is read as the files hold it (Ichinomiya's read,
# whose merge call 149 applies), not through japan_register.rebuilt_register:
# every full-list row is a permit in term on the list's date, and the
# rebuild's rank (latest expiry per address, trade name and type) hid a live
# permit of another 種目 at 11 premises, 5 of them a restaurant shown in no
# other row (3,725 storefronts rebuilt, 3,730 read whole; measured
# 2026-10-07). One pin per premises and bucket folds the repeats (the brief's
# 98 full-list rows in 47 groups; 許可番号 alone is reused across years and
# never a key). The barber and beauty list is one file split by 種別, so
# japan_eigyo's source decides each row (Fukuyama's).
SOURCES = {"food": SOURCE_FILES["food_list"][0], "food_new": "the five monthly new-permit lists",
           "barber": SOURCE_FILES["life_list"][0], "beauty": SOURCE_FILES["life_list"][0]}
# The months' kind is the food list's (Tokyo's SOURCE_KIND).
SOURCE_KIND = {"food_new": "food"}
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. Measured 2026-10-07: the full
# list's earliest 許可満了年月日 is 2026-05-31 and its latest 許可年月日
# 2026-03-31; the months' permits are granted in their own month and end
# 2031 to 2033. No list carries a start date apart from the grant date, so
# no renewal can wait past an as-of (Fukuyama's trap cannot arise here).
TERM_AS_OF = {"food": FOOD_AS_OF, "food_new": FOOD_NEW_TO}
# Declared, never inferred: the full food list and the five months UTF-8
# with a BOM (the months to February 2026, not read, are cp932); the barber
# and beauty list and its June file cp932 (they start with №), July to
# September UTF-8 with a BOM.
SOURCE_ENCODING = {**{k: "utf-8-sig" for k in SOURCE_FILES}, "life_list": "cp932", "life_6": "cp932"}

# The columns each raw file must carry (fetch_sources.py and source_rows stop
# on a header without them); one schema across every food file, and one
# across the barber and beauty files. The operator columns (the food lists'
# 営業者氏名, a sole trader's own name on 2,175 of the full list's 4,375 rows,
# and 代表者氏名（法人）; the register's 開設者 and 代表者氏名（法人のみ）) are
# REQUIRED so the name rule (japan_register.name_is_operator; owner
# 2026-09-27) cannot silently compare nothing; read IN MEMORY by that rule
# only, never kept. Never selected: 営業者住所, 営業者住所気付, 営業者電話番号
# (the operator's own address and phone), 営業所電話番号, the register's
# 開設者住所（法人のみ）, 方書（開設者住所） and 電話番号.
_FOOD = ("営業所名称", "営業所所在地", "営業者氏名", "代表者氏名（法人）", "業種", "種目", "許可番号", "許可年月日",
         "許可満了年月日")
_LIFE = ("名称", "所在地", "種別", "開設者", "代表者氏名（法人のみ）")
REQUIRED_COLUMNS = {
    "food_list": _FOOD,
    **{k: _FOOD for k in _FOOD_MONTH_KEYS},
    "food": _FOOD,
    "food_new": _FOOD,
    "life_list": _LIFE,
    **{k: _LIFE for k in _LIFE_MONTH_KEYS},
    "barber": _LIFE,
    "beauty": _LIFE,
}
# The register's 種別 for each source; a （移動） salon is read into its
# trade's source and leaves by japan_eigyo's mobile-salon rule (one each in
# the 2026-05-31 list). Any other value stops the build.
_KIND = {"barber": ("理容所", "（移動）理容所"), "beauty": ("美容所", "（移動）美容所")}


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def file_rows(key):
    """One fetched file's rows as it stands (japan_fetch's count and header
    check, and every read below), each checked for its own columns."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    rows = list(jr.city_rows(path))
    missing = [c for c in REQUIRED_COLUMNS[key] if rows and c not in rows[0]]
    if missing:
        raise SystemExit(f"{path.name}: header lacks {missing} - not the file the brief read")
    return rows


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    "food" is the full list as it stands, "food_new" the five monthly lists in
    order, each read by step 2 against its own TERM_AS_OF (the operator
    columns reach step 2's name rule in memory and leave with the rows).
    "barber" and "beauty": the 2026-05-31 list plus the four months, split by
    種別 (the months add new premises only; the city publishes no closures)."""
    if key in ("food", "food_new"):
        keys = ["food_list"] if key == "food" else list(_FOOD_MONTH_KEYS)
        return [r for k in keys for r in file_rows(k)]
    rows = [r for k in ("life_list", *_LIFE_MONTH_KEYS) for r in file_rows(k)]
    other = {r["種別"] for r in rows} - {v for vs in _KIND.values() for v in vs}
    if other:
        raise SystemExit(f"ribiyoujo: 種別 {sorted(other)} is neither a barber's nor a beauty salon's")
    return [r for r in rows if r["種別"] in _KIND[key]]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 07204.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Iwaki.
# S, W, N, E: the city's N03 extent (S 36.856, W 140.566, N 37.320,
# E 141.009; 1,230.9 km2) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (36.85, 140.56, 37.33, 141.01)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (no macrons, lowercase after a hyphen, a
# katakana loanword kept as its English word, 前 as -mae).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (~140.786) and the whole extent (140.566 to
# 141.009) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median nearest-station gap is
# 4,181 m (3,255 to 7,369): standard rings by the spacing rule.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 2 lines, no Shinkansen in the city). Every line is cut at the
# city line (owner 2026-09-24): JR's Joban Line keeps 10 of 81 and Ban'etsu
# East Line 5 of 16; neither is cut to a stub. いわき is one N02 group for
# both. No frequency floor (owner, 2026-10-06, calls 46 and 86): the Ban'etsu
# East Line inside the city runs 6 to 8 trains a day each way and the Joban
# Line north of いわき 16 to 20 (JR East's weekday station timetables, 2610
# edition, read 2026-10-06), drawn and named on the page.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), a starting hue for scripts/line_colour_search.py (`hue`) and the
# project's colour. Line names follow the operator's signs with no macrons,
# as Tokyo's JR Joban Line and Maebashi's: JR East's いわき timetable index
# names the 常磐線 and 磐越東線. Hues: JR East's green for the Joban Line, an
# orange for the Ban'etsu East Line; starting points only, since the colours
# are the project's own.
_JR = "東日本旅客鉄道"
LINES = {
    "JB": {"n02": [(_JR, "常磐線")], "name": "JR Joban Line", "name_ja": "常磐線", "short": "JR",
           "hue": "#00B261"},
    "BE": {"n02": [(_JR, "磐越東線")], "name": "JR Ban'etsu East Line", "name_ja": "磐越東線", "short": "JR",
           "hue": "#F68B1E"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# iwaki` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each the
# feasible colour nearest its starting hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. The Joban green moves to a yellower
# green (Maebashi's Joetsu colour), 45.7 from Personal services' pin; the
# Ban'etsu East orange darkens to read on white. The pair is 95.4 apart; the
# dark-mode labels separate, 2 of 2.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "JB": line_registry.colour("jr-east-joban-line"), "BE": "#E07800",
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city. JR East's line timetables (2610
# edition, timetable-v/240d1 and 250d1, read 2026-10-07) list the Joban Line
# through the city from 勿来 to 末続 (10 stations) and the Ban'etsu East Line's
# 16 stations, いわき to 郡山, of which いわき to 川前 (5) lie inside, as N02
# does.
GATE3 = {"source": "JR East's line timetables (timetables.jreast.co.jp, 2610 edition): Joban Line 勿来-末続 10 "
                   "inside the city; Ban'etsu East Line 16 stations, いわき-川前 5 inside",
         "lines": {"JB": 10, "BE": 5}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
IWAKI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = IWAKI_BBOX
