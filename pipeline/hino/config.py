"""Hino-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/hino.md (19/19 checks, 2026-10-07). One of East-1's
Tama-ledger cities, on the same health centre as Tama (南多摩保健所), on the
shared modules (pipeline/countries/japan*.py) and the Tama ledgers' shared leg
(pipeline/countries/tokyo_tama.py).

Business leg: the Tokyo Metropolitan Government's five Tama ledgers (food
permits, food notifications, barbers, beauty salons, laundries; as of
2026-08-31), cut to the city by address, plus MHLW's Tokyo filings the
ledgers lack (owner, call 169), one pin where a premises is in both. The
ledgers are partial by design and the page says so (call 109): the share it
states is at the yearbook's date (calls 187-189). Placed by a JOIN to MLIT's
位置参照情報 for the one municipality (13212, no wards); MHLW's own point
where the block join misses an MHLW row.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): the Keio Line (4 of 35), the Tama Toshi Monorail (5 of 19) and
the JR Chuo Line (2 of 75), each cut at the city line, and the Keio Dobutsuen
Line (2 of 2), wholly inside and drawn whole. 高幡不動 (Keio Line, Dobutsuen Line, monorail) and
多摩動物公園 (Dobutsuen Line, monorail) are one station each, N02's own groups.
No line has a single station inside, so none is left out (calls 54 and 92).
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry
from pipeline.countries import tokyo_tama

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "hino" / "raw"
DATA_PROCESSED = ROOT / "data" / "hino" / "processed"
OUTPUTS = ROOT / "outputs" / "hino"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Hino"
SLUG = "hino"
MUNICIPALITY = "日野市"
PREFECTURE = "東京都"

# The ledgers and MHLW's file, shared by the Tama cities (tokyo_tama): the
# files copied unchanged (the same bytes) from data/tokyo_tama/raw/ into
# data/hino/raw/ (2026-10-06), since a Japanese build reads data/<slug>/raw/.
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
# page (outputs/hino/official_shares.json): restaurants against table
# 19-8, the registers against table 19-7, each also at the yearbook's date
OFFICIAL_SHARES = True
MUNICIPALITY_CODES = {MUNICIPALITY: "13212"}
SHARE_DATES = tokyo_tama.SHARE_DATES
REGISTER_SHARES = True


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """The city's rows of each Tama ledger and of MHLW's Tokyo file, cut by
    address (tokyo_tama.city_rows)."""
    from pipeline.countries.japan_step2 import need
    return tokyo_tama.city_rows(need(source_csv(key), SLUG), key, MUNICIPALITY)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 13212 alone,
# downloaded into data/hino/raw/isj/ for the brief (2026-10-06):
# load_city_isj globs its directory, and data/tokyo_tama/raw/isj/ holds four
# other municipalities' pairs (the brief).
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.639, W 139.357, N 35.692, E 139.442)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.63, 139.35, 35.70, 139.45)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
# OSM splits 多摩動物公園 between its operators' styles: the monorail's
# "Tama-Dobutsukoen" and Keio's "Tama-dobutsukoen" (osm_station_names.json of
# 2026-10-07). Settled in title case, as Tokyo settles its ties (JR's case:
# Shin-Okachimachi, Higashi-Nakano).
OSM_NAME_EN_TIES = {"多摩動物公園": "Tama-Dobutsukoen"}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~139.40) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: step 1's
# median nearest-station gap over the 10 stations is 1,146 m, minimum 790 m
# (2026-10-07; the brief read 1,176 m), far over the 550 m that halves them.
# Re-measure from step 1's gate 1 if the stations change.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 4 lines, no Shinkansen). The Keio Line keeps 4 of 35 (百草園,
# 高幡不動, 南平, 平山城址公園), the Tama Toshi Monorail 5 of 19 (甲州街道, 万願寺,
# 高幡不動, 程久保, 多摩動物公園) and the JR Chuo Line 2 of 75 (日野, 豊田), each
# cut at the city line (owner 2026-09-24); the Keio Dobutsuen Line lies wholly
# inside (2 of 2, 高幡不動 to 多摩動物公園) and is drawn whole. No line keeps a
# single station, so the one-station rule (calls 54 and 92) leaves none out.
# 高幡不動 is one N02 group across the Keio Line, the Dobutsuen Line and the
# monorail (222 m spread), 多摩動物公園 one across the Dobutsuen Line and the
# monorail (190 m): one station each (the brief, N02's own groups).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, in Tokyo's
# signage style. N02 files JR East's line here under its legal name 中央線, the
# one public service through the city (Tokyo's `route` split is not needed).
# Keio's two lines take seeds, not read from Keio (its station numbering
# colour is one magenta for both): the Keio Line a violet, one hue in Chofu,
# Fuchu, Hino and Tama, and the Dobutsuen Line a teal of its own (the owner,
# 2026-10-07: distinct colours; from one magenta the two read 19.4 apart).
LINES = {
    "KO": {"n02": [("京王電鉄", "京王線")], "name": "Keio Line", "name_ja": "京王線",
           "short": "Keio", "hue": "#B030D0"},
    "KD": {"n02": [("京王電鉄", "動物園線")], "name": "Keio Dobutsuen Line", "name_ja": "京王動物園線",
           "short": "Keio", "hue": "#287888"},
    "MONO": {"n02": [("多摩都市モノレール", "多摩都市モノレール線")], "name": "Tama Toshi Monorail",
             "name_ja": "多摩都市モノレール線", "short": "Tama Monorail", "hue": "#F08200"},
    "JC": {"n02": [("東日本旅客鉄道", "中央線")], "name": "JR Chuo Line", "name_ja": "JR中央線",
           "short": "JR", "hue": "#F15A22"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# hino` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its seed that reads 3:1 on both map pages
# and clears CIE76 45 from every pin (the Dobutsuen Line's teal at 48.1).
# Closest pair within 500 m and anywhere 23.6 (the monorail and the Chuo
# Line); the two Keio lines, which share 高幡不動, 98.2. The dark-mode labels,
# 4 of 4. The Keio Line is Chofu's, Fuchu's and Tama's #B030D0; the monorail
# is Higashiyamato's #E07800.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "KO": line_registry.colour("keio-line"), "KD": "#287888",
    "MONO": line_registry.colour("tama-toshi-monorail"), "JC": line_registry.colour("jr-east-chuo-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: Keio's, the monorail's and JR East's own station counts inside the
# city, as the brief gives them (2026-10-06: Keio 5 distinct stations, the
# Keio Line 4 and the Dobutsuen Line 2 with 高幡不動 on both; the monorail 5;
# JR 2), against the city line. Both collapsed interchanges lie wholly inside
# the city, so no platform outside raises a line's count.
GATE3 = {"source": "Keio's, the Tama Toshi Monorail's (tama-monorail.co.jp/monorail/station/) and JR East's "
                   "(timetables.jreast.co.jp) station counts inside the city (the brief, 2026-10-06), against "
                   "the city line",
         "lines": {"KO": 4, "KD": 2, "MONO": 5, "JC": 2}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
HINO_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = HINO_BBOX
