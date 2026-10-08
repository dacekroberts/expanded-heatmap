"""Kasukabe-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/kasukabe.md (11/11 checks, 2026-10-07). Kasukabe City
(春日部市, 11214), one municipality with no wards. One of the four Saitama
pages on the shared Saitama leg (pipeline/countries/saitama_pref.py), after
Ageo (Regional), Sōka and Tokorozawa.

Business leg: Saitama Prefecture's own lists for its health centres' areas,
cut to the city by address. Food: the live new-law layer, and the old-law
permits as the R8.3.31 old-law list with the live old-law layer (owner, call
171: in term, de-duplicated, renewals dropped, an upper bound as of
2026-03-31, disclosed; call 172: rows starting after the as-of dropped).
Personal services: the 春日部保健所 area's FY-end 生活衛生 list (2026-03-31)
plus the months to 2026-08. No food-share sentence (call 173): the
publisher's withholding note is disclosed with no number. No MHLW source (a
control only, calls 126-127). Placed by a JOIN to MLIT's 位置参照情報 for the
one municipality; the layers' own point where the block join misses (call
127c).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): the Tobu Skytree Line (4 of N02's 55 伊勢崎線 stations) and the
Tobu Urban Park Line (5 of N02's 35 野田線 stations), main lines cut at the
line, meeting at 春日部. English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import saitama_pref

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kasukabe" / "raw"
DATA_PROCESSED = ROOT / "data" / "kasukabe" / "processed"
OUTPUTS = ROOT / "outputs" / "kasukabe"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kasukabe"
SLUG = "kasukabe"
MUNICIPALITY = "春日部市"
PREFECTURE = saitama_pref.PREFECTURE
# Kasukabe is in the 春日部保健所 area (春日部市, 北葛飾郡松伏町): its workbook
# in r7nenndo.zip (03春日部保健所管内.xlsx, the one member the name matches)
HEALTH_CENTRE = "03春日部"

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
    (saitama_pref.city_rows) at 春日部市, as MLIT's 市区町村名 and the lists'
    addresses write it; the step stops naming fetch_sources.py where a file is
    missing."""
    from pipeline.countries.japan_step2 import need
    for k in SOURCE_FILES:
        need(source_csv(k), SLUG)
    return saitama_pref.city_rows(key, (MUNICIPALITY,), HEALTH_CENTRE)


def file_rows(key):
    """One file's rows as it stands, for fetch_sources.py's count and column check."""
    return saitama_pref.file_rows(key)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 11214 alone
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.936, W 139.708, N 36.043, E 139.833)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.93, 139.70, 36.05, 139.84)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~139.78) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: step 1's
# median nearest-station gap is 1,802 m (8 stations, 2026-10-07; nearest pair
# 935 m; the brief's figure), over the 550 m that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 2 lines, 9 station records, 8 station groups). The Tobu Skytree
# Line keeps 4 of N02's 55 伊勢崎線 stations (武里, 一ノ割, 春日部, 北春日部)
# and the Tobu Urban Park Line 5 of N02's 35 野田線 stations (豊春, 八木崎,
# 春日部, 藤の牛島, 南桜井): main lines cut at the city line, neither a stub,
# meeting at 春日部 (one station group). No Shinkansen, JR, subway, tram or
# light rail in the city.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
# The Urban Park Line runs on east into Chiba (野田市): its N03 names that
# excluded station (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("12",)

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the lines as 伊勢崎線 and
# 野田線; the operator signs 浅草 / 押上 to 東武動物公園 the Tobu Skytree Line
# (the brief; Tokyo's and Sōka's TS entry, the same N02 track and hue) and
# the 野田線 the Tobu Urban Park Line (東武アーバンパークライン, the brief). Line
# names without macrons, in Tokyo's signage style. The Urban Park Line's hue
# is a seed, not read from Tobu: the green of the line's two brand colours
# (blue and green), so the two lines that meet at 春日部 separate
# (Tokorozawa's approach, the drafts' parked colour call 1, set B). Seeded
# with the brand's blue (#00A0E9) instead, the search gives #488090, 18.2
# from the Skytree Line's cyan at their shared station, the floor.
LINES = {
    "TS": {"n02": [("東武鉄道", "伊勢崎線")], "name": "Tobu Skytree Line", "name_ja": "東武スカイツリーライン",
           "short": "Tobu", "hue": "#0F6CC3"},
    "TD": {"n02": [("東武鉄道", "野田線")], "name": "Tobu Urban Park Line", "name_ja": "東武アーバンパークライン",
           "short": "Tobu", "hue": "#7FBE26"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# kasukabe` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its seed that reads 3:1 on both map pages and
# clears CIE76 45 from every pin. The Skytree Line takes Sōka's cyan (45.1
# from Retail, the nearest pin; 6.06 on the dark page, 3.09 on the light);
# the Urban Park Line a green (45.3 from the nearest pin; 5.82 dark, 3.22
# light). The pair: 89.7 apart, within 500 m at 春日部; the dark-mode labels,
# 2 distinct of 2.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "TS": line_registry.colour("tobu-skytree-line"), "TD": "#60A000",
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own stations inside the city line (the brief: Tōbu's
# Skytree Line 4 and Urban Park Line 5, 春日部 on both, 2026-10-06).
GATE3 = {"source": "Tobu's station pages (tobu.co.jp/railway/guide/station/), read against the city line",
         "lines": {"TS": 4, "TD": 5}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KASUKABE_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KASUKABE_BBOX
