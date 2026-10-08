"""Morioka-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/morioka.md
(14/14 checks, 2026-10-07). Japan's A/B batch (Regional-1), on the shared
modules (pipeline/countries/japan*.py) with the Japan foundation's rules on
(2026-10-07), in Akita's shape (one city food list of every permit in term on
its date, refreshed monthly, so nothing is rebuilt; MHLW's notifications
beside it) and Hamamatsu's for the registers (one file per kind).

Business leg: the city's own CC BY 4.0 CSVs (盛岡市保健所 生活衛生課). Food:
食品営業許可施設一覧, every permit in term on 2026-08-31, temporary permits
left out; the city also leaves out every entry whose operator asked not to be
listed (796 rows with no name and no address, the brief), counted apart and
never filled from another source. Personal services: the barber, beauty-salon
and laundry lists as of 2026-09-30. MHLW's 食品衛生申請等システム open data adds
its notifications (届出) only, as a partial, opt-in food-retail layer
(staging's precedent 127b of 2026-10-06), and its own point for a city row the
block join misses (127c, POINT_DONORS); its permits are the city's own (by
number, the brief) and are not added. All placed by a JOIN to MLIT's
位置参照情報 (one municipality, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR East's Tohoku, Tazawako, Yamada and Hanawa lines and the IGR Iwate
Galaxy Railway. English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "morioka" / "raw"
DATA_PROCESSED = ROOT / "data" / "morioka" / "processed"
OUTPUTS = ROOT / "outputs" / "morioka"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Morioka"
SLUG = "morioka"
MUNICIPALITY = "盛岡市"
PREFECTURE = "岩手県"

# The city's own CMS (no catalogue API; renewed 2026-10-01); every file a
# plain GET under /_res/projects/default_project/_page_/001/. Both pages offer
# their data under CC BY 4.0 (表示4.0国際) and point to the city's open-data
# site, whose 盛岡市オープンデータ利用規約 (terms PDF) binds on use. Read
# 2026-10-07 by staging (licence-read): a 出典 line and a separate processing
# line are required (§2(2)); the terms' example URL is dead since the
# renewal, so the credit cites the open-data index page; §3(2) and §4 are
# fault-based cost clauses (the class accepted for Japan, 2026-09-24). On the
# registers' page only the CSVs are open (「データの一部」); the build reads
# the CSVs only. The host sends no charset.
_HOST = "https://www.city.morioka.iwate.jp"
_RES = _HOST + "/_res/projects/default_project/_page_/001/"
OPENDATA_PAGE = _HOST + "/shisei/johokokai/opendata/index.html"
# 生活衛生課: 食品営業許可施設一覧, page 1006689 (更新日 2026-09-09).
FOOD_PAGE = _HOST + "/kenko_fukushi/hokenjo/shokuhineisei/1017014/1006689.html"
# 生活衛生課: 生活衛生営業施設等一覧, page 1034998 (更新日 2026-10-05).
LIFE_PAGE = _HOST + "/kenko_fukushi/hokenjo/shokuhineisei/seikatsueisei/1034998.html"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL of the edition this build read, the page that
# carries its licence). One entry per file fetched (Step 0, 2026-10-06, each
# HTTP 200 from its publisher's own host).
SOURCE_FILES = {
    "food": ("20260831.csv", _RES + "006/689/20260831.csv", FOOD_PAGE),
    "barber": ("032018_riyou_202609.csv", _RES + "034/998/R8/032018_riyou_202609.csv", LIFE_PAGE),
    "beauty": ("032018_biyou_202609.csv", _RES + "034/998/R8/032018_biyou_202609.csv", LIFE_PAGE),
    "laundry": ("032018_cleaning_202609.csv", _RES + "034/998/R8/032018_cleaning_202609.csv", LIFE_PAGE),
    "mhlw": ("03201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=03201_food_business_all.csv",
             MHLW_TOP),
}
# Every city file is RENAMED each month (the food list YYYYMMDD.csv, the
# registers _YYYYMM.csv under a year folder), so fetch_sources.py reads the
# current link from its page (Kawasaki's and Otsu's SOURCE_LINKS) and the
# pinned URL records which edition the build read.
SOURCE_LINKS = {
    "food": r"/006/689/\d{8}\.csv$",
    "barber": r"/032018_riyou_\d{6}\.csv$",
    "beauty": r"/032018_biyou_\d{6}\.csv$",
    "laundry": r"/032018_cleaning_\d{6}\.csv$",
}
# Kyoto's rule: the date each list states, never the download's. The food
# page's title reads 令和8年8月末時点, the registers' 令和8年9月末時点; MHLW's
# monthly file states none (its newest 許可年月日 2026-08-31).
FOOD_AS_OF = "2026-08-31"
REGISTERS_AS_OF = "2026-09-30"
SOURCE_AS_OF = {"food": FOOD_AS_OF, "barber": REGISTERS_AS_OF, "beauty": REGISTERS_AS_OF,
                "laundry": REGISTERS_AS_OF, "mhlw": None}
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. The food list keeps 18 permits
# past their 満了年月日 (2024-06 to 2026-08, all new-law, 6 of them withheld;
# the brief's open call 2), dropped; its newest 許可年月日 is 2026-08-28.
# MHLW's file covers August 2026 and its notifications carry no term.
TERM_AS_OF = {"food": FOOD_AS_OF, "mhlw": "2026-08-31"}

# What step 2 reads. "mhlw" is MHLW's notifications only (source_rows).
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: every file UTF-8 with a BOM, CRLF.
SOURCE_ENCODING = {k: "utf-8-sig" for k in SOURCE_FILES}
# The columns each file and source must carry; fetch_sources.py and step 2
# stop on a header without them. The operator columns (the food list's 営業者,
# filled on 3,550 rows, and 代表者, on 2,090: no company marker on 1,511 of
# the addressed rows, the shape of a sole trader's own name; the registers'
# 開設者名 and 営業者名; MHLW's 法人名) are REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; read IN MEMORY by that rule only, never kept. Never selected:
# 営業所電話番号, ビル名称, 施設電話番号, 法人番号, 法人住所 and every phone.
_MHLW = ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
         "廃業年月日", "法人名")
REQUIRED_COLUMNS = {
    "food": ("業種", "種目", "屋号商号", "営業所所在地", "営業者", "代表者", "許可年月日", "満了年月日", "許可番号"),
    "barber": ("業種", "施設名称", "開設者名", "施設所在地"),
    "beauty": ("業種", "施設名称", "開設者名", "所在地"),
    "laundry": ("種別", "施設名称", "営業者名", "所在地"),
    "mhlw": _MHLW,
    "mhlw_points": _MHLW,
}
# An address left out by consent is counted apart from "not a premises":
# MHLW publishes one only where the filer agreed (Fukuoka's), and the city's
# food list leaves out the entries whose operators asked not to be listed
# (the food page: 営業者が非公開を希望している情報; 796 rows, 18.2%, the
# brief). Neither is ever placed.
ADDRESS_BY_CONSENT = {"food", "mhlw"}
# MHLW's notification rows the block join misses take MHLW's own point
# (Akita's and Ōita's; the brief: a median 37 m from the block point, 89.4%
# within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# A city food row the block join misses takes MHLW's point for the same
# premises (ward, town, trade name), read from the whole file under its own
# key, never drawn (precedent 127c; Ōita's and Toyama's mechanism). With the
# join at about 0.2% unplaced it reaches few rows.
POINT_DONORS = {"food": "mhlw_points"}
# A premises in both (a city permit and an MHLW notification of one bucket):
# MHLW's row stays (Matsuyama's, Akita's and Ōita's).
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    if key == "mhlw_points":
        key = "mhlw"
    return DATA_RAW / SOURCE_FILES[key][0]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    Each city list as it stands. "mhlw" yields only MHLW's notifications
    (申請区分 届出 / 届出(廃業)): its open permits are the city's own new-law
    permits plus 435 temporary ones the city leaves out by design (the brief),
    so none is added. "mhlw_points" is the whole file, read by POINT_DONORS
    for its coordinates only."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        if key == "mhlw" and not (r.get("申請区分") or "").startswith("届出"):
            continue
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 03201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Morioka.
# S, W, N, E: the city's N03 extent (S 39.564, W 140.995, N 39.930,
# E 141.527; the 2006 merger brought in 玉山村) rounded out; step 1 stops if
# the city leaves it.
OSM_BBOX = (39.56, 140.99, 39.94, 141.53)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (no macrons, lowercase after a hyphen for a
# common word, a katakana loanword as its English word, 前 as -mae).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (~141.269) and the whole extent (140.995 to
# 141.527) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The median nearest-station gap is 2,074 m
# (1,496 to 4,680; the brief, re-measured at build on step 1's 11 stations),
# far over the spacing rule's halving line (about 550 m): standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 5 lines, the brief's table). Every line is cut at the city line
# (owner 2026-09-24): JR's Tohoku Line keeps 3 of 155 station records, the
# Tazawako Line 2 of 18, the Yamada Line 4 of 15, the Hanawa Line 1 of 27 and
# the IGR line 5 of 18. The Hanawa Line's one station, 好摩, is its junction
# with IGR, with 4.0 km of its own track inside: a JR one-station stub kept as
# cut by the standing call (Kobe's JR Takarazuka Line, Akita's Oga Line), not
# an urban line, so no owner question; 好摩 keeps its ring through IGR in any
# case. IGR leaves the city and comes back (巣子 and 滝沢 lie in 滝沢市), so the
# city line cuts it into two pieces, 盛岡-厨川 and 渋民-好摩, both drawn (the
# city line only). The Tohoku Shinkansen's 盛岡 record drops (owner
# 2026-09-24); the Akita Shinkansen runs over the Tazawako Line's track, filed
# as 田沢湖線 (class 11), and stops at 盛岡 only, so no station drops. No
# frequency floor (owner, 2026-10-06, calls 46 and 86): the Yamada Line runs
# 10 trains a weekday each way 盛岡-上米内 and 3 each way beyond, the Hanawa
# Line 7 down and 9 up (JR East's weekday timetables, read 2026-10-06 for the
# brief), both drawn and named on the page.
LEFT_OUT_LINES = {}
# 盛岡 is one N02 group for IGR and the Tohoku, Tazawako and Yamada lines
# (42 m), 好摩 for IGR and the Hanawa Line (0 m).
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), a starting hue for scripts/line_colour_search.py (`hue`) and the
# project's colour. Line names follow the operators' signs with no macrons and
# no "Main", as Fukushima's JR Tohoku Line and Akita's JR Ou Line (JR East's
# station timetable indexes); IGR signs its one line IGRいわて銀河鉄道線. Hues:
# JR East's green for the Tohoku Line (Fukushima's start), and starting points
# only for the rest, since the colours are the project's own.
_JR, _IGR = "東日本旅客鉄道", "アイジーアールいわて銀河鉄道"
LINES = {
    "IG": {"n02": [(_IGR, "いわて銀河鉄道線")], "name": "IGR Iwate Galaxy Railway Line",
           "name_ja": "IGRいわて銀河鉄道線", "short": "IGR", "hue": "#0072BC"},
    "TH": {"n02": [(_JR, "東北線")], "name": "JR Tohoku Line", "name_ja": "東北本線", "short": "JR",
           "hue": "#3CB371"},
    "TZ": {"n02": [(_JR, "田沢湖線")], "name": "JR Tazawako Line", "name_ja": "田沢湖線", "short": "JR",
           "hue": "#9B59B6"},
    "YM": {"n02": [(_JR, "山田線")], "name": "JR Yamada Line", "name_ja": "山田線", "short": "JR",
           "hue": "#F68B1E"},
    "HN": {"n02": [(_JR, "花輪線")], "name": "JR Hanawa Line", "name_ja": "花輪線", "short": "JR",
           "hue": "#E60033"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# morioka` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its starting hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. The Tohoku green, too near Food
# service's pin, darkens to olive and the Yamada orange is Akita's Ou orange
# (both Fukushima's colours); the IGR blue, which no blue clears Retail's pin
# in, goes to a lighter cyan. Closest pair within 500 m 62.5 (Tohoku,
# Yamada), anywhere 45.4 (Yamada, Hanawa, which meet nowhere); the dark-mode
# labels separate, 5 of 5.
_COLOURS = {"IG": "#08A0C0", "TH": "#586818", "TZ": "#9840A0", "YM": "#E07800", "HN": "#E80020"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: JR East's own station timetable pages (timetables.jreast.co.jp, the
# index list<code>.html of each station, read 2026-10-06 for the brief) list
# the Tohoku Line at 3 stations inside the city (盛岡, 仙北町, 岩手飯岡), the
# Tazawako Line at 2 (盛岡, 前潟), the Yamada Line at 4 (盛岡 to 上米内) and the
# Hanawa Line at 1 (好摩); IGR's station timetable page
# (www.igr.jp/timetable/station-timetable) lists 盛岡, 青山, 厨川, 渋民 and 好摩
# inside, with 巣子 and 滝沢 in 滝沢市 between them.
GATE3 = {"source": "JR East's station timetable pages (timetables.jreast.co.jp): Tohoku Line 3 inside the city, "
                   "Tazawako Line 2, Yamada Line 4, Hanawa Line 1; IGR's station timetable page "
                   "(www.igr.jp/timetable/station-timetable): 5 inside the city",
         "lines": {"TH": 3, "TZ": 2, "YM": 4, "HN": 1, "IG": 5}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
MORIOKA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = MORIOKA_BBOX
