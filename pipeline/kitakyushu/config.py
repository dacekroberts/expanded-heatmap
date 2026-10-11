"""Kitakyushu-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/kitakyushu.md
(11/11 checks, 2026-10-02). A city of the 2026-10-01 Japanese batch, on the
shared modules (pipeline/countries/japan*.py), in Fukuoka's two-source shape.

Business leg: two food lists split by the 2021 law. MHLW's
食品衛生申請等システム open data holds every permit since 2021-06 and the
notifications (opt-in, field by field); the city's own CC BY 4.0 list on BODIK
holds the old-law permits (as of 2026-03-31), kept only while in term on
MHLW's date. A premises in both is shown once (config.SUPERSEDES). Personal
services: the city's barber and beauty registers (2026-08-31); the city
publishes NO laundry list (Berlin's gap, disclosed). All placed by a JOIN to
MLIT's 位置参照情報 for the 7 wards; where the block join misses an MHLW row,
MHLW's own point (OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), the Shinkansen left out, stations kept
only inside the city line (N03). The Kitakyushu Monorail, the Chikuho
Electric Railroad and JR Kyushu's lines. English station names from
OpenStreetMap's name:en.
"""

import datetime
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kitakyushu" / "raw"
DATA_PROCESSED = ROOT / "data" / "kitakyushu" / "processed"
OUTPUTS = ROOT / "outputs" / "kitakyushu"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kitakyushu"
SLUG = "kitakyushu"
MUNICIPALITY = "北九州市"
PREFECTURE = "福岡県"

# The city's lists on BODIK (data.bodik.jp, the city's catalogue,
# odcs.bodik.jp/401005), each dataset license_id cc-by, under the catalogue's
# terms (北九州市オープンデータ利用規約 第1条: CC BY 4.0 International; read
# 2026-10-02). Each dataset's organisation and resource name are a MUST
# DISPLAY (第6条): food 保健福祉局 保健衛生課; barber and beauty 保健福祉局
# 東部・西部生活衛生課. The files are the editions this build read, pinned,
# never "the newest" (package_show re-read 2026-10-02: each is its dataset's
# newest resource).
BODIK = "https://data.bodik.jp/dataset"
# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2;
# read 2026-09-24 for Fukuoka). A plain GET. Credit links the top page only.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL, the page that links it and carries its licence)
SOURCE_FILES = {
    "mhlw": ("40100_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=40100_food_business_all.csv",
             MHLW_TOP),
    "food": ("401005_shokuhineiseihotokyokashisetsuichiran_20260331.xlsx",
             f"{BODIK}/822fb681-346a-444e-b482-33c67b50cac3/resource/afce5cb5-8582-4295-8a98-494db2e25466/"
             "download/401005_shokuhineiseihotokyokashisetsuichiran_20260331.xlsx",
             f"{BODIK}/401005_shokuhineiseihotokyokashisetsuichiran"),
    "barber": ("401005_riyosyoichiran_20260831.csv",
               f"{BODIK}/8be510bd-5f67-4570-a250-b34ffdac8d37/resource/c0503e76-86d9-4f14-a052-f17ac06951d0/"
               "download/401005_riyosyoichiran_20260831.csv",
               f"{BODIK}/401005_riyosyoichian"),
    "beauty": ("401005_biyosyoichiran_20260831.csv",
               f"{BODIK}/c8266fc8-5d1f-4d3b-93aa-44486f5187ea/resource/e958d9fd-6e3d-47bf-b557-96af0c3a44ca/"
               "download/401005_biyosyoichiran_20260831.csv",
               f"{BODIK}/401005_biyosyoichiran"),
}
# The dates the lists state (Kyoto's rule, never the download's): the food
# list's sheet 「2026(令和8)年3月末時点」, the registers' resource names; MHLW's
# viewer reads 「2026年08月末現在」 (its newest 許可年月日 2026-08-31), but the
# file itself states none, so the page dates it by download.
SOURCE_AS_OF = {"mhlw": None, "food": "2026-03-31", "barber": "2026-08-31", "beauty": "2026-08-31"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
# The resource names, as the BODIK credit must print them (第6条).
RESOURCE_NAMES = {
    "food": "食品衛生法等許可施設一覧（2026(令和8)年3月中）",
    "barber": "理容所施設一覧（2026(令和8)年8月31日時点）",
    "beauty": "美容所施設一覧（2026(令和8)年8月31日時点）",
}
# The old-law list keeps a permit until its next yearly edition even after its
# 許可終了日 has passed, so step 2 drops rows past expiry against this PINNED
# date, MHLW's end of August 2026 (japan_register.in_term), never today:
# 2,417 of 3,383 rows are in term on it, 966 dropped (measured 2026-10-02).
OLD_LAW_AS_OF = datetime.date(2026, 8, 31)
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: MHLW's file is UTF-8 with a BOM; the old-law list
# an XLSX (one sheet, header on row 1); the two registers cp932 CSV (a line
# break inside the header cell 許可（確認）年月日).
SOURCE_ENCODING = {"mhlw": "utf-8-sig", "food": "xlsx", "barber": "cp932", "beauty": "cp932"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 営業者氏名 and 代表者氏名 (all three city files) are
# REQUIRED so the name rule (japan_register.name_is_operator; owner
# 2026-09-27) cannot silently compare nothing; they are read IN MEMORY by that
# rule only, never kept. Never selected: 代表者肩書 / 肩書, the permit numbers,
# and MHLW's 法人名 / 法人番号 / 法人住所 and phones.
_REGISTER = ("施設名称", "施設所在地", "業種", "営業者氏名", "代表者氏名")
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
    "food": ("屋号名称", "営業所所在地", "営業の種類", "営業者氏名", "代表者氏名", "許可終了日"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses an MHLW row, MHLW's own point places it (the
# brief's check: a median 32 m from the block point, 97.6% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# One premises in both food lists: the city's old-law row goes, MHLW's (the
# newer filing) stays. The brief's screen: 71 of the 1,582 old-law
# restaurants in term share a block and trade name with an MHLW permit.
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    The old-law food list only where its permit is in term on OLD_LAW_AS_OF
    (許可終了日); every other file as it is."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    rows = jr.city_rows(path)
    if key == "food":
        rows = jr.in_term(rows, ("許可終了日",), OLD_LAW_AS_OF)
    yield from rows


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Kitakyushu.
# S, W, N, E: the city's N03 extent (S 33.721, W 130.673, N 34.022, E 131.039)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (33.71, 130.66, 34.04, 131.05)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen, no apostrophe before n (Fukuoka's Gannosu). OSM's
# Kitakyushu names carry macrons and run words together; the other 37 are
# OSM's as they stand. JR's and the Monorail's 城野 and 志井 are separate N02
# groups (MLIT keeps them apart, trap 1), so step 1 appends their operators.
OSM_NAME_EN_OVERRIDES = {
    "安部山公園": "Abeyama-koen",                    # Abeyamakōen
    "穴生": "Ano",                                   # Anō
    "筑豊香月": "Chikuho-Katsuki",                   # Chikuhō-Katsuki
    "平和通": "Heiwadori",                           # Heiwadōri
    "本城": "Honjo",                                 # Honjō
    "陣原": "Jinnoharu",                             # Jin'noharu
    "城野": "Jono",                                  # Jōno (both groups)
    "香春口三萩野": "Kawaraguchi-Mihagino",           # Kawaraguchi Mihagino
    "競馬場前": "Keibajo-mae",                        # Keibajōmae
    "九州工大前": "Kyushu-kodai-mae",                 # Kyūshūkōdaimae
    "門司港": "Mojiko",                              # Mojikō
    "奥洞海": "Okudokai",                            # Okudōkai
    "志井公園": "Shii-koen",                         # Shii-Kōen
    "徳力嵐山口": "Tokuriki-Arashiyamaguchi",         # Tokuriki Arashiyamaguchi
    "徳力公団前": "Tokuriki-kodan-mae",               # Tokuriki Kōdanmae
    "黒崎駅前": "Kurosaki-ekimae",                    # Kurosaki-Ekimae
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 52N: the longitude (~130.88) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 9 lines, no Shinkansen; 小倉 stays as a JR and Monorail
# station). The Monorail lies wholly inside (13 of 13); the Chikuho line keeps
# 14 of 21 (13 of 20 once 西黒崎 is out); JR's Kagoshima (16 of 99), Nippo (7 of
# 113), Hitahikosan (6 of 24) and Chikuho (6 of 26) lines are cut at the city
# line (owner 2026-09-24). JR Kyushu's Sanyo Line keeps one station (門司, of
# 2): a one-station stub stays as cut (Kobe's JR Takarazuka Line, owner
# 2026-09-27).
LEFT_OUT_LINES = {
    # A sightseeing funicular up Mt Sarakura (Kobe's Maya and Rokko, owner
    # 2026-09-27): never in excluded_stations.csv; the page says so.
    ("皿倉登山鉄道", "帆柱ケーブル線"): "a sightseeing funicular (Kobe's rule)",
    # A seasonal sightseeing trolley on weekends and holidays, Mojiko to
    # Kanmonkaikyo-Mekari: left out on Kyoto's Sagano precedent, with a page
    # bullet under The lines.
    ("平成筑豊鉄道", "門司港レトロ観光線"): "a seasonal sightseeing line (Kyoto's Sagano precedent)",
}
# A station N02-25 still has but the operator has closed (japan_step1).
CLOSED_STATIONS = {
    ("筑豊電気鉄道", "筑豊電気鉄道線", "西黒崎"):
        "closed 2026-07-31 (the operator's notice, chikutetsu.co.jp/data/topics/408_20260528nishikurosakihaishi.pdf)",
}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names follow JR Kyushu's signs (no
# macrons), as the station names follow OSM's.
_MO, _CT, _JR = "北九州高速鉄道", "筑豊電気鉄道", "九州旅客鉄道"
LINES = {
    "MO": {"n02": [(_MO, "小倉線")], "name": "Kitakyushu Monorail", "name_ja": "北九州モノレール",
           "short": "Monorail", "hue": "#0072BC"},
    "CT": {"n02": [(_CT, "筑豊電気鉄道線")], "name": "Chikuho Electric Railroad", "name_ja": "筑豊電気鉄道線",
           "short": "Chikutetsu", "hue": "#E4007F"},
    "JK": {"n02": [(_JR, "鹿児島線")], "name": "JR Kagoshima Main Line", "name_ja": "鹿児島本線", "short": "JR",
           "hue": "#E60012"},
    "JN": {"n02": [(_JR, "日豊線")], "name": "JR Nippo Main Line", "name_ja": "日豊本線", "short": "JR",
           "hue": "#0068B7"},
    "JH": {"n02": [(_JR, "日田彦山線")], "name": "JR Hitahikosan Line", "name_ja": "日田彦山線", "short": "JR",
           "hue": "#009944"},
    "JW": {"n02": [], "name": "JR Wakamatsu Line", "name_ja": "若松線", "short": "JR", "hue": "#F39800"},
    "JF": {"n02": [(_JR, "筑豊線")], "name": "JR Fukuhoku Yutaka Line", "name_ja": "福北ゆたか線", "short": "JR",
           "hue": "#8F2E14"},
    "JS": {"n02": [(_JR, "山陽線")], "name": "JR Sanyo Line", "name_ja": "山陽本線", "short": "JR", "hue": "#7F7F7F"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# kitakyushu` (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its operator's hue that reads 3:1 on both
# map pages and clears CIE76 45 from every pin. The Monorail's blue, which no
# blue clears Retail's pin in, goes teal and JR's Nippo blue slate; the Sanyo
# stub, which JR Kyushu gives no colour, is gray. Closest pair within 500 m
# 28.0 (Nippo / Monorail), anywhere 18.4 (Nippo / Sanyo); the dark-mode labels
# separate, 8 of 8.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "MO": "#08A0C0", "CT": "#F000B8", "JK": line_registry.colour("jr-kyushu-kagoshima-main-line"),
    "JN": line_registry.colour("jr-kyushu-nippo-main-line"), "JH": "#30A800", "JW": "#D08000",
    "JF": line_registry.colour("jr-kyushu-fukuhoku-yutaka-line"),
    "JS": line_registry.colour("jr-west-sanyo-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
# N02 files JR Kyushu's 筑豊本線 as one line, 若松 to 原田. Its in-city part,
# 若松 to 折尾, is the line JR Kyushu signs as the Wakamatsu Line (若松線);
# beyond 折尾 it is the Fukuhoku Yutaka Line (福北ゆたか線), which keeps one
# station inside the city (折尾) and stays as cut, as Fukuoka's.
BRANCHES = {
    "JW": {"line": (_JR, "筑豊線"), "terminus": "若松", "junction": "折尾",
           "stations": ["若松", "藤ノ木", "奥洞海", "二島", "本城"], "length_m": (8000, 13000)},
}

# Gate 3: the operator's own station count for the line wholly inside the
# city: Kitakyushu Monorail's site lists 13 stations, 小倉 to 企救丘 (read
# 2026-10-02). The Chikuho line's 13 in-city stops (20 on the operator's list
# since 西黒崎 closed) are N02's less 西黒崎; the lines the city line cuts have
# no in-city count of their own.
GATE3 = {"source": "Kitakyushu Monorail's station list (kitakyushu-monorail.co.jp)", "lines": {"MO": 13}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KITAKYUSHU_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KITAKYUSHU_BBOX
