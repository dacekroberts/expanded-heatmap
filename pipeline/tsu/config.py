"""Tsu-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/tsu.md
(6/6 checks, 2026-10-07). Japan's A/B batch (Regional-1), on the shared
modules (pipeline/countries/japan*.py) with the Japan foundation's rules on
(2026-10-07), in Yokkaichi's shape (a standing list per kind, one
municipality, no wards) with Uji's one difference: the lists are the
prefecture's, so every row is assigned to Tsu by its address (source_rows).

Business leg: Mie Prefecture's three monthly standing lists on BODIK
(organisation 240001, CC BY 4.0 by the 三重県オープンデータ利用規約 第１条; read
2026-10-07 by staging), as of 2026-08-31: every food permit (食品営業許可施設)
and the barber (理容所届出施設) and beauty-salon (美容所届出施設) registers,
covering the prefecture except Yokkaichi, cut to Tsu by address and placed by
a JOIN to MLIT's 位置参照情報 (one municipality, no wards). No laundry list
exists (a disclosed gap). MHLW's open data for Mie (24000) is a control only,
never read by a step: 0 open restaurant permits, and its 159 Tsu retail
notifications too thin for a layer (Iwaki's call 150).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR Central's Kisei and Meisho lines, Kintetsu's Nagoya and Osaka lines
and the Ise Railway's Ise Line. English station names from OpenStreetMap's
name:en.
"""

import unicodedata
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "tsu" / "raw"
DATA_PROCESSED = ROOT / "data" / "tsu" / "processed"
OUTPUTS = ROOT / "outputs" / "tsu"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Tsu"
SLUG = "tsu"
MUNICIPALITY = "津市"
PREFECTURE = "三重県"

# Mie Prefecture's lists on BODIK (data.bodik.jp, the prefecture's catalogue
# odcs.bodik.jp/240001, author 医療保健部食品安全課), each package license_id
# cc-by-40-intl; the 三重県オープンデータ利用規約 (odcs.bodik.jp/240001/tos/)
# 第１条 licenses them under CC BY 4.0 and no resource sets its own licence
# (read 2026-10-07 by staging). All three resources are published as
# .../download/202608.xlsx, so each is saved under its own name, as Toyota's.
# The edition is pinned: a re-fetch is a new build (BODIK is never called
# beyond the cached files in this batch).
BODIK = "https://data.bodik.jp/dataset"
CATALOGUE = "https://odcs.bodik.jp/240001/"
TERMS = "https://odcs.bodik.jp/240001/tos/"
FOOD_PAGE = BODIK + "/240001_food_business_all"
BARBER_PAGE = BODIK + "/240001_barbar"
BEAUTY_PAGE = BODIK + "/240001_hair_dressing"
# source key -> (file, URL of the edition this build read, the dataset page
# that carries its licence). Each URL names the package by its name, which
# CKAN resolves as it does the id, and the resource by its id (the brief's
# package_search check, 2026-10-06, reads all three resource ids).
SOURCE_FILES = {
    "food": ("food_202608.xlsx",
             FOOD_PAGE + "/resource/fc9fba2d-e6f7-4139-ba20-3e572ba99572/download/202608.xlsx", FOOD_PAGE),
    "barber": ("riyo_202608.xlsx",
               BARBER_PAGE + "/resource/8a273176-3714-46de-ba68-aeb2b5742c09/download/202608.xlsx", BARBER_PAGE),
    "beauty": ("biyo_202608.xlsx",
               BEAUTY_PAGE + "/resource/2a625a1b-2efe-4876-9859-49ad35363608/download/202608.xlsx", BEAUTY_PAGE),
}
# The dates the lists state (Kyoto's rule, never the download's): each
# dataset reads 「※現在は令和８年８月末までのデータを掲載しています」, and all
# three were uploaded 2026-09-15. The food list carries only 初許可日 (no
# term, no status), so no TERM_AS_OF applies.
SOURCE_AS_OF = {k: "2026-08-31" for k in SOURCE_FILES}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: three XLSX workbooks, one sheet each
# (【オープンデータ（県庁）】...), the header on row 1, every cell a string.
SOURCE_ENCODING = {k: "xlsx" for k in SOURCES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns (the food list's 営業者氏名, the
# registers' 開設者氏名; a sole trader's own name on most rows without a company
# marker) are REQUIRED so the name rule (japan_register.name_is_operator;
# owner 2026-09-27) cannot silently compare nothing; they are read IN MEMORY
# by that rule only, never kept. Never selected: 営業所電話番号 and
# 施設電話番号.
REQUIRED_COLUMNS = {
    "food": ("業種", "業態", "営業者氏名", "営業所住所", "営業所屋号", "初許可日"),
    "barber": ("開設者氏名", "施設住所", "屋号", "確認年月日"),
    "beauty": ("開設者氏名", "施設住所", "屋号", "確認年月日"),
}

# --- Cutting Tsu out of the prefecture's lists -----------------------------
# The lists cover Mie except Yokkaichi and carry no municipality column. A
# row is Tsu's where its address (NFKC, spaces removed, the prefecture
# dropped) begins 津市, or 久居: Hisai City (久居市), wholly merged into Tsu in
# 2006, its towns now Tsu's 久居...町 in MLIT's file; 4 beauty rows are written
# so (三重県久居中町, 三重県久居市明神町 ...), read as Tsu's as Matsue's 八雲村
# is read as its own town (the Japan foundation, 2026-10-07). Measured
# 2026-10-07: food 2,924 of 18,680 (all begin 津市; 196 prefecture rows carry
# no address), barbers 251 of 1,523, beauty 705 of 3,853 (the brief's 701
# plus the 4 Hisai rows). The shared other_muni rule alone is not the cut: it
# keeps the 196 unaddressed food rows, 10 三重県一円 register rows and 2
# registered elsewhere under district names (多気郡, 志摩郡) as Tsu's.
_OWN_PREFIXES = (MUNICIPALITY, "久居")


def _address(r):
    from pipeline.countries import japan_register as jr

    addr = next((r[c] for c in jr.ADDR_COLS if (r.get(c) or "").strip()), "")
    a = unicodedata.normalize("NFKC", addr).replace(" ", "").replace("　", "")
    return a[len(PREFECTURE):] if a.startswith(PREFECTURE) else a


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's Tsu rows (japan_step2 reads this hook where a city defines
    it): the prefecture's file, kept where the address begins with Tsu's
    name or Hisai's (_OWN_PREFIXES). A row that names 津市 anywhere else in
    its address stops the build: the cut would be missing a row of the city."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        a = _address(r)
        if a.startswith(_OWN_PREFIXES):
            yield r
        elif MUNICIPALITY in a:
            raise SystemExit(f"{key}: an address names {MUNICIPALITY} but does not begin with it; "
                             "the cut by prefix would miss it")


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 24201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Tsu.
# S, W, N, E: the city's N03 extent (S 34.4474, W 136.1597, N 34.8445,
# E 136.5705; the 2006 merger reached the hills of 美杉) rounded out; step 1
# stops if the city leaves it.
OSM_BBOX = (34.44, 136.15, 34.85, 136.58)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (no macrons; a place name after a hyphen
# keeps its capital, as Kodo-Homachigawa). OSM's 67 objects all carry
# name:en; the other 32 of the 33 stations' names stand as OSM has them.
# 川合高岡 (Kintetsu) and 一志 (JR) are separate N02 groups 179 m apart,
# separate stations of different names (Kobe's Tarumi case): kept apart.
OSM_NAME_EN_OVERRIDES = {
    "伊勢大井": "Ise-Oi",                              # Ise-Ōi
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the city centre (~136.51) and the whole N03 extent (136.1597
# to 136.5705) fall in the 132 to 138 band. Derived per city, not copied -
# see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median nearest-group gap is
# 1,432 m (179 to 3,120): standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 5 legal lines, no Shinkansen; the brief's table exactly). Every
# line is cut at the city line (owner 2026-09-24): JR's 名松線 keeps 12 of 15
# (to its terminus 伊勢奥津), Kintetsu's 名古屋線 10 of 44 and 大阪線 5 of 49,
# JR's 紀勢線 4 of 41 and the Ise Railway 4 of 10 (to its terminus 津). No
# line is urban and none is cut to one station: five lines are drawn. No
# frequency floor (owner, 2026-10-06, calls 46 and 86): the Meisho Line's
# low-frequency stretch is drawn and named on the page.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names follow the operators' signs
# with no macrons, as Yokkaichi's (JR Central's "Kansai Line" for 関西本線,
# so "Kisei Line" for 紀勢本線).
_JR, _KT = "東海旅客鉄道", "近畿日本鉄道"
LINES = {
    "KN": {"n02": [(_KT, "名古屋線")], "name": "Kintetsu Nagoya Line", "name_ja": "近鉄名古屋線",
           "short": "Kintetsu", "hue": "#E2001A"},
    "KO": {"n02": [(_KT, "大阪線")], "name": "Kintetsu Osaka Line", "name_ja": "近鉄大阪線",
           "short": "Kintetsu", "hue": "#E2001A"},
    "JK": {"n02": [(_JR, "紀勢線")], "name": "JR Kisei Line", "name_ja": "紀勢本線", "short": "JR",
           "hue": "#F77321"},
    "JM": {"n02": [(_JR, "名松線")], "name": "JR Meisho Line", "name_ja": "名松線", "short": "JR",
           "hue": "#F77321"},
    "IS": {"n02": [("伊勢鉄道", "伊勢線")], "name": "Ise Railway Ise Line", "name_ja": "伊勢線",
           "short": "Ise Railway", "hue": "#004EA2"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py tsu`
# (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each the
# feasible colour nearest its operator's hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. Kintetsu's red stays on the Nagoya Line
# and warms to vermilion on the Osaka Line; JR Central's orange darkens to
# burnt orange on the Meisho Line; the Ise Railway's blue, which no blue
# clears Retail's pin in, goes purple (Yokkaichi's). Closest pair within
# 500 m 18.3 (Kintetsu's two), anywhere 10.8 (JR's two, never within 500 m);
# the dark-mode labels separate, 5 of 5.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "KN": line_registry.colour("kintetsu-nagoya-line"), "KO": line_registry.colour("kintetsu-osaka-line"),
    "JK": "#E86810", "JM": "#C85000", "IS": line_registry.colour("ise-railway-ise-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city, so no line has an in-city
# count of its own; N02's network totals are the operators' (the Meisho
# Line's 15 stations 松阪 to 伊勢奥津, the Ise Railway's 10 河原田 to 津).
GATE3 = {"source": "none: no line is wholly inside the city (N02's totals match JR Central's Meisho Line 15 and "
                   "the Ise Railway's 10)", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
TSU_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = TSU_BBOX
