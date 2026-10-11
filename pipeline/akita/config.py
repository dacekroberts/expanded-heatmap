"""Akita-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/akita.md
(13/13 checks, 2026-10-07). Japan's A/B batch (Regional-1), on the shared
modules (pipeline/countries/japan*.py) with the Japan foundation's rules on
(2026-10-07), in Fukuyama's shape (a complete city food list, MHLW beside it)
but simpler: the city's food list is ONE file of every permit in term on its
date, so nothing is rebuilt; Hamamatsu's for the registers (one file per kind).

Business leg: the city's own CC BY 4.0 XLSX files (秋田市保健所 衛生検査課).
Food: 食品営業許可施設一覧, every permit in term on 2026-10-01, refreshed
monthly. Personal services: the 理容所台帳 and 美容所台帳 as of 2026-08-31; the
city publishes no laundry list (a disclosed gap, owner 2026-10-06). MHLW's
食品衛生申請等システム open data adds its notifications (届出) only, as a
partial, opt-in food-retail layer (staging's precedent of 2026-10-06 naming
Akita: hundreds of rows, Matsuyama's and Ichinomiya's shape); its 245 permits
are about 5% of the city's and are not added. All placed by a JOIN to MLIT's
位置参照情報 (one municipality, no wards); where the block join misses an MHLW
row, MHLW's own point.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR East's Ou, Uetsu and Oga lines. English station names from
OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "akita" / "raw"
DATA_PROCESSED = ROOT / "data" / "akita" / "processed"
OUTPUTS = ROOT / "outputs" / "akita"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Akita"
SLUG = "akita"
MUNICIPALITY = "秋田市"
PREFECTURE = "秋田県"

# The city's own CMS (no catalogue API); every file a plain GET under
# /_res/projects/default_project/_page_/001/. Each dataset page carries 「この
# 作品 は クリエイティブ・コモンズ 表示 4.0 国際 ライセンスの下に提供されています。」
# (catalogue code op_cc_1); the city's 利用にあたって page adds nothing more
# restrictive. Read 2026-10-07 by staging (licence-read): no prescribed
# wording, no cost clause; the use-report request is not a condition.
_HOST = "https://www.city.akita.lg.jp"
_RES = _HOST + "/_res/projects/default_project/_page_/001/"
# 衛生検査課: 食品営業許可施設一覧, page 1017339 (更新日 2026-10-06).
FOOD_PAGE = _HOST + "/kurashi/kenko/1005368/1010019/1017339.html"
# 衛生検査課: 理容師法および美容師法に基づく営業施設一覧, page 1027245 (更新日
# 2026-09-08).
LIFE_PAGE = _HOST + "/kurashi/kenko/1005367/1012953/1027245.html"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL of the edition this build read, the page that
# carries its licence). One entry per file fetched (Step 0, 2026-10-06, each
# HTTP 200 from its publisher's own host).
SOURCE_FILES = {
    "food": ("r081001.xlsx", _RES + "017/339/r081001.xlsx", FOOD_PAGE),
    "barber": ("riyou260831_2.xlsx", _RES + "027/245/riyou260831_2.xlsx", LIFE_PAGE),
    "beauty": ("biyou260831_2.xlsx", _RES + "027/245/biyou260831_2.xlsx", LIFE_PAGE),
    "mhlw": ("05201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=05201_food_business_all.csv",
             MHLW_TOP),
}
# The food file is RENAMED each month (r081001 is R8-10-01), so
# fetch_sources.py reads the current link from the page (Kawasaki's and
# Otsu's SOURCE_LINKS) and the pinned URL records which edition the build read.
SOURCE_LINKS = {"food": r"/r\d{6}\.xlsx$"}
# Kyoto's rule: the date each list states, never the download's. The food
# file's title reads 令和8年10月1日現在, the registers' 令和８年８月３１日現在;
# MHLW's monthly file states none (its newest 許可年月日 2026-08-31).
FOOD_AS_OF = "2026-10-01"
REGISTERS_AS_OF = "2026-08-31"
SOURCE_AS_OF = {"food": FOOD_AS_OF, "barber": REGISTERS_AS_OF, "beauty": REGISTERS_AS_OF, "mhlw": None}
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. The food file holds every permit
# in term on its date (許可期間（開始） 2020-02-14 to 2026-10-01, 許可期間（満了）
# 2026-10-01 to 2033-09-30, the brief); MHLW's file covers August 2026 and
# its notifications carry no term.
TERM_AS_OF = {"food": FOOD_AS_OF, "mhlw": "2026-08-31"}

# What step 2 reads. "mhlw" is MHLW's notifications only (source_rows).
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: the city's three files XLSX (PK magic bytes, one
# sheet each), MHLW's UTF-8 with a BOM.
SOURCE_ENCODING = {"food": "xlsx", "barber": "xlsx", "beauty": "xlsx", "mhlw": "utf-8-sig"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns (the food list's 申請者名, with no
# company marker on 2,155 of 4,041 rows, the shape of a sole trader's own
# name; MHLW's 法人名) are REQUIRED so the name rule (japan_register.
# name_is_operator; owner 2026-09-27) cannot silently compare nothing; read IN
# MEMORY by that rule only, never kept. The registers carry no operator
# column at all: the name rule has only its version 2 sign test there
# (owner, 2026-10-06). Never selected: 営業所電話番号, 施設電話, 法人番号, 法人住所
# and every phone.
REQUIRED_COLUMNS = {
    "food": ("営業所名", "営業所住所", "申請者名", "指令番号", "業種名", "業態名", "許可期間（開始）",
             "許可期間（満了）"),
    "barber": ("施設名称", "施設所在地"),
    "beauty": ("施設名称", "施設所在地"),
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's).
ADDRESS_BY_CONSENT = {"mhlw"}
# MHLW's notification rows the block join misses take MHLW's own point
# (Ichinomiya's; the brief: a median 48 m from the block point, 97.4% within
# 250 m, 151 rows).
OWN_POINT_FALLBACK = {"mhlw"}
# A premises in both (a city permit and an MHLW notification of one bucket):
# MHLW's row stays (Matsuyama's and Ichinomiya's).
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    Each city file as it stands. "mhlw" yields only MHLW's notifications
    (申請区分 届出 / 届出(廃業)): its 245 permits hold about 5% of the city's
    and 203 of them repeat a city row (the brief), so they are not added."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        if key == "mhlw" and not (r.get("申請区分") or "").startswith("届出"):
            continue
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 05201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Akita.
# S, W, N, E: the city's N03 extent (S 39.449, W 140.005, N 39.865,
# E 140.516; the 2005 merger brought in 河辺町 and 雄和町) rounded out; step 1
# stops if the city leaves it.
OSM_BBOX = (39.44, 140.00, 39.87, 140.52)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (no macrons, lowercase after a hyphen for a
# common word, a katakana loanword as its English word, 前 as -mae). None is
# needed: OSM's 12 names stand as they are (28 objects, 26 with name:en,
# 2026-10-07; no macron, a place name after a hyphen capitalised as
# Fukushima's Kami-Matsukawa: Kami-Iijima, Ugo-Ushijima, Izumi-Sotoasahikawa).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (~140.232) and the whole extent (140.005 to
# 140.516) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median nearest-station gap is
# 3,093 m (2,308 to 4,956), far over the spacing rule's halving line (about
# 550 m): standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 3 lines, the brief's table). Every line is cut at the city line
# (owner 2026-09-24): JR's Ou Line keeps 10 of 105 station records (8
# stations), Uetsu Line 5 of 60 and Oga Line 1 of 9. The Oga Line's one
# station, 追分, is its legal junction with the Ou Line, 184 m inside the city
# line, with 0.92 km of its track inside: a JR one-station stub kept as cut by
# the standing call (Kobe's JR Takarazuka Line), not an urban line, so no
# owner question. The Akita Shinkansen runs over the Ou Line's track, which
# N02 files as 奥羽線 (class 11): it is not counted (owner 2026-09-24) and no
# station drops; 秋田 keeps its ring through the conventional lines. No
# frequency floor (owner, 2026-10-06, calls 46 and 86): the Uetsu Line at 桂根
# runs 3 trains a weekday toward 秋田 and 4 toward 酒田 (JR East's weekday
# timetables, recounted 2026-10-06), drawn and named on the page.
LEFT_OUT_LINES = {}
# 秋田 is one N02 group for the Ou and Uetsu lines (35 m), 追分 for the Ou and
# Oga lines (0 m), 泉外旭川's two Ou records 55 m apart.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), a starting hue for scripts/line_colour_search.py (`hue`) and the
# project's colour. Line names follow the operators' signs with no macrons and
# no "Main", as Fukushima's JR Ou Line (the same line, from JR East's 福島
# timetable index) and Fukuyama's JR Sanyo Line. Hues: JR East's line colours
# as starting points only, since the colours are the project's own.
_JR = "東日本旅客鉄道"
LINES = {
    "OU": {"n02": [(_JR, "奥羽線")], "name": "JR Ou Line", "name_ja": "奥羽本線", "short": "JR",
           "hue": "#F68B1E"},
    "UE": {"n02": [(_JR, "羽越線")], "name": "JR Uetsu Line", "name_ja": "羽越本線", "short": "JR",
           "hue": "#0068B7"},
    "OG": {"n02": [(_JR, "男鹿線")], "name": "JR Oga Line", "name_ja": "男鹿線", "short": "JR",
           "hue": "#3CB371"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# akita` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each the
# feasible colour nearest its starting hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. The Ou Line's orange is Fukushima's
# (the same line); the Uetsu blue, which no blue clears Retail's pin in, goes
# teal (Sasebo's and Maebashi's); the Oga green, too near Food service's pin,
# darkens to olive. Closest pair 61.6 (Uetsu, Oga); the dark-mode labels
# separate, 3 of 3.
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search: the Oga
# Line's olive #586818 sat 15.8 from it, under the owner's floor of 20
# (2026-10-07). It takes #007430, a dark green: the colour nearest JR East's
# #3CB371 that reads 3:1 on both pages and clears 25 from every pin (25.2
# from the green pin, 38.0 from olive, between 20 and 45: an accepted trade).
# The JR East green on Fukushima's, Morioka's and Mito's maps is the same.
# Closest pair now 56.3 (Uetsu, Oga).
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "OU": line_registry.colour("jr-east-ou-line"), "UE": "#007890", "OG": "#007430",
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: JR East's own station timetable pages (timetables.jreast.co.jp, the
# index list<code>.html for each of the 12 station groups, recounted
# 2026-10-06 for the brief) list the Ou Line at 8 stations inside the city
# (大張野 to 追分), the Uetsu Line at 5 (秋田 to 下浜) and the Oga Line at 1
# (追分).
GATE3 = {"source": "JR East's station timetable pages (timetables.jreast.co.jp): Ou Line 8 inside the city, "
                   "Uetsu Line 5, Oga Line 1",
         "lines": {"OU": 8, "UE": 5, "OG": 1}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
AKITA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = AKITA_BBOX
