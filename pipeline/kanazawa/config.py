"""Kanazawa-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/kanazawa.md (13/13 checks, 2026-10-11). Part of the A/B
build plan's Regional-2 batch, on the shared modules
(pipeline/countries/japan*.py) with every shared rule on. Food only (Band B,
owner 2026-10-04: Hiroshima's one-bucket page): the city's current barber,
beauty-salon and laundry lists are all rights reserved and never fetched.

Business leg: ONE source, the city catalogue's 食品衛生関係営業許可施設一覧
(catalog-data.city.kanazawa.ishikawa.jp, author 衛生指導課, cc-by), a
snapshot of every food permit in term in early April 2024 (8,842 rows, the
newest permit 2024-04-01), kept whole and dated (owner, 2026-10-05). It holds
6,478 restaurant permits against the 6,420 in force on 2024-03-31 (e-Stat
衛生行政報告例 FY2023; 100.9%). Placed by a JOIN to MLIT's 位置参照情報 (one
municipality, no wards); where the block join misses, the city's own point
(OWN_POINT_FALLBACK). MHLW's open data for 17201 is a control only, read by
no step (owner, 2026-10-05).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). The Hokuriku Railroad's Asanogawa and Ishikawa lines and the IR
Ishikawa Railway Line. English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kanazawa" / "raw"
DATA_PROCESSED = ROOT / "data" / "kanazawa" / "processed"
OUTPUTS = ROOT / "outputs" / "kanazawa"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kanazawa"
SLUG = "kanazawa"
MUNICIPALITY = "金沢市"
PREFECTURE = "石川県"

# The city's CKAN catalogue (金沢市オープンデータポータル). The dataset record
# declares cc-by, 「クリエイティブ・コモンズ 表示」 with no version; the city's
# terms (金沢市オープンデータ利用規約, read 2026-10-05: permitted with
# conditions) prescribe the credit. The resource's own /download/ path
# answers HTTP 500 (2026-10-05), so the file is the datastore dump, the
# resource page's own download link: the upload (2,568,426 B in the record)
# plus a BOM and an `_id` column, 2,756,283 B. The record was last modified
# 2024-07-16; a newer date is a new edition, to re-measure and never merge
# (brief_check.py's kanazawa-package watches it).
_CATALOGUE = "https://catalog-data.city.kanazawa.ishikawa.jp"
FOOD_PAGE = f"{_CATALOGUE}/dataset/172014-syokuhineisei-kyokashisetsu"
_RESOURCE = "09a49521-cabf-40b4-978b-bd61ef02f650"
# source key -> (file, URL, the dataset page that carries its licence).
SOURCE_FILES = {
    "food": ("172014-syokuhineisei-kyokashisetsu.csv", f"{_CATALOGUE}/datastore/dump/{_RESOURCE}?bom=true",
             FOOD_PAGE),
}
# The snapshot's own date, PINNED (Kyoto's rule: the list's date, never the
# download's or today's). The dataset states none; its newest 許可年月日 and
# 開始年月日 are 2024-04-01 and its earliest 許可満了日 2024-04-15, so it was
# extracted between those dates (measured 2026-10-11, all 8,842 dates read).
# Kept whole (owner, 2026-10-05): by 2026-10-05 43% of the storefront rows had
# passed their expiry date, old-law permits that the official stock shows
# renewed almost one for one (FY2023 6,420 restaurant permits, FY2024 6,438),
# and no open source carries the renewals.
FOOD_AS_OF = "2024-04-01"
SOURCE_AS_OF = {"food": FOOD_AS_OF}
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day the file covers, never today. Measured 2026-10-11: no row is
# past its term on that date and none starts after it.
TERM_AS_OF = {"food": FOOD_AS_OF}

SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: UTF-8 with a BOM, the header on row 1, the
# national recommended schema.
SOURCE_ENCODING = {"food": "utf-8-sig"}
# The columns the file must carry; fetch_sources.py and step 2 stop on a
# header without them. 法人名 is the operator column, REQUIRED so the name
# rule (japan_register.name_is_operator; owner 2026-09-27, 法人名 since
# 2026-10-05) cannot silently compare nothing; read IN MEMORY by that rule
# only, never kept. The city fills it on 4,590 of 8,842 rows, 4,570 with a
# company or cooperative marker (the brief, 2026-10-05): it names an operator
# almost only where it is a company (Toyama's position, owner 2026-10-02), so
# the rule compares few rows and version 2 (a bare personal name as the trade
# name, owner 2026-10-06) covers the rest.
REQUIRED_COLUMNS = {
    "food": ("営業所名称", "営業の種類", "業態", "営業所所在地", "緯度", "経度", "法人名", "許可満了日"),
}
# The columns carried into step 2 (Shizuoka's source_rows precedent: the
# premises' own and the name rule's, nothing else). Never selected:
# 営業所電話番号 (filled on 6,696 rows), 営業所名称カナ, 法人番号 (empty), 備考
# (one fixed note on the 389 vehicle and stall rows) and 画像, which the
# licence read says is never read.
_KEEP = ("営業所名称", "営業の種類", "業態", "営業所所在地", "営業所方書", "緯度", "経度", "法人名", "許可番号",
         "許可年月日", "開始年月日", "許可満了日", "廃業年月日", "申請区分", "許可条件")


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """The snapshot's rows (japan_step2 reads this hook where a city defines
    it): the file as it stands, the _KEEP columns only."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        yield {c: r.get(c) for c in _KEEP if c in r}


# The city's own 緯度 / 経度 (on every row) place a row the block join misses
# or gives only a town-chōme centroid (Fukuoka's OWN_POINT_FALLBACK with the
# list's own point, as Hamamatsu's and Fukuyama's). The brief's grounds
# (2026-10-05): at the block tier the city's point sits a median 33 m from
# MLIT's (96.6% within 250 m), so the datum guard passes; the misses are the
# city's イロハ sections (無量寺町ヲ, 沖町イ ...) and newer 区画整理 districts
# MLIT's block edition lacks. One default point at the city hall holds 389
# vehicle and stall rows, all out before the join; japan_step2.shared_points
# refuses any other.
OWN_POINT_FALLBACK = {"food"}

# The list's share of the official restaurant count, measured every build and
# written to outputs/kanazawa/official_shares.json (japan_step2.official_shares).
# It reads e-Stat's FY2024 table (2025-03-31: 6,438), a year AFTER the
# snapshot; the like-for-like count is FY2023's 6,420 on 2024-03-31 (the
# brief: old law 3,353, revised law 3,067).
OFFICIAL_SHARES = True

# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 17201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Kanazawa (the city
# tramway closed in 1967 and is not in N02).
# S, W, N, E: the city's N03 extent (S 36.3382, W 136.5571, N 36.6742,
# E 136.8172) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (36.33, 136.55, 36.68, 136.83)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), to one style across the 21 names OSM gave (39 objects, all with
# name:en, 2026-10-11): OSM hyphenates Higashi-Kanazawa and Nishi-izumi and
# spaces the rest. The hyphen is the operators' own form (IR Ishikawa's
# Higashi-Kanazawa and Nishi-Kanazawa; Gifu's Meitetsu-Gifu for an operator
# prefix), and 前 is -mae (Hiroshima's style). OSM's other 17 stand.
OSM_NAME_EN_OVERRIDES = {
    "北鉄金沢": "Hokutetsu-Kanazawa",                  # Hokutetsu Kanazawa
    "西金沢": "Nishi-Kanazawa",                        # Nishi Kanazawa
    "新西金沢": "Shin-Nishi-Kanazawa",                 # Shin Nishi Kanazawa
    "額住宅前": "Nukajutaku-mae",                      # Nukajutakumae
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the city's centre (~136.66) and its whole extent (136.56 to
# 136.82) fall in the 132 to 138 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings: step 1 measured a median
# nearest-station gap of 561 m over the 21 drawn stations (2026-10-11; the
# brief read the same), above the ~550 m halving threshold
# (docs/ring_rules.md) but inside the 540 to 570 m band the owner decided for
# Gifu (545 m, standard rings, 2026-10-07: every JR and private-rail Japanese
# city is on them). Re-measure if the drawn stations change.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25: 3 lines; the Shinkansen's 金沢 dropped, and 金沢 stays an IR
# Ishikawa station). Each is cut at the city line (owner 2026-09-24): the
# Asanogawa Line keeps 10 of 12 (粟ヶ崎 and 内灘 are in 内灘町), the Ishikawa
# Line 7 of 17 in two runs (it crosses 野々市市 between 新西金沢 and 馬替, and
# runs on into 白山市), the IR Ishikawa Railway Line 4 of 19. No JR line has a
# station inside the city: JR West's Hokuriku Line here passed to IR Ishikawa.
# No frequency floor (owner, 2026-10-06): the thinnest line read, the Ishikawa
# Line at 野町, runs 29 departures a day (the brief, 2026-10-05).
LEFT_OUT_LINES = {}
# 北鉄金沢 / 金沢 (135 m) and 新西金沢 / 西金沢 (140 m) are separate N02 groups
# of different names and stay apart (trap 1: Kobe's Tarumi / Sanyo Tarumi);
# every group holds one record.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names carry no macrons; "Hokutetsu"
# is the Hokuriku Railroad's own short name (北鉄), as Toyama's "Chitetsu".
_HR, _IR = "北陸鉄道", "IRいしかわ鉄道"
LINES = {
    "AS": {"n02": [(_HR, "浅野川線")], "name": "Hokutetsu Asanogawa Line", "name_ja": "北陸鉄道浅野川線",
           "short": "Hokutetsu", "hue": "#F08300"},
    "IS": {"n02": [(_HR, "石川線")], "name": "Hokutetsu Ishikawa Line", "name_ja": "北陸鉄道石川線",
           "short": "Hokutetsu", "hue": "#F08300"},
    "IR": {"n02": [(_IR, "IRいしかわ鉄道線")], "name": "IR Ishikawa Railway Line", "name_ja": "IRいしかわ鉄道線",
           "short": "IR", "hue": "#009FE8"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# kanazawa` (2026-10-11, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin (Asanogawa 53.6, Ishikawa 63.7, IR
# 75.4). Hokutetsu's one orange splits in two, as Toyama's Chitetsu red;
# closest pair within 500 m 121.4 (Asanogawa, IR, at 金沢); anywhere 11.3
# (Asanogawa, Ishikawa, which never come within 500 m). The dark-mode labels
# separate, 3 of 3. No line here is in pipeline/line_registry.py: no other
# map draws one.
_COLOURS = {"AS": "#E07800", "IS": "#E86800", "IR": "#0098E0"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station lists (the brief, read 2026-10-05;
# brief_check.py re-read all three 2026-10-11). Hokutetsu's line pages link 12
# Asanogawa station pages, 10 of them inside the city (all but 粟ヶ崎 and
# 内灘), and 17 Ishikawa station pages, 7 inside (野町, 西泉, 新西金沢, 馬替,
# 額住宅前, 乙丸, 四十万); IR Ishikawa's timetable index links 19, 4 inside
# (森本, 東金沢, 金沢, 西金沢). Each total matches N02.
GATE3 = {"source": "Hokutetsu's line pages (hokutetsu.co.jp/railway/asanogawasen/ and /ishikawasen/: 12 and 17 "
                   "stations, 10 and 7 inside the city) and IR Ishikawa Railway's timetable index "
                   "(ishikawa-railway.jp/timetable/index.html: 19 stations, 4 inside)",
         "lines": {"AS": 10, "IS": 7, "IR": 4}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KANAZAWA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KANAZAWA_BBOX

# Trade names read by eye as a person's own name and nothing else, on
# surnames the sign rule's list does not hold (owner, 2026-10-12; found by
# the name-shape count after the phase 2 landing). KEYS, never names
# (pipeline/name_keys.py, over japan_register._name_key of the name).
PERSON_NAMED = (
    "dc16cdc98af79547",
    "cd38bc2d7449b4ec",
    "a6cdcf4ffec1157e",
)

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3604800041)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "県庁駐車場前": "a signed junction (highway=traffic_signals) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
}
PLACE_DROPPED = {}
