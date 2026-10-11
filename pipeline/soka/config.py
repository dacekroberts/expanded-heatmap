"""Sōka-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/soka.md (9/9 checks, 2026-10-07). Sōka City (草加市, 11221),
one municipality with no wards. The second of the four Saitama pages on the
shared Saitama leg (pipeline/countries/saitama_pref.py), after Ageo
(Regional).

Business leg: Saitama Prefecture's own lists for its health centres' areas,
cut to the city by address. Food: the live new-law layer, and the old-law
permits as the R8.3.31 old-law list with the live old-law layer (owner, call
171: in term, de-duplicated, renewals dropped, an upper bound as of
2026-03-31, disclosed). Personal services: the 草加保健所 area's FY-end 生活衛生
list (2026-03-31) plus the months to 2026-08. No food-share sentence (call
173): the publisher's withholding note is disclosed with no number. No MHLW
source (a control only, calls 126-127). Placed by a JOIN to MLIT's
位置参照情報 for the one municipality; the layers' own point where the block
join misses (call 127c).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): the Tobu Skytree Line (4 of N02's 55 伊勢崎線 stations), a main
line cut at the line (竹ノ塚 south, in Tokyo; 蒲生 north). English station
names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import saitama_pref

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "soka" / "raw"
DATA_PROCESSED = ROOT / "data" / "soka" / "processed"
OUTPUTS = ROOT / "outputs" / "soka"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Sōka"
SLUG = "soka"
MUNICIPALITY = "草加市"
PREFECTURE = saitama_pref.PREFECTURE
# Sōka is in the 草加保健所 area: its workbook in r7nenndo.zip
# (04草加保健所管内.xlsx, the one member the name matches)
HEALTH_CENTRE = "04草加"

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
    """The city's rows of each step-2 source, cut by address
    (saitama_pref.city_rows) at 草加市, as MLIT's 市区町村名 and the lists'
    addresses write it; the step stops naming fetch_sources.py where a file is
    missing."""
    from pipeline.countries.japan_step2 import need
    for k in SOURCE_FILES:
        need(source_csv(k), SLUG)
    return saitama_pref.city_rows(key, (MUNICIPALITY,), HEALTH_CENTRE)


def file_rows(key):
    """One file's rows as it stands, for fetch_sources.py's count and column check."""
    return saitama_pref.file_rows(key)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 11221 alone
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.805, W 139.764, N 35.872, E 139.841)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.80, 139.76, 35.88, 139.85)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-10-07): OSM gives 獨協大学前 its subtitle in 〈〉,
# as Tokyo's 押上〈スカイツリー前〉.
OSM_NAME_ALIASES = {"獨協大学前": "獨協大学前〈草加松原〉"}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons). The
# subtitle dropped, as Tokyo's Oshiage and Nijubashimae, so the English name
# matches N02's Japanese one.
OSM_NAME_EN_OVERRIDES = {
    "獨協大学前": "Dokkyodaigakumae",  # Dokkyodaigakumae〈Soka-Matsubara〉
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~139.80) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# median nearest-station gap is 1,400 m (step 1, 2026-10-07; the brief's
# 1,510 m is the upper of the two middle gaps, 1,289 and 1,510), over the 550 m
# that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 1 line). The Tobu Skytree Line keeps 4 of N02's 55 伊勢崎線
# stations (谷塚, 草加, 獨協大学前, 新田), a main line cut at the line (竹ノ塚
# south, 蒲生 north; 6.31 km inside, one piece), not a stub. No Shinkansen, JR,
# subway, tram or light rail in the city.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
# The line runs on south into Tokyo (足立区): its N03 names that excluded
# station (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("13",)

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the line as 伊勢崎線; the
# operator signs 浅草 / 押上 to 東武動物公園 the Tobu Skytree Line (the brief;
# Tokyo's TS entry, the same N02 track and hue). Line names without macrons,
# in Tokyo's signage style.
LINES = {
    "TS": {"n02": [("東武鉄道", "伊勢崎線")], "name": "Tobu Skytree Line", "name_ja": "東武スカイツリーライン",
           "short": "Tobu", "hue": "#0F6CC3"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py soka`
# (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): the feasible
# colour nearest the operator's hue that reads 3:1 on both map pages and
# clears CIE76 45 from every pin. Tobu's blue sits beside the Retail pin's
# blue, so the search moved it to a cyan (45.1 from Retail, the nearest pin;
# 6.06 on the dark page, 3.09 on the light). One line: no pair; the dark-mode label, 1 of 1.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "TS": line_registry.colour("tobu-skytree-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own stations inside the city line (the brief: Tōbu's
# 谷塚, 草加, 獨協大学前 and 新田, 2026-10-06).
GATE3 = {"source": "Tobu's station pages (tobu.co.jp/railway/guide/station/), read against the city line",
         "lines": {"TS": 4}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
SOKA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = SOKA_BBOX
