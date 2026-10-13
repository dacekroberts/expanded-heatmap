"""Okazaki-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/okazaki.md (6/6 checks, 2026-10-11). Part of the A/B build
plan's Regional-2 batch, on the shared modules (pipeline/countries/japan*.py)
with every shared rule on. Food only (Band B, owner 2026-10-06: Hiroshima's
page shape): the city publishes no barber, beauty-salon or laundry list.

Business leg: the city's own 食品等営業許可・届出一覧 on BODIK (organization
232025, author 岡崎市保健部生活衛生課, CC BY 4.0 under the city's open-data
terms): every food permit in term on 2026-08-31, one CSV in the national
自治体標準 schema, replaced in place. About four restaurant permits in five of
e-Stat's count (the share is stated on the page; Ichinomiya's precedent).
MHLW's 食品衛生申請等システム open data adds two things only (Ichinomiya's and
Matsuyama's precedent): its notifications (届出) as a partial, opt-in
food-retail layer, and its own point for a city row the block join misses
(POINT_DONORS). Its permits are not added (123 of 126 are in the city's list
by number and date). All placed by a JOIN to MLIT's 位置参照情報 (one
municipality, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Meitetsu's Nagoya Main Line, the Aichi Loop Line and JR Central's
Tokaido Line. English station names from OpenStreetMap's name:en.
"""

import re
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "okazaki" / "raw"
DATA_PROCESSED = ROOT / "data" / "okazaki" / "processed"
OUTPUTS = ROOT / "outputs" / "okazaki"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Okazaki"
SLUG = "okazaki"
MUNICIPALITY = "岡崎市"
PREFECTURE = "愛知県"

# The city's one food dataset on BODIK (package 232025_food_business_all,
# license_id cc-by-40-intl, metadata modified 2026-09-11; package_show read
# 2026-10-11), under 岡崎市オープンデータ利用規約 (in force 2015-12-01): CC BY
# 4.0 with a prescribed credit for a modified work, 4(2). Read 2026-10-07
# (licence-read, recorded by staging; clause 5(5) accepted by the owner, call
# 214). BODIK serves the file as 232025_food_business_al.csv, the city's own
# truncation; it is kept under its full name.
BODIK = "https://data.bodik.jp/dataset"
FOOD_PAGE = BODIK + "/232025_food_business_all"
TERMS = "https://odcs.bodik.jp/232025/tos/"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL, the page that carries its licence). One entry per
# file fetched (Step 0, 2026-10-06, each HTTP 200 from its publisher's host).
SOURCE_FILES = {
    "food": ("232025_food_business_all.csv",
             BODIK + "/aabced9d-d86e-422d-8ad0-2781d0f30671/resource/a893c7d6-5c10-4fb4-b9fa-cb48edd81565"
                     "/download/232025_food_business_al.csv", FOOD_PAGE),
    "mhlw": ("23202_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=23202_food_business_all.csv",
             MHLW_TOP),
}
# Kyoto's rule: the last day each list covers, never the download's. The
# city's file states no date; its newest 許可年月日 is 2026-08-31 and no
# 許可満了日 falls before that day (the resource was modified 2026-09-11).
# MHLW's monthly file states none.
FOOD_AS_OF = "2026-08-31"
SOURCE_AS_OF = {"food": FOOD_AS_OF, "mhlw": None}
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. 29 city permits begin on
# 2026-09-01, after the as-of, and wait; 28 end on it and are in term.
# MHLW's notifications carry no term (its key is required because the file
# has the term columns).
TERM_AS_OF = {"food": FOOD_AS_OF, "mhlw": FOOD_AS_OF}

# What step 2 reads. "mhlw" is the notifications only (source_rows).
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: both files UTF-8 with a BOM and CRLF, the header
# on line 1.
SOURCE_ENCODING = {"food": "utf-8-sig", "mhlw": "utf-8-sig"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 法人名 (the city's: filled on 2,121 of 4,022 rows, every
# one with a company or cooperative marker, blank for the rest; MHLW's: a sole
# trader's own name as often as a company's) is REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; read IN MEMORY by that rule only, never kept. 許可条件 is required
# because it alone marks the city's 210 vehicle permits (the shared
# kyoka_joken rule). Never selected: 施設電話番号, 施設名称_カナ, 法人番号, 法人住所
# and every phone.
REQUIRED_COLUMNS = {
    "food": ("施設名称", "営業の種類", "所在地_連結表記", "法人名", "許可番号", "許可年月日", "許可満了日",
             "許可条件"),
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
REQUIRED_COLUMNS["mhlw_points"] = REQUIRED_COLUMNS["mhlw"]
# MHLW publishes an address only where the filer agreed to it.
ADDRESS_BY_CONSENT = {"mhlw"}
# MHLW's notification rows the block join misses take MHLW's own point (the
# brief: a median 47 m from the block point, 93.4% within 250 m, over 379
# addressed rows at the block).
OWN_POINT_FALLBACK = {"mhlw"}
# A city food row the block join misses takes MHLW's point for the same
# premises (town, trade name), read from the whole file under its own key,
# never drawn (Ichinomiya's, Matsuyama's and Toyama's mechanism). The owner's
# calls 178 and 179 (2026-10-06) rest on it: the permits at 舞木町字金森 and in
# the new towns south of JR 岡崎 take MHLW's point where they have a twin.
POINT_DONORS = {"food": "mhlw_points"}
# A premises in both (a city permit and an MHLW notification of one bucket):
# MHLW's row stays (Matsuyama's).
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    if key == "mhlw_points":
        key = "mhlw"
    return DATA_RAW / SOURCE_FILES[key][0]


# The city's file writes U+B743, a Hangul code point, where its system could
# not encode a place-name character: 20 addresses at 戸崎町字<U+B743>山 (and 2
# trade names, left as published). MLIT's block file and MHLW's own rows write
# the place 戸崎町字ばら山, so the code point is read as ばら in that address
# only (the brief's O2: 17 rows leave the district tier and 3 the unplaced for
# a block). City-local, as Gifu's date rewrite in its own source_rows; a
# shared-code finding for review time (japan.CITIES' "gaiji" translates trade
# names too, which this does not).
_BARA = re.compile("(戸崎町字?)띃(山)")


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    "food" is the city's list as it stands, its address column's stand-in
    code point read as ばら (_BARA). "mhlw" yields only MHLW's notifications
    (申請区分 届出 / 届出(廃業)): its 126 permits are not added, 123 of them
    being in the city's list by number and date (Ichinomiya's call 127 (a)).
    "mhlw_points" is the whole file, read by POINT_DONORS for its coordinates
    only."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        if key == "mhlw" and not (r.get("申請区分") or "").startswith("届出"):
            continue
        if key == "food" and r.get("所在地_連結表記"):
            r["所在地_連結表記"] = _BARA.sub(r"\1ばら\2", r["所在地_連結表記"])
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 23202.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Okazaki.
# S, W, N, E: the city's N03 extent (S 34.860, W 137.103, N 35.042, E 137.421;
# 額田町 merged 2006) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.85, 137.10, 35.05, 137.43)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style as Toyota's config applies it (no macrons,
# 前 as -mae, lowercase after a hyphen for a common word, a hyphen between a
# Meitetsu prefix and its place as Mikawa-Yatsuhashi). OSM's other 13 stand
# as they are (24 objects, all with name:en, 2026-10-11); Kitanomasuzuka is
# kept as OSM writes it.
OSM_NAME_EN_OVERRIDES = {
    "岡崎公園前": "Okazaki-koen-mae",                  # Okazakikōen-mae
    "宇頭": "Uto",                                     # Utō
    "名電山中": "Meiden-Yamanaka",                      # Meiden Yamanaka
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the N03 centroid (137.258) and the whole extent (137.103 to
# 137.421) fall in the 132 to 138 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings on the spacing rule
# (docs/ring_rules.md): the brief's median nearest-station gap is 1,741 m,
# far above the ~550 m halving threshold. Re-measure if the drawn stations
# change.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25: 3 lines, no Shinkansen station). Every line is cut at the city
# line (owner 2026-09-24): Meitetsu's Nagoya Main Line keeps 9 of 60 station
# records, the Aichi Loop Line 6 of 23, JR Central's Tokaido Line 2 of 89 (a
# main line crossing the city, as Ichinomiya's, not a stub). 岡崎 is one N02
# group for JR and the Aichi Loop (0 m). 中岡崎 (Aichi Loop) and 岡崎公園前
# (Meitetsu), 168 m apart, are separate groups of different names and stay
# apart (trap 1; Ichinomiya's 名鉄一宮 / 尾張一宮). No frequency floor (owner,
# 2026-10-06, calls 46 and 86), and no stretch is near 11 trains a day: the
# Aichi Loop runs 3 to 4 an hour each way (its station timetables, edition
# UD260314), Meitetsu's locals about 2 an hour east of 東岡崎 (the brief).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names as the other maps write them
# (Ichinomiya's and Gifu's Meitetsu Nagoya Main Line and JR Tokaido Line,
# Toyota's Aichi Loop Line), with no macrons.
_MT, _AK, _JR = "名古屋鉄道", "愛知環状鉄道", "東海旅客鉄道"
LINES = {
    "NH": {"n02": [(_MT, "名古屋本線")], "name": "Meitetsu Nagoya Main Line", "name_ja": "名鉄名古屋本線",
           "short": "Meitetsu", "hue": "#E60012"},
    "AK": {"n02": [(_AK, "愛知環状鉄道線")], "name": "Aichi Loop Line", "name_ja": "愛知環状鉄道線",
           "short": "Aichi Loop", "hue": "#00A040"},
    "TK": {"n02": [(_JR, "東海道線")], "name": "JR Tokaido Line", "name_ja": "東海道線", "short": "JR",
           "hue": "#F77321"},
}
# Colours: one colour per line on every map (owner, 2026-10-07). All three
# lines take theirs from pipeline/line_registry.py; the Aichi Loop Line's
# entry, at the colour Toyota's map already drew (#28A800), was added with
# this build (2026-10-11).
_COLOURS = {
    "NH": line_registry.colour("meitetsu-nagoya-main-line"),
    "AK": line_registry.colour("aichi-loop-railway-aichi-loop-line"),
    "TK": line_registry.colour("jr-central-tokaido-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station lists (read 2026-10-11). Meitetsu's
# Nagoya Main Line page (meitetsu.co.jp/train/station_info/line01/) lists, in
# line order, 名電長沢, then 本宿, 名電山中, 藤川, 美合, 男川, 東岡崎, 岡崎公園前,
# 矢作橋 and 宇頭 (9), then 新安城. The Aichi Loop Railway's station index
# (aikanrailway.co.jp/station/) lists 岡崎, 六名, 中岡崎, 北岡崎, 大門 and 北野桝塚
# (6), then 三河上郷, Toyota's first. JR Central's two (西岡崎, 岡崎) are not
# gated: its timetable was not read.
GATE3 = {"source": "Meitetsu's Nagoya Main Line station list (meitetsu.co.jp/train/station_info/line01/): "
                   "本宿 to 宇頭, 9 inside the city; the Aichi Loop Railway's station index "
                   "(aikanrailway.co.jp/station/): 岡崎 to 北野桝塚, 6",
         "lines": {"NH": 9, "AK": 6}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
OKAZAKI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = OKAZAKI_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3604548232)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
PLACE_DROPPED = {}
