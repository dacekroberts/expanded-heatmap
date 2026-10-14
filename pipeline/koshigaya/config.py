"""Koshigaya-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/koshigaya.md (16/16 checks, 2026-10-11). Koshigaya City
(越谷市, 11222), one municipality with no wards, a core city with its own
health center: Saitama Prefecture's lists (pipeline/countries/saitama_pref.py)
do not cover it. Japan's A/B batch (East-2), on the shared modules
(pipeline/countries/japan*.py) with the Japan foundation's rules on, in
Ichinomiya's shape (a city's own full food list kept whole plus the months
since; owner, call 126).

Business leg: the city's own lists (越谷市 保健医療部 生活衛生課), PDL 1.0 by
Saitama Prefecture's portal records for these exact pages (owner, call 142).
Food: the list of permits in term and notifications on 2026-03-31, kept
whole, plus the monthly lists of April, May, June and August 2026 (the
page's July link serves August's file; no July file exists, the brief's open
call 2, option (a)). The list holds permits and notifications together; the
food-retail notifications count, in Retail (the japan_eigyo module's standing
rule). Personal services: the barber, beauty and laundry lists as of
2026-10-02. MHLW's 食品衛生申請等システム open data gives one thing only: its
own point for a city row the block join misses (POINT_DONORS; call 127c). Its
permits and notifications are not added (calls 126-127; the city's own list
already publishes notifications). All placed by a JOIN to MLIT's 位置参照情報
(one municipality, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03): the Tobu Skytree Line (6 of N02's 55 伊勢崎線 stations) and JR East's
Musashino Line (2 of 27). English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "koshigaya" / "raw"
DATA_PROCESSED = ROOT / "data" / "koshigaya" / "processed"
OUTPUTS = ROOT / "outputs" / "koshigaya"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Koshigaya"
SLUG = "koshigaya"
MUNICIPALITY = "越谷市"
PREFECTURE = "埼玉県"

# The city's own CMS (no catalogue API; it sends no charset). Saitama
# Prefecture's open-data portal records both pages under PDL 1.0 (dataset 530,
# resource 2715, the food page; dataset 2004, resource 6312, the registers
# page): the record relied on (owner, call 142, Hiroshima's shape).
_HOST = "https://www.city.koshigaya.saitama.jp"
# 食品関係営業施設一覧, ページ番号 8077.
FOOD_PAGE = _HOST + "/kurashi_shisei/fukushi/hokenjo/shokuhin/20160401.html"
# 営業施設一覧, ページ番号 7235.
LIFE_PAGE = _HOST + "/kurashi_shisei/fukushi/hokenjo/kankyo/jouhouteikyou.html"
PORTAL_FOOD = "https://opendata.pref.saitama.lg.jp/resources/2715"
PORTAL_LIFE = "https://opendata.pref.saitama.lg.jp/resources/6312"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
_FOOD_FILES = _HOST + "/kurashi_shisei/fukushi/hokenjo/shokuhin/files/"
_LIFE_FILES = _HOST + "/kurashi_shisei/fukushi/hokenjo/kankyo/files/"

# The food months since the full list: month -> the page's file. No July 2026
# file: the page's 7月分 link serves r8.aug.syokuhin.xls (read 2026-10-06 and
# again 2026-10-11, the brief's first check). A July file appearing fails that
# check: fetch it and add it here.
FOOD_MONTHS = {"04": "r8.apr.syokuhin.xls", "05": "r8.may.syokuhin.xls", "06": "r8.june.syokuhin.xls",
               "08": "r8.aug.syokuhin.xls"}
# source key -> (file, URL, the page that carries it). One entry per file
# fetched; the food months are read inside source_rows.
SOURCE_FILES = {
    "food": ("r8.3.31koukai.xls", _FOOD_FILES + "r8.3.31koukai.xls", FOOD_PAGE),
    **{f"food_{m}": (f, _FOOD_FILES + f, FOOD_PAGE) for m, f in FOOD_MONTHS.items()},
    "barber": ("riyou.xls", _LIFE_FILES + "riyou.xls", LIFE_PAGE),
    "beauty": ("biyou.xls", _LIFE_FILES + "biyou.xls", LIFE_PAGE),
    "laundry": ("kurini.xls", _LIFE_FILES + "kurini.xls", LIFE_PAGE),
    "mhlw": ("11222_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=11222_food_business_all.csv",
             MHLW_TOP),
}
FOOD_MONTH_KEYS = tuple(f"food_{m}" for m in FOOD_MONTHS)
# Kyoto's rule: the date each list states, never the download's. The full
# list reads 令和8年3月31日現在; each month file the month it names; the
# registers' page heading 令和8年10月2日現在; MHLW's file states none.
SOURCE_AS_OF = {"food": "2026-03-31", "barber": "2026-10-02", "beauty": "2026-10-02", "laundry": "2026-10-02",
                "mhlw": None, **{f"food_{m}": f"2026-{m}" for m in FOOD_MONTHS}}
FOOD_AS_OF = SOURCE_AS_OF["food"]
REGISTERS_AS_OF = "2026-10-02"
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. The full list is kept whole on
# its own date (call 126); the months against 2026-08-31, the last day the
# newest covers.
TERM_AS_OF = {"food": "2026-03-31", "food_new": "2026-08-31", "mhlw_points": "2026-08-31"}

# What step 2 reads. "food_new" is the four monthly lists as one source of the
# same kind as the full list (japan_step2.kind, Ichinomiya's): they carry
# renewals as well as new permits (the brief: 118 of 235 rows sit at a
# full-list premises), a renewal under a new number is the same premises, and
# one pin per premises and bucket shows it once.
SOURCES = {"food": SOURCE_FILES["food"][0], "food_new": "the four monthly food lists",
           "barber": SOURCE_FILES["barber"][0], "beauty": SOURCE_FILES["beauty"][0],
           "laundry": SOURCE_FILES["laundry"][0]}
SOURCE_KIND = {"food_new": "food"}
# Declared, never inferred: every city file an old BIFF .xls (read through
# xlrd); MHLW's UTF-8 with a BOM.
SOURCE_ENCODING = {**{k: "xls" for k in SOURCE_FILES}, "mhlw": "utf-8-sig"}
# The columns each file and source must carry; fetch_sources.py and step 2
# stop on a header without them. The operator columns (the food lists'
# 申請者名 and 代表者名（法人）, a sole trader's own name on 1,592 of 4,567
# full-list rows by the brief; the registers' 申請者_氏名 and 代表者_氏名;
# MHLW's 法人名) are REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; read IN MEMORY by that rule only, never kept. Never selected:
# 申請者住所, 申請者電話番号, 営業所電話番号, 申請者_所在地, 施設_電話番号, 法人番号,
# 法人住所 and every phone.
_FOOD = ("許可番号", "業種", "種目", "屋号", "営業所所在地", "申請者名", "代表者名（法人）", "許可年月日", "終了年月日")
_REG = ("施設_名称", "施設_所在地", "申請者_氏名", "代表者_氏名")
_MHLW = ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
         "廃業年月日", "法人名")
REQUIRED_COLUMNS = {
    "food": _FOOD, "food_new": _FOOD, **{k: _FOOD for k in FOOD_MONTH_KEYS},
    "barber": _REG, "beauty": _REG, "laundry": (*_REG, "種別"),
    "mhlw": _MHLW, "mhlw_points": _MHLW,
}
# A city food row the block join misses takes MHLW's point for the same
# premises (ward, town, trade name), read from the whole file under its own
# key, never drawn (call 127c, Toyama's mechanism; the brief: block point
# against MHLW's point a median 56 m, 95.8% within 250 m).
POINT_DONORS = {"food": "mhlw_points", "food_new": "mhlw_points"}


def source_csv(key):
    if key == "mhlw_points":
        key = "mhlw"
    return DATA_RAW / SOURCE_FILES[key][0]


def file_rows(key):
    """One fetched file's rows as it stands (japan_fetch's count and header
    check, and every read below)."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    return list(jr.city_rows(path))


def _rows(key):
    path = source_csv(key)
    rows = file_rows(key)
    missing = [c for c in REQUIRED_COLUMNS[key] if rows and c not in rows[0]]
    if missing:
        raise SystemExit(f"{path.name}: header lacks {missing} - not the file the brief read")
    return rows


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    "food" is the full list as it stands; "food_new" the four monthly lists in
    order; each register its one file. "mhlw_points" is MHLW's whole file,
    read by POINT_DONORS for its coordinates only."""
    if key == "food_new":
        for k in FOOD_MONTH_KEYS:
            yield from _rows(k)
        return
    yield from _rows(key)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 11222.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Koshigaya.
# S, W, N, E: the city's N03 extent (S 35.855, W 139.745, N 35.959, E 139.840)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.85, 139.74, 35.96, 139.85)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (~139.79) and the whole extent (139.745 to
# 139.840) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-station gap is 1,295 m (8 stations), over the 550 m
# that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub_test on
# N02-25: 2 lines, 8 station records, 8 station groups). The Tobu Skytree Line
# keeps 6 of N02's 55 伊勢崎線 stations (蒲生, 新越谷, 越谷, 北越谷, 大袋,
# せんげん台) and JR East's Musashino Line 2 of 27 (南越谷, 越谷レイクタウン):
# main lines cut at the city line, neither a stub. 南越谷 (JR) and 新越谷
# (Tobu) are separate N02 groups 132 m apart, an interchange by footway under
# two names, kept apart as MLIT keeps them (trap 1); their rings overlap. No
# Shinkansen, subway, tram or light rail in the city. No frequency floor
# (owner, 2026-10-06, calls 46 and 86): the thinnest station, 大袋, has 111
# and 115 weekday departures (Tobu's timetable, read 2026-10-06).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
# Two different stations 132 m apart (南越谷 and 新越谷) read as "still
# platforms" to gate 1 at its default; the floor is set under that pair
# (Tama's precedent, Tbilisi's before it).
SPACING_MIN_M = 100

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the Skytree Line as 伊勢崎線;
# the operator signs 浅草 / 押上 to 東武動物公園 the Tobu Skytree Line (Tokyo's,
# Soka's and Kasukabe's TS entry, the same N02 track). Line names without
# macrons.
LINES = {
    "TS": {"n02": [("東武鉄道", "伊勢崎線")], "name": "Tobu Skytree Line", "name_ja": "東武スカイツリーライン",
           "short": "Tobu", "hue": "#0F6CC3"},
    "JM": {"n02": [("東日本旅客鉄道", "武蔵野線")], "name": "JR Musashino Line", "name_ja": "武蔵野線",
           "short": "JR", "hue": "#F15A22"},
}
# SHARED LINES: both lines are drawn on other maps and take their one
# site-wide colour from pipeline/line_registry.py (owner, 2026-10-07: one
# colour per line on every map), never a value of this city's own. Measured
# 2026-10-11 against the japan_eigyo pins and each other: see the drafts
# file's Koshigaya entry.
_COLOURS = {
    "TS": line_registry.colour("tobu-skytree-line"),
    "JM": line_registry.colour("jr-east-musashino-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own stations inside the city line (the brief: Tobu's
# Skytree Line 6, JR East's Musashino Line 2, read 2026-10-06 from each
# operator's timetable index).
GATE3 = {"source": "Tobu's and JR East's own station timetables (transfer-internal.navitime.biz/tobu, "
                   "timetables.jreast.co.jp), read against the city line: Skytree Line 6, Musashino Line 2",
         "lines": {"TS": 6, "JM": 2}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KOSHIGAYA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KOSHIGAYA_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3601768402)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
PLACE_DROPPED = {}
