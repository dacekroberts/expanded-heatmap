"""Naha-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/naha.md
(6/6 checks, 2026-10-12). Okinawa's first city, on the shared Japanese modules
(pipeline/countries/japan*.py) with the Japan foundation's rules on
(ALL_RULES). Food plus Personal services (owner, calls S30 and S38).

Business leg: three BODIK packages of Naha City (data.bodik.jp, organization
472018, CC BY 4.0), BODIK's copies only: the city's own site hosts the same
lists under terms that reserve all rights. Food is a REBUILT register, Kyoto's
shape: the city publishes no full food-permit list, only each month's new
permits (140 files, 2015-04 to 2026-08) and, to 2021-05, each month's renewals
(73 files; owner, call S31: both), stitched by
japan_register.rebuilt_register and kept while in term on the pinned AS_OF.
Closures are invisible, so the count is an UPPER BOUND, and the page says so
(owner, call S32). Personal services are the city's barber and beauty-salon
registers as of 2026-09-04, complete lists read as they are; no laundry list
is published. Everything is placed by a JOIN to MLIT's 位置参照情報 for the
one municipality (47201, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). One line, the Okinawa Urban Monorail (Yui Rail), cut at the city line:
its last three stations are in Urasoe. English station names from
OpenStreetMap's name:en.
"""

import calendar
import datetime
import functools
import re
from pathlib import Path

from pipeline import line_registry
from pipeline.naha import bodik_files

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "naha" / "raw"
DATA_PROCESSED = ROOT / "data" / "naha" / "processed"
OUTPUTS = ROOT / "outputs" / "naha"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Naha"
SLUG = "naha"
MUNICIPALITY = "那覇市"
PREFECTURE = "沖縄県"

# The three packages' pages. Each declares cc-by-40-intl and links the city's
# open-data terms (odcs.bodik.jp/472018/tos/: CC BY 4.0 unless annotated);
# read 2026-10-11 and 2026-10-12, PERMITTED WITH CONDITIONS (a credit to the
# city with the dataset names, and a statement that the data was modified).
BODIK = "https://data.bodik.jp/dataset"
FOOD_NEW_PAGE = f"{BODIK}/{bodik_files.SHINKI_PACKAGE[0]}"
FOOD_RENEWAL_PAGE = f"{BODIK}/{bodik_files.KEIZOKU_PACKAGE[0]}"
REGISTERS_PAGE = f"{BODIK}/{bodik_files.RIBIYOU_PACKAGE[0]}"
# BODIK rate-limits (it blocked a probe after about 100 rapid calls,
# 2026-10-04): japan_fetch waits this long after each file it downloads. The
# 215 files were fetched at Step 0 one every 21 to 25 s and are kept on disk.
FETCH_PAUSE_S = 21

_ERA = {"h": 1988, "r": 2018}


def _month_end(name):
    """The last day of the month a monthly file covers, from its name
    (h27.4_shinki.xls is April 2015, r03.5_keizoku.xlsx May 2021)."""
    era, year, month = re.match(r"([hr])(\d+)\.(\d+)", name).groups()
    year = _ERA[era] + int(year)
    return datetime.date(year, int(month), calendar.monthrange(year, int(month))[1])


# Every file's URL is this template filled from pipeline/naha/bodik_files.py
# (source_url): 215 resources, each pinned by its id.
RESOURCE_URL = "https://data.bodik.jp/dataset/{package}/resource/{resource}/download/{file}"
_PACKAGES = {"shinki": bodik_files.SHINKI_PACKAGE, "keizoku": bodik_files.KEIZOKU_PACKAGE,
             "ribiyou": bodik_files.RIBIYOU_PACKAGE}


def _monthly(folder, resources, page):
    """SOURCE_FILES entries for one package's monthly files: the key and the
    cached file both carry the resource id's first eight characters, since two
    August 2026 resources share one file name. No URL is written out
    (japan_fetch asks source_url)."""
    return {f"{folder}_{rid[:8]}": (f"{folder}/{rid[:8]}_{name}", None, page) for rid, name in resources}


_NEW = _monthly("shinki", bodik_files.SHINKI, FOOD_NEW_PAGE)
_RENEWALS = _monthly("keizoku", bodik_files.KEIZOKU, FOOD_RENEWAL_PAGE)
_BEAUTY, _BARBER = bodik_files.RIBIYOU
SOURCE_FILES = {
    **_NEW,
    **_RENEWALS,
    "barber": (f"ribiyou/{_BARBER[1]}", None, REGISTERS_PAGE),
    "beauty": (f"ribiyou/{_BEAUTY[1]}", None, REGISTERS_PAGE),
}
_RESOURCE_IDS = {**{f"shinki_{rid[:8]}": (rid, name) for rid, name in bodik_files.SHINKI},
                 **{f"keizoku_{rid[:8]}": (rid, name) for rid, name in bodik_files.KEIZOKU},
                 "barber": _BARBER, "beauty": _BEAUTY}


def source_url(key):
    """The BODIK download URL of one pinned resource."""
    rid, name = _RESOURCE_IDS[key]
    folder = SOURCE_FILES[key][0].split("/", 1)[0]
    return RESOURCE_URL.format(package=_PACKAGES[folder][1], resource=rid, file=name)


# The rebuild's date, PINNED (owner 2026-09-28, Kyoto: the last day the newest
# list covers, never the download date or today): the newest monthly file is
# August 2026's. A newer month moves it and every count below.
AS_OF = datetime.date(2026, 8, 31)
FOOD_AS_OF = AS_OF.isoformat()
# The registers' own date, from each workbook's title row (令和8年9月4日時点).
REGISTERS_AS_OF = "2026-09-04"
SOURCE_AS_OF = {"food": FOOD_AS_OF, "barber": REGISTERS_AS_OF, "beauty": REGISTERS_AS_OF,
                **{k: _month_end(v[0].split("_", 1)[1]).isoformat() for k, v in {**_NEW, **_RENEWALS}.items()}}
# The permit term rules (calls 161 and 172) read the rebuilt register against
# its own pinned as-of. The registers carry no term column.
TERM_AS_OF = {"food": FOOD_AS_OF}

# What step 2 reads; the key is the taxonomy's `source` column.
SOURCES = {"food": "the rebuilt register", "barber": SOURCE_FILES["barber"][0], "beauty": SOURCE_FILES["beauty"][0]}
SOURCE_ENCODING = {k: "xlsx" if v[0].endswith(".xlsx") else "xls" for k, v in SOURCE_FILES.items()}
# The columns each source must carry. The monthly workbooks arrive under 29
# header rows (new permits) and 21 (renewals), so no one spelling is required
# of them: _monthly_rows checks each file by ROLE through the shared column
# lists instead. The rebuilt register carries only premises columns and the
# name rule's yes or no (japan_register.rebuilt_register compares 申請者名 and
# 代表者名 in memory; owner 2026-09-27). The registers' 開設者氏名 is REQUIRED so
# the name rule cannot silently compare nothing; it is read IN MEMORY by that
# rule only, never kept. Never selected, in any file: the applicant's address
# (one to three columns), 代表者役職 and every phone column.
_REGISTER_COLUMNS = ("施設名称", "施設住所", "開設者氏名", "確認年月日")
REQUIRED_COLUMNS = {
    **{k: () for k in (*_NEW, *_RENEWALS)},
    "food": ("所在地", "施設名称", "業種", "有効期限", "許可日", "name_is_operator"),
    "barber": _REGISTER_COLUMNS,
    "beauty": _REGISTER_COLUMNS,
}
# 法人 (2026-02, 2026-03): a one-or-two-character mark beside a company's
# 申請者名 on 128 rows. A flag, not a name, so the name rule does not read it.
NOT_OPERATOR = {"法人": "a one-character company mark, not a name"}
# The permit term's spellings across the monthly files, read in order
# (japan_register.END_COLS lacks 有効期間: with it alone the stitch keeps
# 2,573 permits, not 10,002; the brief).
END_COLS = ("有効期限", "有効期間", "許可終了日")
GRANTED_COLS = ("許可日", "許可年月日", "許可開始日")
# From 2019 the form (業態: バー, 自動販売機, 臨時営業) sits in an UNNAMED
# column beside the type, which the shared readers name 種目 where the column
# before it carries one of these headers. All four type spellings are needed
# as keys (3,611 forms read; 3,596 with the first alone; Cleanup, 2026-10-12).
# Without it 54 hostess venues, 38 vending machines and 7 caterers in term
# read as restaurants.
UNNAMED_AFTER = {"営業の種類": "種目", "営業所種類": "種目", "業種": "種目", "営業の種目": "種目"}
# One renewal file (October 2016, 68 rows) heads its TYPE column 種目, which
# the shared lists read as the form, so its rows read no type. Every one
# expired by 2023, so nothing of it reaches the stitch's output; _monthly_rows
# stops the build if a row of it is ever in term. A shared-reader gap, parked
# for Cleanup (docs/decisions_drafts/worktree-japan-naha.md), not fixed here.
TYPE_UNREAD = {"b655ef39_h28.10_keizoku.xls": "its type column is headed 種目"}
# The official restaurant count the rebuild is measured against each build
# (e-Stat 衛生行政報告例 FY2024, in force at 2025-03-31), written to
# outputs/naha/official_shares.json for the page's upper-bound sentence.
OFFICIAL_SHARES = True


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def _reader():
    from pipeline.countries import japan_register as jr

    return functools.partial(jr.city_rows, unnamed_after=UNNAMED_AFTER)


def file_rows(key):
    """One cached file's rows as this city reads it (japan_fetch's hook)."""
    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    return _reader()(path)


def _monthly_rows(path):
    """A monthly workbook's rows, after its header is checked by role: an
    address, a trade name, a type and an expiry each under a spelling the
    shared lists read. A file that fails is a shared-reader gap (a parked call
    for Cleanup), never a city-local fix."""
    from pipeline.countries import japan
    from pipeline.countries import japan_register as jr

    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    rows = list(_reader()(path))
    heads = set().union(*(r.keys() for r in rows)) if rows else set()
    roles = {"address": jr.ADDR_COLS, "trade name": jr.NAME_COLS, "type": jr.type_cols(japan.city_rules(SLUG)),
             "expiry": END_COLS}
    unread = [role for role, cols in roles.items() if not heads & set(cols)]
    if unread == ["type"] and path.name in TYPE_UNREAD:
        live = sum(1 for r in rows if (jr._date_of(r, END_COLS) or AS_OF) >= AS_OF)
        if live:
            raise SystemExit(f"{path.name}: {live} row(s) in term on {AS_OF} with no type read ({TYPE_UNREAD[path.name]})")
        unread = []
    if unread:
        raise SystemExit(f"{path.name}: no column read as {unread} (header {sorted(map(str, heads))})")
    return rows


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    "food" is the register rebuilt from every monthly new-permit file and
    every monthly renewal file (owner, call S31), oldest first: where
    (address, trade name, type) repeats, the permit ending latest wins; kept
    while its term runs on or after AS_OF. Only premises columns leave the
    stitch, plus the name rule's answer. "barber" and "beauty" are the two
    registers, read as they are."""
    from pipeline.countries import japan
    from pipeline.countries import japan_register as jr

    if key == "food":
        paths = [source_csv(k) for k in (*_NEW, *_RENEWALS)]
        return jr.rebuilt_register(paths, AS_OF, end_col=END_COLS, granted_col=GRANTED_COLS,
                                   rules=japan.city_rules(SLUG), reader=_monthly_rows)
    return list(file_rows(key))


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 47201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (S 26.176, W 127.630, N 26.253, E 127.739,
# the offshore islets included; the brief) rounded out; step 1 stops if the
# city leaves it.
OSM_BBOX = (26.17, 127.62, 26.26, 127.74)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# No override: the owner chose the operator's own English (2026-10-12), and
# OSM's name:en for all 16 stations is the operator's, word for word
# (www.yui-rail.co.jp/en/, read 2026-10-12: Naha Airport, Onoyama Park,
# Prefectural Office, Naha City Hospital and twelve romanised names). This
# departs from Hiroshima's romanised style (Itami's Osaka-kuko) on purpose.
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 52N: the N03 centroid's longitude (127.684) falls in the 126 to 132
# band. Derived per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# Standard rings by the spacing rule (docs/ring_rules.md): the median
# nearest-group gap among the 16 in-city stations is 733 m (the brief), over
# the rule's 550 m. Re-measure if the stations change.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Okinawa's only N02 line (stub_test on N02-25, the brief): the monorail keeps
# 16 of its 19 stations inside the city line; 経塚, 浦添前田 and てだこ浦西 are
# in Urasoe and are cut (owner 2026-09-24; Urasoe is a separate add-on row).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese) and the project's colour. N02 files the line as 沖縄都市モノレール線;
# the operator signs it, in both languages, as the Yui Rail (ゆいレール).
_OM = "沖縄都市モノレール"
LINES = {
    "YR": {"n02": [(_OM, "沖縄都市モノレール線")], "name": "Yui Rail", "name_ja": "ゆいレール", "short": "Yui Rail",
           "hue": "#C8102E"},
}
# The line's one site-wide colour is pipeline/line_registry.py's (owner,
# 2026-10-07): the Urasoe add-on will draw the same line. Chosen by `python
# scripts/line_colour_search.py naha` (2026-10-12) from `hue`, the red of the
# trains' stripe (the operator publishes no line colour): #E84028, 3:1 on
# both map pages (4.63 dark, 4.04 light), CIE76 45.0 from the nearest pin.
_COLOURS = {"YR": line_registry.colour("okinawa-urban-monorail")}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS[_k]
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city, so step 1 has no per-line count
# to compare. Read against the operator's own station list instead
# (www.yui-rail.co.jp, the home page's 駅情報 list, 2026-10-12): 19 stations,
# 那覇空港 to てだこ浦西, the same 19 names in N02's order; the first 16 are the
# 16 inside the city and the last three (経塚, 浦添前田, てだこ浦西) Urasoe's.
GATE3 = {"source": "no line wholly inside the city; the operator's station list (19) matches N02's", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
NAHA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = NAHA_BBOX
