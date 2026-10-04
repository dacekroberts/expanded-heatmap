"""Takamatsu-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/takamatsu.md
(14/14 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py), in Matsuyama's shape: the city's own lists,
all three buckets, with MHLW's notifications as partial food retail.

Business leg: the city's CC BY 4.0 lists on オープンデータたかまつ (保健所
生活衛生課): every food permit in force at 2026-08-31 and the standing barber,
beauty-salon and laundry registers of 2026-08, plus MHLW's 食品衛生申請等システム
open data for its NOTIFICATIONS only (届出: konbini, supermarkets and other
food retail that notify rather than hold a permit; opt-in, so partial). The
city's list holds every permit (102% of the official restaurant count), so
MHLW's permits add nothing and are not read. All placed by a JOIN to MLIT's
位置参照情報 for the one municipality (no wards); where the block join misses
an MHLW row, MHLW's own point (OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03). Kotoden's Kotohira, Nagao and Shido Lines and JR Shikoku's Yosan
and Kotoku Lines; no Shinkansen; the Yakuri Cable (a sightseeing funicular)
left out. English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "takamatsu" / "raw"
DATA_PROCESSED = ROOT / "data" / "takamatsu" / "processed"
OUTPUTS = ROOT / "outputs" / "takamatsu"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Takamatsu"
SLUG = "takamatsu"
MUNICIPALITY = "高松市"
PREFECTURE = "香川県"

# オープンデータたかまつ: the files are served from opendata.takamatsu-fact.com
# (generated from the city's repository, github.com/takamatsu-city/opendata),
# catalogued on the city's CKAN (every dataset license_id cc-by) under the
# 高松市オープンデータ利用規約 (odp/tos/) 第１条, CC BY 4.0 International (read
# 2026-10-02). Fetched from opendata.takamatsu-fact.com only.
HOST = "https://opendata.takamatsu-fact.com"
CKAN = "https://opendata.smartcity-takamatsu.jp/ckan/dataset"
ODP = "https://opendata.smartcity-takamatsu.jp/odp/"
TERMS = ODP + "tos/"
# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2;
# read 2026-09-24 for Fukuoka). A plain GET. Credit links the top page only.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL, the dataset page that carries its licence). The
# registers are titled 新規開設一覧 but are standing registers (開設確認日 from
# 1948 to 2026-08, and their counts match the official year-end count).
SOURCE_FILES = {
    "food": ("licensed_food_business_facility_list.csv", f"{HOST}/licensed_food_business_facility_list/data.csv",
             f"{CKAN}/licensed_food_business_facility_list"),
    "barber": ("new_barber_shops.csv", f"{HOST}/new_barber_shops/data.csv", f"{CKAN}/new_barber_shops"),
    "beauty": ("new_beauty_salons.csv", f"{HOST}/new_beauty_salons/data.csv", f"{CKAN}/new_beauty_salons"),
    "laundry": ("new_cleanings.csv", f"{HOST}/new_cleanings/data.csv", f"{CKAN}/new_cleanings"),
    "mhlw": ("37201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=37201_food_business_all.csv",
             MHLW_TOP),
}
# The dates the lists state (Kyoto's rule, never the download's): the food
# list's source workbook 食品関係事業者一覧（2026.8.31時点）; the registers'
# 0100_202608 / 0101_202608 / 0102_202608, read as the month's last day. Every
# food permit is in term on 2026-08-31 (the earliest 許可終了日 is that day),
# so nothing is dropped. MHLW's monthly file states none (its newest permit
# 2026-08-24).
SOURCE_AS_OF = {"food": "2026-08-31", "barber": "2026-08-31", "beauty": "2026-08-31", "laundry": "2026-08-31",
                "mhlw": None}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: all five UTF-8 comma CSV, header on line 1 (MHLW's
# with a BOM).
SOURCE_ENCODING = {"food": "utf-8", "barber": "utf-8", "beauty": "utf-8", "laundry": "utf-8",
                   "mhlw": "utf-8-sig"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 業態 is the food list's form of business, read beside
# the type (japan_eigyo.FORM_RULES). The operator columns (the food list's
# 営業者名; the registers' 開設者申請者名 and 開設者代表者名, the laundry
# file's 営業者申請者名 and 営業者代表者名) are REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; they are read IN MEMORY by that rule only, never kept. Never
# selected: the operator's own address (開設者 / 営業者 都道府県名称, 住所１,
# 住所２), 営業者名かな, 役職名, every phone, and MHLW's 法人名 / 法人番号 /
# 法人住所.
REQUIRED_COLUMNS = {
    "food": ("施設名称１", "施設所在地１", "業種", "業態", "営業者名", "許可終了日"),
    "barber": ("業務種別", "施設名称１", "施設所在地１", "開設者申請者名", "開設者代表者名"),
    "beauty": ("業務種別", "施設名称１", "施設所在地１", "開設者申請者名", "開設者代表者名"),
    "laundry": ("業務種別", "施設名称１", "施設所在地１", "営業者申請者名", "営業者代表者名"),
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日"),
}
# MHLW publishes an address only where the filer agreed to it.
ADDRESS_BY_CONSENT = {"mhlw"}
# MHLW's notification rows the block join misses take MHLW's own point (the
# brief's check: a median 46 m from the block point, 91.4% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# A premises in both (a konbini holding a city restaurant permit and filing an
# MHLW notification, in the same bucket): MHLW's row stays (Matsuyama's).
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    MHLW's file yields only its notifications (申請区分 届出 / 届出(廃業)): the
    city's own list holds every permit (5,558 restaurants, 102% of the
    official count), so MHLW adds no permit (the brief; Matsuyama's shape).
    Every other file as it is."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        if key == "mhlw" and not (r.get("申請区分") or "").startswith("届出"):
            continue
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 37201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. Kotoden's lines are railways
# (N02 class 12), not trams.
# S, W, N, E: the city's N03 extent (S 34.111, W 133.920, N 34.434, E 134.176)
# rounded out; step 1 stops if the city leaves it. The box the OSM query used
# (2026-10-03).
OSM_BBOX = (34.1, 133.91, 34.45, 134.19)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
# OSM has no object at all for five of the Nagao Line's stations (2026-10-03
# file): their names are romanised from the readings Kotoden's own station
# index gives (kotoden.co.jp/publichtm/kotoden/station/, read 2026-10-03), in
# Hiroshima's style.
OSM_NAME_EN_MISSING = {
    "花園": "Hanazono",                # はなぞの
    "林道": "Hayashimichi",            # はやしみち
    "木太東口": "Kitahigashiguchi",    # きたひがしぐち
    "西前田": "Nishi-Maeda",           # にしまえだ
    "高田": "Takata",                  # たかた
}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style as Kitakyushu's config describes (no
# macrons, 前 as -mae, lowercase after a hyphen, 丁目 numbers as figures).
OSM_NAME_EN_OVERRIDES = {
    "松島二丁目": "Matsushima-2-Chome",            # Matsushima-Nichome
    "栗林公園": "Ritsurin-koen",                   # Ritsurin-Koen
    "栗林公園北口": "Ritsurin-koen-kitaguchi",      # Ritsurinkōen Kitaguchi
    "香西": "Kozai",                               # Kōzai
    "琴電屋島": "Kotoden-Yashima",                  # Kotodenyashima (OSM's 琴電志度: Kotoden-Shido)
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~134.05) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median gap to the nearest station
# is 703 m: standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25:
# 6 lines, no Shinkansen). Kotoden's Kotohira Line keeps 12 of 23, its Nagao
# Line 8 of 16 and its Shido Line 15 of 16; JR's Yosan Line 5 of 95 and
# Kotoku Line 9 of 29; each cut at the city line (owner 2026-09-24). No line
# is cut to a stub. The Yakuri Cable is a sightseeing funicular, left out by
# the standing rule (Kobe's Maya and Rokko, owner 2026-09-27); its stations
# are never written to excluded_stations.csv, and the page says so.
# Kotoden's 八栗新道 and JR's 讃岐牟礼, 61 m apart, are separate N02 groups of
# different names and stay apart (trap 1); 瓦町's three Kotoden platforms
# collapse within 130 m.
LEFT_OUT_LINES = {
    ("四国ケーブル", "八栗ケーブル"): "a sightseeing funicular (Kobe's rule)",
}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour.
#
# The Nagao Line runs through to 高松築港 over the Kotohira Line's track
# (片原町, 高松築港; Kotoden numbers them K00/N00 and K01/N01), while N02
# files the legal line from 瓦町: drawn as its N02 line plus a `route` over
# 琴平線 from 高松築港 to 瓦町 (Tokyo's Fukutoshin Line has both).
_KT, _JR = "高松琴平電気鉄道", "四国旅客鉄道"
LINES = {
    "KT": {"n02": [(_KT, "琴平線")], "name": "Kotoden Kotohira Line", "name_ja": "琴平線", "short": "Kotoden",
           "hue": "#FFD400"},
    "KN": {"n02": [(_KT, "長尾線")], "route": [(_KT, "琴平線", ["高松築港", "片原町", "瓦町"])],
           "name": "Kotoden Nagao Line", "name_ja": "長尾線", "short": "Kotoden", "hue": "#00A04B"},
    "KS": {"n02": [(_KT, "志度線")], "name": "Kotoden Shido Line", "name_ja": "志度線", "short": "Kotoden",
           "hue": "#E2007E"},
    "JY": {"n02": [(_JR, "予讃線")], "name": "JR Yosan Line", "name_ja": "予讃線", "short": "JR",
           "hue": "#0072BC"},
    "JK": {"n02": [(_JR, "高徳線")], "name": "JR Kotoku Line", "name_ja": "高徳線", "short": "JR",
           "hue": "#8F5FA7"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# takamatsu` (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its operator's hue that reads 3:1 on both
# map pages and clears CIE76 45 from every pin. Kotoden's yellow goes to
# ochre, JR Shikoku's blue to teal. Closest pair 39.6 (Shido / Kotoku); the
# dark-mode labels separate, 5 of 5.
_COLOURS = {"KT": "#B09000", "KN": "#30A800", "KS": "#F000B8", "JY": "#08A0C0", "JK": "#C870C8"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: Kotoden's own station index (kotoden.co.jp/publichtm/kotoden/station/,
# read 2026-10-03), in line order: the Kotohira Line's 高松築港 to 岡本 (12,
# 挿頭丘 onward beyond the city line), the Nagao Line's 高松築港 to 高田 (10,
# the two through stops included; 池戸 onward beyond), the Shido Line's 瓦町 to
# 原 (15; 琴電志度 beyond). The whole index is 53 stations, N02's 23 / 16 / 16.
GATE3 = {"source": "Kotoden's station index (kotoden.co.jp/publichtm/kotoden/station/): Kotohira Line "
                   "高松築港-岡本 12, Nagao Line 高松築港-高田 10, Shido Line 瓦町-原 15, inside the city",
         "lines": {"KT": 12, "KN": 10, "KS": 15}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
TAKAMATSU_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = TAKAMATSU_BBOX
