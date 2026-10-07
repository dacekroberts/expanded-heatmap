"""Ōita-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/oita.md
(12/12 checks, 2026-10-07). Japan's A/B batch (Regional-1), on the shared
modules (pipeline/countries/japan*.py) with the Japan foundation's rules on
(2026-10-07), in Matsuyama's shape (one complete city food list beside MHLW's
file) with Hamamatsu's for the registers and Ichinomiya's for MHLW's
notifications.

Business leg: the city's own lists on BODIK (organisation 442011, author
福祉保健部衛生課; each dataset cc-by-40-intl, and the 大分市オープンデータ利用規約
of 2023-03-15, compatible with CC BY 4.0; read 2026-10-07 by staging). Food:
every permit in term on 2026-09-01 (すべての許可施設一覧), one complete list,
no months. The city masks 301 rows' address with asterisks and gives no
reason; the foundation's `asterisk` rule sets them aside and counts them
apart. Personal services: the barber, beauty-salon and laundry lists as of
2026-03-31, plus the 2026 monthly lists of new beauty salons (April to
August) and laundries (July, the one month posted); no barber set (owner,
call 211, Ichinomiya's call 128). The city's own notification list
(すべての営業届出施設一覧, as of 2026-09-01) supplies the Food shops layer the
permits do not (owner, call 212; Gifu's and Yokkaichi's precedent). MHLW's
食品衛生申請等システム open data is read only for its own point for a city
row the block join misses (POINT_DONORS; Toyama's precedent): nothing of it
is drawn. All placed by a JOIN to MLIT's 位置参照情報 (one municipality, no
wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR Kyushu's Nippo, Hohi and Kyudai main lines. English station names
from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "oita" / "raw"
DATA_PROCESSED = ROOT / "data" / "oita" / "processed"
OUTPUTS = ROOT / "outputs" / "oita"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Ōita"
SLUG = "oita"
MUNICIPALITY = "大分市"
PREFECTURE = "大分県"

# The city's BODIK datasets (data.bodik.jp, organisation 442011): four at
# Step 0, three more on calls 211 and 212 (2026-10-07). Each resource also
# sits on the city's own site (its resourceurl); the build reads BODIK's copy,
# as Step 0 did. The edition is pinned: a re-fetch is a new build (one
# request at a time, 20 s apart, URLs from package_show, never
# datastore_search_sql).
BODIK = "https://data.bodik.jp/dataset"
FOOD_PAGE = BODIK + "/442011_permitted_facility"
BARBER_PAGE = BODIK + "/442011_barber_shop"
BEAUTY_PAGE = BODIK + "/442011_beauty_salon"
LAUNDRY_PAGE = BODIK + "/442011_cleaning"
NOTIFY_PAGE = BODIK + "/442011_licensed_facility"
# The 2026 monthly lists of new premises (美容所新規施設, クリーニング所新規施設;
# owner, call 211, 2026-10-07): one resource per month, each named by its
# month and stating データ時点日付 the first of the next. The laundry set
# carries July only and there is no barber set (package_show, 2026-10-07).
# New confirmations only: each month file has the register's columns and no
# closure column, and the city publishes no closures.
BEAUTY_NEW_PAGE = BODIK + "/442011_beauty_salon_new"
LAUNDRY_NEW_PAGE = BODIK + "/442011_cleaning_new"
_BEAUTY_NEW = BODIK + "/8f45b2b8-549e-4ca4-a1e8-bd54439b2052/resource/"
_LAUNDRY_NEW = BODIK + "/eb03c13a-dbad-43ab-a5c2-c42c07939fd6/resource/"
# month -> (resource id, file)
BEAUTY_MONTHS = {"04": ("e1ba96f7-6e10-42b5-abe9-a78bc13b4d8a", "202604biyousyo.csv"),
                 "05": ("7d217404-43ac-405d-a9ec-f0ff72ec19ec", "202605biyousyo.csv"),
                 "06": ("1ed49cbf-4d74-444e-a854-0106fba8f242", "202606biyousyo.csv"),
                 "07": ("3c97cb82-1ee2-481b-9f73-23a344787555", "202607biyousyo.csv"),
                 "08": ("d8c82c36-d606-4fdc-92a8-3e6ce8067ea6", "202608biyousyo.csv")}
LAUNDRY_MONTHS = {"07": ("be28d1a9-9fe8-4288-a625-cc183fa43411", "202607kuriningu.csv")}
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL of the edition this build read, the dataset page
# that carries its licence). The month files were fetched 2026-10-07, one
# request at a time 20 s apart, their URLs from package_show.
SOURCE_FILES = {
    "food": ("r080901allkyoka.csv",
             BODIK + "/b03c9bdb-a1cc-4d7a-8891-bc7980ec693e/resource/02ed0f35-9a57-4025-ab5b-e274150f3381/download/"
             "r080901allkyoka.csv", FOOD_PAGE),
    "barber": ("20260331riyousyo.csv",
               BODIK + "/68c0d0a8-7b2c-4217-ba83-90fd8accca19/resource/fcde9e81-40a5-4da8-bdbd-a9b882074224/download/"
               "20260331riyousyo.csv", BARBER_PAGE),
    "beauty": ("20260331biyousyo.csv",
               BODIK + "/38ee3063-3b34-4a32-bff3-2ad92611b7a4/resource/66130b2d-f2d2-4be2-b163-c0e41f5a33d0/download/"
               "20260331biyousyo.csv", BEAUTY_PAGE),
    "laundry": ("20260331kuriningu.csv",
                BODIK + "/1ab16997-d139-4bba-84e9-e819df58675f/resource/a10fb2da-35e7-4e9e-866b-2e19769b7300/download/"
                "20260331kuriningu.csv", LAUNDRY_PAGE),
    **{f"beauty_{m}": (f, f"{_BEAUTY_NEW}{rid}/download/{f}", BEAUTY_NEW_PAGE)
       for m, (rid, f) in BEAUTY_MONTHS.items()},
    **{f"laundry_{m}": (f, f"{_LAUNDRY_NEW}{rid}/download/{f}", LAUNDRY_NEW_PAGE)
       for m, (rid, f) in LAUNDRY_MONTHS.items()},
    # The city's own notification list (すべての営業届出施設一覧,
    # 442011_licensed_facility, データ時点日付 2026-09-01; owner, call 212):
    # read as a food source (SOURCES, SOURCE_KIND). Its notifier column
    # 届出者氏名 joined japan_register.OPERATOR_COLS_WAVE5 for it (2026-10-07).
    # Header read 2026-10-07: 1,424 rows, 26 types, 48 addresses masked with
    # asterisks, 66 大分市内一円.
    "notify": ("r080901alltodoke.csv",
               BODIK + "/be87ff3e-fb41-4f46-be45-1609d7550887/resource/cfa63aff-dc94-495a-9574-38b4c56a0db7/download/"
               "r080901alltodoke.csv", NOTIFY_PAGE),
    "mhlw": ("44201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=44201_food_business_all.csv",
             MHLW_TOP),
}
# Kyoto's rule: the date each list states, never the download's. The food
# file states データ時点日付 2026-09-01; the registers 令和8年3月31日現在; MHLW's
# monthly file states none (its newest 許可年月日 2026-08-17, no closures). Each
# month file states データ時点日付 the first of the next month (April's
# 2026-05-01, August's 2026-09-01).
_NEXT = {"04": "05", "05": "06", "06": "07", "07": "08", "08": "09"}
REGISTER_MONTH_KEYS = {"barber": (), "beauty": tuple(f"beauty_{m}" for m in BEAUTY_MONTHS),
                       "laundry": tuple(f"laundry_{m}" for m in LAUNDRY_MONTHS)}
SOURCE_AS_OF = {"food": "2026-09-01", "barber": "2026-03-31", "beauty": "2026-03-31", "laundry": "2026-03-31",
                "mhlw": None, "notify": "2026-09-01",
                **{f"beauty_{m}": f"2026-{_NEXT[m]}-01" for m in BEAUTY_MONTHS},
                **{f"laundry_{m}": f"2026-{_NEXT[m]}-01" for m in LAUNDRY_MONTHS}}
FOOD_AS_OF = SOURCE_AS_OF["food"]
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. The food file holds only permits
# in term on its date (the earliest 許可満了日 2026-11-30, the latest
# 許可開始日 2026-09-01): past term 0, late 0, as the brief measured. MHLW's
# notifications carry no term.
TERM_AS_OF = {"food": "2026-09-01", "mhlw": "2026-08-31"}

# What step 2 reads. The city's own notification list ("notify", a food
# source by SOURCE_KIND) supplies the Food shops layer the city's permits do
# not (owner, call 212; Gifu's and Yokkaichi's precedent), so MHLW's opt-in
# notifications are no longer drawn: its file is a points donor only
# (Toyama's precedent). 届出者氏名 joined japan_register.OPERATOR_COLS_WAVE5
# for it (2026-10-07).
SOURCES = {"food": SOURCE_FILES["food"][0], "notify": SOURCE_FILES["notify"][0],
           "barber": SOURCE_FILES["barber"][0], "beauty": SOURCE_FILES["beauty"][0],
           "laundry": SOURCE_FILES["laundry"][0]}
SOURCE_KIND = {"notify": "food"}
# Declared, never inferred: every city file a cp932 CSV without a BOM; MHLW's
# UTF-8 with a BOM.
SOURCE_ENCODING = {**{k: "cp932" for k in SOURCE_FILES}, "mhlw": "utf-8-sig"}
# The columns each file and source must carry; fetch_sources.py and step 2
# stop on a header without them. The operator columns (the food list's
# 申請者氏名 and 代表者氏名, no company marker on 3,283 of 6,199 rows; the
# registers' 開設者, none on 366 of 391 barbers; MHLW's 法人名) are REQUIRED so
# the name rule (japan_register.name_is_operator; owner 2026-09-27) cannot
# silently compare nothing; read IN MEMORY by that rule only, never kept.
# Never selected: 申請者カナ氏名, 申請者住所１ / ２ (the operator's own address),
# 申請者電話番号, 営業所電話番号, 施設電話番号, 法人番号, 法人住所 and every phone.
_FOOD = ("営業許可№", "業種名", "業態", "営業所屋号", "営業所住所１", "申請者氏名", "代表者氏名", "許可開始日",
         "許可満了日")
_REG = ("施設名称", "施設所在地", "開設者")
_MHLW = ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
         "廃業年月日", "法人名")
# The month files carry the registers' own header (確認年月日 written
# 2026/04/02 there, 令和 in the full lists; no term either way).
REQUIRED_COLUMNS = {"food": _FOOD, "barber": _REG, "beauty": _REG, "laundry": (*_REG, "種別"),
                    **{k: _REG for k in REGISTER_MONTH_KEYS["beauty"]},
                    **{k: (*_REG, "種別") for k in REGISTER_MONTH_KEYS["laundry"]},
                    # never selected: 届出者カナ氏名, 届出者住所１ / ２, 届出者電話番号,
                    # 営業所電話番号
                    "notify": ("届出管理№", "業種名", "営業所屋号", "営業所住所１", "届出者氏名", "代表者氏名",
                               "届出日"),
                    "mhlw": _MHLW, "mhlw_points": _MHLW}
# MHLW is no longer a drawn source (call 212), so nothing is published by
# consent, no row takes its own point and no list supersedes another.
ADDRESS_BY_CONSENT = set()
OWN_POINT_FALLBACK = set()
SUPERSEDES = {}
# A city permit or notification row the block join misses takes MHLW's point
# for the same premises (ward, town, trade name), read from the whole file
# under its own key, never drawn (Ichinomiya's call 127 (c), Matsuyama's and
# Toyama's mechanism; 21 rows in the 2026-10-07 measurement).
POINT_DONORS = {"food": "mhlw_points", "notify": "mhlw_points"}


def source_csv(key):
    if key == "mhlw_points":
        key = "mhlw"
    return DATA_RAW / SOURCE_FILES[key][0]


def _rows(key):
    """One fetched file's rows as it stands, its header checked."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    rows = list(jr.city_rows(path))
    missing = [c for c in REQUIRED_COLUMNS[key] if rows and c not in rows[0]]
    if missing:
        raise SystemExit(f"{path.name}: header lacks {missing} - not the file the brief read")
    return rows


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    Each city list as it stands; each register its 2026-03-31 list plus the
    2026 months (new confirmations only; the city publishes no closures),
    Ichinomiya's form. "mhlw" yields only MHLW's notifications (申請区分
    届出): its 85 permits are all in the city's list by number (the brief)
    and are not added. "mhlw_points" is the whole file, read by POINT_DONORS
    for its coordinates only."""
    if key in REGISTER_MONTH_KEYS:
        for k in (key, *REGISTER_MONTH_KEYS[key]):
            yield from _rows(k)
        return
    for r in _rows(key):
        if key == "mhlw" and not (r.get("申請区分") or "").startswith("届出"):
            continue
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 44201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Ōita.
# S, W, N, E: the city's N03 extent (S 33.070, W 131.419, N 33.290, E 131.963)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (33.06, 131.41, 33.30, 131.97)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (no macrons, lowercase after a hyphen for a
# common word, 前 as -mae). OSM's other 8 in-city names stand (34 objects, 30
# with name:en, 2026-10-07). 豊後国分 is JR Kyushu's ぶんごこくぶ (its
# timetable station index); OSM reads it Bungo-Kobuku.
OSM_NAME_EN_OVERRIDES = {
    "大分": "Oita",                                   # Ōita
    "西大分": "Nishi-Oita",                           # Nishi-Ōita
    "南大分": "Minami-Oita",                          # Minami-Ōita
    "大分大学前": "Oita-daigaku-mae",                 # Ōita-Daigaku-mae
    "大在": "Ozai",                                   # Ōzai
    "高城": "Takajo",                                 # Takajō
    "幸崎": "Kozaki",                                 # Kōzaki
    "古国府": "Furugo",                               # Furugō
    "豊後国分": "Bungo-Kokubu",                       # Bungo-Kobuku
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 52N: the N03 centroid (~131.641) and the whole extent (131.419 to
# 131.963) fall in the 126 to 132 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median nearest-station gap is
# 2,209 m: standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25: 3 lines, no Shinkansen in the prefecture): JR Kyushu's Nippo
# Main Line keeps 8 of 113, the Hohi Main Line 6 of 37 and the Kyudai Main
# Line 5 of 37 (大分 one group for all three). Every line is cut at the city
# line (owner 2026-09-24); none is cut to one station. No frequency floor
# (owner, 2026-10-06, calls 46 and 86): the thinnest stretch, the Hohi Main
# Line from 中判田 to 竹中, runs 25 to 26 trains a weekday each way (JR
# Kyushu's station timetables, read 2026-10-06).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names follow the operator's signs
# with no macrons, as Sasebo's and Kitakyushu's.
_JR = "九州旅客鉄道"
LINES = {
    "NP": {"n02": [(_JR, "日豊線")], "name": "JR Nippo Main Line", "name_ja": "日豊本線", "short": "JR",
           "hue": "#0068B7"},
    "HH": {"n02": [(_JR, "豊肥線")], "name": "JR Hohi Main Line", "name_ja": "豊肥本線", "short": "JR",
           "hue": "#E60012"},
    "KD": {"n02": [(_JR, "久大線")], "name": "JR Kyudai Main Line", "name_ja": "久大本線", "short": "JR",
           "hue": "#009944"},
}
# JR Kyushu signs no line colours; each hue is the one the built Kyushu cities
# start from (Kagoshima's and Kitakyushu's Nippo blue, Kumamoto's JR red for
# the Hohi line, Kurume's Kyudai green).
# Colours: the project's own, from `python scripts/line_colour_search.py
# oita` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. The Nippo blue goes teal
# (Kagoshima's same colour), the Kyudai green is Kurume's. Closest pair 92.3
# (Nippo, Kyudai, which share 大分); the dark-mode labels separate, 3 of 3.
_COLOURS = {"NP": "#007890", "HH": "#E80010", "KD": "#30A800"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: JR Kyushu's own timetable station index
# (jrkyushu-timetable.jp/sp/railway_list.html, read 2026-10-07) lists the
# Nippo Main Line's 113 stations, 小倉 to 鹿児島中央, the Hohi Main Line's 37,
# 熊本 to 大分, and the Kyudai Main Line's 37, 久留米 to 大分, as N02 does.
# Inside the city: 西大分 to 幸崎 (8), 竹中 to 大分 (6), 豊後国分 to 大分 (5).
GATE3 = {"source": "JR Kyushu's timetable station index (jrkyushu-timetable.jp/sp/railway_list.html): Nippo Main "
                   "Line 西大分-幸崎 8 inside the city, Hohi Main Line 竹中-大分 6, Kyudai Main Line 豊後国分-大分 5",
         "lines": {"NP": 8, "HH": 6, "KD": 5}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
OITA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = OITA_BBOX
