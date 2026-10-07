"""Tokorozawa-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/tokorozawa.md (17/17 checks, 2026-10-07). Tokorozawa City
(所沢市, 11208), one municipality with no wards. The second of the four
Saitama pages on the shared Saitama leg (pipeline/countries/saitama_pref.py),
after Ageo (Regional).

Business leg: Saitama Prefecture's own lists for its health centres' areas,
cut to the city by address. Food: the live new-law layer, and the old-law
permits as the R8.3.31 old-law list with the live old-law layer (owner, call
171: in term, de-duplicated, renewals dropped, an upper bound as of
2026-03-31, disclosed; call 172: rows starting after the as-of dropped).
Personal services: the 狭山保健所 area's FY-end 生活衛生 list (2026-03-31) plus
the months to 2026-08. No food-share sentence (call 173): the publisher's
withholding note is disclosed with no number. No MHLW source (a control
only, calls 126-127). Placed by a JOIN to MLIT's 位置参照情報 for the one
municipality; the layers' own point where the block join misses (call 127c).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city
line (N03): Seibu's Ikebukuro (4 of 31), Shinjuku (3 of 29) and Sayama (3 of
3) lines, the Seibu Yamaguchi Line (Leo Liner, 2 of 3, drawn cut at the line,
owner's band-row call) and JR East's Musashino Line (1 of 27, 東所沢, a JR
one-station stub kept as cut). English station names from OpenStreetMap's
name:en.
"""

from pathlib import Path

from pipeline.countries import saitama_pref

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "tokorozawa" / "raw"
DATA_PROCESSED = ROOT / "data" / "tokorozawa" / "processed"
OUTPUTS = ROOT / "outputs" / "tokorozawa"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Tokorozawa"
SLUG = "tokorozawa"
MUNICIPALITY = "所沢市"
PREFECTURE = saitama_pref.PREFECTURE
# Tokorozawa is in the 狭山保健所 area (所沢市, 入間市, 狭山市, 飯能市, 日高市):
# its workbook in r7nenndo.zip, 08狭山保健所管内.xlsx
HEALTH_CENTRE = "08狭山"

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
    (saitama_pref.city_rows) at 所沢市, as MLIT's 市区町村名 and the lists'
    addresses write it; the step stops naming fetch_sources.py where a file is
    missing."""
    from pipeline.countries.japan_step2 import need
    for k in SOURCE_FILES:
        need(source_csv(k), SLUG)
    return saitama_pref.city_rows(key, (MUNICIPALITY,), HEALTH_CENTRE)


def file_rows(key):
    """One file's rows as it stands, for fetch_sources.py's count and column check."""
    return saitama_pref.file_rows(key)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 11208 alone
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram here.
# S, W, N, E: the city's N03 extent (S 35.763, W 139.379, N 35.844, E 139.546)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.76, 139.37, 35.85, 139.55)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons).
OSM_NAME_EN_OVERRIDES = {
    # the one stray macron of the 10 names, to the signs' spelling
    "西武園ゆうえんち": "Seibuen-yuenchi",  # Seibuen-yūenchi
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~139.46) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: step 1's
# median nearest-station gap is 1,411 m (10 stations, 2026-10-07; nearest pair
# 1,125 m; the brief read 1,465 m), over the 550 m that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 5 lines, 13 station records, 10 station groups). The Seibu
# Ikebukuro Line keeps 4 of 31 and the Shinjuku Line 3 of 29, main lines cut
# at the city line (owner 2026-09-24); the Sayama Line lies wholly inside (3
# of 3). The Seibu Yamaguchi Line (Leo Liner, AGT, N02 class 16) keeps 2 of
# 3 (西武球場前, 西武園ゆうえんち), so it is not a one-station line: drawn and
# cut at the line (owner, band row), 多摩湖 beyond in 東村山市 (N03; the
# brief wrote 東大和市). JR East's
# Musashino Line keeps 1 of 27 (東所沢), a JR one-station stub kept as cut
# (the standing call, Kobe's JR Takarazuka Line). No Shinkansen.
LEFT_OUT_LINES = {}
# The Seibu lines and the Leo Liner run on into Tokyo, the Musashino Line too:
# Tokyo's N03 names those excluded stations (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("13",)
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, in Tokyo's
# signage style. The hues are seeds, not read from Seibu: the Shinjuku Line
# from Seibu's corporate blue and the Ikebukuro Line from Nishitokyo's seed
# (the same two colours as Nishitokyo's page where the search allows), the
# Sayama and Yamaguchi lines each a hue of its own, so lines that meet
# separate (the drafts' parked colour call 1, set B's approach). JR East's
# orange for the Musashino Line.
LINES = {
    "SI": {"n02": [("西武鉄道", "池袋線")], "name": "Seibu Ikebukuro Line", "name_ja": "西武池袋線",
           "short": "Seibu", "hue": "#F5A200"},
    "SS": {"n02": [("西武鉄道", "新宿線")], "name": "Seibu Shinjuku Line", "name_ja": "西武新宿線",
           "short": "Seibu", "hue": "#00A0DE"},
    "SA": {"n02": [("西武鉄道", "狭山線")], "name": "Seibu Sayama Line", "name_ja": "西武狭山線",
           "short": "Seibu", "hue": "#9040C0"},
    "SY": {"n02": [("西武鉄道", "山口線")], "name": "Seibu Yamaguchi Line (Leo Liner)",
           "name_ja": "西武山口線（レオライナー）", "short": "Seibu", "hue": "#A06030"},
    "JM": {"n02": [("東日本旅客鉄道", "武蔵野線")], "name": "JR Musashino Line", "name_ja": "JR武蔵野線",
           "short": "JR", "hue": "#F15A22"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# tokorozawa` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its seed that reads 3:1 on both map pages
# and clears CIE76 45 from every pin (the Shinjuku Line's blue at 45.1, the
# Sayama Line's purple at 45.5). The Ikebukuro and Shinjuku lines take
# Nishitokyo's two colours. Closest pair within 500 m 33.6 (the Musashino and
# Ikebukuro lines, at 新秋津 and 秋津 beyond the city line), anywhere 32.3 (the
# Ikebukuro and Yamaguchi lines); the dark-mode labels, 5 of 5.
_COLOURS = {"SI": "#D08000", "SS": "#08A0C0", "SA": "#9040C0", "SY": "#A06030", "JM": "#F05820"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: Seibu's and JR East's own stations inside the city (the brief, read
# 2026-10-06 from the operators' station and timetable pages against the city
# line). The interchanges count on each line, as the operators count them:
# 所沢 (Ikebukuro, Shinjuku), 西所沢 (Ikebukuro, Sayama), 西武球場前 (Sayama,
# Yamaguchi).
GATE3 = {"source": "Seibu's station pages (seibu.ekitan.com) and JR East's (timetables.jreast.co.jp), read "
                   "against the city line",
         "lines": {"SI": 4, "SS": 3, "SA": 3, "SY": 2, "JM": 1}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
TOKOROZAWA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = TOKOROZAWA_BBOX
