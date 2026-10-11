"""Fuchū (Tokyo)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/fuchu_tokyo.md (20/20 checks, 2026-10-07). One of East-1's
Tama-ledger cities, Higashiyamato's twin on the same ledgers, on the shared
modules (pipeline/countries/japan*.py) and the Tama ledgers' shared leg
(pipeline/countries/tokyo_tama.py). Not Hiroshima's 府中市 (34208): the
japan.CITIES entry's prefecture, 13, keeps them apart.

Business leg: the Tokyo Metropolitan Government's five Tama ledgers (food
permits, food notifications, barbers, beauty salons, laundries; as of
2026-08-31), cut to the city by address, plus MHLW's Tokyo filings the
ledgers lack (owner, call 169), one pin where a premises is in both. The
ledgers are partial by design and the page says so (call 109): the share it
states is at the yearbook's date (calls 187-189). Placed by a JOIN to MLIT's
位置参照情報 for the one municipality (13206, no wards); MHLW's own point
where the block join misses an MHLW row.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): the Keio Line (6 of 35) and the Keio Keibajo Line (2 of 2, the
whole branch), JR East's Nambu Line (3 of 30) and Musashino Line (2 of 27,
from its terminus, 府中本町), and the Seibu Tamagawa Line (4 of 6, to its
terminus, 是政), cut at the city line: 17 station records in 14 N02 station
groups. No line has one station inside, so none is left out. English station
names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import tokyo_tama

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "fuchu_tokyo" / "raw"
DATA_PROCESSED = ROOT / "data" / "fuchu_tokyo" / "processed"
OUTPUTS = ROOT / "outputs" / "fuchu_tokyo"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Fuchū (Tokyo)"
SLUG = "fuchu_tokyo"
MUNICIPALITY = "府中市"
PREFECTURE = "東京都"

# The ledgers and MHLW's file, shared by the Tama cities (tokyo_tama): the
# files copied unchanged from data/tokyo_tama/raw/ into data/fuchu_tokyo/raw/
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
# page (outputs/fuchu_tokyo/official_shares.json): restaurants against table
# 19-8, the registers against table 19-7, each also at the yearbook's date
OFFICIAL_SHARES = True
MUNICIPALITY_CODES = {MUNICIPALITY: "13206"}
SHARE_DATES = tokyo_tama.SHARE_DATES
REGISTER_SHARES = True


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """The city's rows of each Tama ledger and of MHLW's Tokyo file, cut by
    address (tokyo_tama.city_rows)."""
    from pipeline.countries.japan_step2 import need
    return tokyo_tama.city_rows(need(source_csv(key), SLUG), key, MUNICIPALITY)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 13206 alone:
# load_city_isj globs its directory, and data/tokyo_tama/raw/isj/ holds four
# municipalities' pairs (the brief).
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.646, W 139.4298, N 35.700, E 139.526)
# as the brief rounded it, the box the station names were fetched with
# (2026-10-07). Its west edge, 139.43, misses the city's western tip by about
# 15 m, where no station stands (the westernmost, 中河原 and 西府, are near
# 139.457), so the names need no new query; CITY_BBOX below widens that edge
# instead, since step 1 stops if the city leaves it.
OSM_BBOX = (35.64, 139.43, 35.71, 139.53)
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

# UTM zone 54N: the longitude (~139.48) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: step 1's
# median nearest-station gap is 784 m (14 stations, 2026-10-07; nearest pair
# 290 m, 白糸台 to 武蔵野台, two names in two N02 groups), over the 550 m that
# halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 5 lines, 17 station records, 14 station groups, no Shinkansen).
# The Keio Line keeps 6 of 35 (中河原, 分倍河原, 府中, 東府中, 多磨霊園, 武蔵野台),
# JR East's Nambu Line 3 of 30 (西府, 分倍河原, 府中本町), its Musashino Line 2 of
# 27 (府中本町, its terminus, and 北府中) and the Seibu Tamagawa Line 4 of 6
# (多磨, 白糸台, 競艇場前, 是政, its terminus): main lines cut at the city line
# (owner 2026-09-24). The Keio Keibajo Line, 東府中 to 府中競馬正門前, lies
# wholly inside (2 of 2). N02 groups 分倍河原 (Keio and JR, 61 m), 府中本町
# (Nambu and Musashino, 17 m) and 東府中 (the two Keio lines) as one station
# each. No line keeps one station, so the one-station rule (calls 54 and 92)
# leaves nothing out. Near the line, outside: 西国分寺 (JR Chuo and Musashino
# lines, 国分寺市, about 250 m) and 南多摩 (JR Nambu Line, 稲城市, 258 m), no
# ring (the brief). N02's JR Chuo Line crosses about 260 m of the city with no
# station inside, so it is not drawn.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
# The Nambu Line runs on into Kanagawa (Kawasaki's 多摩区, 稲田堤 within 3 km):
# Kanagawa's N03 names that excluded station, which Tokyo's alone names only
# "another prefecture" (japan_step1.n03_municipalities). The Musashino Line's
# Saitama stations lie beyond the 3 km that excluded_stations.csv covers.
N03_NEIGHBOR_PREFS = ("14",)

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, in Tokyo's
# signage style. Keio's two lines take seeds, not read from Keio (its station
# numbering colour is one magenta for both): the Keio Line a violet, one hue
# in Chofu, Fuchu, Hino and Tama, and the Keibajo Line a brown of its own (the
# owner, 2026-10-07: distinct colours; from one magenta the two read 19.4
# apart). The Nambu Line starts from JR East's yellow (Kawasaki's), the
# Musashino Line from its orange (Higashimurayama's) and the Tamagawa Line
# from Seibu's blue (Higashimurayama's and Nishitokyo's Shinjuku Line).
LINES = {
    "KO": {"n02": [("京王電鉄", "京王線")], "name": "Keio Line", "name_ja": "京王線",
           "short": "Keio", "hue": "#B030D0"},
    "KK": {"n02": [("京王電鉄", "競馬場線")], "name": "Keio Keibajo Line", "name_ja": "京王競馬場線",
           "short": "Keio", "hue": "#806040"},
    "JN": {"n02": [("東日本旅客鉄道", "南武線")], "name": "JR Nambu Line", "name_ja": "JR南武線",
           "short": "JR", "hue": "#FFD400"},
    "JM": {"n02": [("東日本旅客鉄道", "武蔵野線")], "name": "JR Musashino Line", "name_ja": "JR武蔵野線",
           "short": "JR", "hue": "#F15A22"},
    "SW": {"n02": [("西武鉄道", "多摩川線")], "name": "Seibu Tamagawa Line", "name_ja": "西武多摩川線",
           "short": "Seibu", "hue": "#00A0DE"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# fuchu_tokyo` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its seed that reads 3:1 on both map pages
# and clears CIE76 45 from every pin (the Tamagawa Line's blue at 45.1).
# Closest pair within 500 m 56.0 (the Nambu and Musashino lines at 府中本町),
# anywhere 46.3 (the Keibajo and Nambu lines); the two Keio lines, meeting at
# 東府中, 101.3. The dark-mode labels, 5 of 5.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "KO": line_registry.colour("keio-line"), "KK": "#806040",
    "JN": line_registry.colour("jr-east-nambu-line"), "JM": line_registry.colour("jr-east-musashino-line"),
    "SW": "#08A0C0",
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own stations inside the city (the brief, read
# 2026-10-06 against the city line: Keio 8 records in 7 groups, JR East 5 in
# 4, Seibu 4). Every record of the three collapsed groups lies inside the
# line, so no interchange collapse inflates a line's count here.
GATE3 = {"source": "Keio's, JR East's (timetables.jreast.co.jp) and Seibu's (seibu.ekitan.com) station counts "
                   "inside the city (the brief, 2026-10-06), against the city line",
         "lines": {"KO": 6, "KK": 2, "JN": 3, "JM": 2, "SW": 4}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
# The west edge is 139.42, not OSM_BBOX's 139.43, which the city's western tip
# (139.4298) crosses (above).
FUCHU_TOKYO_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": 139.42,
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = FUCHU_TOKYO_BBOX
