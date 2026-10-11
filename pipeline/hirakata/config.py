"""Hirakata-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/hirakata.md.
Japan A/B batch (Kansai-1, 2026-10-07), on the shared modules
(pipeline/countries/japan*.py) and the Japan foundation's rules (ALL_RULES).

Business leg: the city's own lists (枚方市保健所 保健衛生課, CC BY 2.1 JP), each
from its page on www.city.hirakata.osaka.jp. Food: 食品等営業許可施設について,
every permit in term on 2026-03-31 (露店, 自動車 and 自動販売機 left out by the
list itself) KEPT WHOLE, plus the five monthly new-permit files of April to
August 2026, merged by japan_register.rebuilt_register (Ichinomiya's and
Higashiōsaka's shape, call 126). Personal services: 環境衛生営業施設について, one
register per kind (Hamamatsu's shape) as of the end of March 2026, plus the
monthly new-premises files (beauty April to July, barbers July; owner, call
155). Food shops also from MHLW's notifications (partial, opt-in; call 127b),
MHLW's own point where the block join misses (127c); MHLW's permits are out
(126). All placed by a JOIN to MLIT's 位置参照情報 for the one municipality
(27210, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Keihan's Main and Katano lines and JR West's Gakkentoshi Line, cut at
the city line. English station names from OpenStreetMap's name:en.
"""

import datetime
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "hirakata" / "raw"
DATA_PROCESSED = ROOT / "data" / "hirakata" / "processed"
OUTPUTS = ROOT / "outputs" / "hirakata"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Hirakata"
SLUG = "hirakata"
MUNICIPALITY = "枚方市"
PREFECTURE = "大阪府"

# The city's two pages (利用条件: CC BY 2.1 JP, read 2026-10-07, PERMITTED WITH
# CONDITIONS; the credit cites the data titles and the licence link, never a
# deep link to the city's pages, whose link policy asks for an enquiry first).
# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2;
# read 2026-09-24 for Fukuoka). Credit links the MHLW top page only.
FOOD_PAGE = "https://www.city.hirakata.osaka.jp/0000023479.html"
REGISTERS_PAGE = "https://www.city.hirakata.osaka.jp/0000025284.html"
_FOOD_DIR = "https://www.city.hirakata.osaka.jp/cmsfiles/contents/0000023/23479/"
_REG_DIR = "https://www.city.hirakata.osaka.jp/cmsfiles/contents/0000025/25284/"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# The food months read: each month's NEW permits (101- only), April to August
# 2026, (month, last day). No closure file exists.
MONTHS = (("04", "30"), ("05", "31"), ("06", "30"), ("07", "31"), ("08", "31"))
# The registers' monthly new-premises files (owner, call 155), as the page
# links them on 2026-10-07: (key, file, the month's last day). The page posts
# a month only where one was filed: beauty April to July, barbers July, no
# laundry month. bbjul is the barbers' (理容所新規一覧（令和8年7月）, linked
# first in the July row), btjul the beauty salons'.
REGISTER_MONTHS = {
    "beauty": (("beauty_04", "biyouapr.xlsx", "2026-04-30"), ("beauty_05", "beautymay.xlsx", "2026-05-31"),
               ("beauty_06", "beauty6.xlsx", "2026-06-30"), ("beauty_07", "btjul.xlsx", "2026-07-31")),
    "barber": (("barber_07", "bbjul.xlsx", "2026-07-31"),),
    "laundry": (),
}
# The March registers, one file per kind (Hamamatsu's shape): 理容所施設一覧,
# 美容所施設一覧, クリーニング所施設一覧（令和8年3月末）.
REGISTER_FILES = {"barber": "riyouall.xlsx", "beauty": "biyouall.xlsx", "laundry": "cleaningall.xlsx"}

SOURCE_FILES = {
    # 2026年3月末日時点 全ての許可施設: every permit in term on 2026-03-31
    "food": ("272108_food_business_all_202603_end.csv", _FOOD_DIR + "272108_food_business_all_202603_end.csv",
             FOOD_PAGE),
    **{f"new_{m}": (f"272108_food_business_new_2026{m}.csv", f"{_FOOD_DIR}272108_food_business_new_2026{m}.csv",
                    FOOD_PAGE) for m, _ in MONTHS},
    **{f"{kind}_all": (f, _REG_DIR + f, REGISTERS_PAGE) for kind, f in REGISTER_FILES.items()},
    **{k: (f, _REG_DIR + f, REGISTERS_PAGE) for months in REGISTER_MONTHS.values() for k, f, _ in months},
    "mhlw": ("27210_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27210_food_business_all.csv",
             MHLW_TOP),
}
# The food register's date, PINNED (never the download date or today): the
# March list is kept whole (call 126), so the rebuild keeps every permit in
# term on 2026-03-31 and adds the months' new permits to 2026-08-31. The
# page's date reads "permits in term on 2026-03-31, with new permits to
# 2026-08-31".
AS_OF = datetime.date(2026, 3, 31)
NEW_PERMITS_TO = "2026-08-31"
REGISTERS_MARCH = "2026-03-31"
# Each source's date: the lists' own. The registers follow the newest month
# each covers (barbers and beauty July, laundries March); MHLW's file states
# none, so it is dated by download.
SOURCE_AS_OF = {"food": AS_OF.isoformat(), "mhlw": None,
                **{f"new_{m}": f"2026-{m}-{end}" for m, end in MONTHS},
                **{f"{kind}_all": REGISTERS_MARCH for kind in REGISTER_FILES},
                **{k: d for months in REGISTER_MONTHS.values() for k, _, d in months},
                **{kind: (months[-1][2] if months else REGISTERS_MARCH) for kind, months in REGISTER_MONTHS.items()}}
FOOD_AS_OF = NEW_PERMITS_TO
# The permit term rules (calls 161 and 172) read each source against its
# pinned date, never today (the Japan foundation's rule: the last day the
# source covers). Food: 2026-03-31, the rebuild's own as-of, since call 126
# keeps the March list whole and the months only add new permits: on
# 2026-08-31 the past-term rule would drop the 232 March permits ending April
# to August (143 of them re-permitted in a month, the rest kept as call 126
# keeps them), the brief's 2,503 restaurants instead of 2,560. The food rows
# carry no start column (許可年月日 is the grant), so the late-start rule reads
# nothing there. Registers: their 開始年月日 is read against the newest month
# each covers, so a July premises is not a late starter.
TERM_AS_OF = {"food": AS_OF.isoformat(),
              **{kind: SOURCE_AS_OF[kind] for kind in REGISTER_FILES}}
# What step 2 reads: the rebuilt food register, the three registers (each the
# March file plus its months) and MHLW's notifications.
SOURCES = {"food": SOURCE_FILES["food"][0],
           **{kind: SOURCE_FILES[f"{kind}_all"][0] for kind in REGISTER_FILES},
           "mhlw": SOURCE_FILES["mhlw"][0]}
# Declared, never inferred: the food CSVs are cp932 (CRLF), the registers
# XLSX, MHLW's file UTF-8 with a BOM.
SOURCE_ENCODING = {**{k: ("xlsx" if v[0].endswith(".xlsx") else "cp932") for k, v in SOURCE_FILES.items()},
                   "mhlw": "utf-8-sig"}
# The columns each raw file must carry; fetch_sources.py and source_rows stop
# on a header without them. 営業者氏名 (food), 開設者(申請者) (registers) and
# 法人名 (MHLW) are REQUIRED so the name rule (japan_register.name_is_operator)
# cannot silently compare nothing; they are read IN MEMORY by that rule only,
# never kept. Never selected: 施設電話番号, MHLW's 法人番号 / 法人住所 / phones.
FOOD_RAW_COLUMNS = ("許可番号", "営業所名称", "営業所所在地①", "営業者氏名", "営業の種類", "許可年月日",
                    "許可満了年月日")
REGISTER_RAW_COLUMNS = ("施設名称", "施設所在地", "開設者(申請者)", "開始年月日")
# Step 2 checks the rebuilt food rows (japan_register.rebuilt_register's
# premises columns) against REQUIRED_COLUMNS["food"], and fetch_sources.py the
# raw March list: the columns both shapes carry.
REQUIRED_COLUMNS = {
    "food": ("許可年月日", "許可満了年月日"),
    **{f"new_{m}": FOOD_RAW_COLUMNS for m, _ in MONTHS},
    **{f"{kind}_all": REGISTER_RAW_COLUMNS for kind in REGISTER_FILES},
    **{k: REGISTER_RAW_COLUMNS for months in REGISTER_MONTHS.values() for k, _, _ in months},
    **{kind: REGISTER_RAW_COLUMNS for kind in REGISTER_FILES},
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
# MHLW publishes an address only where the filer agreed to it.
ADDRESS_BY_CONSENT = {"mhlw"}
# MHLW's notification rows the block join misses take MHLW's own point (the
# brief: a median 39 m from the block point, 94.2% within 250 m; call 127c).
OWN_POINT_FALLBACK = {"mhlw"}
# A premises in both, in one bucket (a shop holding a city permit and filing
# an MHLW notification): MHLW's row stays, as in Matsuyama, Sakai and Toyonaka.
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def _checked(key, columns):
    """A raw file's path, after its header is checked for `columns`."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    head = next(iter(jr.city_rows(path)))
    missing = [c for c in columns if c not in head]
    if missing:
        raise SystemExit(f"{path.name}: header lacks {missing} - not the file the brief read")
    return path


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    "food" is the March list kept whole plus the five months' new permits,
    rebuilt by japan_register.rebuilt_register (call 126): where (address,
    trade name, type without （旧）) repeats, the permit ending latest wins;
    kept while 許可満了年月日 is on or after 2026-03-31. The brief: 3,175 + 236
    rows, 3,221 permits, 2,560 restaurants. Only premises columns are carried,
    plus the name rule's answer; no contact column leaves the file.
    "barber", "beauty" and "laundry" are each the March register plus its
    monthly new premises (call 155; Ichinomiya's call 128 shape). "mhlw" is
    MHLW's file, its notifications only (申請区分 届出 / 届出(廃業)), since the
    city's list holds every fixed permit; MHLW's permits are out (call 126)."""
    from pipeline.countries import japan
    from pipeline.countries import japan_register as jr

    if key == "food":
        paths = [_checked("food", FOOD_RAW_COLUMNS)] + [_checked(f"new_{m}", FOOD_RAW_COLUMNS) for m, _ in MONTHS]
        return jr.rebuilt_register(paths, AS_OF, end_col="許可満了年月日", rules=japan.city_rules(SLUG))
    if key in REGISTER_FILES:
        keys = [f"{key}_all"] + [k for k, _, _ in REGISTER_MONTHS[key]]
        return [r for k in keys for r in jr.city_rows(_checked(k, REGISTER_RAW_COLUMNS))]
    if key == "mhlw":
        return [r for r in jr.city_rows(_checked("mhlw", REQUIRED_COLUMNS["mhlw"]))
                if (r.get("申請区分") or "").startswith("届出")]
    raise KeyError(key)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 27210.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Hirakata.
# S, W, N, E: the city's N03 extent (S 34.773, W 135.614, N 34.881, E 135.747)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.77, 135.61, 34.89, 135.75)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word.
# 2026-10-07: 27 objects; Keihan signs 御殿山 as one word. The other 11 are
# OSM's as they stand.
OSM_NAME_EN_OVERRIDES = {
    "御殿山": "Gotenyama",                           # Goten-yama
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the N03 centroid's longitude (135.682) falls in the 132 to 138
# band. Derived per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule
# (docs/ring_rules.md): the median nearest-group gap is 1,510 m (the brief;
# re-measure if the stations change).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25, the
# brief: 3 lines, no Shinkansen): Keihan's Main Line (6 of 41) and Katano Line
# (4 of 8) and JR West's 片町線 (3 of 24), cut at the city line (owner
# 2026-09-24). No line is cut to one station.
LEFT_OUT_LINES = {}
# The Keihan Main Line and the Gakkentoshi Line run on into Kyoto Prefecture:
# its N03 names the stations beyond the prefecture line
# (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("26",)
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the JR line as 片町線; JR West
# signs it the JR Gakkentoshi Line (学研都市線), as Osaka's and Higashiōsaka's
# maps draw it.
_KH, _JR = "京阪電気鉄道", "西日本旅客鉄道"
LINES = {
    "KM": {"n02": [(_KH, "京阪本線")], "name": "Keihan Main Line", "name_ja": "京阪本線", "short": "Keihan",
           "hue": "#7B7B5A"},
    "KK": {"n02": [(_KH, "交野線")], "name": "Keihan Katano Line", "name_ja": "交野線", "short": "Keihan",
           "hue": "#00A040"},
    "JG": {"n02": [(_JR, "片町線")], "name": "JR Gakkentoshi Line", "name_ja": "学研都市線", "short": "JR",
           "hue": "#C303A8"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# hirakata` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its start (the Keihan Main and Gakkentoshi lines
# from Osaka's colours, landing on Higashiōsaka's for the latter; the Katano
# Line from a Keihan green) that reads 3:1 on both map pages and clears CIE76
# 45 from every pin. Closest pair 70.1 (Keihan's two lines, at 枚方市); the
# dark-mode labels separate, 3 of 3.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "KM": line_registry.colour("keihan-main-line"), "KK": "#28A800",
    "JG": line_registry.colour("jr-west-gakkentoshi-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city; step 1 lists each line's
# in-city stations (the brief: Main 6, Katano 4, Gakkentoshi 3).
GATE3 = {"source": "no line wholly inside the city", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
HIRAKATA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = HIRAKATA_BBOX
