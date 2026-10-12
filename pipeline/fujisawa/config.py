"""Fujisawa-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/fujisawa.md (18/18 checks, 2026-10-11). Fujisawa City
(藤沢市, 14205), one municipality with no wards, a city with its own health
center. Japan's A/B batch (East-2), on the shared modules
(pipeline/countries/japan*.py) with the Japan foundation's rules on, in
Yokosuka's shape (the same Kanagawa permit system: 業種 with 詳細業種 as the
form) with Ichinomiya's merge (a city's own full food list kept whole plus the
months since; owner, call 126).

Business leg: the city's own lists (藤沢市 健康医療部 生活衛生課, 藤沢市保健所),
CC BY 4.0 by the city's open-data terms. Food: the list of every permit held
on 2026-06-30, in two files (companies, and individual operators with no
operator column at all), kept whole, plus the monthly lists of July and
August 2026 (new and renewed permits; June's 72 are all in the full list by
number). The six permits MHLW marks closed in August 2026 are dropped (owner,
call 159). Personal services: the barber, beauty and laundry lists as of
2026-06-30. MHLW's 食品衛生申請等システム open data adds two things only (calls
127b and 127c, Ichinomiya's precedent): its notifications (届出) as a partial,
opt-in food-retail layer, and its own point where the block join misses. Its
permits are the city's own and are not read twice. All placed by a JOIN to
MLIT's 位置参照情報 (one municipality, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03): the Odakyu Enoshima Line (9 of 17), the Enoshima Electric Railway (6 of
15), JR East's Tokaido Line (2 of 46), the Shonan Monorail (2 of 8) and
Sotetsu's Izumino Line (1 of 8, its terminus). The Yokohama Municipal Subway's
Blue Line (1 of 17) is left out. English station names from OpenStreetMap's
name:en.
"""

import re
import unicodedata
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "fujisawa" / "raw"
DATA_PROCESSED = ROOT / "data" / "fujisawa" / "processed"
OUTPUTS = ROOT / "outputs" / "fujisawa"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Fujisawa"
SLUG = "fujisawa"
MUNICIPALITY = "藤沢市"
PREFECTURE = "神奈川県"

# The city's own CMS (no catalogue API; it sends no charset). Neither dataset
# page carries a licence line: the city's open-data library (page 13230) lists
# both pages, and its terms (riyoukiyaku20250401.pdf, section 3(2)) license the
# data CC BY 4.0, use counting as acceptance (the licence read of 2026-10-07).
_HOST = "https://www.city.fujisawa.kanagawa.jp"
# 食品衛生法に基づく営業許可施設情報, page 28905.
FOOD_PAGE = _HOST + "/seiei/shokuhineisei/opendatabase.html"
# 理容所・美容所・クリーニング所, page 32931.
LIFE_PAGE = _HOST + "/seiei/kankyouopendate.html"
LIBRARY_PAGE = _HOST + "/kyoso/shise/kekaku/kakushu/datalibrary.html"
TERMS_PDF = _HOST + "/documents/13230/riyoukiyaku20250401.pdf"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
_FOOD_FILES = _HOST + "/documents/28905/"
_LIFE_FILES = _HOST + "/documents/32931/"

# The food months since the full list. The page keeps the latest three months
# only and the full list is replaced each quarter; June's two files (72 rows)
# are all in the full list by permit number and are not read.
FOOD_MONTHS = ("07", "08")
_PARTS = ("houjin", "kojin")  # companies, individual operators
# source key -> (file, URL, the page that carries it). One entry per file
# fetched. EVERY FILE IS RENAMED EACH EDITION (zende-taYYYYMM..., the months'
# shokuhinYYYYMM..., the registers' upload timestamps), and the local name
# carries the edition, so each URL is pinned to the edition this build read;
# the brief's first two checks fail when the pages move on, and the next
# edition is a new set of names, dates and measurements here, never a silent
# re-fetch under an old name. The registers' names are timestamps, which no
# link pattern can tell from the page's monthly files (japan_fetch.current_url
# reads hrefs only).
SOURCE_FILES = {
    **{f"food_{p}": (f"zende-ta202606{p}.csv", f"{_FOOD_FILES}zende-ta202606{p}.csv", FOOD_PAGE) for p in _PARTS},
    **{f"food_{m}_{p}": (f"shokuhin2026{m}{p}.csv", f"{_FOOD_FILES}shokuhin2026{m}{p}.csv", FOOD_PAGE)
       for m in FOOD_MONTHS for p in _PARTS},
    "barber": ("20260713103834.csv", _LIFE_FILES + "20260713103834.csv", LIFE_PAGE),
    "beauty": ("20260713104008.csv", _LIFE_FILES + "20260713104008.csv", LIFE_PAGE),
    "laundry": ("20260713104127.csv", _LIFE_FILES + "20260713104127.csv", LIFE_PAGE),
    "mhlw": ("14205_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=14205_food_business_all.csv",
             MHLW_TOP),
}
FOOD_FULL_KEYS = tuple(f"food_{p}" for p in _PARTS)
FOOD_MONTH_KEYS = tuple(f"food_{m}_{p}" for m in FOOD_MONTHS for p in _PARTS)
# Kyoto's rule: the date each list states, never the download's. The full
# lists' and the registers' link text reads 2026年6月末現在; each month file the
# month it names (施行日 to 2026-07-31 and 2026-08-31); MHLW's file states none
# (its newest 許可年月日 2026-08-26, its six closures dated August 2026).
SOURCE_AS_OF = {**{k: "2026-06-30" for k in FOOD_FULL_KEYS}, "barber": "2026-06-30", "beauty": "2026-06-30",
                "laundry": "2026-06-30", "mhlw": None,
                **{f"food_{m}_{p}": f"2026-{m}" for m in FOOD_MONTHS for p in _PARTS}}
FOOD_AS_OF = "2026-06-30"
REGISTERS_AS_OF = "2026-06-30"
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. The city's food lists carry no
# term (施行日 is the grant date; no expiry column); MHLW's rows carry
# 許可満了日 and are read against the last day the months cover.
TERM_AS_OF = {"mhlw": "2026-08-31", "mhlw_points": "2026-08-31"}

# What step 2 reads. "food" is the full list's two files as one source;
# "food_new" the July and August lists as one source of the same kind
# (japan_step2.kind, Ichinomiya's): they carry renewals as well as new permits
# (the brief: 55 of 109 rows sit at a full-list premises under a new number),
# and one pin per premises and bucket shows a renewed premises once. "mhlw" is
# MHLW's notifications only.
SOURCES = {"food": "the full food list (companies and individual operators)",
           "food_new": "the July and August 2026 food lists", "mhlw": SOURCE_FILES["mhlw"][0],
           "barber": SOURCE_FILES["barber"][0], "beauty": SOURCE_FILES["beauty"][0],
           "laundry": SOURCE_FILES["laundry"][0]}
SOURCE_KIND = {"food_new": "food"}
# Declared, never inferred: every city file Shift-JIS (cp932) with no BOM (the
# food files LF, the registers CRLF); MHLW's UTF-8 with a BOM.
SOURCE_ENCODING = {**{k: "cp932" for k in SOURCE_FILES}, "mhlw": "utf-8-sig"}
# The columns each file and source must carry; fetch_sources.py and step 2
# stop on a header without them. The operator columns (the companies' food
# files' 申請者法人名 and 申請者名, a representative's own name; the registers'
# 申請者名 and 代表者名, filled for companies only; MHLW's 法人名) are REQUIRED
# so the name rule (japan_register.name_is_operator; owner 2026-09-27) cannot
# silently compare nothing; read IN MEMORY by that rule only, never kept. THE
# INDIVIDUAL OPERATORS' FOOD FILES CARRY NO OPERATOR COLUMN AT ALL (the city
# publishes a sole trader's trade name, address and phone only), so there the
# rule has only its sign test (version 2, a bare personal name). Never
# selected: 営業所電話番号1, 営業所電話番号, 法人番号, 法人住所 and every phone.
_FOOD_KOJIN = ("営業所名1", "営業所所在地1", "業種", "詳細業種", "許可番号", "施行日")
_FOOD_HOUJIN = (*_FOOD_KOJIN, "申請者法人名", "申請者名")
_REG = ("営業所名", "営業所所在地", "申請者名", "代表者名")
_MHLW = ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
         "廃業年月日", "法人名", "許可番号")
REQUIRED_COLUMNS = {
    # a source's first rows are the companies' file's
    "food": _FOOD_HOUJIN, "food_new": _FOOD_HOUJIN,
    **{k: (_FOOD_HOUJIN if k.endswith("houjin") else _FOOD_KOJIN) for k in (*FOOD_FULL_KEYS, *FOOD_MONTH_KEYS)},
    "barber": _REG, "beauty": _REG, "laundry": (*_REG, "種目"),
    "mhlw": _MHLW, "mhlw_points": _MHLW,
}
# MHLW publishes an address only where the filer agreed to it.
ADDRESS_BY_CONSENT = {"mhlw"}
# MHLW's notification rows the block join misses take MHLW's own point (call
# 127c; the brief: a median 39 m from the block point, 94.2% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# A city food row the block join misses takes MHLW's point for the same
# premises (ward, town, trade name), read from the whole file under its own
# key, never drawn (call 127c, Ichinomiya's and Toyama's mechanism).
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


def permit_number(s):
    """A permit number's digit groups: the city writes 第2026-123-4567, MHLW
    the same with 号 and, on 15 rows, a long-vowel mark or a dash of another
    kind between the groups."""
    return "-".join(re.findall(r"[0-9]+", unicodedata.normalize("NFKC", s or "")))


def mhlw_closed_numbers():
    """The permit numbers MHLW marks closed (申請区分 許可(廃業)): six, all
    closed in August 2026 and all in the city's June list (measured
    2026-10-11)."""
    return {permit_number(r.get("許可番号")) for r in _rows("mhlw")
            if (r.get("申請区分") or "").startswith("許可") and "廃業" in (r.get("申請区分") or "")} - {""}


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).

    "food" is the full list's two files, companies first, less the permits
    MHLW marks closed (owner, call 159: six known closures; only MHLW-filed
    premises can be filtered so, and the page keeps "may include closed
    premises"). "food_new" is the July and August lists in order. "laundry"
    passes its 種目 (取次, 一般, 無店舗) as the type as well: the register has
    no type column, and both japan_register's premises test and japan_eigyo
    read 無店舗 (a storeless pick-up, not a premises) from the type. "mhlw"
    yields only MHLW's notifications (申請区分 届出 / 届出(廃業)): its permits
    are the city's own (271 of 272 open permits match a city file by number;
    the other is the brief's open item). "mhlw_points" is the whole file, read
    by POINT_DONORS for its coordinates only."""
    if key == "food":
        from pipeline.baseline import emit

        closed, dropped = mhlw_closed_numbers(), 0
        for k in FOOD_FULL_KEYS:
            for r in _rows(k):
                if permit_number(r.get("許可番号")) in closed:
                    dropped += 1
                    continue
                yield r
        print(f"  closed by MHLW's record (call 159), dropped from the full list: {dropped} of {len(closed)}")
        emit("closed_by_mhlw_record", dropped)
        return
    if key == "food_new":
        for k in FOOD_MONTH_KEYS:
            yield from _rows(k)
        return
    for r in _rows(key):
        if key == "mhlw" and not (r.get("申請区分") or "").startswith("届出"):
            continue
        if key == "laundry":
            r = {**r, "種別": r.get("種目")}
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 14205.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Fujisawa: the
# Enoshima Electric Railway is a railway by law and by N02 class (12), and OSM
# tags its stops railway=station.
# S, W, N, E: the city's N03 extent (S 35.296, W 139.394, N 35.429, E 139.517)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.29, 139.39, 35.43, 139.52)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons). OSM's
# other 16 stand as they are (37 objects, 2026-10-11).
OSM_NAME_EN_OVERRIDES = {
    "辻堂": "Tsujido",  # Tsujidō
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (~139.459) and the whole extent (139.394 to
# 139.517) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-station gap is 690 m (17 stations), over the 550 m
# that halves them. Seven pairs sit under 600 m, all at the coast, and their
# rings overlap.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-11: 6 lines, 21 station records, 17 station groups; no Shinkansen).
# Odakyu's Enoshima Line keeps 9 of 17, the Enoshima Electric Railway 6 of 15,
# JR East's Tokaido Line 2 of 46 and the Shonan Monorail 2 of 8 (目白山下 and
# 湘南江の島, drawn cut: not a one-station stub), each cut at the city line
# (owner 2026-09-24). Sotetsu's Izumino Line keeps 1 of 8, its terminus 湘南台:
# a private line, so the stub stays as cut (the standing call, 2026-09-27; the
# band row, call 113). 湘南台 is one N02 group for Odakyu, Sotetsu and the Blue
# Line, 藤沢 one for Odakyu, JR and Enoden. The Enoshima Electric Railway is a
# railway (N02 class 12), the Monorail a suspended monorail (class 14): no tram
# or light rail. No frequency floor (owner, 2026-10-06, calls 46 and 86), and
# nothing here is near 11 trains a day: JR at 辻堂 runs 162 and 157 weekday
# departures, Enoden at 石上 76 each way (read 2026-10-06).
LEFT_OUT_LINES = {
    # An urban line cut to ONE station, whose place other lines serve (owner,
    # 2026-10-06, calls 54 and 92; the band row, call 113): 湘南台, 1 of 17,
    # the Blue Line's terminus, in the same N02 group as Odakyu's and Sotetsu's
    # 湘南台, which keep the ring.
    ("横浜市", "1号線"): "an urban line with one station inside, 湘南台, served by the Odakyu Enoshima Line and "
                      "the Sotetsu Izumino Line (owner 2026-10-06, calls 54 and 92)",
}
COLLAPSE_MAX_SPREAD_M = 300
# Two different stations 96 m apart (Enoden's 江ノ島 and the Monorail's
# 湘南江の島, separate N02 groups) read as "still platforms" to gate 1 at its
# default; the floor is set under that pair (Koshigaya's and Tama's
# precedent).
SPACING_MIN_M = 90

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the Enoden as 江ノ島電鉄線 and
# the Monorail as 江の島線; each is drawn under the name its operator signs.
# Line names without macrons.
_JR = "東日本旅客鉄道"
LINES = {
    "OE": {"n02": [("小田急電鉄", "江ノ島線")], "name": "Odakyu Enoshima Line", "name_ja": "江ノ島線",
           "short": "Odakyu", "hue": "#0D82C7"},
    "EN": {"n02": [("江ノ島電鉄", "江ノ島電鉄線")], "name": "Enoshima Electric Railway (Enoden)",
           "name_ja": "江ノ島電鉄線", "short": "Enoden", "hue": "#006A3A"},
    "JT": {"n02": [(_JR, "東海道線")], "name": "JR Tokaido Line", "name_ja": "東海道線", "short": "JR",
           "hue": "#F68B1E"},
    "SM": {"n02": [("湘南モノレール", "江の島線")], "name": "Shonan Monorail", "name_ja": "湘南モノレール",
           "short": "Monorail", "hue": "#E60012"},
    "SI": {"n02": [("相模鉄道", "相鉄いずみ野線")], "name": "Sotetsu Izumino Line", "name_ja": "相鉄いずみ野線",
           "short": "Sotetsu", "hue": "#004098"},
}
# Colours: scripts/line_colour_search.py's search with the shared lines held
# fixed (2026-10-11: >= 18 within 500 m, >= 12 from every Yokohama line and
# the registry's Odakyu and JR Yokosuka colours), each the feasible colour
# nearest its operator's hue that reads 3:1 on both map pages and clears CIE76
# 45 from every pin. Pins: Enoshima Line 72.3, Enoden 45.0, Tokaido Line 53.6,
# Monorail 58.1, Izumino Line 83.1. Closest pair within 500 m and anywhere:
# Enoshima Line / Enoden 39.4. The Enoshima Line's blue sits 24.0 from the
# Odakyu Odawara Line (which meets it at 相模大野, on Sagamihara's map) and 12.4
# from the Odakyu Tama Line (never beside it). Enoden's green is greyed to
# hold 45 from the green Personal-services pin. The dark-mode labels
# separate, 5 of 5.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own. The JR Tokaido Line
# reads the registry. The Sotetsu Izumino Line holds Yokohama's value
# (pipeline/yokohama/config.py, "SI") until the registry joins the two maps;
# the Odakyu Enoshima Line is new to the site and Sagamihara's map draws it
# too: both are registry entries to add, never values to change here alone.
_COLOURS = {
    "OE": line_registry.colour("odakyu-enoshima-line"), "EN": "#486860", "JT": line_registry.colour("jr-east-tokaido-line"), "SM": "#F01000",
    "SI": line_registry.colour("sotetsu-izumino-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: each operator's own stations inside the city line (the brief, read
# 2026-10-06 against the operators' station lists and timetables): Odakyu 9
# (湘南台 to 片瀬江ノ島), Enoden 6 (藤沢 to 江ノ島), JR East 2 (藤沢, 辻堂), the
# Shonan Monorail 2 (目白山下, 湘南江の島), Sotetsu 1 (湘南台).
GATE3 = {"source": "the operators' own station lists read against the city line (Odakyu, Enoshima Electric "
                   "Railway, JR East, Shonan Monorail, Sotetsu): Enoshima Line 9, Enoden 6, Tokaido Line 2, "
                   "Monorail 2, Izumino Line 1",
         "lines": {"OE": 9, "EN": 6, "JT": 2, "SM": 2, "SI": 1}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
FUJISAWA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = FUJISAWA_BBOX
