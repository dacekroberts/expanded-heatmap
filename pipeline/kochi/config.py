"""Kōchi-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/kochi.md
(7/7 checks, 2026-10-02). Part of the 2026-10-01 Japanese batch, on the shared
modules (pipeline/countries/japan*.py). The slug is ASCII; the name keeps its
macron, since "Kochi" is India's discard row on the master list. Personal
services only (Band B, owner 2026-10-01: Yokohama's page shape): MHLW's food
file publishes an address for 2,459 of 4,564 open restaurant permits (53.9%),
under the placement bar. The city publishes no laundry list (as Kitakyushu).

Business leg: the city's own CC BY 4.0 lists of barbers and beauty salons
(生活衛生営業施設情報), complete as of 2026-03-31, plus the monthly files of new
openings since (April to August 2026). Closures after 2026-03-31 are not
published, so the register is an UPPER BOUND on 2026-08-31 (Kyoto's call:
pinned to the last month read). The full lists hold 321 barbers and 1,074
salons against the official 327 and 1,061 a year earlier (e-Stat 衛生行政報告例
FY2024 第10表, row 高知県高知市, the year end 2025-03-31; a measurement, not
drawn): complete. Everything placed by a JOIN to MLIT's 位置参照情報 for the
one municipality (no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Tosaden's four tram lines and JR's Dosan Line. English station names
from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kochi" / "raw"
DATA_PROCESSED = ROOT / "data" / "kochi" / "processed"
OUTPUTS = ROOT / "outputs" / "kochi"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kōchi"
SLUG = "kochi"
MUNICIPALITY = "高知市"
PREFECTURE = "高知県"

# The 生活食品課's page 「生活衛生営業施設情報（高知市オープンデータ）」 (updated
# 2026-08-01): 【オープンデータ利用ルール】 applies CC BY 4.0 International, and
# the 高知市オープンデータ利用規約 (269801_1162152_misc.pdf) follows it. The full
# lists are as of 2026-03-31; since 2026-04 the city adds only new openings
# (「令和8年4月以降、新規開設があった情報のみ追加します」), one file per month and
# kind. No new barber file for May, July or August. The page's 旅館業 files are
# out of scope.
DATASET_PAGE = "https://www.city.kochi.kochi.jp/soshiki/36/opendata.html"
_FILES = "https://www.city.kochi.kochi.jp/uploaded/life"
# key -> (the city's file number, its as-of date)
_LISTS = {
    "barber": ("1162162", "2026-03-31"),        # 理容所一覧 (full)
    "beauty": ("1162161", "2026-03-31"),        # 美容所一覧 (full)
    "barber_0804": ("1162163", "2026-04-30"),
    "beauty_0804": ("1162164", "2026-04-30"),
    "beauty_0805": ("1162165", "2026-05-31"),
    "barber_0806": ("1162167", "2026-06-30"),
    "beauty_0806": ("1162168", "2026-06-30"),
    "beauty_0807": ("1162170", "2026-07-31"),
    "beauty_0808": ("1162171", "2026-08-31"),
}
SOURCE_FILES = {k: (f"269801_{n}_misc.xlsx", f"{_FILES}/269801_{n}_misc.xlsx", DATASET_PAGE)
                for k, (n, _) in _LISTS.items()}
SOURCE_AS_OF = {k: d for k, (_, d) in _LISTS.items()}
# The register's date, PINNED to the last month read (never the download's):
# an upper bound, openings added, closures not.
REGISTERS_AS_OF = "2026-08-31"
FOOD_AS_OF = None  # no food leg (MHLW's addresses fail placement)
# What step 2 reads: each kind's full list plus its monthly additions
# (source_rows); the monthly files are read inside it only.
SOURCES = {"barber": SOURCE_FILES["barber"][0], "beauty": SOURCE_FILES["beauty"][0]}
MONTHLY = {"barber": ("barber_0804", "barber_0806"),
           "beauty": ("beauty_0804", "beauty_0805", "beauty_0806", "beauty_0807", "beauty_0808")}
# Declared, never inferred: XLSX; the full lists open with a title row above
# the header, which xlsx_rows passes over to the address column.
SOURCE_ENCODING = {k: "xlsx" for k in SOURCE_FILES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The full lists' 営業者氏名 and the monthly files'
# 申請者名 are REQUIRED so the name rule (japan_register.name_is_operator; owner
# 2026-09-27) cannot silently compare nothing; they are read IN MEMORY by that
# rule only, never kept. Never selected: 施設電話番号 / 営業所電話番号,
# 申請者法人名, 申請者役職.
_FULL = ("施設名称", "施設住所名称", "営業者氏名")
_MONTH = ("営業所名称", "営業所所在地", "申請者名")
REQUIRED_COLUMNS = {k: (_FULL if k in ("barber", "beauty") else _MONTH) for k in SOURCE_FILES}
# The columns carried into step 2: the premises' own and the operator-name
# column for the name rule (in memory).
_KEEP = ("施設名称", "施設住所名称", "営業者氏名", "営業所名称", "営業所所在地", "申請者名")


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def source_rows(key):
    """A register's rows (japan_step2 reads this hook where a city defines it):
    its full list (2026-03-31) and every monthly addition since, in one
    stream, the premises columns only. The two schemas differ (施設名称 /
    施設住所名称 from the town; 営業所名称 / 営業所所在地 from the prefecture);
    japan_register reads both spellings. Measured 2026-10-02 (the brief):
    barbers 321 + 2, beauty salons 1,074 + 18, none repeating a full-list row."""
    from pipeline.countries import japan_register as jr

    for k in (key, *MONTHLY[key]):
        path = source_csv(k)
        if not path.exists():
            raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
        for r in jr.city_rows(path):
            yield {c: r.get(c) for c in _KEEP if c in r}


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 39201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and Tosaden's tram stops
# (railway=tram_stop, which the station query does not take). Which stations
# exist is N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (S 33.458, W 133.394, N 33.682, E 133.626),
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (33.44, 133.38, 33.7, 133.64)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-10-02): N02 and the operator's stop index write
# 文珠通, OSM 文殊通.
OSM_NAME_ALIASES = {"文珠通": "文殊通"}
OSM_NAME_EN_TIES = {}
# OSM's object carries no name:en (2026-10-02): romanised in Hiroshima's style.
OSM_NAME_EN_MISSING = {"田辺島通": "Tanabejima-dori"}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae, a 丁目
# stop as "1-chome" (Matsuyama's Hommachi 1-chome; the numerals rule, owner
# 2026-09-28: OSM spells out every 丁目 number). 桟橋 stays Sanbashi, as OSM and
# the operator write it.
OSM_NAME_EN_OVERRIDES = {
    "知寄町一丁目": "Chiyoricho 1-chome",            # Chiyorichō-itchōme
    "知寄町二丁目": "Chiyoricho 2-chome",            # Chiyorichō-nichōme
    "知寄町三丁目": "Chiyoricho 3-chome",            # Chiyorichō-sanchōme
    "上町一丁目": "Kamimachi 1-chome",               # Kamimachi-itchōme
    "上町二丁目": "Kamimachi 2-chome",               # Kamimachi-nichōme
    "上町四丁目": "Kamimachi 4-chome",               # Kamimachi-yonchōme
    "上町五丁目": "Kamimachi 5-chome",               # Kamimachi-gochōme
    "旭町一丁目": "Asahimachi 1-chome",              # Asahimachi-itchōme
    "旭町三丁目": "Asahimachi 3-chome",              # Asahimachi-sanchōme
    "桟橋通一丁目": "Sanbashi-dori 1-chome",          # Sanbashi-dōri-itchōme
    "桟橋通二丁目": "Sanbashi-dori 2-chome",          # Sanbashi-dōri-nichōme
    "桟橋通三丁目": "Sanbashi-dori 3-chome",          # Sanbashi-dōri-sanchōme
    "桟橋通四丁目": "Sanbashi-dori 4-chome",          # Sanbashi-dōri-yonchōme
    "桟橋通五丁目": "Sanbashi-dori 5-chome",          # Sanbashi-dōri-gochōme
    "桟橋車庫前": "Sanbashi-shako-mae",               # Sanbashi-shakomae
    "薊野": "Azono",                                 # Azōno
    "土佐大津": "Tosa-Otsu",                         # Tosa-Ōtsu
    "高知": "Kochi",                                 # Kōchi
    "円行寺口": "Engyojiguchi",                       # Engyōjiguchi
    "高知商業前": "Kochi-shogyo-mae",                 # Kōchi-Shōgyō-Mae
    "高知駅前": "Kochi-ekimae",                       # Kōchi-Ekimae
    "高知橋": "Kochi-bashi",                         # Kōchi-bashi
    "蓮池町通": "Hasuikemachi-dori",                  # Hasuikemachi-dōri
    "明見橋": "Myokenbashi",                         # Myōkenbashi
    "一条橋": "Ichijobashi",                         # Ichijōbashi
    "領石通": "Ryoseki-dori",                        # Ryōseki-dōri
    "デンテツターミナルビル前": "Dentetsu-taminarubiru-mae",  # Dentetsu-Tāminarubiru-mae
    "文珠通": "Monju-dori",                          # Monju-dōri
    "菜園場町": "Saenbacho",                          # Saenbachō
    "県立美術館通": "Kenritsubijutsukan-dori",         # Kenritsubijutsukan-dōri
    "宝永町": "Hoeicho",                             # Hōeichō
    "知寄町": "Chiyoricho",                          # Chiyorichō
    "大橋通": "Ohashidori",                          # Ōhashidōri
    "高知城前": "Kochijo-mae",                        # Kōchijō-mae
    "県庁前": "Kencho-mae",                          # Kenchō-mae
    "グランド通": "Gurando-dori",                     # Gurando-dōri
    "咥内": "Konai",                                 # Kōnai
    "曙町東町": "Akebonocho-higashimachi",            # Akebonochō-higashimachi
    "曙町": "Akebonocho",                            # Akebonochō
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~133.53) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# HALVED, on the spacing rule (docs/ring_rules.md: the halved edges where the
# median station gap is about 550 m or less): step 1 measured 271 m among the
# 67 in-city stations, 58 of them Tosaden's stops (2026-10-02), as Hiroshima's
# 357 m and Matsuyama's 374 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
# Gate 1's floor: Hiroshima's, Matsuyama's, Paris's and Riga's 200 m, not a
# new number - a tram network is genuinely closer than 400 m.
SPACING_MIN_M = 200.0

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 5 lines, no Shinkansen): Tosaden's Sanbashi (8 of 8) and Ekimae
# (4 of 4) lines wholly inside, its Ino (24 of 34) and Gomen (25 of 33) lines
# and JR's Dosan Line (10 of 61) cut at the city line (owner 2026-09-24). No
# line is cut to a stub. N02 groups JR's 朝倉 with the tram's 朝倉 (275 m), the
# widest group.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Tosaden's four tram lines are drawn by
# line, as Hiroden's in Hiroshima: the operator signs each by name (伊野線,
# 後免線, 桟橋線, 駅前線), and its two services (東西線 伊野 - 後免町, and
# 高知駅前 - 桟橋通五丁目) each join two of them at はりまや橋 rather than share
# one track. The Tosa Kuroshio Railway starts at 後免, outside the city: not
# drawn.
_TD, _JR = "とさでん交通", "四国旅客鉄道"
LINES = {
    "TI": {"n02": [(_TD, "伊野線")], "name": "Tosaden Ino Line", "name_ja": "伊野線", "short": "Tosaden",
           "hue": "#E60012"},
    "TG": {"n02": [(_TD, "後免線")], "name": "Tosaden Gomen Line", "name_ja": "後免線", "short": "Tosaden",
           "hue": "#E60012"},
    "TS": {"n02": [(_TD, "桟橋線")], "name": "Tosaden Sanbashi Line", "name_ja": "桟橋線", "short": "Tosaden",
           "hue": "#E60012"},
    "TE": {"n02": [(_TD, "駅前線")], "name": "Tosaden Ekimae Line", "name_ja": "駅前線", "short": "Tosaden",
           "hue": "#E60012"},
    "JD": {"n02": [(_JR, "土讃線")], "name": "JR Dosan Line", "name_ja": "土讃線", "short": "JR", "hue": "#00A5E3"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# kochi` (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide): each the
# feasible colour nearest its operator's hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. Tosaden's four share one red and spread
# over vermilion, orange and brown. Closest pair within 500 m 18.1 (Ino /
# Gomen, which meet only at はりまや橋); the dark-mode labels separate, 5 of 5.
_COLOURS = {"TI": "#E80010", "TG": "#F05030", "TS": "#F86000", "TE": "#B03800", "JD": "#08A0C0"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own counts for the lines wholly inside the city:
# Tosaden's route map (tosaden.co.jp/train/rosenzu.php, read 2026-10-02) links
# a timetable for each of its 76 stops, which make the Sanbashi Line 8
# (はりまや橋 to 桟橋通五丁目) and the Ekimae Line 4 (高知駅前 to はりまや橋), and
# the Ino Line 34 and the Gomen Line 33, as N02 (34 + 33 + 8 + 4, はりまや橋
# shared by all four: 76). The Ino and Gomen lines and JR are cut at the city
# line.
GATE3 = {"source": "Tosaden's route map, one timetable per stop (76 stops)", "lines": {"TS": 8, "TE": 4}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KOCHI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KOCHI_BBOX
