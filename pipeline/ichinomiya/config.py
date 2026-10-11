"""Ichinomiya-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/ichinomiya.md (15/15 checks, 2026-10-07). Japan's A/B batch
(Regional-1), on the shared modules (pipeline/countries/japan*.py) with the
Japan foundation's rules on (2026-10-07), in Fukuyama's shape (a city's own
full food list plus the months since) with Toyota's precedent for a city list
that leaves rows out by design.

Business leg: the city's own CC BY 4.0 lists (一宮市オープンデータ). Food: the
食品営業許可台帳 of permits in term on 2026-03-31, kept whole, plus the five
monthly lists of new permits, April to August 2026 (owner, call 126: merge
(a)). The city leaves out vending, vehicle, stall and temporary permits,
rows containing personal information and operators who asked not to be
listed: about two restaurants in three of e-Stat's count (owner, call 125:
Band A with the share stated). Personal services: the barber, beauty and
laundry 営業確認台帳 as of 2026-03-31, plus the 2026 monthly beauty and
laundry lists (call 128). MHLW's 食品衛生申請等システム open data adds two
things only (call 127, Matsuyama's precedent): its notifications (届出) as a
partial, opt-in food-retail layer, and its own point for a city row the block
join misses (POINT_DONORS). Its 129 permits are not added (call 127 (a)).
All placed by a JOIN to MLIT's 位置参照情報 (one municipality, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Meitetsu's Nagoya Main and Bisai lines and JR Central's Tokaido Line.
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "ichinomiya" / "raw"
DATA_PROCESSED = ROOT / "data" / "ichinomiya" / "processed"
OUTPUTS = ROOT / "outputs" / "ichinomiya"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Ichinomiya"
SLUG = "ichinomiya"
MUNICIPALITY = "一宮市"
PREFECTURE = "愛知県"

# The city's own CMS (no catalogue API). Every dataset page carries 「この作品
# は クリエイティブ・コモンズ 表示 4.0 国際 ライセンスの下に提供されています。」;
# the city's open-data terms (TERMS_PAGE, 2024-08-02) prescribe the credit
# for a modified work, 第3条(2)(イ). Read 2026-10-06 (licence-read, staging).
_HOST = "https://www.city.ichinomiya.aichi.jp"
_RES = _HOST + "/_res/projects/default_project/_page_/001/"
TERMS_PAGE = _HOST + "/opendata/1010817/1010820.html"
# 保健衛生課: 食品営業許可台帳（最新）, page ID 1040636.
FOOD_PAGE = _HOST + "/hokenjo/hoken-eisei/1044314/1039899/1040636.html"
# 保健予防課: 生活衛生関係営業確認（許可）台帳（2025年度）, page ID 1075449 (the
# lists as of 2026-03-31), and the current year's page, ID 1040689 (each
# month's new confirmations, posted only for a month that has some).
LIFE_PAGE = _HOST + "/hokenjo/hokenyobou/1044311/1039814/1075449.html"
LIFE_NOW_PAGE = _HOST + "/hokenjo/hokenyobou/1044311/1039814/1040689.html"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"

# The food months since the full list: (month, last day).
FOOD_MONTHS = (("04", "30"), ("05", "31"), ("06", "30"), ("07", "31"), ("08", "31"))
# The register months on the current page (2026-10-07): beauty April to
# August (May's file carries an "a"), laundry April; no barber month.
BEAUTY_MONTHS = {"04": "biyou_20260430.csv", "05": "biyou_20260531a.csv", "06": "biyou_20260630.csv",
                 "07": "biyou_20260731.csv", "08": "biyou_20260831.csv"}
LAUNDRY_MONTHS = {"04": "clerning_20260430.csv"}
# source key -> (file, URL, the page that carries its licence). One entry per
# file fetched; the food months and the register months are read inside
# source_rows.
SOURCE_FILES = {
    "food": ("232033_Food_Business_All_20260331.csv", _RES + "040/636/232033_Food_Business_All_20260331.csv",
             FOOD_PAGE),
    **{f"food_{m}": (f"232033_food_business_new_2026{m}01_2026{m}{d}.csv",
                     f"{_RES}040/636/232033_food_business_new_2026{m}01_2026{m}{d}.csv", FOOD_PAGE)
       for m, d in FOOD_MONTHS},
    "barber": ("2025riyouitiran.csv", _RES + "075/449/2025riyouitiran.csv", LIFE_PAGE),
    "beauty": ("2025biyoushoichirann.csv", _RES + "075/449/2025biyoushoichirann.csv", LIFE_PAGE),
    "laundry": ("2025clearningitiran.csv", _RES + "075/449/2025clearningitiran.csv", LIFE_PAGE),
    **{f"beauty_{m}": (f, _RES + "040/689/" + f, LIFE_NOW_PAGE) for m, f in BEAUTY_MONTHS.items()},
    **{f"laundry_{m}": (f, _RES + "040/689/" + f, LIFE_NOW_PAGE) for m, f in LAUNDRY_MONTHS.items()},
    "mhlw": ("23203_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=23203_food_business_all.csv",
             MHLW_TOP),
}
FOOD_MONTH_KEYS = tuple(f"food_{m}" for m, _ in FOOD_MONTHS)
REGISTER_MONTH_KEYS = {"barber": (), "beauty": tuple(f"beauty_{m}" for m in BEAUTY_MONTHS),
                       "laundry": tuple(f"laundry_{m}" for m in LAUNDRY_MONTHS)}
# Kyoto's rule: the date each list states, never the download's. The full
# list and the registers read 令和8年3月31日時点 / 2026年3月31日時点; each month
# file the month it names; MHLW's monthly file states none (its newest
# 許可年月日 2026-07-31, closures dated to 2026-08-28).
SOURCE_AS_OF = {"food": "2026-03-31", "barber": "2026-03-31", "beauty": "2026-03-31", "laundry": "2026-03-31",
                "mhlw": None,
                **{f"food_{m}": f"2026-{m}" for m, _ in FOOD_MONTHS},
                **{f"beauty_{m}": f"2026-{m}" for m in BEAUTY_MONTHS},
                **{f"laundry_{m}": f"2026-{m}" for m in LAUNDRY_MONTHS}}
FOOD_AS_OF = SOURCE_AS_OF["food"]
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. The full list is kept whole on
# its own date (call 126: no 許可満了日 before 2026-03-31, no 許可開始日 after
# it); the months against 2026-08-31, so a permit they list as starting later
# (to 2027-01-01) waits. MHLW's notifications carry no term.
TERM_AS_OF = {"food": "2026-03-31", "food_new": "2026-08-31", "mhlw": "2026-08-31"}

# What step 2 reads. "food_new" is the five monthly lists as one source of
# the same kind as the full list (japan_step2.kind, Matsuyama's two food
# lists): a renewal under a new number is the same premises, and one pin per
# premises and bucket shows it once. "mhlw" is the notifications only.
SOURCES = {"food": SOURCE_FILES["food"][0], "food_new": "the five monthly food lists",
           "mhlw": SOURCE_FILES["mhlw"][0], "barber": SOURCE_FILES["barber"][0],
           "beauty": SOURCE_FILES["beauty"][0], "laundry": SOURCE_FILES["laundry"][0]}
SOURCE_KIND = {"food_new": "food"}
# Declared, never inferred: every city file Shift-JIS (cp932) with CRLF but
# July's beauty file, an XLSX under a .csv name (file_rows); MHLW's UTF-8 with
# a BOM.
SOURCE_ENCODING = {**{k: "cp932" for k in SOURCE_FILES}, "beauty_07": "xlsx", "mhlw": "utf-8-sig"}
# The columns each file and source must carry; fetch_sources.py and step 2
# stop on a header without them. The operator columns (the food lists'
# 営業者名 and 代表者名, a sole trader's own name on about 1,370 of 2,815
# full-list rows; the registers' 申請者氏名 and 代表者氏名; MHLW's 法人名) are
# REQUIRED so the name rule (japan_register.name_is_operator; owner
# 2026-09-27) cannot silently compare nothing; read IN MEMORY by that rule
# only, never kept. Never selected: 営業者所在地, 営業者方書, 営業者電話番号,
# 代表者肩書, 営業所電話番号, 法人番号, 法人住所 and every phone.
_FOOD = ("営業所名称", "営業の種類", "業態", "営業所所在地", "営業者名", "代表者名", "許可番号", "許可開始日",
         "許可満了日")
_REG = ("施設名称", "施設住所", "申請者氏名", "代表者氏名")
# A month's file carries 代表者氏名 only where a row has one (June's two rows
# have none and the file has no such column).
_REG_MONTH = ("施設名称", "施設住所", "申請者氏名")
_MHLW = ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
         "廃業年月日", "法人名")
REQUIRED_COLUMNS = {
    "food": _FOOD, "food_new": _FOOD, **{k: _FOOD for k in FOOD_MONTH_KEYS},
    "barber": _REG, "beauty": _REG, "laundry": _REG,
    **{k: _REG_MONTH for ks in REGISTER_MONTH_KEYS.values() for k in ks},
    "mhlw": _MHLW, "mhlw_points": _MHLW,
}
# MHLW publishes an address only where the filer agreed to it.
ADDRESS_BY_CONSENT = {"mhlw"}
# MHLW's notification rows the block join misses take MHLW's own point (call
# 127 (c); the brief: a median 26 m from the block point, 95.3% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# A city food row the block join misses takes MHLW's point for the same
# premises (ward, town, trade name), read from the whole file under its own
# key, never drawn (call 127 (c), Matsuyama's and Toyama's mechanism; the
# brief matched 78 permits by number, the shared key matches by premises).
POINT_DONORS = {"food": "mhlw_points", "food_new": "mhlw_points"}
# A premises in both (a city permit and an MHLW notification of one bucket):
# MHLW's row stays (Matsuyama's).
SUPERSEDES = {"mhlw": ("food", "food_new")}


def source_csv(key):
    if key == "mhlw_points":
        key = "mhlw"
    return DATA_RAW / SOURCE_FILES[key][0]


def file_rows(key):
    """One fetched file's rows as it stands (japan_fetch's count and header
    check, and every read below). The July 2026 beauty file is an XLSX
    workbook served under a .csv name (biyou_20260731.csv, PK magic bytes), so
    a file is read by its bytes, never its extension; every other city file is
    a cp932 CSV."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    data = path.read_bytes()
    if data.startswith(b"PK\x03\x04"):
        return list(jr.xlsx_rows(data))
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
    "food" is the full list as it stands; "food_new" the five monthly lists
    in order; each register its 2026-03-31 list plus the 2026 months (new
    confirmations only; the city publishes no closures). "mhlw" yields only
    MHLW's notifications (申請区分 届出 / 届出(廃業)): its 129 permits are not
    added (call 127 (a)), being largely the rows the city leaves out on
    purpose. "mhlw_points" is the whole file, read by POINT_DONORS for its
    coordinates only."""
    if key == "food_new":
        for k in FOOD_MONTH_KEYS:
            yield from _rows(k)
        return
    if key in REGISTER_MONTH_KEYS:
        for k in (key, *REGISTER_MONTH_KEYS[key]):
            yield from _rows(k)
        return
    for r in _rows(key):
        if key == "mhlw" and not (r.get("申請区分") or "").startswith("届出"):
            continue
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 23203.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Ichinomiya.
# S, W, N, E: the city's N03 extent (S 35.250, W 136.705, N 35.370, E 136.877)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.24, 136.70, 35.38, 136.88)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (no macrons, lowercase after a hyphen for a
# common word, 前 as -mae). OSM's other 17 stand as they are (38 objects, all
# with name:en, 2026-10-07).
OSM_NAME_EN_OVERRIDES = {
    "妙興寺": "Myokoji",                              # Myōkōji
    "奥町": "Okucho",                                 # Okuchō
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the N03 centroid (~136.79) and the whole extent (136.705 to
# 136.877) fall in the 132 to 138 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median nearest-station gap is
# 935 m: standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 3 lines, no Shinkansen station): Meitetsu's Bisai Line keeps 10
# of 22 and Nagoya Main Line 8 of 60, JR Central's Tokaido Line 2 of 89 (a
# main line cut at the line, as Kurume's Kagoshima Line, not a stub). Every
# line is cut at the city line (owner 2026-09-24). 名鉄一宮 is one N02 group
# for both Meitetsu lines; 尾張一宮 (JR) beside it, 38 m away, is a group of
# its own and stays apart (trap 1). No frequency floor (owner, 2026-10-06,
# calls 46 and 86): the thinnest stretch, the Bisai Line to 玉ノ井, runs 38
# trains a weekday (Meitetsu's timetable, read 2026-10-06).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names follow the operators' signs
# with no macrons, as Sasebo's and Kitakyushu's.
_MT, _JR = "名古屋鉄道", "東海旅客鉄道"
LINES = {
    "NH": {"n02": [(_MT, "名古屋本線")], "name": "Meitetsu Nagoya Main Line", "name_ja": "名鉄名古屋本線",
           "short": "Meitetsu", "hue": "#E60012"},
    "BS": {"n02": [(_MT, "尾西線")], "name": "Meitetsu Bisai Line", "name_ja": "名鉄尾西線", "short": "Meitetsu",
           "hue": "#E60012"},
    "TK": {"n02": [(_JR, "東海道線")], "name": "JR Tokaido Line", "name_ja": "東海道線", "short": "JR",
           "hue": "#F77321"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# ichinomiya` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its operator's hue that reads 3:1 on both
# map pages and clears CIE76 45 from every pin. Meitetsu's one red splits into
# red (Nagoya Main Line) and red-orange (Bisai Line), 18.1 apart at 名鉄一宮,
# the closest pair (Toyota's same split); JR Central's orange darkens, 19.4
# from the Bisai Line. The dark-mode labels separate, 3 of 3.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "NH": line_registry.colour("meitetsu-nagoya-main-line"), "BS": "#F05030",
    "TK": line_registry.colour("jr-central-tokaido-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: Meitetsu's own station index (meitetsu.co.jp/train/station_info/,
# line01 and line10, read 2026-10-07) lists the Nagoya Main Line's 60
# stations, NH01 豊橋 to NH60 名鉄岐阜, and the Bisai Line's 22, 弥富 to BS24
# 玉ノ井 through 名鉄一宮 (NH50). Inside the city: NH48 島氏永 to NH55 木曽川堤
# (8) and BS08 玉野 to BS12 観音寺, 名鉄一宮, BS21 西一宮 to BS24 玉ノ井 (10).
GATE3 = {"source": "Meitetsu's station index (meitetsu.co.jp/train/station_info/): Nagoya Main Line NH48-NH55 "
                   "8 inside the city; Bisai Line BS08-BS12, NH50 and BS21-BS24, 10",
         "lines": {"NH": 8, "BS": 10}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
ICHINOMIYA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = ICHINOMIYA_BBOX
