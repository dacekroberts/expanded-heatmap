"""Suwon-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; generated from Incheon's config (the
Korean pattern: SEMAS's register, OSM rail on Busan's step 1). One of the
Gyeonggi satellites (owner, 2026-09-28: Goyang, Seongnam and Yongin first,
then Suwon and Bucheon; one page each, 2026-09-29). Copied from Yongin's.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "suwon" / "raw"
DATA_PROCESSED = ROOT / "data" / "suwon" / "processed"
OUTPUTS = ROOT / "outputs" / "suwon"

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
SEMAS_SIGUNGU = ("수원시",)   # 시군구명 prefix: the city and its 구

# --- Rail ------------------------------------------------------------------

OSM_BBOX = (37.20, 126.90, 37.37, 127.11)       # S, W, N, E: the city plus about 2 km
# The Korail lines the metropolitan subway signs (route=train), queried by ref
# beside every subway, light-rail and monorail relation in the box.
OSM_TRAIN_REFS = ('수인·분당', '경의·중앙', '경강', '서해', 'GTX-A', '경춘')
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 수원시, admin_level 6, resolved by name 2026-09-29.
BOUNDARY_RELATION = 2409182
BOUNDARY_NAME = "수원시"
# 121 km2 measured 2026-09-29 (the city publishes 121.1).
BOUNDARY_AREA_KM2 = (116, 126)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude falls in the 126 to 132 band. Derived per city,
# not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
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
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
LINES = {
    "L1": ("1", line_registry.colour("seoul-subway-line-1"), "Line 1", None),
    "SB": ("수인·분당", line_registry.colour("suin-bundang-line"), "Suin–Bundang Line", None),
    "SBD": ("신분당", line_registry.colour("shinbundang-line"), "Shinbundang Line", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train"}
# Gate 3: each WHOLE line's station count, English Wikipedia's line infoboxes
# read 2026-09-29 (a SECONDARY source, as Busan's). Line 1 is left out of the
# whole-line gate, as in Incheon: the query brings only its service relations
# that touch the box, never the whole 102-station line.
LINE_STATION_COUNTS = {"Suin–Bundang Line": 63, "Shinbundang Line": 16}
NOT_DRAWN = {"GTX-A": "GTX-A", "4": "Line 4"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
# OSM's English name, where the operator signs it otherwise (read 2026-09-29).
OSM_NAME_EN_OVERRIDES = {
    "매탄권선": "Maetan-Gwonseon",   # OSM name:en "MaetanGwonseon"
}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

CITY_PREFIX = "경기도 수원시"
TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602409182)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ko",)
PLACE_FOLD = None
PLACE_REVIEWED = {}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/suwon.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # A facility of an apartment estate (owner, 2026-10-13)
    "way/297881214": "'LG빌리지 광장': the plaza of the LG Village apartment complex, tagged a park",
    "way/843716483": "'월드마크푸르지오 원형 분수': \"round fountain\" of the World Mark Prugio apartment complex, tagged a park",
    "way/1186698182": "'하늘채 코오롱 공터': \"vacant lot\" (공터) of the Haneulchae Kolon apartment complex, tagged a park",
    "way/471352737": "'한일타운 휴식공터': \"rest lot\" (휴식공터) of the Hanil Town apartment complex, tagged a park",
    # A business (owner, 2026-10-13)
    "node/13051084102": "'노브랜드': a No Brand store (a retail chain) tagged amenity=marketplace; the wikidata and article are the company's, not this shop's",
    "way/841761806": "'R4공원': \"R4 park\", the grounds of a Samsung building (operator=삼성) inside the Digital City campus",
    # A glitched name (owner, 2026-10-13)
    "way/841764130": "'blue': \"blue\", operator=s, a plot inside the Samsung campus; a placeholder, not a name",
    "way/841764718": "'r3': \"r3\", operator=s, a plot inside the Samsung campus; a code, not a name",
    "way/841784969": "'스드스바크': 스드스바크, not a Korean word; a keyboard slip on a plot at the Samsung campus edge",
    # Worship named only by its body or chain (owner, 2026-10-13)
    "way/1135441516": "'구세군교회': 구세군교회 = \"Salvation Army church\", the denomination alone",
    "way/665327705": "'성결교회': 성결교회 = \"Holiness church\", the denomination alone",
    "way/477908698": "'예수그리스도 후기성도 교회': the Latter-day Saints' church name alone",
    "way/1474325913": "'은혜와진리교회': 은혜와진리교회, the chain's name alone (its branch 은혜와진리교회 영통성전 keeps its row)",
    # A religious office (owner, 2026-10-13)
    "way/470456028": "'세한성결교회 비전센터': 비전센터 = a church's \"vision centre\" annex, 20 m from the church 세한교회 itself, tagged a place of worship",
    # A bare type word (owner, 2026-10-13)
    "way/474535931": "'게이트볼전용구장': 게이트볼전용구장 = \"gateball-only ground\", tagged leisure=stadium",
    "node/13525519598": "'무대': 무대 = \"stage\", tagged place=square",
    "way/477535067": "'중앙광장': 중앙광장 = \"central plaza\"",
    "way/1474378318": "'체육공원': 체육공원 = \"sports park\"",
    "way/467977097": "'수변공원': 수변공원 = \"waterside park\", the type word alone",
    "way/1208463516": "'7호 수변공원': \"No. 7 waterside park\", a lot number beside the type word",
    "way/1203520117": "'제 5호 수변공원': \"No. 5 waterside park\", a lot number beside the type word (written 제 5호 with a space, which the coded-type rule may miss)",
    "way/1203505829": "'제 6호 수변공원': \"No. 6 waterside park\", a lot number beside the type word",
    "way/547444350": "'범종루': 범종루 = \"bell pavilion\", a building type inside the same temple",
    "way/547444345": "'약사보전': 약사보전 = \"Medicine Buddha hall\", a standard hall type inside the same temple",
    # A description standing in for a name (owner, 2026-10-13)
    "way/468669618": "'성호관잔디': 성호관잔디 = \"the lawn of Seongho Hall\", a campus building's lawn",
    "way/492695134": "'Environmental Building Park': \"Environmental Building Park\", an English description of a lawn beside a university building; no Korean name",
    "node/4656395966": "'지구본 조형물': 지구본 조형물 = \"globe sculpture\", the object described",
    "node/5532424095": "'독수리상': 독수리상 = \"eagle statue\", the object described",
    # A second row of one object (owner, 2026-10-13)
    "node/1791243454": "'수원화성': a second row for the fortress: relation/21586932 수원 화성 carries the article and the node lies inside it",
    # Unsure rows a ruling drops: a part of one temple that has no row of its own: the main hall stays as the way to find it, the other parts go (ruling 4) (owner, 2026-10-13)
    "way/547444346": "'용화각': a part of one temple that has no row of its own: the main hall stays as the way to find it, the other parts go",
    "way/547444349": "'우화궁': a part of one temple that has no row of its own: the main hall stays as the way to find it, the other parts go",
    "way/547444351": "'육화당': a part of one temple that has no row of its own: the main hall stays as the way to find it, the other parts go",
    "way/547444348": "'청운당': a part of one temple that has no row of its own: the main hall stays as the way to find it, the other parts go",
    "way/547444343": "'향하당': a part of one temple that has no row of its own: the main hall stays as the way to find it, the other parts go",
    "way/741628552": "'회향원': a part of one temple that has no row of its own: the main hall stays as the way to find it, the other parts go",
}
