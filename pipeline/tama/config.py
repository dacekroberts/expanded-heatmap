"""Tama-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/tama.md (13/13 checks, 2026-10-07). One of East-1's
Tama-ledger cities, Higashiyamato's twin on the same ledgers, on the shared
modules (pipeline/countries/japan*.py) and the Tama ledgers' shared leg
(pipeline/countries/tokyo_tama.py).

Business leg: the Tokyo Metropolitan Government's five Tama ledgers (food
permits, food notifications, barbers, beauty salons, laundries; as of
2026-08-31), cut to the city by address, plus MHLW's Tokyo filings the
ledgers lack (owner, call 169), one pin where a premises is in both. The
ledgers are partial by design and the page says so (call 109): the share it
states is at the yearbook's date (calls 187-189). Placed by a JOIN to MLIT's
位置参照情報 for the one municipality (13224, no wards); MHLW's own point
where the block join misses an MHLW row.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): the Odakyu Tama Line (3 of 8), the Keio Sagamihara Line (2 of
12) and the Keio Line's one station, 聖蹟桜ヶ丘, drawn as cut (a private
one-station stub, the standing call). The Tama Toshi Monorail's one station,
多摩センター, is left out with its line (calls 54 and 92): the Keio and Odakyu
stations of the same name keep the ring. English station names from
OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import tokyo_tama

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "tama" / "raw"
DATA_PROCESSED = ROOT / "data" / "tama" / "processed"
OUTPUTS = ROOT / "outputs" / "tama"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Tama"
SLUG = "tama"
MUNICIPALITY = "多摩市"
PREFECTURE = "東京都"

# The ledgers and MHLW's file, shared by the Tama cities (tokyo_tama): the
# files copied unchanged from data/tokyo_tama/raw/ into data/tama/raw/
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
# page (outputs/tama/official_shares.json): restaurants against table
# 19-8, the registers against table 19-7, each also at the yearbook's date
OFFICIAL_SHARES = True
MUNICIPALITY_CODES = {MUNICIPALITY: "13224"}
SHARE_DATES = tokyo_tama.SHARE_DATES
REGISTER_SHARES = True


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """The city's rows of each Tama ledger and of MHLW's Tokyo file, cut by
    address (tokyo_tama.city_rows)."""
    from pipeline.countries.japan_step2 import need
    return tokyo_tama.city_rows(need(source_csv(key), SLUG), key, MUNICIPALITY)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 13224 alone:
# load_city_isj globs its directory, and data/tokyo_tama/raw/isj/ holds four
# municipalities' pairs (the brief).
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.605, W 139.394, N 35.658, E 139.474)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.60, 139.39, 35.66, 139.48)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons).
# OSM writes "Keio-Nagayama"; Keio's other names here keep the lowercase after
# the hyphen (OSM's Keio-tama-center and Seiseki-sakuragaoka, Kawasaki's
# Keio-inadazutsumi), so one Keio style.
OSM_NAME_EN_OVERRIDES = {"京王永山": "Keio-nagayama"}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~139.44) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: step 1's
# six stations stand at four places (the two 38 m Keio / Odakyu pairs), whose
# median nearest-place gap is 1,856 m (2026-10-07), far over the 550 m that
# halves them. The literal station median is 38 m, the pairs themselves.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]
# Gate 1's floor: PROVISIONAL (parked for the owner). Four of the six stations
# are the two 38 m Keio / Odakyu pairs the brief keeps apart, so the literal
# median nearest-station gap is 38 m and the 400 m default stops step 1. Set
# just under the pair, as Tbilisi's 100 m sits under its two Station Squares
# (110 m, both in the operator's count); gate 3 counts both of each pair.
SPACING_MIN_M = 30.0

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 4 lines, no Shinkansen). The Odakyu Tama Line keeps 3 of 8
# (小田急永山, 小田急多摩センター, 唐木田, its terminus) and the Keio Sagamihara Line
# 2 of 12 (京王永山, 京王多摩センター), private lines cut at the city line (owner
# 2026-09-24); the Keio Line keeps 1 of 35 (聖蹟桜ヶ丘), a private line drawn as
# cut (the standing call, Kobe's JR Takarazuka Line). N02 files the Keio and
# Odakyu stations at 永山 and at 多摩センター under their own group codes, 38 m
# apart each; they stay two stations each (the brief: Kyoto's Yamashina and
# Keihan-Yamashina precedent).
LEFT_OUT_LINES = {
    # An urban line cut to ONE station, whose place other lines serve (owner,
    # calls 54 and 92): 多摩センター, 1 of 19, its own group 187 m from
    # 小田急多摩センター and 197 m from 京王多摩センター, which keep the ring.
    ("多摩都市モノレール", "多摩都市モノレール線"):
        "one station inside the city (多摩センター), served by the Keio and Odakyu stations beside it (calls 54, 92)",
}
COLLAPSE_MAX_SPREAD_M = 300
# The Tama and Sagamihara lines run on into Kanagawa (Kawasaki's 麻生区):
# Kanagawa's N03 names those stations, which Tokyo's alone names only "another
# prefecture" (Kawasaki's precedent, the other way across the line).
N03_NEIGHBOR_PREFS = ("14",)

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, in Tokyo's
# signage style. The Sagamihara Line starts from Keio's magenta (its station
# numbering colour; Chofu's and Kawasaki's #F000B8). The Keio Line's violet
# is a seed, not read from Keio: one distinct hue for the Keio Line in Chofu,
# Fuchu, Hino and Tama (the owner, 2026-10-07: distinct colours; from one
# magenta the two read 11.1 apart here).
LINES = {
    "OT": {"n02": [("小田急電鉄", "多摩線")], "name": "Odakyu Tama Line", "name_ja": "小田急多摩線",
           "short": "Odakyu", "hue": "#2288CC"},
    "KS": {"n02": [("京王電鉄", "相模原線")], "name": "Keio Sagamihara Line", "name_ja": "京王相模原線",
           "short": "Keio", "hue": "#DD0077"},
    "KO": {"n02": [("京王電鉄", "京王線")], "name": "Keio Line", "name_ja": "京王線",
           "short": "Keio", "hue": "#B030D0"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# tama` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its seed that reads 3:1 on both map pages
# and clears CIE76 45 from every pin (the Tama Line's blue at 45.1).
# Closest pair within 500 m 110.1 (Sagamihara / Tama Line), anywhere 31.3 (the
# two Keio lines, which never come within 500 m here); the dark-mode labels,
# 3 of 3.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "OT": line_registry.colour("odakyu-tama-line"), "KS": line_registry.colour("keio-sagamihara-line"),
    "KO": line_registry.colour("keio-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: Keio's and Odakyu's own station counts inside the city, as the brief
# gives them (2026-10-06: Keio 1 + 2, Odakyu 3), against the city line. No
# interchange collapse inflates a count here: the 38 m pairs stay apart.
GATE3 = {"source": "Keio's and Odakyu's station counts inside the city (the brief, 2026-10-06), against the "
                   "city line",
         "lines": {"OT": 3, "KS": 2, "KO": 1}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
TAMA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = TAMA_BBOX
