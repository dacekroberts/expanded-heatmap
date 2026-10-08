"""Kakogawa-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/kakogawa.md.
Japan A/B batch (Kansai-1, 2026-10-07), on the shared modules
(pipeline/countries/japan*.py) and the Japan foundation's rules (ALL_RULES).

Business leg: Hyōgo Prefecture's 生活衛生課 lists, which cover the prefecture
less its five health-centre cities (Kobe, Himeji, Amagasaki, Akashi,
Nishinomiya), so Kakogawa is in them: the food permit list (every permit in term,
old and new law), the food notification list (the Food-shops layer, owner call
164, Yokkaichi's precedent), and the barber, beauty-salon and laundry
registers, all as of 2026-08-31. Every row is assigned to Kakogawa BY ITS ADDRESS
(Tsu's shape): one that begins 加古川市, after 兵庫県 is cut. Placed by a JOIN to
MLIT's 位置参照情報 for the one municipality (28210, no wards). MHLW's file for
the prefecture (28000) is a control only: its 市区町村名 is the prefectural
seat on every row.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR West's Kobe and Kakogawa lines and the Sanyo Electric Railway's Main
Line, cut at the city line. English station names from OpenStreetMap's
name:en.

The block join is lower than elsewhere (the brief: 86.5% block, 13.3% at the
town-chōme centroid): built with the tiers disclosed (owner, call 145).
"""

import unicodedata
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kakogawa" / "raw"
DATA_PROCESSED = ROOT / "data" / "kakogawa" / "processed"
OUTPUTS = ROOT / "outputs" / "kakogawa"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kakogawa"
SLUG = "kakogawa"
MUNICIPALITY = "加古川市"
PREFECTURE = "兵庫県"

# Hyōgo Prefecture's catalogue (web.pref.hyogo.lg.jp/opendata/index.php)
# lists the three registers with a CC BY licence, and the food lists' page
# under CC BY; the catalogue terms (kiyaku_opendata.pdf) 3(3) license its
# works under CC BY 4.0 and 2(1) put them above the site's copyright page
# (read 2026-10-07; the food files on Ōtsu's precedent, docs/decisions_drafts/
# worktree-japan-kansai-1.md). The file names never change: each month's
# edition replaces the last at the same URL.
_FILES = "https://web.pref.hyogo.lg.jp/kf14/documents/"
FOOD_PAGE = "https://web.pref.hyogo.lg.jp/kf14/shokuhineigyoushisetsu_list.html"
ENV_PAGE = "https://web.pref.hyogo.lg.jp/kf14/kankyoueigyoushisetsu_list.html"
SOURCE_FILES = {
    # 許可営業施設 (the publisher's spelling, "lisence")
    "food": ("000028_food_business_lisence_all.xlsx", _FILES + "000028_food_business_lisence_all.xlsx", FOOD_PAGE),
    # 届出営業施設
    "notify": ("000028_food_business_notification_all.xlsx",
               _FILES + "000028_food_business_notification_all.xlsx", FOOD_PAGE),
    "barber": ("000028_barbershop_all.xlsx", _FILES + "000028_barbershop_all.xlsx", ENV_PAGE),
    "beauty": ("000028_beauty_salon_all.xlsx", _FILES + "000028_beauty_salon_all.xlsx", ENV_PAGE),
    "laundry": ("000028_cleaningbusiness_all.xlsx", _FILES + "000028_cleaningbusiness_all.xlsx", ENV_PAGE),
}
# The pages' edition lines (Kyoto's rule, never the download's): the food
# lists 「令和8年8月までのリスト（令和8年9月15日更新）」, the registers
# 「令和8年8月末時点のリスト（令和8年9月10日更新）」. A new edition replaces the
# file at the same URL: re-measure then.
SOURCE_AS_OF = {k: "2026-08-31" for k in SOURCE_FILES}
FOOD_AS_OF = "2026-08-31"
# The food list carries each permit's 有効期限: the term rules (calls 161 and
# 172) read it against the list's own date, never today. Hyōgo ends every
# permit on the last day of February, May, August or November, so nothing in
# the list lapsed before 2026-11-30 (the brief).
TERM_AS_OF = {"food": "2026-08-31"}
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# The notification list is a food list too: japan_eigyo reads its types
# (Yokkaichi's).
SOURCE_KIND = {"notify": "food"}
SOURCE_ENCODING = {k: "xlsx" for k in SOURCE_FILES}
# The columns each file must carry, as city_rows reads them (the registers'
# header numbers each column with a leading circled numeral, ①営業所名称,
# which japan_register strips). 営業者氏名 (a company's representative or the
# sole trader, filled on every row), 営業者法人名称 and the registers'
# 代表者氏名 are REQUIRED so the name rule cannot silently compare nothing;
# they are read IN MEMORY by that rule only, never kept. Never selected:
# 営業所電話番号, 営業者住所, 営業者電話番号, 営業者役職 / 役職.
_FOOD = ("営業所名称", "営業所所在地", "業種", "形態", "営業者法人名称", "営業者氏名")
_REG = ("営業所名称", "営業所所在地", "営業の種類", "営業者氏名", "代表者氏名")
REQUIRED_COLUMNS = {
    "food": _FOOD + ("許可番号", "許可日", "有効期限"),
    "notify": _FOOD + ("届出番号",),
    "barber": _REG,
    "beauty": _REG,
    "laundry": _REG,
}


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def _address(r):
    a = unicodedata.normalize("NFKC", (r.get("営業所所在地") or "")).replace(" ", "").replace("　", "")
    return a[len(PREFECTURE):] if a.startswith(PREFECTURE) else a


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    the prefecture's list cut to the rows whose address begins 加古川市, once
    兵庫県 is cut (the brief: 2 food rows carry it prefecture-wide). A
    row that names 加古川市 anywhere else stops the build (Tsu's rule): its
    municipality would be a guess. The 県下一円 permits (vehicles and stalls
    licensed across the jurisdiction) belong to no town and are not Kakogawa's;
    the neighbouring towns 稲美町 and 播磨町 are written 加古郡… and never match."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        a = _address(r)
        if a.startswith(MUNICIPALITY):
            yield r
        elif MUNICIPALITY in a and not a.endswith("一円"):
            # An area licensed across several towns (3 vehicle notifications,
            # 「たつの市、高砂市、加古川市内一円」, 2026-10-07) is no premises in
            # any of them: passed over, as every 一円 row is set aside.
            raise SystemExit(f"{path.name}: a row names {MUNICIPALITY} after its start - assign it by hand")


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 28210.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Kakogawa.
# S, W, N, E: the city's N03 extent (S 34.698, W 134.764, N 34.867, E 134.936)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.69, 134.75, 34.88, 134.95)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word (2026-10-07: 32 objects). The
# other 7 are OSM's as they stand.
OSM_NAME_EN_OVERRIDES = {
    "東加古川": "Higashi-Kakogawa",                  # Higashi Kakogawa
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~134.85) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-group gap is 2,019 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# the brief: 3 lines, no Shinkansen station inside), each cut at the city line
# (owner 2026-09-24): JR West's 山陽線, signed the JR Kobe Line east of 姫路
# (2 of 131: 東加古川, 加古川), its 加古川線 (4 of 21: 加古川, 日岡, 神野, 厄神)
# and the Sanyo Electric Railway's 本線 (3 of 43: 別府, 浜の宮, 尾上の松). 宝殿
# lies 38 m beyond the city line (Takasago by N03 and by JR West's own station
# page) and 土山 182 m beyond (Harima). No line is cut to one station.
LEFT_OUT_LINES = {}
# JR's Sanyo Line runs on into Okayama and Osaka: their N03 is not read, and
# step 1 names the stations beyond by the municipalities of Hyōgo it reaches.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02's 山陽線 east of 姫路 is signed the JR
# Kobe Line (JR神戸線), as on Himeji's and Kobe's maps; the stretch drawn here
# is the in-city one, so no route split is needed (Himeji's split is at 姫路).
_JR, _SY = "西日本旅客鉄道", "山陽電気鉄道"
LINES = {
    "JA": {"n02": [(_JR, "山陽線")], "name": "JR Kobe Line", "name_ja": "JR神戸線", "short": "JR",
           "hue": "#08A0C0"},
    "JG": {"n02": [(_JR, "加古川線")], "name": "JR Kakogawa Line", "name_ja": "加古川線", "short": "JR",
           "hue": "#00A040"},
    "SM": {"n02": [(_SY, "本線")], "name": "Sanyo Electric Main Line", "name_ja": "山陽電鉄本線",
           "short": "Sanyo", "hue": "#D01810"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# kakogawa` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): the
# JR Kobe Line and the Sanyo Main Line keep Himeji's colours, the Kakogawa Line
# the feasible green nearest its start; each reads 3:1 on both map pages and
# clears CIE76 45 from every pin. Closest pair 94.8 (the two JR lines, at
# 加古川); the dark-mode labels separate, 3 of 3.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "JA": line_registry.colour("jr-west-kobe-line"), "JG": "#28A800",
    "SM": line_registry.colour("sanyo-electric-main-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city; step 1 lists each line's
# in-city stations.
GATE3 = {"source": "no line wholly inside the city", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KAKOGAWA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KAKOGAWA_BBOX
