"""Tachikawa-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/tachikawa.md (20/20 checks, 2026-10-07). Built on the
shared modules (pipeline/countries/japan*.py) and the Tama ledgers' shared
leg (pipeline/countries/tokyo_tama.py), in Higashiyamato's shape.

Business leg: the Tokyo Metropolitan Government's five Tama ledgers (food
permits, food notifications, barbers, beauty salons, laundries; as of
2026-08-31), cut to the city by address, plus MHLW's Tokyo filings the
ledgers lack (owner, call 169), one pin where a premises is in both. The
ledgers are partial by design and the page says so (call 109): the share it
states is at the yearbook's date (calls 187-189). Placed by a JOIN to MLIT's
位置参照情報 for the one municipality (13202, no wards); MHLW's own point
where the block join misses an MHLW row.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): the Tama Toshi Monorail (7 of 19), the Seibu Haijima Line (3 of
8), JR East's Nambu Line (2 of 30), and its Chuo and Ome lines, each with
one station, 立川, drawn as cut (JR one-station stubs, the standing call).
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import tokyo_tama

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "tachikawa" / "raw"
DATA_PROCESSED = ROOT / "data" / "tachikawa" / "processed"
OUTPUTS = ROOT / "outputs" / "tachikawa"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Tachikawa"
SLUG = "tachikawa"
MUNICIPALITY = "立川市"
PREFECTURE = "東京都"

# The ledgers and MHLW's file, shared by the Tama cities (tokyo_tama): the
# files copied unchanged from data/tokyo_tama/raw/ into data/tachikawa/raw/
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
# page (outputs/tachikawa/official_shares.json): restaurants against table
# 19-8, the registers against table 19-7, each also at the yearbook's date
OFFICIAL_SHARES = True
MUNICIPALITY_CODES = {MUNICIPALITY: "13202"}
SHARE_DATES = tokyo_tama.SHARE_DATES
REGISTER_SHARES = True


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """The city's rows of each Tama ledger and of MHLW's Tokyo file, cut by
    address (tokyo_tama.city_rows)."""
    from pipeline.countries.japan_step2 import need
    return tokyo_tama.city_rows(need(source_csv(key), SLUG), key, MUNICIPALITY)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 13202 alone:
# load_city_isj globs its directory, so it holds 13202's pair and nothing
# else (the brief).
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.683, W 139.352, N 35.745, E 139.446)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.68, 139.35, 35.75, 139.45)
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

# UTM zone 54N: the longitude (~139.405) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: step 1's
# median nearest-station gap is 568 m (12 stations, 2026-10-07; the brief's
# 581 m; nearest pair 217 m, 立川北 to 立川, two names in two N02 groups), over
# the 550 m that halves them (Most's comment: over 550, the standard edges).
# Re-measure if a line is added.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 5 lines, 16 station records, 12 station groups, no Shinkansen).
# The Tama Toshi Monorail keeps 7 of 19 (砂川七番, 泉体育館, 立飛, 高松, 立川北,
# 立川南, 柴崎体育館), the Seibu Haijima Line 3 of 8 (玉川上水, 武蔵砂川, 西武立川)
# and JR East's Nambu Line 2 of 30 (立川, its terminus, and 西国立). JR East's
# Chuo Line (1 of 75) and Ome Line (1 of 26, its terminus) keep 立川 alone: JR
# one-station stubs, drawn as cut (the standing call; Kobe's JR Takarazuka
# Line), not urban lines, so the one-station rule (calls 54 and 92) leaves
# nothing out. Every line runs on to neighbors, cut at the line (owner
# 2026-09-24). N02 groups 立川's Chuo, Ome and Nambu platforms as one station
# (84 m). 立川北, 立川 and 立川南 (217 m and 231 m apart) stay three stations:
# three names in three N02 groups (the brief; Tama's precedent). Near the line,
# outside, no ring: the monorail's 玉川上水 platform (16 m, 東大和市; N02 groups
# it with Seibu's, 32 m inside) and 西立川 (Ome Line, 昭島市, 36 m).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, in Tokyo's
# signage style. N02 files JR East under legal lines; here each legal line is
# the public line of the same name (the brief), so no `route` is needed. The
# monorail and the Haijima Line start from Higashiyamato's hues, the Nambu
# Line from JR East's yellow (Fuchu's), and the Chuo Line from JR East's
# orange (Tokyo's Chuo Line (Rapid)). JR East gives the Ome Line the same
# orange, so its pink is a seed, not read from JR East (the owner,
# 2026-10-07: distinct colours; from one orange the two read 18.1 apart).
LINES = {
    "MONO": {"n02": [("多摩都市モノレール", "多摩都市モノレール線")], "name": "Tama Toshi Monorail",
             "name_ja": "多摩都市モノレール線", "short": "Tama Monorail", "hue": "#F08200"},
    "SH": {"n02": [("西武鉄道", "拝島線")], "name": "Seibu Haijima Line", "name_ja": "西武拝島線",
           "short": "Seibu", "hue": "#00A0DE"},
    "JN": {"n02": [("東日本旅客鉄道", "南武線")], "name": "JR Nambu Line", "name_ja": "JR南武線",
           "short": "JR", "hue": "#FFD400"},
    "JC": {"n02": [("東日本旅客鉄道", "中央線")], "name": "JR Chuo Line", "name_ja": "JR中央線",
           "short": "JR", "hue": "#F15A22"},
    "JO": {"n02": [("東日本旅客鉄道", "青梅線")], "name": "JR Ome Line", "name_ja": "JR青梅線",
           "short": "JR", "hue": "#E060D0"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# tachikawa` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its seed that reads 3:1 on both map pages
# and clears CIE76 45 from every pin (the Haijima Line's blue at 45.1, the Ome
# Line's pink at 45.8). The monorail, the Haijima Line and the Nambu Line keep
# Higashiyamato's and Fuchu's colours; the Chuo Line keeps Tokyo's Chuo Line
# (Rapid) orange, as Hino's. Closest pair within 500 m and anywhere 23.6 (the
# monorail and the Chuo Line); the Chuo and Ome lines, meeting at 立川, 94.1.
# The dark-mode labels, 5 of 5.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "MONO": line_registry.colour("tama-toshi-monorail"), "SH": line_registry.colour("seibu-haijima-line"),
    "JN": line_registry.colour("jr-east-nambu-line"), "JC": line_registry.colour("jr-east-chuo-line"),
    "JO": "#E060D0",
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own stations inside the city (the brief, read
# 2026-10-06 against the city line: JR East 立川 on three lines and 西国立,
# Seibu 3). Not the monorail: its own 玉川上水 platform is 16 m outside the
# line (東大和市), but N02's group code collapses it with Seibu's, 32 m inside,
# so step 1 counts that interchange on both lines (8 against the monorail's 7;
# Higashiyamato's mirror image).
GATE3 = {"source": "JR East's (timetables.jreast.co.jp) and Seibu's (seibu.ekitan.com) station counts inside the "
                   "city (the brief, 2026-10-06), against the city line",
         "lines": {"SH": 3, "JN": 2, "JC": 1, "JO": 1}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
TACHIKAWA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = TACHIKAWA_BBOX
