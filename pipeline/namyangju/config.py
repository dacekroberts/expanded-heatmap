"""Namyangju-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; copied from Bucheon's (the Korean
pattern: SEMAS's register, OSM rail on Busan's step 1). One of the Gyeonggi
satellites' second round (owner, 2026-09-29: Namyangju, Ansan and Uijeongbu,
one page each; docs/build_briefs/gyeonggi.md, "The next satellites").
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "namyangju" / "raw"
DATA_PROCESSED = ROOT / "data" / "namyangju" / "processed"
OUTPUTS = ROOT / "outputs" / "namyangju"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- The register ----------------------------------------------------------
#
# SEMAS's 상가(상권)정보 (data.go.kr 15083033), read through
# pipeline/countries/korea_sbiz.py from the country cache (owner, 2026-09-29,
# for Incheon and the Gyeonggi satellites): the national LOCALDATA API needs a
# Korean identity check, and the city's own files are not a register
# (docs/build_briefs/gyeonggi.md).
SEMAS_SIDO = "경기도"
SEMAS_SIGUNGU = ("남양주시",)   # 시군구명 prefix: the city has no 구 (the brief)

# --- Rail ------------------------------------------------------------------

# S, W, N, E: the city plus about 2 km (Namyangju spans about 37.55-37.79 N,
# 127.13-127.42 E; step 1 checks the boundary lies inside).
OSM_BBOX = (37.52, 127.10, 37.81, 127.45)
# The Korail lines the metropolitan subway signs (route=train), queried by ref
# beside every subway, light-rail and monorail relation in the box.
OSM_TRAIN_REFS = ('수인·분당', '경의·중앙', '경강', '서해', 'GTX-A', '경춘')
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 남양주시, admin_level 6 (the brief, 2026-09-29).
BOUNDARY_RELATION = 2409175
BOUNDARY_NAME = "남양주시"
# 457 km2 measured 2026-09-29 (the brief).
BOUNDARY_AREA_KM2 = (440, 475)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~127.2) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# Standard: the brief's median gap is 2,294 m (a sprawling city, 457 km2).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Seoul's precedent applied to a satellite (2026-09-29): every metropolitan
# subway, Korail metro and light-rail line with stations in the city is drawn,
# in the operators' colours (Seoul's drawn ones where Seoul draws the line);
# GTX-A (an express) and lines that never enter the city are not. Stations
# inside the city only; lines drawn to their ends.
# key -> (OSM ref, colour, public name, label end).
# Seoul's colours (pipeline/seoul/config.py): Line 4, the Gyeongui–Jungang and
# Gyeongchun lines; Line 8 as Seoul and Seongnam draw it (Seoul Metro's
# #D11D70 darkened, hue kept, clear of Food service's magenta).
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
LINES = {
    "L4": ("4", line_registry.colour("seoul-subway-line-4"), "Line 4", None),
    "L8": ("8", line_registry.colour("seoul-subway-line-8"), "Line 8", None),
    "GJ": ("경의·중앙", line_registry.colour("gyeongui-jungang-line"), "Gyeongui–Jungang Line", None),
    "GC": ("경춘", line_registry.colour("gyeongchun-line"), "Gyeongchun Line", None),
}
OSM_COLOUR = {"L8": "#D11D70"}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train"}
# Gate 3: each WHOLE line's station count, English Wikipedia's line infoboxes
# (a SECONDARY source, as Busan's). None of the four lines can take it here,
# each for a reason an earlier city recorded:
#   * Line 4: the query brings only its service relations that touch the box
#     (29 stations, of 51), as Line 1 in Incheon and Suwon;
#   * Line 8: OSM carries 24 stations, the infobox 25 (Seongnam's note);
#   * the Gyeongui–Jungang Line: OSM 55, the infobox 57 (Goyang's note);
#   * the Gyeongchun Line: OSM's relations carry 25 with the Cheongnyangni and
#     Kwangwoon University branches, the infobox 20, its own table 21
#     Sangbong-Chuncheon (read 2026-09-30).
# In their place, the IN-CITY stations of each line read against the line
# tables (English Wikipedia, 2026-09-30): Gyeongchun Byeollae, Toegyewon,
# Sareung, Geumgok, Pyeongnaehopyeong, Cheonmasan and Maseok (7);
# Gyeongui–Jungang Donong, Yangjeong, Deokso, Dosim, Paldang and Ungilsan (6);
# Line 4's Jinjeop extension Byeollae Byeolgaram, Onam and Jinjeop (3); Line 8's
# Byeollae extension Dasan and Byeollae (2). Step 1's 17 agree, line by line.
LINE_STATION_COUNTS = {}
NOT_DRAWN = {"GTX-A": "GTX-A", "2": "Line 2", "5": "Line 5", "6": "Line 6", "9": "Line 9"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
# OSM's English name, where the operator signs it otherwise (Suwon's
# precedent: a compound run together, hyphenated or spaced as signed).
OSM_NAME_EN_OVERRIDES = {
    "별내별가람": "Byeollae Byeolgaram",     # OSM name:en "Byeollaebyeolgaram"
    "평내호평": "Pyeongnae-Hopyeong",        # OSM name:en "PyeongnaeHopyeong"
}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

CITY_PREFIX = "경기도 남양주시"
TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602409175)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ko",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "삼신아파트앞": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "영남아파트입구교차로": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "창현아파트단지입구": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "효성아파트앞": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read of this
# index (rule passes 5 and 6), each id read with its cached name and its index
# row; grouped by the reader's class.
PLACE_DROPPED = {
    # A station row that is no working passenger station (reader's drop; owner, 2026-10-13)
    "node/5842009774": "'팔당역(폐역)'",
    # A code or a number beside a type word, or a number alone (reader's drop; owner, 2026-10-13)
    "node/14212399191": "'10통'",
    "node/14212360663": "'11통'",
    "node/14212390994": "'12통'",
    "node/14212399199": "'13통'",
    "node/14212399194": "'14통'",
    "node/14212391000": "'15통'",
    "node/14212399205": "'16통'",
    "node/14212399140": "'17통'",
    "node/14212399178": "'18통'",
    "node/14212390959": "'19통'",
    "node/14212399145": "'1통'",
    "node/14212399104": "'20통'",
    "node/14212360546": "'21통'",
    "node/14212399134": "'22통'",
    "node/14212390992": "'23통'",
    "node/14212399117": "'24통'",
    "node/14212399115": "'2통'",
    "node/14212390980": "'3통'",
    "node/14212399143": "'4통'",
    "node/14212399180": "'50통'",
    "node/14212399174": "'5통'",
    "node/14212334998": "'61통'",
    "node/14212360810": "'62통'",
    "node/14212390965": "'6통'",
    "node/14212399154": "'7통'",
    "node/14212390985": "'8통'",
    "node/14212390966": "'9통'",
    # A description standing in for a name (reader's drop; owner, 2026-10-13)
    "way/1068265437": "'다리 아래 쉼터'",
    "way/789146064": "'땅밑집터 전시장'",
    # A bare type word standing alone (reader's drop; owner, 2026-10-13)
    "way/914511549": "'분수시계탑'",
    "way/864119585": "'휴식공간'",
    "node/10096927305": "'진입광장'",
    "way/864684163": "'재실'",
    "way/480153337": "'정자각'",
    "node/11469141008": "'돌덧널 무덤'",
    "node/11469141010": "'돌방 무덤'",
    "node/10253004756": "'산성'",
    # A business's or a mall's own facility (reader's drop; owner, 2026-10-13)
    "node/8141896916": "'당구클럽'",
    "node/8141908527": "'독수리 당구클럽'",
    # Worship named only by a body, a denomination or a chain (reader's drop; owner, 2026-10-13)
    "way/617951712": "'SDA교회'",
    "node/4639636397": "'순복음교회'",
    # A second row for one object (the surviving row named in each note) (reader's drop; owner, 2026-10-13)
    "node/4656376558": "'보린교회 입구': \"entrance of Borin church\", a node 40 m from the church's own row",
    # A religious office, hall or residence tagged a place of worship (reader's drop; owner, 2026-10-13)
    "way/1219038711": "'장현교회 공감과공간(청소년부)'",
    "node/9711322650": "'목양수양관'",
    # Twin round 1 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "node/11469141009": "'돌덧널 무덤': the twin of node/11469141008; A bare type word standing alone (reader's drop; owner, 2026-10-13)",
    "node/11469141011": "'돌방 무덤': the twin of node/11469141010; A bare type word standing alone (reader's drop; owner, 2026-10-13)",
    "way/789146066": "'땅밑집터 전시장': the twin of way/789146064; A description standing in for a name (reader's drop; owner, 2026-10-13)",
    # Twin round 2 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/789146067": "'땅밑집터 전시장': the twin of way/789146064; A description standing in for a name (reader's drop; owner, 2026-10-13)",
}
