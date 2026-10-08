"""Okayama-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/okayama.md
(5/5 checks, 2026-10-02). A city of the 2026-10-01 Japanese batch, on the
shared modules (pipeline/countries/japan*.py): food only, Hiroshima's page
shape, from ONE source.

Business leg: MHLW's 食品衛生申請等システム open data for Okayama City alone
(every permit and notification the city entered since 2021-06; opt-in, field
by field). The city's own food lists stop at 2021-05 and point to MHLW; its
barber, beauty and laundry lists are PDFs under the site's all-rights-reserved
default, so there are no personal services (Band B, food only). No source
names an individual operator, so the name rule cannot run anywhere (owner,
2026-10-02, "approve all recommendations"). Placed by a JOIN to MLIT's
位置参照情報 for the 4 wards; where the block join misses, MHLW's own point
(OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), the Shinkansen left out, stations kept
only inside the city line (N03). Okaden's two tram lines and JR West's six.
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "okayama" / "raw"
DATA_PROCESSED = ROOT / "data" / "okayama" / "processed"
OUTPUTS = ROOT / "outputs" / "okayama"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Okayama"
SLUG = "okayama"
MUNICIPALITY = "岡山市"
PREFECTURE = "岡山県"

# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2,
# termsofuse.htm; read 2026-09-24 for Fukuoka, re-read 2026-10-02). A plain
# GET. Credit links the top page only, as the site asks.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    "mhlw": ("33100_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=33100_food_business_all.csv",
             MHLW_TOP),
}
# MHLW's monthly file states no date: its newest 許可年月日 is 2026-08-28, and
# the page dates it by download (provenance.json).
SOURCE_AS_OF = {"mhlw": None}
FOOD_AS_OF = None
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: UTF-8 with a BOM.
SOURCE_ENCODING = {"mhlw": "utf-8-sig"}
# The columns the file must carry; fetch_sources.py and step 2 stop on a
# header without them. MHLW's 法人名 holds a sole trader's own name as
# well as a company's, so it is REQUIRED and read IN MEMORY by the name rule only,
# never kept (owner 2026-10-05, reversing the whole-city call of 2026-10-02). Never selected: 法人番号, 法人住所 and
# 営業施設電話番号.
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's): a
# row without one is counted apart for the page's disclosure.
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses, MHLW's own point places it (the brief's check:
# a median 39 m from the block point, 97.7% within 250 m; block or own 100%).
OWN_POINT_FALLBACK = {"mhlw"}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and Okaden's tram stops
# (railway=tram_stop, which the station query does not take). Which stations
# exist is N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (S 34.519, W 133.740, N 34.949, E 134.123)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.5, 133.72, 34.96, 134.14)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-10-02): N02 carries the two Okaden stops' current
# long names (a naming-rights suffix and a museum), OSM the short ones.
OSM_NAME_ALIASES = {"西大寺町・岡山芸術創造劇場ハレノワ前": "西大寺町", "東山・おかでんミュージアム": "東山"}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen, Hepburn throughout (OSM writes some Okaden stops
# in Kunrei, Tamati and -suzi). The two long Okaden names keep their short
# form first and the suffix riders see in brackets.
OSM_NAME_EN_OVERRIDES = {
    "西大寺町・岡山芸術創造劇場ハレノワ前": "Saidaijicho (Harenowa)",  # Saidaijicho
    "東山・おかでんミュージアム": "Higashiyama (Okaden Museum)",       # Higashiyama
    "新西大寺町筋": "Shin-Saidaijicho-suji",          # Shinsaidaizichosuzi
    "田町": "Tamachi",                                # Tamati
    "県庁通り": "Kenchodori",                         # Kenchoudori
    "西川緑道公園": "Nishigawa-ryokudo-koen",         # Nishigawaryokudokouen
    "大雲寺前": "Daiunji-mae",                        # Daiunjimae
    "郵便局前": "Yubinkyoku-mae",                     # Yubinkyokumae
    "岡山駅前": "Okayama-ekimae",                     # Okayama Ekimae
    "上道": "Joto",                                   # Jyoto
    "大多羅": "Odara",                                # Ōdara
    "法界院": "Hokaiin",                              # Hōkaiin
    "大元": "Omoto",                                  # Ōmoto
    "妹尾": "Seno",                                   # Senō
    "備中箕島": "Bitchu-Mishima",                     # Bitchū-Mishima
    "備中高松": "Bitchu-Takamatsu",                   # Bitchū-Takamatsu
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~133.92) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 8 lines, no Shinkansen; 岡山 stays as a JR station). Okaden's two
# lines lie wholly inside (10 of 10, 7 of 7). JR West's Sanyo (9 of 131), Ako
# (3 of 19), Kibi (7 of 10), Tsuyama (9 of 17) and Uno (8 of 15) lines are cut
# at the city line (owner 2026-09-24). 本四備讃線 keeps one station (植松, of
# 5): a one-station stub stays as cut (Kobe's JR Takarazuka Line, owner
# 2026-09-27).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Okaden signs its two lines by name
# (東山線, 清輝橋線), so each is drawn under it, as Hiroden's are. JR West signs
# 吉備線 as the Momotaro Line (桃太郎線), 宇野線 as the Uno Minato Line
# (宇野みなと線) and 本四備讃線 as the Seto-Ohashi Line (瀬戸大橋線): the names
# riders read, Fukuoka's precedent (篠栗線 as 福北ゆたか線). Line names
# without macrons, as JR West's signs.
_OK, _JR = "岡山電気軌道", "西日本旅客鉄道"
LINES = {
    "OH": {"n02": [(_OK, "東山本線")], "name": "Okaden Higashiyama Line", "name_ja": "東山線", "short": "Okaden",
           "hue": "#E60012"},
    "OS": {"n02": [(_OK, "清輝橋線")], "name": "Okaden Seikibashi Line", "name_ja": "清輝橋線", "short": "Okaden",
           "hue": "#E60012"},
    "JS": {"n02": [(_JR, "山陽線")], "name": "JR Sanyo Line", "name_ja": "山陽本線", "short": "JR", "hue": "#0068B7"},
    "JA": {"n02": [(_JR, "赤穂線")], "name": "JR Ako Line", "name_ja": "赤穂線", "short": "JR", "hue": "#E4007F"},
    "JK": {"n02": [(_JR, "吉備線")], "name": "JR Momotaro Line", "name_ja": "桃太郎線", "short": "JR",
           "hue": "#E83820"},
    "JT": {"n02": [(_JR, "津山線")], "name": "JR Tsuyama Line", "name_ja": "津山線", "short": "JR", "hue": "#F39800"},
    "JU": {"n02": [(_JR, "宇野線")], "name": "JR Uno Minato Line", "name_ja": "宇野みなと線", "short": "JR",
           "hue": "#00A0E9"},
    "JB": {"n02": [(_JR, "本四備讃線")], "name": "JR Seto-Ohashi Line", "name_ja": "瀬戸大橋線", "short": "JR",
           "hue": "#00A7A7"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# okayama` (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Okaden's two lines share one red
# and spread to red and vermilion; JR West's blues, which none clears Retail's
# pin in, go teal and slate. Closest pair within 500 m 18.1 (the two Okaden
# lines, which meet at 柳川), anywhere 14.4 (Seikibashi / Momotaro, which never
# meet); the dark-mode labels separate, 8 of 8.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "OH": "#E80010", "OS": "#F05030", "JS": line_registry.colour("jr-west-sanyo-line"), "JA": "#F000B8",
    "JK": "#C02808", "JT": "#D08000", "JU": "#7098A8", "JB": "#00A0B8",
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: Okaden's own timetables (okayama-kido.co.jp/tram/route-map/, the
# weekday PDFs of 2025-12-01, read 2026-10-02) head a column per stop: the
# Higashiyama route 10 (岡山駅前 to 東山), the Seikibashi route 9, of which the
# 7 from 柳川 to 清輝橋 are its own line (the first two share the Higashiyama
# Line's track, as N02 files it). Every JR line is cut by the city line and
# has no in-city count of its own.
GATE3 = {"source": "Okaden's route timetables (okayama-kido.co.jp/tram/route-map/, 2025-12-01)",
         "lines": {"OH": 10, "OS": 7}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
OKAYAMA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = OKAYAMA_BBOX
