"""Fukui-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/fukui.md
(11/11 checks, 2026-10-02). Built in the 2026-10-01 Japanese batch, on the
shared modules (pipeline/countries/japan*.py), in Matsuyama's shape.

Business leg: the city's own month-end lists (福井市, CC BY-SA, the site
default; the owner offers outputs/fukui/ under CC BY-SA 4.0, 2026-10-01): every
food permit for a fixed premises (食品衛生法に基づく営業許可施設一覧) and its
barbers, beauty salons and laundries (環境衛生関係施設一覧), each workbook
twelve month-end sheets, the newest (R8.8月末, 2026-08-31) the list. Closures
are already out of it. MHLW's 食品衛生申請等システム file is a count control
only (90 restaurant permits; Fukui files at the counter), not a source.
Everything placed by a JOIN to MLIT's 位置参照情報 for the one municipality (no
wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Fukui Railway's Fukubu Line (street track and railway), Echizen
Railway's two lines, the Hapi-line Fukui and JR West's Etsumi-Hoku Line.
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "fukui" / "raw"
DATA_PROCESSED = ROOT / "data" / "fukui" / "processed"
OUTPUTS = ROOT / "outputs" / "fukui"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Fukui"
SLUG = "fukui"
MUNICIPALITY = "福井市"
PREFECTURE = "福井県"

# The city's two pages (each updated 2026-09-07), one XLSX per list, under the
# site policy's default licence, CC BY-SA with no version named
# (sisei/kohou/hp/site-p.html, 1 著作権). The pages' closure workbooks
# (12syokuhinhaigyo, 07kankyohaigyo) are not read: none of the June, July or
# August closures is in the R8.8月末 sheet (the brief). The monthly file names
# change (_202608 becomes _202609); a newer edition is a brief to update.
_SITE = "https://www.city.fukui.lg.jp/fukusi/eisei"
FOOD_PAGE = f"{_SITE}/syokuhin/p070519.html"
PERSONAL_PAGE = f"{_SITE}/kankyo/p070518.html"
SOURCE_FILES = {
    "food": ("11syokuhin_202608.xlsx", f"{_SITE}/syokuhin/p070519_d/fil/11syokuhin_202608.xlsx", FOOD_PAGE),
    "barber": ("01riyou_202608.xlsx", f"{_SITE}/kankyo/p070518_d/fil/01riyou_202608.xlsx", PERSONAL_PAGE),
    "beauty": ("02biyou_202608.xlsx", f"{_SITE}/kankyo/p070518_d/fil/02biyou_202608.xlsx", PERSONAL_PAGE),
    "laundry": ("03cleaning_202608.xlsx", f"{_SITE}/kankyo/p070518_d/fil/03cleaning_202608.xlsx", PERSONAL_PAGE),
}
# The newest month-end sheet IS the list: 「令和8年8月末日現在」 in every
# workbook's title row (Kyoto's rule: the date the list states, never the
# download's); newest 許可年月日 2026-08-31; every 許可期限 2026-09-30 or later.
NEWEST_SHEET = "R8.8月末"
SOURCE_AS_OF = {"food": "2026-08-31", "barber": "2026-08-31", "beauty": "2026-08-31", "laundry": "2026-08-31"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: XLSX, twelve month-end sheets each, the newest
# first, a title on row 1 and the header on row 2 (city_rows finds it by its
# address column).
SOURCE_ENCODING = {k: "xlsx" for k in SOURCES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 申請者名(法人名) / 申請者名（法人名） (half-width brackets
# in the food list, full-width in the registers) and 法人代表者名 are REQUIRED
# so the name rule (japan_register.name_is_operator; owner 2026-09-27) cannot
# silently compare nothing; they are read IN MEMORY by that rule only, never
# kept. The city names an operator only where it is a company (the brief:
# 2,118 of 2,209 filled food rows carry a company marker), so the rule
# compares few rows (owner, 2026-10-02: accepted, as MHLW's rows in Fukuoka).
# Never selected: 申請者住所 (an operator's own address), the phones.
_REGISTER = ("営業所名称", "営業所所在地", "申請者名（法人名）", "法人代表者名", "業種")
REQUIRED_COLUMNS = {
    "food": ("施設名称", "施設所在地", "申請者名(法人名)", "法人代表者名", "許可期限", "業種"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry": _REGISTER + ("詳細業種",),
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    the newest month-end sheet only (japan_register.xlsx_rows' `sheet`), which
    must be NEWEST_SHEET: a re-downloaded workbook with a newer month first
    stops here rather than being read under the old as-of date."""
    import io

    import openpyxl

    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    wb = openpyxl.load_workbook(io.BytesIO(path.read_bytes()), read_only=True)
    first = wb.sheetnames[0].replace(" ", "")
    if first != NEWEST_SHEET:
        raise SystemExit(f"{path.name}: the newest sheet is {first!r}, not {NEWEST_SHEET!r}; "
                         "update NEWEST_SHEET and SOURCE_AS_OF")
    yield from jr.city_rows(path, sheet=0)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 18201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram-stop query: OSM tags
# all six of the Fukubu Line's street stops (N02 class 21, 田原町 to 福井駅 and
# 仁愛女子高校) railway=station or halt, so the station query takes them
# (read in the cache, 2026-10-02).
# S, W, N, E: the city's N03 extent (S 35.9204, W 135.9638, N 36.1729,
# E 136.4672, the coast to the Ōno border), rounded out; step 1 stops if the
# city leaves it.
OSM_BBOX = (35.91, 135.95, 36.19, 136.48)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
# 清明 (the Fukubu Line): OSM's object has name=清明 and no name:en
# (2026-10-02), and Fukui Railway's station guide (fukutetsu.jp/train/
# stationguide.php) gives no English; romanised in Hepburn.
OSM_NAME_EN_MISSING = {"清明": "Seimei"}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae. OSM
# names the Fukubu Line's 福井駅 stop "Fukui", as JR's and Echizen's 福井 142 m
# away; it is romanised as Toyama's tram stop 富山駅 is (Toyama-eki).
OSM_NAME_EN_OVERRIDES = {
    "福井駅": "Fukui-eki",                       # Fukui
    "福井城址大名町": "Fukuijoshi-Daimyomachi",    # Fukuijousidaimyoumachi
    "足羽山公園口": "Asuwayama-Koenguchi",         # Asuwayama-Kōenguchi
    "仁愛女子高校": "Jin'ai-Joshikoko",           # Jin'ai Joshikōkō
    "赤十字前": "Sekijuji-mae",                   # Sekijūjimae
    "日華化学前": "Nikkakagaku-mae",              # Nikkakagaku-Mae
    "浅水": "Asozu",                             # Asōzu
    "花堂": "Hanando",                           # Hanandō
    "越前花堂": "Echizen-Hanando",                # Echizen-Hanandō
    "越前東郷": "Echizen-Togo",                   # Echizen-Tōgō
    "越前大宮": "Echizen-Omiya",                  # Echizen-Ōmiya
    "一乗谷": "Ichijodani",                       # Ichijōdani
    "小和清水": "Kowashozu",                      # Kowashōzu
    "六条": "Rokujo",                            # Rokujō
    "三十八社": "Sanjuhassha",                    # Sanjūhassha
    "泰澄の里": "Taichonosato",                   # Taichōnosato
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~136.22) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# STANDARD, on the spacing rule (docs/ring_rules.md: halved edges only where
# the median station gap is about 550 m or less): step 1 measured 793 m among
# the 45 in-city stations (2026-10-02); only six are street stops, and the
# rest are railway stations reaching far up the valleys. Gate 1 keeps its
# default 400 m floor.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 6 legal sections, no Shinkansen; 福井 on the 北陸新幹線 is
# dropped and stays an Echizen and Hapi-line station). N02-25, not N02-24,
# which still files the former Hokuriku Main Line under JR West (the Hapi-line
# since 2024-03-16). Fukui Railway's Fukubu Line (15 of 25), Echizen's Mikuni
# Awara Line (10 of 22) and Katsuyama Eiheiji Line (8 of 23), the Hapi-line
# (4 of 19) and JR's Etsumi-Hoku Line (12 of 22), each cut at the city line
# (owner 2026-09-24). No line is wholly inside, and none is cut to a stub.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the Fukubu Line in two railway
# classes, 福武線 (12, the railway, 18.3 km) and 福武線 (21, the 軌道 street
# section through the center, 3.1 km, with its 福井駅 and 田原町 ends): one
# public line, one entry. Its trams also run through onto Echizen's Mikuni
# Awara Line to 鷲塚針原, track drawn as that line.
_FR, _ER, _HP, _JW = "福井鉄道", "えちぜん鉄道", "ハピラインふくい", "西日本旅客鉄道"
LINES = {
    "FB": {"n02": [(_FR, "福武線")], "name": "Fukui Railway Fukubu Line", "name_ja": "福武線", "short": "Fukutetsu",
           "hue": "#E60012"},
    "EM": {"n02": [(_ER, "三国芦原線")], "name": "Echizen Railway Mikuni Awara Line", "name_ja": "三国芦原線",
           "short": "Echizen", "hue": "#0068B7"},
    "EK": {"n02": [(_ER, "勝山永平寺線")], "name": "Echizen Railway Katsuyama Eiheiji Line",
           "name_ja": "勝山永平寺線", "short": "Echizen", "hue": "#0068B7"},
    "HP": {"n02": [(_HP, "ハピラインふくい線")], "name": "Hapi-line Fukui Line", "name_ja": "ハピラインふくい線",
           "short": "Hapi-line", "hue": "#F08300"},
    "JE": {"n02": [(_JW, "越美北線")], "name": "JR Etsumi-Hoku Line", "name_ja": "越美北線", "short": "JR",
           "hue": "#0072BC"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# fukui` (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide): each the
# feasible colour nearest its operator's hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. Echizen's two share one blue and spread
# over teal and slate. Closest pair within 500 m 20.1 (Echizen's two, which
# meet at 福井口); anywhere 15.9 (Mikuni Awara / Etsumi-Hoku, which never come
# within 500 m); the dark-mode labels separate, 5 of 5.
_COLOURS = {"FB": "#E80010", "EM": "#007890", "EK": "#586878", "HP": "#E07800", "JE": "#08A0C0"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}
# Gate 3 has no in-city count to compare: every line runs on past the city
# line. Read by hand instead (2026-10-02): Fukui Railway's station guide
# (fukutetsu.jp/train/stationguide.php) names the same 25 Fukubu Line
# stations as N02, 15 of them inside.
GATE3 = {"source": "none: no line is wholly inside the city (Fukui Railway's station guide matches N02's 25 "
                   "Fukubu Line stations)", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
FUKUI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = FUKUI_BBOX
