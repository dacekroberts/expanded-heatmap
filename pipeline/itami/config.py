"""Itami-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/itami.md.
Japan A/B batch (Kansai-1, 2026-10-07), on the shared modules
(pipeline/countries/japan*.py) and the Japan foundation's rules (ALL_RULES).

Business leg: Hyōgo Prefecture's 生活衛生課 lists, which cover the prefecture
less its five health-centre cities (Kobe, Himeji, Amagasaki, Akashi,
Nishinomiya), so Itami is in them: the food permit list (every permit in term,
old and new law), the food notification list (the Food-shops layer, owner call
164, Yokkaichi's precedent), and the barber, beauty-salon and laundry
registers, all as of 2026-08-31. Every row is assigned to Itami BY ITS ADDRESS
(Tsu's shape): one that begins 伊丹市, after 兵庫県 is cut. Placed by a JOIN to
MLIT's 位置参照情報 for the one municipality (28207, no wards). MHLW's file for
the prefecture (28000) is a control only: its 市区町村名 is the prefectural
seat on every row.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Hankyu's Itami Line, JR West's Takarazuka Line and the Osaka Monorail
(its one station, 大阪空港, drawn cut: owner call 163), cut at the city line.
English station names from OpenStreetMap's name:en.
"""

import unicodedata
from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "itami" / "raw"
DATA_PROCESSED = ROOT / "data" / "itami" / "processed"
OUTPUTS = ROOT / "outputs" / "itami"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Itami"
SLUG = "itami"
MUNICIPALITY = "伊丹市"
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
    the prefecture's list cut to the rows whose address begins 伊丹市, once
    兵庫県 is cut (the brief: 2 food rows carry it, none of them Itami's). A
    row that names 伊丹市 anywhere else stops the build (Tsu's rule): its
    municipality would be a guess. The 県下一円 permits (vehicles and stalls
    licensed across the jurisdiction) belong to no town and are not Itami's."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        a = _address(r)
        if a.startswith(MUNICIPALITY):
            yield r
        elif MUNICIPALITY in a and not a.endswith("一円"):
            # An area licensed across several towns is no premises in any of
            # them (Kakogawa's 3 vehicle notifications): passed over.
            raise SystemExit(f"{path.name}: a row names {MUNICIPALITY} after its start - assign it by hand")


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 28207.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Itami.
# S, W, N, E: the city's N03 extent (S 34.757, W 135.370, N 34.816, E 135.446)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.75, 135.36, 34.82, 135.45)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word (2026-10-07: 17 objects). OSM
# translates 大阪空港, which is romanized as Fukuoka's 福岡空港 was; the other 3
# are OSM's as they stand.
OSM_NAME_EN_OVERRIDES = {
    "新伊丹": "Shin-Itami",                          # Shinitami
    "大阪空港": "Osaka-kuko",                        # Osaka Airport
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.41) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-group gap is 810 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# the brief: 3 lines, no Shinkansen), each cut at the city line (owner
# 2026-09-24): Hankyu's 伊丹線 (3 of 4), JR West's 福知山線, signed the JR
# Takarazuka Line (2 of 30), and the Osaka Monorail (1 of 14: 大阪空港, its
# terminus 21 m inside the line). The Monorail is an urban line cut to one
# station that no other line serves, so it is drawn cut (owner, call 163;
# calls 54 and 92).
LEFT_OUT_LINES = {}
# The Monorail runs on into Osaka Prefecture (Toyonaka): its N03 names the
# stations beyond the prefecture line (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("27",)
# JR 伊丹 and Hankyu 伊丹 are separate stations 740 m apart, kept apart as N02
# keeps them (trap 1); their English names take the operator.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02's 福知山線 is signed the JR Takarazuka
# Line (JR宝塚線), as on Osaka's and Nishinomiya's maps.
_HK, _JR, _MO = "阪急電鉄", "西日本旅客鉄道", "大阪モノレール"
LINES = {
    "HI": {"n02": [(_HK, "伊丹線")], "name": "Hankyu Itami Line", "name_ja": "阪急伊丹線", "short": "Hankyu",
           "hue": "#B7572D"},
    "JT": {"n02": [(_JR, "福知山線")], "name": "JR Takarazuka Line", "name_ja": "JR宝塚線", "short": "JR",
           "hue": "#A8903C"},
    "MO": {"n02": [(_MO, "大阪モノレール線")], "name": "Osaka Monorail Main Line", "name_ja": "大阪モノレール本線",
           "short": "Monorail", "hue": "#0067B0"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# itami` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each the
# feasible colour nearest its start (Hankyu from Osaka's Takarazuka colour, as
# Toyonaka's, the JR Takarazuka Line from Kobe's, the Monorail from its hue)
# that reads 3:1 on both map pages and clears CIE76 45 from every pin; the
# Hankyu and Monorail colours are Toyonaka's. Closest pair anywhere 34.9; the
# dark-mode labels separate, 3 of 3.
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search: the JR
# Takarazuka Line's #A09808 sat 16.7 from it, under the owner's floor of 20
# (2026-10-07), and takes Kobe's new colour for the same line, #A8903C (olive
# 20.1, between 20 and 45: an accepted trade; Kobe's config gives the
# search). Its start hue follows. Closest pair now 38.1.
_COLOURS = {"HI": "#C06038", "JT": "#A8903C", "MO": "#007890"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the Hankyu Itami Line's own station list (4 stations, 塚口 the
# junction in Amagasaki, so 3 inside: 稲野, 新伊丹, 伊丹); JR's and the
# Monorail's in-city stations are N02's.
GATE3 = {"source": "Hankyu's Itami Line station list (4 stations; 塚口 is in Amagasaki)",
         "lines": {"HI": 3}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
ITAMI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = ITAMI_BBOX
