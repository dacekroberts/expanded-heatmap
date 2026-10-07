"""Fukushima-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/fukushima.md (18/18 checks, 2026-10-07). Japan's A/B batch
(Regional-1), on the shared modules (pipeline/countries/japan*.py) with the
Japan foundation's rules on (2026-10-07), in Fukuyama's shape (a city's own
full food list plus the months since) with Ichinomiya's answered merge (owner,
calls 125-128): the full list kept whole, the months added.

Business leg: all three buckets from the city's own CSVs on its
食品営業許可施設、生活衛生関係施設一覧 page (保健所衛生課, page 18472; CC BY 2.1 JP
by the city's open-data terms, page 1696). Food: the list of permits in term
on 2026-03-31 plus the five monthly lists of NEW permits, April to August
2026 (the months publish no renewals and the city publishes no closures, so
the food leg is an upper bound, disclosed as Kyoto's is). Personal services:
the barber, beauty-salon, laundry and coin-laundry lists as of 2026-03-31,
with the barber and beauty lists' monthly files of newly opened premises to
2026-08-31 (owner, call 210; Ichinomiya's call 128). All placed by a JOIN
to MLIT's 位置参照情報 (one municipality, no wards).
MHLW's file for 07201 was read at Step 0 as a control only (opt-in filing:
44 permits, every one already in the city's files); never a source here
(Iwaki's call 150 and Tsu's precedent: a thin notifications layer stays out).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Fukushima Kotsu's Iizaka Line, the Abukuma Express Line and JR East's
Tohoku and Ou lines. English station names from OpenStreetMap's name:en.
"""

import datetime
from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "fukushima" / "raw"
DATA_PROCESSED = ROOT / "data" / "fukushima" / "processed"
OUTPUTS = ROOT / "outputs" / "fukushima"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Fukushima"
SLUG = "fukushima"
MUNICIPALITY = "福島市"
PREFECTURE = "福島県"

# The city's 食品営業許可施設、生活衛生関係施設一覧 page (ページID 18472), linked from
# its open-data list (2312) through the 保健・医療・福祉 entry (2340). The page
# carries no licence line; the open-data list sends every user to the
# 福島市オープンデータ利用規約 (page 1696 and its PDF): CC BY 2.1 JP, read
# 2026-10-06 (staging; the uncapped section 4 reimbursement clause accepted by
# the owner, call 110).
HOST = "https://www.city.fukushima.fukushima.jp"
LIST_PAGE = HOST + "/soshiki/2/1005/1/1/5/1_1/index.html"
TERMS_PAGE = HOST + "/soshiki/2/1005/1/1/1696.html"
_FILES = HOST + "/material/files/group/7/"
# The monthly lists of new food permits since the full list's date: (month,
# the last day it covers).
MONTHS = (("04", "2026-04-30"), ("05", "2026-05-31"), ("06", "2026-06-30"), ("07", "2026-07-31"),
          ("08", "2026-08-31"))
_MONTH_KEYS = {f"food_{m}": f"r08{m}syokuhin.csv" for m, _ in MONTHS}
# The registers' monthly files of newly opened premises (令和8年N月の新規開設
# 理容所一覧 / 美容所一覧; owner, call 210, 2026-10-07): the page lists a file
# only for a month with an opening and says 新規事業者なし for the rest (barbers
# April to July, beauty salons August, laundries and coin laundries every
# month), so there is no laundry month file. Each holds openings only: the
# register's columns, every 検査確認年月日 inside its month, no closure column;
# the city publishes no closures. key -> (register, file, the last day it
# covers).
_REGISTER_MONTH_KEYS = {
    "barber_08": ("barber", "r0808riyou.csv", "2026-08-31"),
    **{f"beauty_{m}": ("beauty", f"r08{m}biyou.csv", end) for m, end in MONTHS[:4]},
}
REGISTER_MONTHS = {reg: tuple(k for k, (r, _, _) in _REGISTER_MONTH_KEYS.items() if r == reg)
                   for reg in ("barber", "beauty")}
# source key -> (file, URL, the page that lists it). One entry per file
# fetched (Step 0, 2026-10-06, and the register months 2026-10-07, each HTTP
# 200 from the city's own host).
SOURCE_FILES = {
    "food_list": ("r07nendomatsusyokuhin.csv", _FILES + "r07nendomatsusyokuhin.csv", LIST_PAGE),
    **{k: (name, _FILES + name, LIST_PAGE) for k, name in _MONTH_KEYS.items()},
    "barber": ("r07nendomatsuriyou.csv", _FILES + "r07nendomatsuriyou.csv", LIST_PAGE),
    "beauty": ("r07nendomatsubiyou.csv", _FILES + "r07nendomatsubiyou.csv", LIST_PAGE),
    "laundry": ("r07nendomatsucleaning.csv", _FILES + "r07nendomatsucleaning.csv", LIST_PAGE),
    "coinlaundry": ("r07nendomatsucoincleaning.csv", _FILES + "r07nendomatsucoincleaning.csv", LIST_PAGE),
    **{k: (name, _FILES + name, LIST_PAGE) for k, (_, name, _) in _REGISTER_MONTH_KEYS.items()},
}
# Kyoto's rule: the date each list states, never the download's. The full
# food list and the four registers read 令和8年3月31日現在; each month file
# names its month (令和8年N月の新規食品営業許可施設一覧, 令和8年N月の新規開設
# 理容所一覧 / 美容所一覧).
REGISTERS_AS_OF = "2026-03-31"
SOURCE_AS_OF = {"food_list": "2026-03-31", **{f"food_{m}": end for m, end in MONTHS},
                "barber": REGISTERS_AS_OF, "beauty": REGISTERS_AS_OF, "laundry": REGISTERS_AS_OF,
                "coinlaundry": REGISTERS_AS_OF, **{k: end for k, (_, _, end) in _REGISTER_MONTH_KEYS.items()}}
FOOD_AS_OF = "2026-03-31"
FOOD_NEW_TO = MONTHS[-1][1]

# What step 2 reads. The food leg is two sources, each read against its own
# file's date (calls 161 and 172): "food", the full list of permits in term
# on 2026-03-31, and "food_new", the five months' new permits, in term on
# 2026-08-31. One source rebuilt from all six files would read every permit
# against one date: 2026-03-31 holds back the 89 new permits as late
# starters, 2026-08-31 drops the 98 permits expiring in May and July that the
# months never republish (Fukuyama's method, merge (b), which the brief's open
# call 1 and Ichinomiya's answered call set aside). The 7 new permits at a
# premises already in the full list fold into one pin per premises.
SOURCES = {"food": SOURCE_FILES["food_list"][0], "food_new": "the five monthly new-permit lists",
           "barber": SOURCE_FILES["barber"][0], "beauty": SOURCE_FILES["beauty"][0],
           "laundry": SOURCE_FILES["laundry"][0], "coinlaundry": SOURCE_FILES["coinlaundry"][0]}
# The months' kind is the food list's (Tokyo's SOURCE_KIND); the registers'
# keys name their kind (coin laundries "coinlaundry", Sapporo's: Personal
# services, owner 2026-09-28).
SOURCE_KIND = {"food_new": "food"}
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. The full list holds no permit
# ending before 2026-03-31; the months' permits start in their own month.
TERM_AS_OF = {"food": "2026-03-31", "food_new": FOOD_NEW_TO}
# Declared, never inferred: UTF-8 with a BOM, CRLF, header on line 1, every
# file (the server sends no charset).
SOURCE_ENCODING = {k: "utf-8-sig" for k in SOURCE_FILES}

# The columns each raw file must carry (fetch_sources.py and source_rows stop
# on a header without them). The months spell four of them differently:
# 営業所屋号 for the trade name (all five), 種目又は業態 (April, May, August),
# 種目または業態 (June) and 種目 (July) for the form, 業種名 for the type
# (July), 営業者氏名漢字 for the operator (June). The operator's name is
# REQUIRED so the name rule (japan_register.name_is_operator; owner
# 2026-09-27) cannot silently compare nothing; read IN MEMORY by that rule
# only, never kept. Never selected: 営業者住所, 営業者電話番号 (the operator's own
# address and phone), 営業所電話番号.
_FOOD_LIST = ("営業所所在地", "営業所屋号名称", "業種", "種目", "許可始期", "許可終期", "営業者氏名")
_MONTH_COLUMNS = {
    "food_04": ("営業所所在地", "営業所屋号", "業種", "種目又は業態", "許可始期", "許可終期", "営業者氏名"),
    "food_05": ("営業所所在地", "営業所屋号", "業種", "種目又は業態", "許可始期", "許可終期", "営業者氏名"),
    "food_06": ("営業所所在地", "営業所屋号", "業種", "種目または業態", "許可始期", "許可終期", "営業者氏名漢字"),
    "food_07": ("営業所所在地", "営業所屋号", "業種名", "種目", "許可始期", "許可終期", "営業者氏名"),
    "food_08": ("営業所所在地", "営業所屋号", "業種", "種目又は業態", "許可始期", "許可終期", "営業者氏名"),
}
# The registers: 区分 (the laundry and coin lists' kind), 施設名称, 施設住所
# (from the town; 施設市町村名 is 福島市 on every row) and 開設者氏名, read in
# memory by the name rule. Never selected: 施設電話番号, 開設者都道府県名,
# 開設者市町村名, 開設者住所 and 開設者電話番号 (the operator's own address and
# phone), 検査確認済証. The register months carry the same header.
_REGISTER = ("施設名称", "施設住所", "施設市町村名", "開設者氏名")
# The rebuilt food rows (japan_register.rebuilt_register's premises columns):
# step 2 checks them against REQUIRED_COLUMNS["food"] and ["food_new"].
_REBUILT = ("所在地", "施設名称", "業種", "業態", "許可始期", "許可終期")
REQUIRED_COLUMNS = {
    "food_list": _FOOD_LIST,
    **_MONTH_COLUMNS,
    "food": _REBUILT,
    "food_new": _REBUILT,
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry": ("区分",) + _REGISTER,
    "coinlaundry": ("区分",) + _REGISTER,
    **{k: _REGISTER for k in _REGISTER_MONTH_KEYS},
}


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def _paths(keys):
    """The files behind one food source, each checked for its own columns
    before it is read."""
    from pipeline.countries import japan_register as jr

    paths = []
    for k in keys:
        p = source_csv(k)
        if not p.exists():
            raise SystemExit(f"missing {p}\nRun: python pipeline/{SLUG}/fetch_sources.py")
        head = next(iter(jr.city_rows(p)))
        missing = [c for c in REQUIRED_COLUMNS[k] if c not in head]
        if missing:
            raise SystemExit(f"{p.name}: header lacks {missing} - not the file the brief read")
        paths.append(p)
    return paths


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    "food" and "food_new" through japan_register.rebuilt_register (Kyoto's
    method, as of the full list's date, so every row of either is kept):
    where (address, trade name, type without （旧）) repeats, the permit ending
    latest wins (the brief's 44 full-list repeats under another number). Only
    premises columns are carried, plus the name rule's answer; no operator or
    contact column leaves the file. Each register as it stands, then its
    2026 month files in order (Ichinomiya's shape; openings only, so a
    premises that moved keeps its old row too: the registers are an upper
    bound, as the food leg is)."""
    from pipeline.countries import japan
    from pipeline.countries import japan_register as jr

    rules = japan.city_rules(SLUG)
    if key in ("food", "food_new"):
        keys = ["food_list"] if key == "food" else list(_MONTH_KEYS)
        return jr.rebuilt_register(_paths(keys), datetime.date.fromisoformat(FOOD_AS_OF), end_col="許可終期",
                                   granted_col="許可始期", rules=rules)
    return [r for p in _paths([key, *REGISTER_MONTHS.get(key, ())]) for r in jr.city_rows(p)]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 07201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Fukushima.
# S, W, N, E: the city's N03 extent (S 37.624, W 140.229, N 37.977,
# E 140.570; the 2008 merger brought in 飯野町) rounded out; step 1 stops if
# the city leaves it.
OSM_BBOX = (37.62, 140.22, 37.98, 140.58)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (no macrons, lowercase after a hyphen, a
# katakana loanword kept as its English word, 前 as -mae; Hakodate's
# Yunokawa-onsen for 温泉). OSM's other 19 stand: a place name after a hyphen
# keeps its capital (Higashi-Fukushima, Kami-Matsukawa), as Maebashi's
# Shin-Maebashi.
OSM_NAME_EN_OVERRIDES = {
    "美術館図書館前": "Bijutsukan-toshokan-mae",          # Bijutsukan-Toshokan-mae
    "飯坂温泉": "Iizaka-onsen",                           # Iizaka-Onsen
    "医王寺前": "Ioji-mae",                               # Iohji-mae
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (~140.389) and the whole extent (140.229 to
# 140.570) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median nearest-station gap is
# 886 m (332 to 4,142): standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25, reproduced 2026-10-07: 4 lines). Every line is cut at the city
# line (owner 2026-09-24): the Iizaka Line keeps 12 of 12, the Abukuma
# Express 5 of 24, JR's Tohoku Line 5 of 155 and Ou Line 3 of 105; no urban
# line is cut to a stub. The Tohoku Shinkansen is dropped (owner
# 2026-09-24); the Yamagata Shinkansen runs through on the Ou Line but stops
# at neither 笹木野 nor 庭坂, and N02 files that line as conventional (class
# 11). No frequency floor (owner, 2026-10-06, calls 46 and 86): the Ou Line
# from 福島 to 庭坂 runs about 11 trains a day each way (JR East's weekday
# timetables, read 2026-10-06), drawn and named on the page.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), a starting hue for scripts/line_colour_search.py (`hue`) and the
# project's colour. Line names follow the operators' signs with no macrons,
# as Sasebo's and Maebashi's: JR East's 福島 timetable index names the
# 東北本線 and 奥羽本線, Fukushima Kotsu its 飯坂線 (ii-den.jp). Hues: JR East's
# green for the Tohoku Line and orange for the Ou Line, the Abukuma Express's
# blue, a red for the Iizaka Line; starting points only, since the colours
# are the project's own.
_FK, _AB, _JR = "福島交通", "阿武隈急行", "東日本旅客鉄道"
LINES = {
    "II": {"n02": [(_FK, "飯坂線")], "name": "Iizaka Line", "name_ja": "飯坂線", "short": "Fukushima Kotsu",
           "hue": "#E60033"},
    "AB": {"n02": [(_AB, "阿武隈急行線")], "name": "Abukuma Express Line", "name_ja": "阿武隈急行線",
           "short": "Abukuma Express", "hue": "#0068B7"},
    "TH": {"n02": [(_JR, "東北線")], "name": "JR Tohoku Line", "name_ja": "東北本線", "short": "JR",
           "hue": "#3CB371"},
    "OU": {"n02": [(_JR, "奥羽線")], "name": "JR Ou Line", "name_ja": "奥羽本線", "short": "JR",
           "hue": "#F68B1E"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# fukushima` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its starting hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. The Abukuma blue, which no blue
# clears Retail's pin in, goes teal (Sasebo's and Maebashi's); the Tohoku
# green, too near Food service's pin, darkens to olive. Closest pair 45.4
# (Iizaka, Ou); the dark-mode labels separate, 4 of 4.
_COLOURS = {"II": "#E80020", "AB": "#007890", "TH": "#586818", "OU": "#E07800"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the Iizaka Line lies wholly inside the city. Fukushima Kotsu's
# timetable page (ii-den.jp/time/station.php?id=1, read 2026-10-07) lists its
# 12 stations, 福島 to 飯坂温泉, as N02 does.
GATE3 = {"source": "Fukushima Kotsu's Iizaka Line timetable page (ii-den.jp/time/station.php?id=1): 12 stations, "
                   "福島-飯坂温泉, all inside the city",
         "lines": {"II": 12}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
FUKUSHIMA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = FUKUSHIMA_BBOX
