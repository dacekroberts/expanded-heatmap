"""Amagasaki-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/amagasaki.md.
Japan A/B batch (Kansai-1, 2026-10-07), on the shared modules
(pipeline/countries/japan*.py) and the Japan foundation's rules (ALL_RULES).

Business leg: the city's own open data (生活衛生課, CC BY 4.0 by each page and
尼崎市オープンデータ利用規約 §2), five CSVs as of 2026-08-31: every food permit
in term (Akita's shape), every food notification (届出; its food-retail types
count as Food shops, Yokkaichi's precedent and owner call 164), and the
barber, beauty-salon and laundry registers (one file per kind, Hamamatsu's
shape). All placed by a JOIN to MLIT's 位置参照情報 for the one municipality
(28202, no wards). MHLW's open data for 28202 holds 2% of the city's permits:
a control, never a source (Kawasaki's precedent; call 126).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Hanshin's Main and Namba Lines, JR West's Kobe, Takarazuka and Tozai
Lines and Hankyu's Kobe and Itami Lines, every one cut at the city line.
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "amagasaki" / "raw"
DATA_PROCESSED = ROOT / "data" / "amagasaki" / "processed"
OUTPUTS = ROOT / "outputs" / "amagasaki"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Amagasaki"
SLUG = "amagasaki"
MUNICIPALITY = "尼崎市"
PREFECTURE = "兵庫県"

# The city's own CMS (no catalogue API): each dataset is a page under
# /op_data/1000922/ that states CC BY 4.0 and links its files; the city's
# terms (尼崎市オープンデータ利用規約 §2) apply CC BY 4.0, which needs the
# source and that it was modified (read 2026-10-07).
SITE = "https://www.city.amagasaki.hyogo.jp"
TERMS = SITE + "/opendata/1000081/1000084.html"
_FILES = SITE + "/_res/projects/default_project/_page_/001/001/"


def _page(n):
    return f"{SITE}/op_data/1000922/{n}.html"


# source key -> (file, URL of the edition this build read, the page that links
# it and carries its licence). Page 1001025 is 食品関係営業施設 (both food
# lists), 1001026 to 1001028 the 検査確認済施設一覧 of barbers, beauty salons
# and laundries.
SOURCE_FILES = {
    "food": ("kyoka202608.csv", _FILES + "025/kyoka202608.csv", _page(1001025)),
    "notify": ("todoke202608.csv", _FILES + "025/todoke202608.csv", _page(1001025)),
    "barber": ("riyouR80831.csv", _FILES + "026/riyouR80831.csv", _page(1001026)),
    "beauty": ("biyouR80831.csv", _FILES + "027/biyouR80831.csv", _page(1001027)),
    "laundry": ("cleaningR80831.csv", _FILES + "028/cleaningR80831.csv", _page(1001028)),
}
# The two food lists are named by month (kyoka202608, todoke202608), so
# fetch_sources.py reads the current link from the page (Kawasaki's and
# Otsu's precedent) and the pinned URL records which edition the build read.
# The registers carry their date in the name (R80831) and are pinned: a new
# edition is a brief to correct.
SOURCE_LINKS = {"food": r"/kyoka\d{6}\.csv$", "notify": r"/todoke\d{6}\.csv$"}
# The dates the lists state (Kyoto's rule, never the download's): the food
# files' 【令和8年(2026年）8月31日現在】 and the registers' 令和8年8月31日現在.
SOURCE_AS_OF = {k: "2026-08-31" for k in SOURCE_FILES}
FOOD_AS_OF = SOURCE_AS_OF["food"]
# The permit term rules (calls 161 and 172) read the food permits against
# this date, never today. 174 restaurant permits end on 2026-08-31 itself:
# in term on the list's date, so kept (the brief).
TERM_AS_OF = {"food": FOOD_AS_OF}
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# The notification list is a food list too: japan_eigyo reads its types
# (その他の食料・飲料販売業, コンビニエンスストア, 乳類販売業 ...) as food ones.
SOURCE_KIND = {"notify": "food"}
# Declared, never inferred: all five UTF-8 with a BOM, comma CSV, CRLF.
SOURCE_ENCODING = {k: "utf-8-sig" for k in SOURCES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns (the food lists' 申請者名 and
# 代表者名, the registers' 申請者名) are REQUIRED so the name rule
# (japan_register.name_is_operator) cannot silently compare nothing; they are
# read IN MEMORY by that rule only, never kept. Never selected: 申請者住所 /
# 開設者住所 / 開設者住所１ / 営業者住所１ (operators' own addresses), every
# 電話番号, 自動車登録番号 and the permit and inspection numbers.
REQUIRED_COLUMNS = {
    "food": ("施設名称", "施設所在地", "申請者名", "代表者名", "許可年月日", "許可終了日", "業種", "業態",
             "自動車登録番号"),
    "notify": ("施設名称", "施設所在地", "申請者名", "代表者名", "届出年月日", "業態"),
    "barber": ("施設名称", "施設所在地", "申請者名", "業務種別"),
    "beauty": ("施設名称", "施設所在地", "申請者名", "業務種別"),
    # クリーニング種別１ (取次所, 一般クリーニング所, 無店舗取次店) is the kind,
    # read ahead of 業務種別 (クリーニング所 on every row) by the shared
    # "type_cols5" rule, so the 4 無店舗取次店 are not premises.
    "laundry": ("施設名称１", "施設所在地１", "申請者名", "業務種別", "クリーニング種別１"),
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    each file as it stands, except the notification list, which has no 業種
    and carries its type in 業態; that value is copied into 業種 so the type
    reads it (Yokkaichi's notifications read as types), and 業態 stays as the
    form beside it."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        if key == "notify":
            r = {**r, "業種": r.get("業態")}
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 28202.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Amagasaki.
# S, W, N, E: the city's N03 extent (S 34.677, W 135.369, N 34.781, E 135.460)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.67, 135.36, 34.79, 135.47)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word. JR's and Hanshin's 尼崎, and
# JR's and Hankyu's 塚口, are separate N02 groups at least 821 m apart:
# separate stations, so step 1 appends their operators (Kobe's Mikage).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.41) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: step 1's
# station check measures a median gap of 1,023 m (closest 821 m; the brief's
# nearest-group median 1,181 m), far above the 550 m that halves the rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 7 lines, no Shinkansen), each cut at the city line (owner
# 2026-09-24): Hanshin's 本線 (5 of 33) and 阪神なんば線 (2 of 12), JR's
# 東海道線 (2 of 59), 福知山線 (3 of 30) and JR東西線 (1 of 9), Hankyu's
# 神戸線 (3 of 17) and 伊丹線 (1 of 4). The JR Tozai Line (尼崎, its
# terminus) and the Hankyu Itami Line (塚口, its junction) are one-station
# stubs of JR and private lines: drawn as cut (owner 2026-09-27, Kobe's JR
# Takarazuka Line); each station keeps its ring through the other lines.
LEFT_OUT_LINES = {}
# Hanshin, JR and Hankyu run on into Osaka Prefecture: its N03 names the
# stations beyond the prefecture line (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("27",)
# The widest interchange is Hankyu's 塚口 (Kobe and Itami Lines), 32 m.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Lines Osaka's map also draws start from
# Osaka's colours (the neighbour the lines run into); the JR Takarazuka Line
# from Kobe's; the Hankyu Itami Line from Hankyu's maroon. N02's 東海道線 is
# the JR Kyoto Line east of 大阪 and the JR Kobe Line west of it (Osaka's
# BRANCHES): the 13 sections step 1 draws here (within 3 km of the city
# line) run from 135.492 E, short of 大阪, west to Nishinomiya, so all are
# the JR Kobe Line and no branch walk is needed (Nishinomiya's precedent).
_HS, _HK, _JR = "阪神電気鉄道", "阪急電鉄", "西日本旅客鉄道"
LINES = {
    "SH": {"n02": [(_HS, "本線")], "name": "Hanshin Main Line", "name_ja": "阪神本線", "short": "Hanshin",
           "hue": "#817B7B"},
    "SN": {"n02": [(_HS, "阪神なんば線")], "name": "Hanshin Namba Line", "name_ja": "阪神なんば線",
           "short": "Hanshin", "hue": "#4E665A"},
    "JK": {"n02": [(_JR, "東海道線")], "name": "JR Kobe Line", "name_ja": "JR神戸線", "short": "JR",
           "hue": "#755A75"},
    "JT": {"n02": [(_JR, "福知山線")], "name": "JR Takarazuka Line", "name_ja": "JR宝塚線", "short": "JR",
           "hue": "#9F9504"},
    "JH": {"n02": [(_JR, "JR東西線")], "name": "JR Tōzai Line", "name_ja": "JR東西線", "short": "JR",
           "hue": "#FF21C0"},
    "HK": {"n02": [(_HK, "神戸線")], "name": "Hankyu Kobe Line", "name_ja": "阪急神戸線", "short": "Hankyu",
           "hue": "#C9785D"},
    "HI": {"n02": [(_HK, "伊丹線")], "name": "Hankyu Itami Line", "name_ja": "阪急伊丹線", "short": "Hankyu",
           "hue": "#8C1C2D"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# amagasaki` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. Osaka's five and Kobe's JR Takarazuka
# ochre come back to within the search's step of 8; the Hankyu Itami Line's
# maroon goes rust (45.2 from the pins, 20.1 from the Hankyu Kobe Line). Closest
# pair within 500 m and anywhere 19.2 (Hanshin Main / Namba); the dark-mode
# labels separate, 7 of 7.
_COLOURS = {"SH": "#807878", "SN": "#486860", "JK": "#785870", "JT": "#A09808", "JH": "#F820C0", "HK": "#C87858",
            "HI": "#A04820"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city, so no operator publishes an
# in-city count; step 1 lists each line's in-city stations (the brief's 17
# station records in 12 N02_005g groups).
GATE3 = {"source": "no line wholly inside the city", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
AMAGASAKI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = AMAGASAKI_BBOX
