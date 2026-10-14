"""Incheon-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/incheon.md), Busan's config (the Korean rail pattern) and
the SEMAS register (owner, 2026-09-29).
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "incheon" / "raw"
DATA_PROCESSED = ROOT / "data" / "incheon" / "processed"
OUTPUTS = ROOT / "outputs" / "incheon"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- The register ----------------------------------------------------------
#
# SEMAS's 상가(상권)정보 (data.go.kr 15083033), the national storefront register,
# read through pipeline/countries/korea_sbiz.py from the country cache
# (data/korea/raw/). Chosen over the brief's route (owner, 2026-09-29): the
# national LOCALDATA API needs a data.go.kr key, and data.go.kr accounts need a
# Korean identity check (본인인증), closed to this project; Incheon's own permit
# lists place only 73% through KESA's lift-building join and its salons list
# carries lot-number addresses that no keyless file places. SEMAS carries a
# WGS84 point on every row and all three buckets.
SEMAS_SIDO = "인천광역시"
SEMAS_SIGUNGU = None          # the whole city, its ten 구/군

# --- Rail ------------------------------------------------------------------

OSM_BBOX = (37.35, 126.55, 37.62, 126.80)       # S, W, N, E
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 인천광역시, admin_level 4 (ISO KR-28), resolved by name 2026-09-29.
BOUNDARY_RELATION = 2297419
BOUNDARY_NAME = "인천광역시"
# Its polygon holds territorial sea around the Ongjin islands (Busan's shape):
# 9,906 km2 measured 2026-09-29 against about 1,067 of land.
BOUNDARY_AREA_KM2 = (9800, 10000)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~126.71) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Seoul's precedent (the brief's recommendation, applied 2026-09-29): the
# city's own lines and the metropolitan subway lines that serve it, with the
# Korail line Seoul signs as subway. NOT drawn: AREX (Seoul left it out on
# spacing), the airport maglev (suspended), the Wolmi Sea Train (a tourist
# ride), and lines that only touch the bbox. Stations inside Incheon only;
# lines drawn to their ends.
# key -> (OSM ref, colour, public name, label end). Operator colours.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
LINES = {
    "IC1": ("인천1", "#B4C7E7", "Incheon Line 1", None),
    "IC2": ("I2", "#F4A462", "Incheon Line 2", None),
    "L1": ("1", line_registry.colour("seoul-subway-line-1"), "Line 1", None),
    "L7": ("7", line_registry.colour("seoul-subway-line-7"), "Line 7", None),
    "SB": ("수인·분당", line_registry.colour("suin-bundang-line"), "Suin–Bundang Line", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train"}
# Gate 3: each WHOLE line's station count, termini to termini (inside Incheon
# and out). English Wikipedia's line infoboxes, read 2026-09-29 - a SECONDARY
# source, as Busan's and Daegu's. Line 1 (102 stations) is left out of the
# whole-line gate: the query brings only its service relations that touch
# Incheon (65 stations), and its southern branches (Cheonan, Sinchang,
# Seodongtan, Gwangmyeong) never do. Its 11 stations inside Incheon are the
# Gyeongin Line's Incheon section, Bugae to Incheon (Stockholm's precedent).
LINE_STATION_COUNTS = {"Incheon Line 1": 33, "Incheon Line 2": 27, "Line 7": 53,
                       "Suin–Bundang Line": 63}
NOT_DRAWN = {"공항철도": "AREX", "4": "Line 4", "9": "Line 9", "김포 골드라인": "Gimpo Goldline",
             "서해": "Seohae Line", "GTX-A": "GTX-A", "경의·중앙": "Gyeongui–Jungang Line",
             "WOLMI": "Wolmi Sea Train (a tourist ride)"}
# The Wolmi Sea Train's relation carries no ref; placed by its name, as NOT drawn.
NOT_DRAWN_BY_NAME = {"월미바다열차": "WOLMI"}
STOP_NAME_FIX = {}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

CITY_PREFIX = "인천광역시"
TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

INCHEON_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602297419)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ko",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "간석풍림오거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "금호아파트삼거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "장기주차장": "a monorail station (railway=station), named for the place beside it (the Prague precedent, Hotel Golf); tags read 2026-10-13",
}
# Dropped by id on the full read of 2026-10-13 under the owner's rulings of the
# same day, each id read with its cached name (docs/decisions_drafts/search-rollout.md).
PLACE_DROPPED = {
    # estate facility: dropped in the full read (owner, 2026-10-13)
    "way/1237533940": "'가든 라운지': garden of the Hillstate Prugio Juan apartment estate; the operator is the estate, the estate-operator rule did not see the brand (full read, estate facility)",
    "way/1237533946": "'아로마가든': same estate (full read, estate facility)",
    "way/1237533957": "'클러스터 가든': same estate (full read, estate facility)",
    "way/1237533958": "'수공원 & 석가산': same estate (full read, estate facility)",
    "way/1237533959": "'잔디공원': same estate; also a bare type (lawn park) (full read, estate facility)",
    "way/1245774448": "'바람의 숲': same estate (full read, estate facility)",
    "way/470497892": "'3단지 공원': \"complex 3 park\": named only by an estate block number; no operator tag to say whose it is (full read, estate facility)",
    "way/404080789": "'일단지공원': \"complex 1 park\": same pattern, 6 km from the other (full read, estate facility)",
    # business: dropped in the full read (owner, 2026-10-13)
    "way/1434217677": "'Songdo Shopping': a shopping label on a park outline, no park name (full read, business)",
    "way/1267597131": "'카페테리아': \"cafeteria\" on a park outline; one of five placeholder parks one mapper drew within 175 m (full read, business)",
    "node/4719769899": "'그랜드오스티엄 웨딩컨벤션(예식장)': a wedding hall tagged a place of worship (full read, business)",
    # description: dropped in the full read (owner, 2026-10-13)
    "way/1267597136": "'공개용지': \"open land\", a planning term; same cluster (full read, description)",
    "way/1267597132": "'도시개발1구역공원': \"urban development zone 1 park\", a plan label with no place name; same cluster (full read, description)",
    "node/8411370365": "'Room for Namaz (Islamic praying)': a description of a prayer room, no name (full read, description)",
    "way/472532236": "'야외 교실': \"outdoor classroom\" (full read, description)",
    "way/819667933": "'숲속 놀이터': \"playground in the woods\" (full read, description)",
    "way/471502098": "'소방차구역': \"fire engine zone\" on a park outline (full read, description)",
    # bare type: dropped in the full read (owner, 2026-10-13)
    "way/1267597128": "'어린이공원(1)': \"children's park (1)\", type and a count; same cluster (full read, bare type)",
    "way/1267597127": "'어린이놀이터(2)': \"playground (2)\"; same cluster (full read, bare type)",
    "node/4643605459": "'경로당': \"senior citizens' hall\", a type word, and not worship (full read, bare type)",
    "way/472472814": "'다목적광장': \"multi-purpose plaza\" (full read, bare type)",
    "way/471354737": "'론볼경기장': \"lawn bowls ground\" (full read, bare type)",
    "node/10101648940": "'보조경기장': \"auxiliary stadium\" (full read, bare type)",
    "way/471666489": "'풋살경기장': \"futsal ground\" (full read, bare type)",
    "way/642770118": "'축구장': \"football pitch\" (full read, bare type)",
    "way/1061040879": "'체육공원': \"sports park\" (full read, bare type)",
    "way/1187215469": "'체육공원': \"sports park\" (full read, bare type)",
    "way/1187215468": "'휴식공원': \"rest park\" (full read, bare type)",
    "way/472539543": "'생태공원': \"ecological park\" (full read, bare type)",
    "way/470847936": "'작은공원': \"small park\" (full read, bare type)",
    "way/474523666": "'보호수': \"protected tree\" (full read, bare type)",
    "way/819668046": "'커뮤니티 정원': \"community garden\" (full read, bare type)",
    "node/13036421366": "'성모상': \"statue of the Virgin\", a type word; in a church garden 18 m from 베드로 동산 (full read, bare type)",
    # worship by denomination: dropped in the full read (owner, 2026-10-13)
    "way/1558559670": "'기독교대한감리회': the Korean Methodist Church, the body's name alone (full read, worship by denomination)",
    "node/4866521610": "'순복음교회': \"Full Gospel church\", the denomination alone (full read, worship by denomination)",
    "node/2505137756": "'하나님의교회 (WMC)': World Mission Society Church of God, the body's name alone; its English alias in the index carries a web address and keywords (full read, worship by denomination)",
    # religious residence: dropped in the full read (owner, 2026-10-13)
    "way/1122660619": "'기독교 대한감리회 원로원': the Methodist Church's home for retired clergy (full read, religious residence)",
    # religious office: dropped in the full read (owner, 2026-10-13)
    "way/488854289": "'미륵대도 총무원': a sect's general affairs office (총무원) (full read, religious office)",
    "way/281486852": "'숭의사회종합복지관 · 숭의교회 비전선교관': a social welfare center and mission hall (full read, religious office)",
    "way/691965966": "'천성복지관': a church's welfare hall; 천성장로교회 beside it has its own row (full read, religious office)",
    # religious education hall: dropped in the full read (owner, 2026-10-13)
    "way/640064562": "'남촌교회비전센터': a church's \"vision center\" annex (full read, religious education hall)",
    "node/2857380319": "'숭의교회 선교센터': mission center of 숭의교회, whose main hall has its own row (full read, religious education hall)",
    "way/469409898": "'제물포 교회 선교관': mission hall 53 m from 제물포 교회, which has its own row (full read, religious education hall)",
    "way/691965965": "'천성선교원': a church's mission nursery, same compound (full read, religious education hall)",
    # duplicate: dropped in the full read (owner, 2026-10-13)
    "node/4637353478": "'제물표 교회 선교관': the same mission hall again at 0 m, name misspelt (full read, duplicate)",
}
# Kept by the owner's word (place_index, PLACE_KEPT; owner, 2026-10-13): a famous
# place the rules pass over for want of a tag, the id read with its cached name
# (docs/decisions_drafts/search-rollout.md). Not yet confirmed by a rebuild.
PLACE_KEPT = {
    "node/7403763386": "'월미도', Wolmido (place=island, a Wikidata entry and no Wikipedia tag): a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "node/5634901321": "'인천차이나타운', Incheon Chinatown (tourism=viewpoint node, no Wikidata or Wikipedia tag): a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
}
