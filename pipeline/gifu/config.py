"""Gifu-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/gifu.md
(16/16 checks, 2026-10-07). Japan's A/B batch (Regional-1), on the shared
modules (pipeline/countries/japan*.py) with the Japan foundation's rules on
(2026-10-07), in Akita's shape (one standing food list of every permit in
term on its date, nothing rebuilt) with Toyota's precedent for a city list
that leaves rows out by design and Hamamatsu's for the registers (one file
per kind).

Business leg: Gifu City's own packages on Gifu Prefecture's CKAN
(gifu-opendata.pref.gifu.lg.jp, organization 40010 岐阜市), CC BY 2.0 as
declared. Food: c212016-072, the permit list and the notification list as of
2025-06-01 (vending, vehicle, stall and temporary permits left out by the
city); the notification list is the city's own, so its food-retail types
count as Food shops (Yokkaichi's precedent). Personal services: c212016-075,
the barber and beauty registers as of 2025-03-31; the city publishes no
laundry list (a disclosed gap, Akita's precedent). MHLW's open data for
21201 is a control only, read by no step (Yokkaichi's and Toyama's
precedent: the city's own notification list supplies the Food-shops layer).
All placed by a JOIN to MLIT's 位置参照情報 (one municipality, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Meitetsu's Nagoya Main, Kakamigahara and Takehana lines and JR
Central's Tokaido and Takayama lines. English station names from
OpenStreetMap's name:en.
"""

import re
from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "gifu" / "raw"
DATA_PROCESSED = ROOT / "data" / "gifu" / "processed"
OUTPUTS = ROOT / "outputs" / "gifu"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Gifu"
SLUG = "gifu"
MUNICIPALITY = "岐阜市"
PREFECTURE = "岐阜県"

# Gifu Prefecture's CKAN, Gifu City's own packages only (author 岐阜市,
# license_id CC-BY-2.0 on each dataset page). Read 2026-10-06 (licence-read,
# recorded by staging): permitted with conditions, CC BY 2.0 as declared, the
# portal's prescribed credit for a modified work naming 岐阜市, the portal's
# cost clause fault-based. The older editions under the same organization
# (c212016-004 to -065) carry other licences and are not read; the city
# page's newer food list needs the food hygiene section's permission and is
# not used (owner, 2026-10-06).
_PORTAL = "https://gifu-opendata.pref.gifu.lg.jp/dataset/"
FOOD_PAGE = _PORTAL + "c212016-072"
LIFE_PAGE = _PORTAL + "c212016-075"
_FOOD_RES = _PORTAL + "2f9f1b1c-be25-4a27-96c6-47b597f1a0bd/resource/"
_LIFE_RES = _PORTAL + "0e989e17-7093-4cbd-b931-6a24cf93fdb2/resource/"
# source key -> (file, URL of the edition this build read, the dataset page
# that carries its licence). One entry per file fetched (Step 0, 2026-10-06,
# each HTTP 200 from the portal). The editions do not roll: a new edition is
# a new package (c212016-0xx), to re-measure and re-read.
SOURCE_FILES = {
    "food": ("gifushisyokuhinkyokar7.6.1.csv",
             _FOOD_RES + "16ef7794-d2b6-4d7d-8353-f55193432530/download/gifushisyokuhinkyokar7.6.1.csv",
             FOOD_PAGE),
    "notify": ("gifushisyokuhintodokeder7.6.1.csv",
               _FOOD_RES + "6c758a77-694e-46bd-8d08-f67530532d5a/download/gifushisyokuhintodokeder7.6.1.csv",
               FOOD_PAGE),
    "barber": ("20250331riyo.xlsx",
               _LIFE_RES + "fe88c7c1-3bbe-42ed-aa77-525f940ed6fe/download/20250331riyo.xlsx", LIFE_PAGE),
    "beauty": ("20250331biyousho.xlsx",
               _LIFE_RES + "0030e554-51b5-47ca-9bec-5724fb0dc617/download/20250331biyousho.xlsx", LIFE_PAGE),
}
# Kyoto's rule: the date each list states, never the download's. The food
# package reads 2025年6月1日時点, the registers' 令和7年3月31日現在.
FOOD_AS_OF = "2025-06-01"
REGISTERS_AS_OF = "2025-03-31"
SOURCE_AS_OF = {"food": FOOD_AS_OF, "notify": FOOD_AS_OF, "barber": REGISTERS_AS_OF, "beauty": REGISTERS_AS_OF}
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. The permit list holds every
# permit in term on its date (許可満了日 2025-08-31 onward, the brief); one
# permit starts after it (2025-06-20) and waits. The notifications carry no
# term.
TERM_AS_OF = {"food": FOOD_AS_OF}

SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# The notification list is a food list too: japan_eigyo reads its types
# (乳類販売業, コンビニエンスストア, 野菜果物販売業 ...) as food ones
# (Yokkaichi's).
SOURCE_KIND = {"notify": "food"}
# Declared, never inferred: the two food lists UTF-8 with a BOM and CRLF, the
# header on row 1; the registers XLSX (PK magic bytes, one sheet each).
SOURCE_ENCODING = {"food": "utf-8-sig", "notify": "utf-8-sig", "barber": "xlsx", "beauty": "xlsx"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns (the food lists' 営業者名, with no
# company marker on 2,098 of 4,453 permit rows and 414 of 1,093
# notifications, the shape of a sole trader's own name, and 代表者名; the
# registers' 申請者氏名, no company marker on 328 of 362 barbers and 885 of
# 1,177 beauty salons) are REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; read IN MEMORY by that rule only, never kept. Never selected:
# 営業者住所 (the operator's own address), 営業所電話番号 and 施設ＴＥＬ.
_REGISTER = ("確認日", "施設名称", "施設住所", "申請者氏名")
REQUIRED_COLUMNS = {
    "food": ("許可番号", "営業所名称", "営業所在地", "営業種別", "営業者名", "代表者名", "許可開始日", "許可満了日"),
    "notify": ("営業所名称", "営業所在地", "営業種別", "営業者名", "代表者名", "届出年月日"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# The permit list writes its term as YYYYMMDD (20250620), a form
# japan_register.wareki_date reads as no date, so calls 161 and 172 would
# compare nothing (2026-10-07: 0 of 4,453 starts read). Rewritten to
# YYYY-MM-DD here, city-locally (Fukuyama's rebuilt_food and Ichinomiya's
# file_rows are the batch's precedent; the shared reader is a review-time
# finding). Measured: one 菓子製造業 permit starts 2025-06-20, after the as-of,
# and waits; no expiry falls before it.
_TERM_COLS = ("許可開始日", "許可満了日", "初回許可開始年月日")
_YYYYMMDD = re.compile(r"(\d{4})(\d{2})(\d{2})")


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    each file as it stands, the permit list's YYYYMMDD term dates rewritten
    as YYYY-MM-DD (_TERM_COLS)."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        for c in _TERM_COLS:
            if m := _YYYYMMDD.fullmatch((r.get(c) or "").strip()):
                r[c] = "-".join(m.groups())
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 21201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Gifu (the city's
# tramway closed in 2005 and is not in N02).
# S, W, N, E: the city's N03 extent (S 35.351, W 136.679, N 35.543,
# E 136.886; the 2006 merger brought in 柳津町) rounded out; step 1 stops if
# the city leaves it.
OSM_BBOX = (35.35, 136.67, 35.55, 136.89)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (no macrons, lowercase after a hyphen for a
# common word, a katakana loanword as its English word, 前 as -mae). 名鉄岐阜
# takes Meitetsu's hyphen, as OSM's own Meitetsu-Ichinomiya on Ichinomiya's
# map (Yokkaichi's Kintetsu-Tomida). OSM's other 9 stand as they are (30
# objects, all with name:en, 2026-10-07).
OSM_NAME_EN_OVERRIDES = {
    "加納": "Kano",                                   # Kanō
    "切通": "Kiridoshi",                              # Kiridōshi
    "名鉄岐阜": "Meitetsu-Gifu",                      # Meitetsu Gifu
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the N03 centroid (~136.765) and the whole extent (136.679 to
# 136.886) fall in the 132 to 138 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median nearest-station gap is
# 641 m (418 to 4,635), over the spacing rule's halving line (about 550 m,
# docs/ring_rules.md): standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 5 lines, no Shinkansen station; 岐阜羽島 is in 羽島市). Every
# line is cut at the city line (owner 2026-09-24): Meitetsu's Kakamigahara
# Line keeps 6 of 18 station records, Nagoya Main Line 3 of 60 (both end at
# their own terminus, 名鉄岐阜, inside the city), Takehana Line 1 of 9; JR
# Central's Tokaido Line 2 of 89 and Takayama Line 2 of 36 (main lines cut at
# the line, as Ichinomiya's Tokaido Line, not stubs). The Takehana Line's one
# station, 柳津, 453 m inside the city line, has no other line: a private
# one-station stub kept as cut by the standing call (Kobe's JR Takarazuka
# Line), so its ring comes from the Takehana Line itself. No frequency floor
# (owner, 2026-10-06, calls 46 and 86): the thinnest stretch, the Takayama
# Line at 長森, runs 37 and 40 trains a weekday (JR Central's timetables, read
# 2026-10-06 for the brief); nothing is near 11.
LEFT_OUT_LINES = {}
# The Tokaido and Nagoya Main lines run on into Aichi (木曽川, 木曽川堤 and 黒田,
# in 一宮市): Aichi's N03, already in the shared cache, names the stations
# beyond the prefecture line (japan_step1.n03_municipalities; Ōtsu's).
N03_NEIGHBOR_PREFS = ("23",)
# 名鉄岐阜 is one N02 group for the Main and Kakamigahara lines (102 m), 岐阜
# for the Tokaido and Takayama lines (0 m). 名鉄岐阜 and 岐阜 (JR), 418 m
# apart, are separate groups of different names and stay apart (trap 1;
# Ichinomiya's 名鉄一宮 / 尾張一宮).
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names follow the operators' signs
# with no macrons and no "Main" for JR, as Ichinomiya's.
_MT, _JR = "名古屋鉄道", "東海旅客鉄道"
LINES = {
    "NH": {"n02": [(_MT, "名古屋本線")], "name": "Meitetsu Nagoya Main Line", "name_ja": "名鉄名古屋本線",
           "short": "Meitetsu", "hue": "#E60012"},
    "KG": {"n02": [(_MT, "各務原線")], "name": "Meitetsu Kakamigahara Line", "name_ja": "名鉄各務原線",
           "short": "Meitetsu", "hue": "#E60012"},
    "TH": {"n02": [(_MT, "竹鼻線")], "name": "Meitetsu Takehana Line", "name_ja": "名鉄竹鼻線", "short": "Meitetsu",
           "hue": "#E60012"},
    "TK": {"n02": [(_JR, "東海道線")], "name": "JR Tokaido Line", "name_ja": "東海道線", "short": "JR",
           "hue": "#F77321"},
    "TY": {"n02": [(_JR, "高山線")], "name": "JR Takayama Line", "name_ja": "高山本線", "short": "JR",
           "hue": "#F77321"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# gifu` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each the
# feasible colour nearest its operator's hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. Meitetsu's one red splits three ways,
# red (Nagoya Main Line), red-orange (Kakamigahara Line) and orange (Takehana
# Line), Toyota's and Ichinomiya's split carried one step on; JR Central's
# orange darkens for the Tokaido Line and goes brown for the Takayama Line.
# Closest pair within 500 m 18.1 (Kakamigahara, Nagoya Main, at 名鉄岐阜);
# anywhere 15.5 (Kakamigahara, Takehana, which never meet). The dark-mode
# labels separate, 5 of 5.
_COLOURS = {"NH": "#E80010", "KG": "#F05030", "TH": "#F85008", "TK": "#E86810", "TY": "#B84008"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own counts inside the city (the brief, read
# 2026-10-06): Meitetsu's station numbers, Nagoya Main Line NH58-NH60 (3),
# Kakamigahara Line KG12-KG16 plus 名鉄岐阜 (6), Takehana Line TH02 (1); JR
# Central's station timetable index, Tokaido Line 岐阜 and 西岐阜 (2),
# Takayama Line 岐阜 and 長森 (2).
GATE3 = {"source": "Meitetsu's station numbers (trainbus.meitetsu.co.jp) and JR Central's station index "
                   "(railway.jr-central.co.jp/time-schedule/): Nagoya Main Line NH58-NH60 3 inside the city, "
                   "Kakamigahara Line KG12-KG16 and NH60 6, Takehana Line TH02 1, Tokaido Line 2, Takayama Line 2",
         "lines": {"NH": 3, "KG": 6, "TH": 1, "TK": 2, "TY": 2}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
GIFU_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = GIFU_BBOX
