"""Nara-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/nara.md
(10/10 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py), in Kitakyushu's shape: MHLW's filings plus
the city's own list of pre-2021-law permits, with three registers.

Business leg: two food lists split by the 2021 law. MHLW's
食品衛生申請等システム open data holds every permit since 2021-06 and the
notifications (opt-in, field by field); the city's own CC BY 2.1 JP list holds
the old-law permits (as of 2025-11-01), kept only while in term on MHLW's
date. A premises in both is shown once (config.SUPERSEDES). Personal
services: the city's barber, beauty and laundry registers (2026-04-01). All
placed by a JOIN to MLIT's 位置参照情報 (one municipality, no wards); where
the block join misses an MHLW row, MHLW's own point (OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Kintetsu's Nara, Kyoto and Kashihara lines and JR West's Yamatoji and
Man-yo Mahoroba lines: 14 stations, built despite thin rail (owner,
2026-10-02). English station names from OpenStreetMap's name:en.
"""

import datetime
from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "nara" / "raw"
DATA_PROCESSED = ROOT / "data" / "nara" / "processed"
OUTPUTS = ROOT / "outputs" / "nara"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Nara"
SLUG = "nara"
MUNICIPALITY = "奈良市"
PREFECTURE = "奈良県"

# The city's lists on its own pages, each stating 「このページに掲載されている
# データは、クリエイティブ・コモンズ表示2.1日本ライセンスの下に提供されています」
# and pointing to the catalogue's terms (奈良市オープンデータカタログ利用規約
# 第1.2版; read 2026-10-02). The files are the editions this build read,
# pinned. MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site
# terms §2; read 2026-09-24 for Fukuoka). Credit links the top page only.
FOOD_PAGE = "https://www.city.nara.lg.jp/soshiki/97/10411.html"
ENV_PAGE = "https://www.city.nara.lg.jp/soshiki/97/9688.html"
_FILES = "https://www.city.nara.lg.jp/uploaded/attachment/"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL, the page that links it and carries its licence)
SOURCE_FILES = {
    "mhlw": ("29201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=29201_food_business_all.csv",
             MHLW_TOP),
    "food": ("203480.csv", _FILES + "203480.csv", FOOD_PAGE),
    "barber": ("209465.csv", _FILES + "209465.csv", ENV_PAGE),
    "beauty": ("209467.csv", _FILES + "209467.csv", ENV_PAGE),
    "laundry": ("209463.csv", _FILES + "209463.csv", ENV_PAGE),
}
# The dates the lists state (Kyoto's rule, never the download's): the old-law
# list's 「令和7年11月1日時点」, the registers' 「令和8年4月1日更新」; MHLW's
# file states none (its newest 許可年月日 2026-08-31), so the page dates it by
# download (provenance.json).
SOURCE_AS_OF = {"mhlw": None, "food": "2025-11-01", "barber": "2026-04-01", "beauty": "2026-04-01",
                "laundry": "2026-04-01"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
# The titles the city's credit must print (catalogue terms ３).
DATASET_TITLES = {"food": "食品営業許可施設オープンデータ", "barber": "理容所検査確認施設一覧",
                  "beauty": "美容所検査確認施設一覧", "laundry": "クリーニング所検査確認施設一覧"}
# The old-law list keeps a permit until its next edition even after its
# 許可有効期限 has passed, so step 2 drops rows past expiry against this PINNED
# date, MHLW's end of August 2026 (japan_register.in_term), never today:
# 820 of 1,341 rows are in term on it (the brief's count).
OLD_LAW_AS_OF = datetime.date(2026, 8, 31)
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: MHLW's file and the old-law list are UTF-8 with a
# BOM; the three registers cp932 CSV.
SOURCE_ENCODING = {"mhlw": "utf-8-sig", "food": "utf-8-sig", "barber": "cp932", "beauty": "cp932",
                   "laundry": "cp932"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The old-law list's 申請者_氏名 and the registers'
# 開設者名 / 開設者氏名 and 開設者代表者 are REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; they are read IN MEMORY by that rule only, never kept, and since
# 2026-10-05 MHLW's 法人名 too (owner: it holds a sole trader's own name as
# well as a company's). Never selected: MHLW's 法人番号 / 法人住所 and phones.
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
    "food": ("営業所名称", "営業所_住所１", "業種", "許可有効期限", "申請者_氏名"),
    "barber": ("理容所名称", "理容所所在地", "開設者名", "開設者代表者"),
    "beauty": ("美容所名称", "美容所所在地", "開設者氏名", "開設者代表者"),
    "laundry": ("クリーニング名称", "クリーニング所在地", "開設者氏名", "開設者代表者"),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses an MHLW row, MHLW's own point places it (the
# brief's check: a median 40 m from the block point, 95.1% within 250 m; at
# the chōme tier the centroid sits a median 387 m from MHLW's point).
OWN_POINT_FALLBACK = {"mhlw"}
# One premises in both food lists: the city's old-law row goes, MHLW's (the
# newer filing) stays.
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    The old-law food list only where its permit is in term on OLD_LAW_AS_OF
    (許可有効期限); every other file as it is."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    rows = jr.city_rows(path)
    if key == "food":
        rows = jr.in_term(rows, ("許可有効期限",), OLD_LAW_AS_OF)
    yield from rows


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one municipality.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Nara.
# S, W, N, E: the city's N03 extent (S 34.558, W 135.713, N 34.758, E 136.071)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.54, 135.70, 34.77, 136.09)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen. 近鉄奈良 takes Kintetsu's hyphen, as Yokkaichi's
# Kintetsu-Yokkaichi; the other 10 are OSM's as they stand.
OSM_NAME_EN_OVERRIDES = {
    "学園前": "Gakuen-mae",          # Gakuemmae
    "近鉄奈良": "Kintetsu-Nara",     # Kintetsu Nara
    "京終": "Kyobate",               # Kyōbate
    "西ノ京": "Nishinokyo",          # Nishinokyō
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.80) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-03: 5 lines, no Shinkansen). Every line is cut at the city line
# (owner 2026-09-24): Kintetsu's 奈良線 6 of 19, 京都線 3 of 26 and 橿原線 3 of
# 17, JR's 関西線 2 of 34 and 桜井線 3 of 14. No line is cut to one station;
# the two shortest stretches are radials through a small built-up area
# (Sakai's Midosuji, 3 stations drawn cut, the precedent). Thin rail, built
# anyway (owner, 2026-10-02).
LEFT_OUT_LINES = {}
# Kintetsu's Kyoto Line and JR's Yamatoji Line run on into Kyoto Prefecture:
# its N03 names the stations beyond the prefecture line
# (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("26",)
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. JR West signs N02's legal lines by their
# public names (trap 2): 関西線 is the Yamatoji Line (大和路線), 桜井線 the
# Man-yo Mahoroba Line (万葉まほろば線); no macron, Hiroshima's style.
_KT, _JR = "近畿日本鉄道", "西日本旅客鉄道"
LINES = {
    "KN": {"n02": [(_KT, "奈良線")], "name": "Kintetsu Nara Line", "name_ja": "近鉄奈良線",
           "short": "Kintetsu", "hue": "#E2001A"},
    "KT": {"n02": [(_KT, "京都線")], "name": "Kintetsu Kyoto Line", "name_ja": "近鉄京都線",
           "short": "Kintetsu", "hue": "#E2001A"},
    "KH": {"n02": [(_KT, "橿原線")], "name": "Kintetsu Kashihara Line", "name_ja": "近鉄橿原線",
           "short": "Kintetsu", "hue": "#E2001A"},
    "JY": {"n02": [(_JR, "関西線")], "name": "JR Yamatoji Line", "name_ja": "大和路線", "short": "JR",
           "hue": "#00A23E"},
    "JM": {"n02": [(_JR, "桜井線")], "name": "JR Man-yo Mahoroba Line", "name_ja": "万葉まほろば線",
           "short": "JR", "hue": "#A0522D"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py nara`
# (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide): each the
# feasible colour nearest its operator's hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. Kintetsu's three reds part into red,
# coral and orange. Closest pair within 500 m and anywhere 18.2 (the Kyoto and
# Kashihara lines); the dark-mode labels separate, 5 of 5.
_COLOURS = {"KN": "#E00018", "KT": "#F85838", "KH": "#F84800", "JY": "#20A800", "JM": "#A85830"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city, so Kintetsu's own station index
# (kintetsu.co.jp/station/, read 2026-10-03), read against the city line,
# gives each cut line's in-city stops: the Nara Line 富雄 to 近鉄奈良 (6; 東生駒
# beyond is Ikoma's), the Kyoto Line 高の原 to 大和西大寺 (3; 山田川 is
# Seika's) and the Kashihara Line 大和西大寺 to 西ノ京 (3; 九条 is
# Yamatokoriyama's). JR's two lines, 2 and 3 stops, are N02's.
GATE3 = {"source": "Kintetsu's station index (kintetsu.co.jp/station/), read against the city line",
         "lines": {"KN": 6, "KT": 3, "KH": 3}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
NARA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = NARA_BBOX
