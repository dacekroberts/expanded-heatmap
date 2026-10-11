"""Maebashi-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/maebashi.md (9/9 checks, 2026-10-07). Japan's A/B batch
(Regional-1), on the shared modules (pipeline/countries/japan*.py) with the
Japan foundation's rules on (2026-10-07), in Fukuoka's and Utsunomiya's
two-source food shape plus registers rebuilt from a base list and its months.

Business leg: two food lists that split by date. MHLW's
食品衛生申請等システム open data holds every permit first granted from 2023 and
the notifications (opt-in, field by field); the city's own CC BY 4.0 file on
BODIK holds the permits from its former system still in term (granted
2019-10 to 2023-03-31; as of 2026-06-30). A premises in both is shown once
(config.SUPERSEDES). Personal services: the city's 生活衛生 registers (CC BY
2.1 JP on BODIK) rebuilt to 2026-08-31 from the 2026-03-31 base and five
months of new and closed files, every closure matched by 整理番号
(source_rows). All placed by a JOIN to MLIT's 位置参照情報 (one municipality, no
wards); where the block join misses an MHLW row, MHLW's own point.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). The Jomo Electric Railway's Jomo Line and JR East's Ryomo and Joetsu
lines. English station names from OpenStreetMap's name:en.
"""

import csv
import io
import re
import zipfile
from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "maebashi" / "raw"
DATA_PROCESSED = ROOT / "data" / "maebashi" / "processed"
OUTPUTS = ROOT / "outputs" / "maebashi"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Maebashi"
SLUG = "maebashi"
MUNICIPALITY = "前橋市"
PREFECTURE = "群馬県"

# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2;
# read 2026-09-24 for Fukuoka). A plain GET. Credit links the top page only.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# The city's two BODIK datasets (organisation 102016, author 健康部衛生検査課):
# the food file declares cc-by-40-intl, the registers cc-by-21-jp; the
# city's terms read 2026-10-05 put both under one credit naming both
# licences (owner, call 29).
BODIK = "https://data.bodik.jp"
BODIK_API = BODIK + "/api/3/action"
FOOD_PAGE = BODIK + "/dataset/102016_eiseikensa01"
LIFE_PAGE = BODIK + "/dataset/102016_eiseikensa02"
_FOOD_DS = BODIK + "/dataset/be0e8464-4b96-41f6-901d-1aa4bf11bcc0/resource/"
_LIFE_DS = BODIK + "/dataset/d66b613e-d058-4074-a343-9d86bb20381f/resource/"
# The registers' files: the base list and each month's new (sinki) and
# closed (haigyou) zips, 2026-04 to 2026-08. Fetched at Step 0 (2026-10-05);
# the resource ids are read from package_show at a re-fetch.
BASE_ZIP = "seikatueiseieigyousisetuitiranr8.3.31.zip"
MONTHS = (4, 5, 6, 7, 8)
NEW_ZIPS = tuple(f"sinkiseikatueiseieigyousisetuitiran_r8.{m}.zip" for m in MONTHS)
CLOSED_ZIPS = tuple(f"haigyouseikatueiseieigyousisetuitiran_r8.{m}.zip" for m in MONTHS)
# source key -> (file, URL of the edition this build read, the page that
# carries its licence). One entry per file fetched; the eleven register zips
# are one rebuild (source_rows). Only the base zip's resource URL is pinned:
# a monthly zip's URL is read from the dataset page's link to its file name
# (SOURCE_LINKS) at a re-fetch, never at a step.
_MONTH_KEYS = {f"reg_{kind}_{m}": name for kind, names in (("new", NEW_ZIPS), ("closed", CLOSED_ZIPS))
               for m, name in zip(MONTHS, names)}
SOURCE_FILES = {
    "mhlw": ("10201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=10201_food_business_all.csv",
             MHLW_TOP),
    "food": ("syokuhin20260630.xlsx",
             _FOOD_DS + "6808f251-ce78-4c09-a5d8-24a871a5d7e9/download/syokuhin20260630.xlsx", FOOD_PAGE),
    "reg_base": (BASE_ZIP, _LIFE_DS + "2bd28b54-0e08-497c-9c9a-2b708a84b8aa/download/" + BASE_ZIP, LIFE_PAGE),
    **{k: (name, LIFE_PAGE, LIFE_PAGE) for k, name in _MONTH_KEYS.items()},
}
SOURCE_LINKS = {k: re.escape(name) + "$" for k, name in _MONTH_KEYS.items()}
# Kyoto's rule: the date each list states, never the download's. MHLW's
# monthly file states none (its newest 許可年月日 2026-08-28, closures dated
# 2026-08); the food file's sheet reads R8.6.30現在; the base list 令和8年3月末現在,
# and each month file the month it names.
SOURCE_AS_OF = {"mhlw": None, "food": "2026-06-30", "reg_base": "2026-03-31",
                **{k: f"2026-{int(k.rsplit('_', 1)[1]):02d}" for k in _MONTH_KEYS}}
FOOD_AS_OF = SOURCE_AS_OF["food"]
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. MHLW's file covers August 2026;
# the food file's 179 rows expiring 2026-09-30 are in term on its own date.
TERM_AS_OF = {"mhlw": "2026-08-31", "food": "2026-06-30"}

SOURCES = {"mhlw": "10201_food_business_all.csv", "food": "syokuhin20260630.xlsx",
           "barber": BASE_ZIP, "beauty": BASE_ZIP, "laundry": BASE_ZIP}
# Declared, never inferred: MHLW's file UTF-8, the food file an XLSX, every
# register member a cp932 CSV (some padded with empty comma rows).
SOURCE_ENCODING = {"mhlw": "utf-8-sig", "barber": "cp932", "beauty": "cp932", "laundry": "cp932"}
# The columns each source must carry; step 2 stops on a header without them.
# The operator columns (MHLW's 法人名, a sole trader's own name on 1,482 rows;
# the food file's 営業者名; the registers' 開設者氏名 / 営業者氏名 and their
# representatives) are REQUIRED so the name rule (japan_register.
# name_is_operator; owner 2026-09-27) cannot silently compare nothing; read IN
# MEMORY by that rule only, never kept. Never selected: 法人番号, 法人住所,
# 開設者住所（法人のみ） / 営業者住所（法人のみ） (a company's address) and every phone.
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
    "food": ("営業の種類", "業態", "営業所名", "営業所所在地", "営業者名", "許可満了日"),
    "barber": ("整理番号", "施設名称", "施設所在地"),
    "beauty": ("整理番号", "施設名称", "施設所在地"),
    "laundry": ("整理番号", "施設名称", "施設所在地"),
    "reg_base": ("整理番号", "施設名称", "施設所在地"),
    **{k: ("整理番号", "施設名称", "施設所在地") for k in _MONTH_KEYS},
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses an MHLW row, MHLW's own point places it (the
# brief: 239 of 241 non-block rows carry one; a median 42 m from the block
# point, 92.4% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# One premises in both food lists: the city's old-system row goes, MHLW's
# (the renewal filed through the national system) stays. The brief's screen:
# 18 of the city's 1,431 block-tier restaurant permits (1.3%).
SUPERSEDES = {"mhlw": ("food",)}

# Each register's trade, as its member file names it (01理容所施設一覧,
# 02美容所施設一覧, 03クリーニング所施設一覧 / 03【廃業】クリーニング施設一覧).
_TRADE = {"barber": "理容", "beauty": "美容", "laundry": "クリーニング"}
# The register rows' key: unique in every base list and never blank (brief).
REGISTER_KEY = "整理番号"


def source_csv(key):
    return DATA_RAW / (SOURCES[key] if key in SOURCES else SOURCE_FILES[key][0])


def _register_members(zip_name, key=None):
    """Rows of one trade's CSV in one zip, or of every trade's where key is
    None (cp932; empty padding rows and the header's line breaks dropped). A
    trade with nothing that month has no CSV (its folder name says 該当なし)."""
    from pipeline.countries import japan_register as jr

    path = DATA_RAW / zip_name
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            name = jr.zip_member_name(info)
            leaf = name.rsplit("/", 1)[-1]
            if not leaf.lower().endswith(".csv") or (key and _TRADE[key] not in leaf):
                continue
            rows = csv.reader(io.StringIO(zf.read(info).decode("cp932")))
            head = [jr._header(c) for c in next(rows)]
            for r in rows:
                if not any(c.strip() for c in r):
                    continue
                yield dict(zip(head, r))


def _key(r):
    return re.sub(r"\s", "", r.get(REGISTER_KEY) or "")


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    The food lists as they are; each register rebuilt to 2026-08-31: the
    2026-03-31 base, plus each month's new premises, minus each month's
    closures, keyed by 整理番号. Exact, not an upper bound: a closure that
    matches no base or new row, a new row repeating a key, or a blank key
    stops the build."""
    from pipeline.countries import japan_register as jr

    if key in ("mhlw", "food"):
        path = source_csv(key)
        if not path.exists():
            raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
        yield from jr.city_rows(path)
        return
    live = {}
    for zip_name in (BASE_ZIP, *NEW_ZIPS):
        for r in _register_members(zip_name, key):
            k = _key(r)
            if not k or k in live:
                raise SystemExit(f"{key}: {zip_name}: a {'blank' if not k else 'repeated'} {REGISTER_KEY}")
            live[k] = r
    unmatched = 0
    for zip_name in CLOSED_ZIPS:
        for r in _register_members(zip_name, key):
            if live.pop(_key(r), None) is None:
                unmatched += 1
    if unmatched:
        raise SystemExit(f"{key}: {unmatched} closure(s) match no base or new {REGISTER_KEY}; the rebuild "
                         "would be an upper bound")
    yield from live.values()


def file_rows(key):
    """One fetched file's rows as it stands, for fetch_sources.py's count and
    header check (japan_fetch): a register zip's CSV members, every trade;
    the food lists by city_rows."""
    from pipeline.countries import japan_register as jr

    if key in ("mhlw", "food"):
        return jr.city_rows(source_csv(key))
    return _register_members(SOURCE_FILES[key][0])


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 10201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Maebashi.
# S, W, N, E: the city's N03 extent (S 36.3162, W 139.0019, N 36.5624,
# E 139.2301) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (36.30, 138.99, 36.58, 139.25)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (no macrons, lowercase after a hyphen, a
# katakana loanword kept as its English word, as Utsunomiya's センター). OSM's
# other 18 stand, JR's own Shim-Maebashi and Gumma-Soja among them.
OSM_NAME_EN_OVERRIDES = {
    "心臓血管センター": "Shinzo-kekkan Center",          # Shinzo-Kekkan Center
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the centre (~139.13) and the western edge (139.0019) fall in
# the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median nearest-station gap is
# 1,000 m: standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25: 3 lines, no Shinkansen station). Every line is cut at the city
# line (owner 2026-09-24): the Jomo Line keeps 14 of 23, JR's Ryomo Line 4 of
# 19 and Joetsu Line 2 of 39. JR's Agatsuma Line trains run through 群馬総社
# on the Joetsu Line's track, but N02 files that line from 渋川: no in-city
# station of its own, so it is not drawn. No frequency floor (owner,
# 2026-10-06, calls 46 and 86): the Jomo Line runs every 30 minutes.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names follow the operators' signs
# with no macrons, as Sasebo's and Kitakyushu's.
_JM, _JR = "上毛電気鉄道", "東日本旅客鉄道"
LINES = {
    "JM": {"n02": [(_JM, "上毛線")], "name": "Jomo Line", "name_ja": "上毛線", "short": "Jomo",
           "hue": "#0068B7"},
    "RY": {"n02": [(_JR, "両毛線")], "name": "JR Ryomo Line", "name_ja": "両毛線", "short": "JR",
           "hue": "#FFD400"},
    "JE": {"n02": [(_JR, "上越線")], "name": "JR Joetsu Line", "name_ja": "上越線", "short": "JR",
           "hue": "#00B261"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# maebashi` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. The Jomo Line's blue, which no
# blue clears Retail's pin in, goes teal (Sasebo's); the Ryomo yellow darkens
# to ochre to read on white. Closest pair 61.3 (Ryomo, Joetsu); the dark-mode
# labels separate, 3 of 3.
_COLOURS = {"JM": "#007890", "RY": "#B09000", "JE": "#20A800"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city. The Jomo Electric Railway's
# timetable index (jomorailway.com/timetable.html, read 2026-10-04) lists its
# 23 stations, 中央前橋 to 西桐生, as N02 does; 中央前橋 to 膳 (14) lie inside
# the city.
GATE3 = {"source": "The Jomo Electric Railway's timetable index (jomorailway.com/timetable.html): 23 stations, "
                   "中央前橋-膳 14 inside the city",
         "lines": {"JM": 14}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
MAEBASHI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = MAEBASHI_BBOX
