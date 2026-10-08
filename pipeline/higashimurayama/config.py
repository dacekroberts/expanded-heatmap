"""Higashimurayama-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/higashimurayama.md (15/15 checks, 2026-10-07). One of East-1's
Tama cities, Higashiyamato's twin on the same ledgers, on the shared modules
(pipeline/countries/japan*.py) and the Tama ledgers' shared leg
(pipeline/countries/tokyo_tama.py).

Business leg: the Tokyo Metropolitan Government's five Tama ledgers (food
permits, food notifications, barbers, beauty salons, laundries; as of
2026-08-31), cut to the city by address, plus MHLW's Tokyo filings the
ledgers lack (owner, call 169), one pin where a premises is in both. The
ledgers are partial by design and the page says so (call 109): the share it
states is at the yearbook's date (calls 187-189). Placed by a JOIN to MLIT's
位置参照情報 for the one municipality (13213, no wards); MHLW's own point
where the block join misses an MHLW row.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): Seibu's Shinjuku, Kokubunji, Seibuen, Tamako and Haijima lines
and JR East's Musashino Line, 8 stations. The Musashino, Kokubunji and Haijima
lines keep one station each, drawn as cut (one-station stubs of JR and a
private railway, the standing call). The Seibu Yamaguchi Line (Leo Liner) is
left out: its one station here, 多摩湖, is served by the Tamako Line (calls 54
and 92). English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import tokyo_tama

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "higashimurayama" / "raw"
DATA_PROCESSED = ROOT / "data" / "higashimurayama" / "processed"
OUTPUTS = ROOT / "outputs" / "higashimurayama"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Higashimurayama"
SLUG = "higashimurayama"
MUNICIPALITY = "東村山市"
PREFECTURE = "東京都"

# The ledgers and MHLW's file, shared by the Tama cities (tokyo_tama): the
# files copied unchanged from data/tokyo_tama/raw/ into data/higashimurayama/raw/
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
# page (outputs/higashimurayama/official_shares.json): restaurants against table
# 19-8, the registers against table 19-7, each also at the yearbook's date
OFFICIAL_SHARES = True
MUNICIPALITY_CODES = {MUNICIPALITY: "13213"}
SHARE_DATES = tokyo_tama.SHARE_DATES
REGISTER_SHARES = True


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """The city's rows of each Tama ledger and of MHLW's Tokyo file, cut by
    address (tokyo_tama.city_rows)."""
    from pipeline.countries.japan_step2 import need
    return tokyo_tama.city_rows(need(source_csv(key), SLUG), key, MUNICIPALITY)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 13213 alone:
# load_city_isj globs its directory, and data/tokyo_tama/raw/isj/ holds four
# municipalities' pairs (the brief).
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.735, W 139.440, N 35.782, E 139.505)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.73, 139.44, 35.79, 139.51)
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

# UTM zone 54N: the longitude (~139.47) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: step 1's
# median nearest-station gap is 810 m (8 stations, 2026-10-07; nearest pair
# 599 m, 西武園 to 多摩湖), over the 550 m that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 7 lines, 12 station records, 8 station groups). Seibu's
# Seibuen Line is wholly inside (2 of 2); the Tamako Line keeps 4 of 7 and the
# Shinjuku Line 2 of 29, cut at the city line (owner 2026-09-24). Three keep
# one station each and are drawn as cut, a JR or private one-station stub (the
# standing call, Kobe's JR Takarazuka Line): JR East's Musashino Line 1 of 27
# (新秋津), the Kokubunji Line 1 of 5 (東村山, its terminus) and the Haijima
# Line 1 of 8 (萩山, its junction), the last two at stations other lines
# also serve. 秋津 (the Seibu Ikebukuro Line) is 12 m outside the line in
# 清瀬市 (the brief), so that line has no station here and is not drawn.
LEFT_OUT_LINES = {
    # The Leo Liner (AGT, N02 class 16, an urban line) keeps 1 of its 3
    # stations, 多摩湖, in the same N02 group as the Tamako Line's 多摩湖, which
    # keeps the ring; the other two are in 所沢市 (owner, calls 54 and 92: an
    # urban line cut to one station is left out where another line serves it).
    ("西武鉄道", "山口線"): "an urban line with one station inside, 多摩湖, served by the Tamako Line "
                       "(owner, calls 54 and 92)",
}
# The Shinjuku and Musashino lines run on into Saitama (所沢市, 新座市): its N03
# names those excluded stations (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("11",)
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, in Tokyo's
# signage style; 西武園線 as Seibuen, the station's spelling (OSM name:en).
# The Shinjuku Line starts from Seibu's corporate blue (Nishitokyo's and
# Tokorozawa's), the Musashino Line from JR East's orange. The other four
# Seibu hues are seeds, not read from Seibu: each line a distinct hue of its
# own, so lines of one operator that meet separate (the owner, 2026-10-07:
# distinct colours; the earlier run started all five from one blue and landed
# them near-grey, closest pair 18.3).
LINES = {
    "SS": {"n02": [("西武鉄道", "新宿線")], "name": "Seibu Shinjuku Line", "name_ja": "西武新宿線",
           "short": "Seibu", "hue": "#00A0DE"},
    "SK": {"n02": [("西武鉄道", "国分寺線")], "name": "Seibu Kokubunji Line", "name_ja": "西武国分寺線",
           "short": "Seibu", "hue": "#C88800"},
    "SE": {"n02": [("西武鉄道", "西武園線")], "name": "Seibu Seibuen Line", "name_ja": "西武西武園線",
           "short": "Seibu", "hue": "#9040C0"},
    "ST": {"n02": [("西武鉄道", "多摩湖線")], "name": "Seibu Tamako Line", "name_ja": "西武多摩湖線",
           "short": "Seibu", "hue": "#A06030"},
    "SH": {"n02": [("西武鉄道", "拝島線")], "name": "Seibu Haijima Line", "name_ja": "西武拝島線",
           "short": "Seibu", "hue": "#805878"},
    "JM": {"n02": [("東日本旅客鉄道", "武蔵野線")], "name": "JR Musashino Line", "name_ja": "JR武蔵野線",
           "short": "JR", "hue": "#F15A22"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# higashimurayama` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its seed that reads 3:1 on both map pages
# and clears CIE76 45 from every pin (the Shinjuku Line's blue at 45.1, the
# Seibuen Line's purple at 45.5, the Haijima Line's mauve at 45.7). The
# Shinjuku and Musashino lines take Nishitokyo's and Tokorozawa's colours. The
# Haijima Line cannot take Higashiyamato's and Tachikawa's blue here, which is
# the Shinjuku Line's. Closest pair within 500 m and anywhere 33.2 (the
# Kokubunji and Tamako lines); the dark-mode labels, 6 of 6.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "SS": line_registry.colour("seibu-shinjuku-line"), "SK": "#C88800", "SE": "#9040C0", "ST": "#A06030",
    "SH": line_registry.colour("seibu-haijima-line"), "JM": line_registry.colour("jr-east-musashino-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: Seibu's and JR East's own stations inside the city (the brief, read
# 2026-10-06 from the operators' station and timetable pages against the city
# line: Seibu 7 stations, JR East 1). Each N02 group's records are 0 m apart
# (the brief), so no interchange collapse inflates a line's count here.
GATE3 = {"source": "Seibu's station pages (seibu.ekitan.com) and JR East's (timetables.jreast.co.jp), read "
                   "against the city line",
         "lines": {"SS": 2, "SK": 1, "SE": 2, "ST": 4, "SH": 1, "JM": 1}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
HIGASHIMURAYAMA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = HIGASHIMURAYAMA_BBOX
