"""Hamamatsu-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/hamamatsu.md
(18/18 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py). Personal services only (Band B, owner
2026-10-02: Hakodate's and Yokohama's page): the city publishes only NEW food
permits (a stream since 2017-04, no renewal and no closure, so no register can
be rebuilt), and MHLW's file holds notifications only; MHLW's 6,033
notifications are NOT added as a partial food layer (owner, 2026-10-02).

Business leg: the city's four CC BY 2.1 JP registers (生活衛生課: 理容所台帳,
美容所台帳, クリーニング所(取次)台帳, クリーニング所(一般)台帳), published
2026-08-18, 3,212 premises against the official 3,164 (101.5%; e-Stat
衛生行政報告例 FY2024, a measurement, not drawn). Placed by a JOIN to MLIT's
位置参照情報 for the 3 wards of 2024 (22138-22140); where the block join gives
only a town-chōme or 大字 centroid, the city's own point (OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), the Shinkansen left out, stations kept
only inside the city line (N03). The Enshu Railway (wholly inside), the Tenryu
Hamanako Railroad and JR Central's Tokaido and Iida lines, cut at the city
line. English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "hamamatsu" / "raw"
DATA_PROCESSED = ROOT / "data" / "hamamatsu" / "processed"
OUTPUTS = ROOT / "outputs" / "hamamatsu"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Hamamatsu"
SLUG = "hamamatsu"
MUNICIPALITY = "浜松市"
PREFECTURE = "静岡県"

# The city's open-data portal (a JavaScript page whose records come from its
# API, ?x=<dataset>); each CSV is served from the portal's own storage. The
# portal's top and the 「くらし」 listing put every dataset under CC BY 2.1 JP and
# incorporate the 浜松市オープンデータ利用規約 (koho2/opendata/kiyaku.html, updated
# 2025-04-01); read 2026-10-02.
PORTAL_API = "https://www.city.hamamatsu.shizuoka.jp/api/odpf/opendata/v1?x="
_FILES = "https://prd-hmpf-s3-odpf-01.s3.ap-northeast-1.amazonaws.com/opendata/v01/"
TERMS_PAGE = "https://www.city.hamamatsu.shizuoka.jp/koho2/opendata/kiyaku.html"
# source key -> (file, URL, the dataset record that links it).
SOURCE_FILES = {
    "barber": ("riyoujyo.csv", _FILES + "riyoujyo/riyoujyo.csv", PORTAL_API + "riyoujyo"),
    "beauty": ("biyoujyo.csv", _FILES + "biyoujyo/biyoujyo.csv", PORTAL_API + "biyoujyo"),
    "laundry_pickup": ("cleaning_toritugi.csv", _FILES + "cleaning_toritugi/cleaning_toritugi.csv",
                       PORTAL_API + "cleaning_toritugi"),
    "laundry": ("cleaning_ippan.csv", _FILES + "cleaning_ippan/cleaning_ippan.csv", PORTAL_API + "cleaning_ippan"),
}
# Two laundry registers (pick-up counters 取次 and general laundries 一般), one
# kind: the KEY names the source, the kind decides the bucket (Tokyo's
# SOURCE_KIND).
SOURCE_KIND = {"laundry_pickup": "laundry"}
# The registers state no as-of line; each dataset's 更新日 and the files'
# Last-Modified are 2026-08-18, the publication date, pinned (the brief). The
# newest 確認通知年月日 is 2026-07-28 (beauty).
REGISTERS_AS_OF = "2026-08-18"
SOURCE_AS_OF = {k: REGISTERS_AS_OF for k in SOURCE_FILES}
FOOD_AS_OF = None  # no food register is published
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: cp932 CSV, header on the first line.
SOURCE_ENCODING = {k: "cp932" for k in SOURCES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The registers carry NO operator column at all, so the
# name rule has nothing to compare (Okayama's precedent, owner 2026-10-02);
# the page takes Hiroshima's MHLW-style bullet. Never selected: 施設_電話番号
# (the premises' phone).
_REGISTER = ("業種", "施設_名称", "施設_所在地", "緯度", "経度", "区")
REQUIRED_COLUMNS = {k: _REGISTER for k in SOURCES}
# The city's own 緯度 / 経度 place a row where the block join gives only a
# town-chōme or 大字 centroid (Fukuoka's OWN_POINT_FALLBACK, chōme tier
# included). The brief's grounds (2026-10-02): at the block tier the city's
# point sits a median 40 m from MLIT's (p90 102 m, 96.0% within 250 m); at
# the chōme tier the centroid is a median 741 m from it (165 rows, 164 of
# them 大字 with 地番 addresses, 68 over 1 km). Every row but one carries a
# point, none repeated more than 6 times; datum_guard confirms the datum.
OWN_POINT_FALLBACK = set(SOURCES)

# The official count the registers were measured against (the brief): e-Stat
# 衛生行政報告例 FY2024, 生活衛生 第10表 (理容所 / 美容所) and 第11表
# (クリーニング所), row 静岡県浜松市; the files Hakodate's build fetched. A
# measurement only, never drawn; recorded by fetch_sources.py estat.
ESTAT_CONTROL = {
    "estat_riyo_biyo": ("estat_eisei_r6_riyo_biyo_by_city.csv",
                        "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359178&fileKind=1"),
    "estat_cleaning": ("estat_eisei_r6_cleaning_by_city.csv",
                       "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359179&fileKind=1"),
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward
# (the 2024 codes; the old 22131-22137 answer 404).
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Hamamatsu.
# S, W, N, E: the city's N03 extent (S 34.646, W 137.487, N 35.304, E 138.059:
# the merged city reaches from the coast into the mountains of 天竜区), rounded
# out; step 1 stops if the city leaves it.
OSM_BBOX = (34.63, 137.47, 35.32, 138.07)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
# Where no OSM object in range carries a name:en (2026-10-03): OSM's 浜北
# (node 8093209328) has none, and its 天竜二俣 (node 13165767449) carries only a
# wrong name:ja_rm. The operators' own station pages spell them
# (entetsu.co.jp/tetsudou/station/hamakita.html,
# tenhama.co.jp/about/station/tenryufutamata/).
OSM_NAME_EN_MISSING = {"浜北": "Hamakita", "天竜二俣": "Tenryu-Futamata"}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word (Kitakyushu's Abeyama-koen,
# Kyushu-kodai-mae), a place name after a hyphen capitalised (Okayama's
# Bitchu-Takamatsu, Kitakyushu's Chikuho-Katsuki). OSM's Enshu Railway names
# carry macrons and title case; the other 43 are OSM's as they stand.
OSM_NAME_EN_OVERRIDES = {
    "中部天竜": "Chubu-Tenryu",                      # Chubutenryu
    "第一通り": "Daiichi-dori",                      # Dai-Ichi-dōri
    "遠州病院": "Enshu-byoin",                       # Enshubyoin
    "遠州岩水寺": "Enshu-Gansuiji",                  # Enshū-Gansuiji
    "遠州小林": "Enshu-Kobayashi",                   # Enshū-Kobayashi
    "遠州小松": "Enshu-Komatsu",                     # Enshū-Komatsu
    "遠州西ヶ崎": "Enshu-Nishigasaki",               # Enshū-Nishigasaki
    "遠州芝本": "Enshu-Shibamoto",                   # Enshū-Shibamoto
    "自動車学校前": "Jidosha-gakko-mae",             # Jidōsha-Gakkō-Mae
    "美薗中央公園": "Misono-chuo-koen",              # Misono-Chūō-kōen
    "常葉大学前": "Tokoha-daigaku-mae",              # Tokohadaigakumae
    "大嵐": "Ozore",                                 # Ōzore
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~137.73) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-station gap is 1,158 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-03: 4 lines; the Shinkansen's 浜松 dropped): the Enshu Railway
# (18 of 18, wholly inside), the Tenryu Hamanako Line (19 of 39), JR's Iida
# Line (13 of 94: 中部天竜 to 大嵐, its mountain stretch in 天竜区) and Tokaido
# Line (5 of 89), cut at the city line (owner 2026-09-24). The 32 rural
# groups (Tenhama and the Iida Line) are drawn by the standing call; no urban
# line is cut to a stub.
LEFT_OUT_LINES = {}
# The Iida Line runs on into Aichi and Nagano: their N03 names the stations
# beyond the prefecture line (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("23", "20")
# 西鹿島 is one group for the Enshu Railway and Tenhama.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour.
_JR = "東海旅客鉄道"
LINES = {
    "EN": {"n02": [("遠州鉄道", "鉄道線")], "name": "Enshu Railway Line", "name_ja": "遠州鉄道線",
           "short": "Entetsu", "hue": "#E60012"},
    "TH": {"n02": [("天竜浜名湖鉄道", "天竜浜名湖線")], "name": "Tenryu Hamanako Line", "name_ja": "天竜浜名湖線",
           "short": "Tenhama", "hue": "#00A040"},
    "JT": {"n02": [(_JR, "東海道線")], "name": "JR Tokaido Line", "name_ja": "東海道線", "short": "JR",
           "hue": "#F77321"},
    "JI": {"n02": [(_JR, "飯田線")], "name": "JR Iida Line", "name_ja": "飯田線", "short": "JR", "hue": "#0070B9"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# hamamatsu` (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its operator's hue that reads 3:1 on both
# map pages and clears CIE76 45 from every pin. Closest pair within 500 m and
# anywhere 31.4 (Enshu / Tokaido, at 浜松 and 新浜松); the dark-mode labels
# separate, 4 of 4.
_COLOURS = {"EN": "#E80010", "TH": "#28A800", "JT": "#E86810", "JI": "#08A0C0"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own count for the line wholly inside the city: the
# Enshu Railway's station index (entetsu.co.jp/tetsudou/) lists 18 stations,
# 新浜松 to 西鹿島 (the brief's check, re-run 2026-10-03). The lines the city
# line cuts have no in-city count of their own; step 1 lists them.
GATE3 = {"source": "the Enshu Railway's station index (entetsu.co.jp/tetsudou/, 18 stations)", "lines": {"EN": 18}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
HAMAMATSU_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = HAMAMATSU_BBOX
