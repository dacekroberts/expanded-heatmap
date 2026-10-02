"""Kagoshima-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/kagoshima.md
(9/9 checks, 2026-10-02). A city of the 2026-10-01 Japanese batch, on the
shared modules (pipeline/countries/japan*.py): food only (Band B), Fukuoka's
two-source shape without its registers.

Business leg: two food lists split by the 2021 reform. MHLW's
食品衛生申請等システム open data holds every permit since 2021-06 and the
notifications (opt-in, field by field); the city's own CC BY 4.0 list holds
the old-law permits still held (令和8年6月末, updated quarterly). A premises in
both is shown once (config.SUPERSEDES). No personal services: the city's
barber and salon files are a 12-month stream of new openings, and it
publishes no laundry list. All placed by a JOIN to MLIT's 位置参照情報 for the
one municipality (no wards); where the block join misses an MHLW row, MHLW's
own point (OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM; N02-24 lacks 仙巌園), the Shinkansen left
out, stations kept only inside the city line (N03). The city tram, drawn as
one line, and JR Kyushu's three lines. English station names from
OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kagoshima" / "raw"
DATA_PROCESSED = ROOT / "data" / "kagoshima" / "processed"
OUTPUTS = ROOT / "outputs" / "kagoshima"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kagoshima"
SLUG = "kagoshima"
MUNICIPALITY = "鹿児島市"
PREFECTURE = "鹿児島県"

# The city's list page (「飲食店営業などの食品営業許可施設一覧（オープンデータ）」),
# under the city's open-data terms (鹿児島市オープンデータ利用規約, in force
# 2016-07-01, ict/documents/riyoukiyaku.pdf): CC BY 4.0, with a PRESCRIBED
# credit for a processed work (read 2026-10-02). The file is renamed each
# quarter (opendetar8_6matsu.csv is 2026-06-30's; the next update is due
# 2026-10-15): pinned, never "the newest". BODIK's 2023 copy is stale, not used.
CITY_PAGE = ("https://www.city.kagoshima.lg.jp/kenkofukushi/hokenjo/seiei-shoku/kenko/ese/sekatsu/shoku/"
             "shokuopendata.html")
TERMS_PDF = "https://www.city.kagoshima.lg.jp/ict/documents/riyoukiyaku.pdf"
# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2;
# re-read 2026-10-02). A plain GET. Credit links the top page only.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    "mhlw": ("46201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=46201_food_business_all.csv",
             MHLW_TOP),
    "food": ("opendetar8_6matsu.csv",
             "https://www.city.kagoshima.lg.jp/kenkofukushi/hokenjo/seiei-shoku/kenko/ese/sekatsu/shoku/documents/"
             "opendetar8_6matsu.csv",
             CITY_PAGE),
}
# Kyoto's rule: the date the list states (令和8年6月末), never the download's;
# MHLW's monthly file states none (its newest 許可年月日 is 2026-08-31).
SOURCE_AS_OF = {"mhlw": None, "food": "2026-06-30"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: MHLW's file is UTF-8 with a BOM; the city's list
# cp932, comma-separated, with one empty trailing column. Its 許可年月日 is
# wareki (R020601) and is not read: the list carries no expiry, and the city
# drops a lapsed permit each quarter.
SOURCE_ENCODING = {"mhlw": "utf-8-sig", "food": "cp932"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 営業者氏名 is REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; it is read IN MEMORY by that rule only, never kept. Never selected:
# 営業所の電話番号, 営業許可番号, and MHLW's 法人名 / 法人番号 / 法人住所 and
# phones.
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日"),
    "food": ("営業所の名称、屋号又は商号", "営業所の所在地", "営業の種類", "営業者氏名"),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses an MHLW row, MHLW's own point places it (the
# brief's check: a median 37 m from the block point, 94.8% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# One premises in both food lists: the city's old-law row goes, MHLW's (the
# newer filing) stays. The brief's screen: 123 of MHLW's 3,794 block-placed
# restaurants (3.2%), likely renewals the quarterly list has not yet dropped.
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 46201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and the city tram's stops
# (railway=tram_stop, which the station query does not take). Which stations
# exist is N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (S 31.293, W 130.387, N 31.753, E 130.730,
# Sakurajima included) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (31.28, 130.37, 31.77, 130.74)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae, a 丁目
# stop as "1-chome". OSM's tram stops carry stop codes and route numbers in
# name:en (I-22, #1-07), one misspelling (市役所前) and run-together station
# names; JR's carry macrons. The other 37 are OSM's as they stand. Tram 郡元 /
# JR 郡元 and tram 谷山 / JR 谷山 are separate N02 groups, so step 1 appends
# their operators (Korimoto (City Tram) / Korimoto (JR)).
OSM_NAME_EN_OVERRIDES = {
    "鹿児島中央": "Kagoshima-Chuo",                   # Kagoshima-Chūō
    "上伊集院": "Kami-Ijuin",                         # Kami-Ijūin
    "二中通": "Nichudori",                            # Nichū-dōri
    "市役所前": "Shiyakusho-mae",                     # Shikayusho-mae
    "天文館通": "Tenmonkandori",                      # Tenmonkandori #1- 07, #2-07
    "宇宿一丁目": "Usuki 1-chome",                    # Usuki-icchome 1-21
    "脇田": "Wakita",                                 # Wakita (I-22)
    "神田（交通局前）": "Shinden (Kotsukyoku-mae)",    # Shinden(Kotsukyoku-mae)
    "鹿児島駅前": "Kagoshima-ekimae",                  # Kagoshimaekimae
    "鹿児島中央駅前": "Kagoshima-Chuo-ekimae",          # Kagoshimachuoekimae
    "南鹿児島駅前": "Minami-Kagoshima-ekimae",          # Minami-Kagoshima Eki-mae
    "純心学園前": "Junshingakuen-mae",                 # Junshingakuen-Mae
    "工学部前": "Kogakubu-mae",                        # Kogakubu-Mae
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 52N: the longitude (~130.56) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# HALVED, on the spacing rule (docs/ring_rules.md: the halved edges where the
# median station gap is about 550 m or less): step 1 measured 272 m among the
# 55 in-city stations, 35 of them the city tram's stops (2026-10-02), as
# Hiroshima's 357 m and Matsuyama's 374 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
# Gate 1's floor: Hiroshima's, Matsuyama's, Paris's and Riga's 200 m, not a
# new number - a tram network is genuinely closer than 400 m (collapsed
# median 272 m; platforms 248 m).
SPACING_MIN_M = 200.0

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 7 lines, no Shinkansen; 鹿児島中央 stays as a JR station). The
# tram's four legal sections lie wholly inside. JR Kyushu's Ibusuki-Makurazaki
# (14 of 36), Kagoshima (5 of 99) and Nippo (3 of 113) lines are cut at the
# city line (owner 2026-09-24). No line is cut to a stub.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the city tram under four LEGAL
# sections (第一期線, 第二期線, 唐湊線, 谷山線) that no rider reads; the city's
# transport bureau runs routes 1 and 2 over them. Drawn as ONE line under the
# tram's public name, on Matsuyama's and Sapporo's precedent. Line names
# follow JR Kyushu's signs (no macrons), as the station names follow OSM's.
_KT, _JR = "鹿児島市", "九州旅客鉄道"
LINES = {
    "KT": {"n02": [(_KT, "第一期線"), (_KT, "第二期線"), (_KT, "唐湊線"), (_KT, "谷山線")],
           "name": "Kagoshima City Tram", "name_ja": "鹿児島市電", "short": "City Tram", "hue": "#009944"},
    "JI": {"n02": [(_JR, "指宿枕崎線")], "name": "JR Ibusuki Makurazaki Line", "name_ja": "指宿枕崎線",
           "short": "JR", "hue": "#F39800"},
    "JK": {"n02": [(_JR, "鹿児島線")], "name": "JR Kagoshima Main Line", "name_ja": "鹿児島本線", "short": "JR",
           "hue": "#E60012"},
    "JN": {"n02": [(_JR, "日豊線")], "name": "JR Nippo Main Line", "name_ja": "日豊本線", "short": "JR",
           "hue": "#0068B7"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# kagoshima` (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its operator's hue that reads 3:1 on both
# map pages and clears CIE76 45 from every pin. JR's Nippo blue, which no blue
# clears Retail's pin in, goes teal. Closest pair 53.2 (Ibusuki Makurazaki /
# Kagoshima Main); the dark-mode labels separate, 4 of 4.
_COLOURS = {"KT": "#30A800", "JI": "#D08000", "JK": "#E80010", "JN": "#007890"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the transport bureau's own stop table (its 2022 naming-rights list,
# kotsu-city-kagoshima.jp/wp/wp-content/uploads/2022/04/09d0f2bcee270a4cedad2b194bfa1aa1.pdf,
# read 2026-10-02) has 37 rows, with 高見馬場 listed once per route and 郡元 /
# 郡元(南側) apart: 35 stops, every one inside the city. The JR lines the city
# line cuts have no in-city count of their own.
GATE3 = {"source": "Kagoshima City Transportation Bureau's stop table (2022): 37 rows, 35 stops",
         "lines": {"KT": 35}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KAGOSHIMA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KAGOSHIMA_BBOX
