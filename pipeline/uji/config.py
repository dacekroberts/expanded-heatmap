"""Uji-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/uji.md.
Japan A/B batch (Kansai-1, 2026-10-07), on the shared modules
(pipeline/countries/japan*.py) and the Japan foundation's rules (ALL_RULES).

Business leg: MHLW's 食品衛生申請等システム open data for KYOTO PREFECTURE
(26000: every permit and notification the prefecture has entered since
2021-06; opt-in, field by field), its own page (owner, 2026-10-06; not Kyoto
(Regional)), food only (Kurume's shape). The file names no municipality (its
市区町村名 is the prefectural seat on every row), so every row is assigned to
Uji BY ITS ADDRESS: one that begins 京都府宇治市. Placed by a JOIN to MLIT's
位置参照情報 for the one municipality (26204, no wards), through the
foundation's 字 rule (aza_insert) and spelling pairs (spelling5, 蔵 / 藏); where
the block join misses, MHLW's own point (OWN_POINT_FALLBACK). The prefecture's
barber, beauty and laundry PDFs are not used (its site terms forbid copying
without permission).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR West's Nara Line, Keihan's Uji Line and Kintetsu's Kyoto Line, cut at
the city line; the Kyoto Municipal Subway's Tōzai Line left out (its one
station in Uji, 六地蔵, shares its N02 group with JR's: calls 54 and 92).
English station names from OpenStreetMap's name:en.
"""

import unicodedata
from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "uji" / "raw"
DATA_PROCESSED = ROOT / "data" / "uji" / "processed"
OUTPUTS = ROOT / "outputs" / "uji"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Uji"
SLUG = "uji"
MUNICIPALITY = "宇治市"
PREFECTURE = "京都府"

# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2,
# termsofuse.htm; read 2026-09-24 for Fukuoka, re-read 2026-10-02). A plain
# GET. Credit links the top page only, as the site asks.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    "mhlw": ("26000_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=26000_food_business_all.csv",
             MHLW_TOP),
}
# MHLW's monthly file states no date: its newest 許可年月日 is 2026-08-31 and
# its closures run to 2026-08-31, and the page dates it by download
# (provenance.json).
SOURCE_AS_OF = {"mhlw": None}
FOOD_AS_OF = None
# The file carries each permit's 許可満了日 and 許可開始日: the term rules
# (calls 161 and 172) read them against the file's last day, never today.
TERM_AS_OF = {"mhlw": "2026-08-31"}
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: UTF-8 with a BOM.
SOURCE_ENCODING = {"mhlw": "utf-8-sig"}
# The columns the file must carry; fetch_sources.py and step 2 stop on a
# header without them. MHLW's 法人名 holds a sole trader's own name as well
# as a company's, so it is REQUIRED and read IN MEMORY by the name rule only,
# never kept (owner 2026-10-05). Never selected: 法人番号, 法人住所 and
# 営業施設電話番号.
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's). A
# row without one cannot be assigned to Uji at all (the file names no
# municipality), so the withheld share is measured prefecture-wide (the brief:
# 6,144 of 7,151 fixed open restaurants publish an address, 85.9%).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses, MHLW's own point places it (the brief's check:
# a median 51 m from the block point, 95.4% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# The prefecture's town beside Uji, a separate municipality whose name starts
# with the city's: never Uji's (the brief: 189 rows, every one 京都府綴喜郡宇治田原町).
NEIGHBOUR_PREFIX = "京都府綴喜郡宇治田原町"
OWN_PREFIX = PREFECTURE + MUNICIPALITY


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    the prefecture's file cut to the rows whose address begins 京都府宇治市
    (NFKC, spaces removed). A row that mentions 宇治市 and does not begin with
    it stops the build: a re-spelled address must not leak a row in or out
    (the brief: 0 such rows, 2026-10-06). 宇治 alone is not tested: 伊根町's
    字本庄宇治 (3 rows, 2026-10-07) is a village of another town."""
    from pipeline.countries import japan_register as jr

    if key != "mhlw":
        raise KeyError(key)
    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        a = unicodedata.normalize("NFKC", r.get("営業施設所在地") or "").replace(" ", "").replace("　", "")
        if a.startswith(OWN_PREFIX):
            yield r
        elif MUNICIPALITY in a and not a.startswith(NEIGHBOUR_PREFIX):
            raise SystemExit(f"{path.name}: an address names {MUNICIPALITY} after its start - assign it by hand")


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 26204.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Uji.
# S, W, N, E: the city's N03 extent (S 34.858, W 135.760, N 34.957, E 135.880)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.85, 135.75, 34.96, 135.89)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word.
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.82) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-group gap is 588 m, above the 550 m line for halved
# rings (docs/ring_rules.md); step 1 re-measures it.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25, the
# brief: 4 lines, no Shinkansen): JR West's 奈良線 (6 of 19), Keihan's 宇治線
# (4 of 8, to its terminus), Kintetsu's 京都線 (3 of 26), cut at the city line
# (owner 2026-09-24); and the Kyoto Municipal Subway's 東西線 (1 of 17).
LEFT_OUT_LINES = {
    ("京都市", "東西線"): "an urban line cut to one station, 六地蔵, which shares its N02 group with JR's 六地蔵 "
                       "and keeps its ring through the JR Nara Line (calls 54 and 92)",
}
COLLAPSE_MAX_SPREAD_M = 300
# 宇治 (JR, Keihan) and 木幡 (JR, Keihan) are two stations each, kept apart as
# N02 keeps them (trap 1); their English names take the operator. Keihan's
# 六地蔵 is in Kyoto's Fushimi Ward, outside the city.

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. The three lines Kyoto's map also draws
# start from Kyoto's colours (pipeline/kyoto/config.py), so the two maps agree
# where they meet.
_JR, _KH, _KT = "西日本旅客鉄道", "京阪電気鉄道", "近畿日本鉄道"
LINES = {
    "JD": {"n02": [(_JR, "奈良線")], "name": "JR Nara Line", "name_ja": "奈良線", "short": "JR", "hue": "#A87840"},
    "KU": {"n02": [(_KH, "宇治線")], "name": "Keihan Uji Line", "name_ja": "宇治線", "short": "Keihan",
           "hue": "#20A800"},
    "KT": {"n02": [(_KT, "京都線")], "name": "Kintetsu Kyoto Line", "name_ja": "近鉄京都線", "short": "Kintetsu",
           "hue": "#E80010"},
}
_COLOURS = {}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city; step 1 lists each line's
# in-city stations.
GATE3 = {"source": "no line wholly inside the city", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
UJI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = UJI_BBOX
