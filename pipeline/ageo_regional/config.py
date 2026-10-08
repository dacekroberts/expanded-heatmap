"""Ageo (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/ageo_regional.md (15/15 checks, 2026-10-07). Ageo City
(上尾市, 11219) and Ina Town (伊奈町, 11301) on one page (owner, call 102: Ina
too thin alone; the same source and the same line). A first build of a
two-municipality page, not an extension of a built one. The first of the four
Saitama pages on the shared Saitama leg (pipeline/countries/saitama_pref.py).

Business leg: Saitama Prefecture's own lists for its health centres' areas,
cut to the two municipalities by address. Food: the live new-law layer, and
the old-law permits as the R8.3.31 old-law list with the live old-law layer
(owner, call 171: in term, de-duplicated, renewals dropped, an upper bound as
of 2026-03-31, disclosed). Personal services: the 鴻巣保健所 area's FY-end
生活衛生 list (2026-03-31) plus the months to 2026-08. No food-share sentence
(call 173): the publisher's withholding note is disclosed with no number. No
MHLW source (a control only, calls 126-127). Placed by a JOIN to MLIT's
位置参照情報 keyed by municipality (japan.CITIES "municipalities"); the
layers' own point where the block join misses (call 127c).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the two
municipalities' line (N03): the New Shuttle (7 of 13, cut once at the Saitama
City line; 内宿 is its terminus, in Ina) and the JR Takasaki Line (2 of 19).
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import saitama_pref

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "ageo_regional" / "raw"
DATA_PROCESSED = ROOT / "data" / "ageo_regional" / "processed"
OUTPUTS = ROOT / "outputs" / "ageo_regional"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the two municipalities, with where each is (a citable
# scoping record, as in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Ageo (Regional)"
SLUG = "ageo_regional"
MUNICIPALITY = "上尾市"
PREFECTURE = saitama_pref.PREFECTURE
# Ageo and Ina are both in the 鴻巣保健所 area: its workbook in r7nenndo.zip
HEALTH_CENTRE = "05鴻巣"

# Saitama Prefecture's files, shared by the four Saitama pages in
# data/saitama_pref/raw/ (saitama_pref.SOURCE_FILES; never re-pulled from a
# branch, the shared data/ rule)
SOURCE_FILES = saitama_pref.SOURCE_FILES
SOURCES = saitama_pref.SOURCES
SOURCE_KIND = saitama_pref.SOURCE_KIND
SOURCE_AS_OF = saitama_pref.SOURCE_AS_OF
FOOD_AS_OF = saitama_pref.FOOD_AS_OF
REGISTERS_AS_OF = saitama_pref.REGISTERS_AS_OF
TERM_AS_OF = saitama_pref.TERM_AS_OF
REQUIRED_COLUMNS = saitama_pref.REQUIRED_COLUMNS
OWN_POINT_FALLBACK = saitama_pref.OWN_POINT_FALLBACK


def source_csv(key):
    """A file in the shared Saitama cache, by file key or step-2 source key."""
    name = SOURCE_FILES[key][0] if key in SOURCE_FILES else SOURCES[key]
    return saitama_pref.RAW_DIR / name


def source_rows(key):
    """The two municipalities' rows of each step-2 source, cut by address
    (saitama_pref.city_rows) at the names japan.CITIES gives them, as MLIT's
    市区町村名 and the lists' addresses write them (上尾市, 北足立郡伊奈町); the
    step stops naming fetch_sources.py where a file is missing."""
    from pipeline.countries import japan
    from pipeline.countries.japan_step2 import need
    for k in SOURCE_FILES:
        need(source_csv(k), SLUG)
    return saitama_pref.city_rows(key, tuple(japan.CITIES[SLUG]["municipalities"].values()), HEALTH_CENTRE)


def file_rows(key):
    """One file's rows as it stands, for fetch_sources.py's count and column check."""
    return saitama_pref.file_rows(key)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 11219 and 11301:
# load_city_isj keys each by its municipality (the page names several)
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the two municipalities' N03 extent (S 35.926, W 139.534,
# N 36.027, E 139.650) rounded out; step 1 stops if the scope leaves it.
OSM_BBOX = (35.92, 139.53, 36.03, 139.65)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment). None: the nine groups' OSM names are in one style already
# (Ina-Chuo, Kita-Ageo; no macrons), read 2026-10-07.
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~139.59) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# median nearest-station gap is 1,045 m (the brief; step 1 reprints it), over
# the 550 m that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the two municipalities (stub_test on
# N02-25: 2 lines). The New Shuttle keeps 7 of 13 (Ageo 原市, 沼南; Ina 丸山,
# 志久, 伊奈中央, 羽貫, 内宿), cut once at the Saitama City line south of 原市;
# 内宿 is its terminus. The JR Takasaki Line keeps 2 of 19 (上尾, 北上尾), a
# main line cut at the line (宮原 south, 桶川 north), not a stub. The
# Shinkansen crosses with no station (the standing call), and the JR Tohoku
# (Utsunomiya) Line crosses Ageo's eastern edge for 1.44 km with no station
# (the brief): neither is in LINES.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
# No N03_NEIGHBOR_PREFS: step 1 reads stations within 3 km of the line, and
# those 7 excluded are all in Saitama (さいたま市北区 5, 大宮区 1, 桶川市 1).

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. The New Shuttle's English name is the
# operator's own, on its timetable (the brief).
LINES = {
    "NS": {"n02": [("埼玉新都市交通", "伊奈線")], "name": "New Shuttle", "name_ja": "ニューシャトル",
           "short": "New Shuttle", "hue": "#00A06E"},
    "JT": {"n02": [("東日本旅客鉄道", "高崎線")], "name": "JR Takasaki Line", "name_ja": "高崎線",
           "short": "JR", "hue": "#F68B1E"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# ageo_regional` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. The New Shuttle's green hue sits beside
# the Food-service pin, so the search muted it (45.0 from the pins; 3.05 on the
# dark page). The pair separates by 85.1; the dark-mode labels, 2 of 2.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "NS": "#486860", "JT": line_registry.colour("jr-east-utsunomiya-takasaki-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own stations inside the two municipalities (the
# brief, read 2026-10-06): JR East's station pages for 上尾 and 北上尾, the New
# Shuttle's station pages for its seven.
GATE3 = {"source": "JR East's and the New Shuttle's station pages (timetables.jreast.co.jp, new-shuttle.jp), "
                   "read against the two municipalities' line",
         "lines": {"NS": 7, "JT": 2}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the two municipalities' N03 extent,
# rounded out.
AGEO_REGIONAL_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = AGEO_REGIONAL_BBOX
