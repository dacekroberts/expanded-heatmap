"""Chōfu-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/chofu.md (16/16 checks, 2026-10-07). One of East-1's
Tama-ledger cities, on the shared modules (pipeline/countries/japan*.py)
and the Tama ledgers' shared leg (pipeline/countries/tokyo_tama.py).

Business leg: the Tokyo Metropolitan Government's five Tama ledgers (food
permits, food notifications, barbers, beauty salons, laundries; as of
2026-08-31), cut to the city by address, plus MHLW's Tokyo filings the
ledgers lack (owner, call 169), one pin where a premises is in both. The
ledgers are partial by design and the page says so (call 109): the share it
states is at the yearbook's date (calls 187-189). Placed by a JOIN to MLIT's
位置参照情報 for the one municipality (13208, no wards); MHLW's own point
where the block join misses an MHLW row.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): Keio only, the Keio Line (8 of 35) and the Keio Sagamihara Line
(2 of 12, from its junction at 調布), both private lines cut at the city
line. No line has one station here, so nothing is left out. English station
names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline.countries import tokyo_tama

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "chofu" / "raw"
DATA_PROCESSED = ROOT / "data" / "chofu" / "processed"
OUTPUTS = ROOT / "outputs" / "chofu"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Chōfu"
SLUG = "chofu"
MUNICIPALITY = "調布市"
PREFECTURE = "東京都"

# The ledgers and MHLW's file, shared by the Tama cities (tokyo_tama): the
# files copied unchanged from data/tokyo_tama/raw/ into data/chofu/raw/
# at Step 0 (2026-10-06), since a Japanese build reads data/<slug>/raw/.
SOURCE_FILES = tokyo_tama.SOURCE_FILES
SOURCES = tokyo_tama.SOURCES
SOURCE_KIND = tokyo_tama.SOURCE_KIND
SOURCE_ENCODING = tokyo_tama.SOURCE_ENCODING
SOURCE_AS_OF = tokyo_tama.SOURCE_AS_OF
FOOD_AS_OF = tokyo_tama.AS_OF
TERM_AS_OF = tokyo_tama.TERM_AS_OF
REQUIRED_COLUMNS = tokyo_tama.REQUIRED_COLUMNS
ADDRESS_BY_CONSENT = tokyo_tama.ADDRESS_BY_CONSENT
OWN_POINT_FALLBACK = tokyo_tama.OWN_POINT_FALLBACK
SUPERSEDES = tokyo_tama.SUPERSEDES
SHARE_SKIP = tokyo_tama.SHARE_SKIP
# The share of the yearbook's counts, measured every build and written for the
# page (outputs/chofu/official_shares.json): restaurants against table
# 19-8, the registers against table 19-7, each also at the yearbook's date
OFFICIAL_SHARES = True
MUNICIPALITY_CODES = {MUNICIPALITY: "13208"}
SHARE_DATES = tokyo_tama.SHARE_DATES
REGISTER_SHARES = True


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """The city's rows of each Tama ledger and of MHLW's Tokyo file, cut by
    address (tokyo_tama.city_rows)."""
    from pipeline.countries.japan_step2 import need
    return tokyo_tama.city_rows(need(source_csv(key), SLUG), key, MUNICIPALITY)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 13208 alone:
# load_city_isj globs its directory, and data/tokyo_tama/raw/isj/ holds four
# municipalities' pairs (the brief).
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.633, W 139.517, N 35.688, E 139.593)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.63, 139.51, 35.69, 139.60)
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

# UTM zone 54N: the longitude (~139.55) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-group gap is 667 m (606 to 1,141 m), over the 550 m
# that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 2 lines, both Keio, no Shinkansen, JR, subway or monorail). The
# Keio Line keeps 8 of 35 (仙川 to 飛田給) and the Keio Sagamihara Line 2 of 12
# (調布, its junction with the Keio Line, and 京王多摩川), private lines cut at
# the city line (owner 2026-09-24). N02 files 調布 as one group for both lines
# (0 m span): 9 places. No line has one station inside, so no line is left out
# (calls 54 and 92 do not arise), and no N02 station lies within 300 m of the
# city line outside it (the brief).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
# The Sagamihara Line runs on into Kanagawa (Kawasaki's 多摩区, 京王稲田堤):
# Kanagawa's N03 names those stations, which Tokyo's alone names only "another
# prefecture" (Tama's precedent).
N03_NEIGHBOR_PREFS = ("14",)

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, in Tokyo's
# signage style; Keio's hue as in pipeline/tama/config.py, the same order, so
# the Sagamihara Line keeps Tama's colour.
LINES = {
    "KS": {"n02": [("京王電鉄", "相模原線")], "name": "Keio Sagamihara Line", "name_ja": "京王相模原線",
           "short": "Keio", "hue": "#DD0077"},
    "KO": {"n02": [("京王電鉄", "京王線")], "name": "Keio Line", "name_ja": "京王線",
           "short": "Keio", "hue": "#DD0077"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# chofu` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its operator's hue that reads 3:1 on both
# map pages and clears CIE76 45 from every pin (the Sagamihara Line's at 45.2).
# The Sagamihara Line's #F000B8 is Tama's and Kawasaki's; the Keio Line moves
# from Tama's #F848D0 (11.1 from it) to #E858D0, since here the two meet at 調布.
# The one pair, two Keio pinks, separates by 19.4 (re-measure if a line is
# added); the dark-mode labels, 2 of 2.
_COLOURS = {"KS": "#F000B8", "KO": "#E858D0"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: Keio's own station counts inside the city, as the brief gives them
# (2026-10-06: the Keio Line 8, the Sagamihara Line 2, 9 places), against the
# city line. 調布 is on both lines in Keio's own count too, so N02's shared
# group inflates neither.
GATE3 = {"source": "Keio's station counts inside the city (the brief, 2026-10-06), against the city line",
         "lines": {"KO": 8, "KS": 2}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
CHOFU_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = CHOFU_BBOX
