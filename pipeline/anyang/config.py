"""Anyang-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; copied from Bucheon's (the Korean
pattern: SEMAS's register, OSM rail on Busan's step 1), via Namyangju's. One of the Gyeonggi
satellites' second round (owner, 2026-09-29: Namyangju, Ansan and Uijeongbu,
one page each; docs/build_briefs/gyeonggi.md, "The next satellites").
"""

from pathlib import Path

from pipeline import line_registry

# --- Scope: the city, or Anyang (Regional) ---------------------------------
#
# REGIONAL adds Gunpo (6 stations) and Uiwang (1) on the lines the map already
# draws, the owner's mark of 2026-10-04 (docs/build_briefs/anyang_regional.md;
# the regional-extension skill). False reproduces the city-alone build byte
# for byte, which the drift check proved before the switch went on.
REGIONAL = True
NAME = "Anyang (Regional)" if REGIONAL else "Anyang"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "anyang" / "raw"
# Regional outputs in their own folder: data/ is shared by every worktree.
DATA_PROCESSED = ROOT / "data" / "anyang" / "processed" / ("regional" if REGIONAL else "")
OUTPUTS = ROOT / "outputs" / "anyang"

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
# The city alone keys on its 시군구명 prefix, as built (the city and its two 구,
# 만안구 and 동안구). The regional page keys on codes, never names (owner,
# 2026-10-03): 41171 만안구 and 41173 동안구 pick exactly the prefix's rows,
# 41410 군포시 and 41430 의왕시 join (the brief, measured 2026-10-06).
SEMAS_SIGUNGU = None if REGIONAL else ("안양시",)
SEMAS_SIGUNGU_CODES = ("41171", "41173", "41410", "41430") if REGIONAL else None

# --- Rail ------------------------------------------------------------------

# S, W, N, E: the city plus about 2 km (Anyang spans about 37.36-37.44 N, 126.88-126.99 E; step 1 checks the boundary lies inside).
OSM_BBOX = (37.34, 126.86, 37.46, 127.01)
# The Korail lines the metropolitan subway signs (route=train), queried by ref
# beside every subway, light-rail and monorail relation in the box.
OSM_TRAIN_REFS = ('수인·분당', '경의·중앙', '경강', '서해', 'GTX-A', '경춘')
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 안양시, admin_level 6 (the brief, 2026-09-29).
BOUNDARY_RELATION = 2409161
BOUNDARY_NAME = "안양시"
# 59 km2 measured 2026-09-29 (the brief).
BOUNDARY_AREA_KM2 = (55, 63)
# The regional scope: 안양시 with 군포시 and 의왕시, each relation taken by id and
# checked by name, from their own query file so the city's cache stays as it
# is. Fetched 2026-10-07: 안양시 59.1, 군포시 35.9 and 의왕시 53.8 km2, the union
# 149 km2.
REGIONAL_BBOX = (37.28, 126.85, 37.47, 127.05)        # S, W, N, E
REGIONAL_BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary_regional.json"
REGIONAL_RELATIONS = {2409161: "안양시", 2409167: "군포시", 2409184: "의왕시"}
REGIONAL_AREA_KM2 = (142, 156)
# The word station_scope.py reads is "outside".
OUTSIDE_REASON = ("outside Anyang, Gunpo and Uiwang" if REGIONAL
                  else "outside Anyang's boundary")

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~127.2) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# Standard: the brief's median gap is 1,487 m.
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
# Seoul's colours (the brief). Two lines with no shared station in the city.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
LINES = {
    "L1": ("1", line_registry.colour("seoul-subway-line-1"), "Line 1", None),
    "L4": ("4", line_registry.colour("seoul-subway-line-4"), "Line 4", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train"}
# Gate 3: each WHOLE line's station count, English Wikipedia's line infoboxes
# (a SECONDARY source, as Busan's). Line 1 is left out, as in Incheon and
# Bucheon (the brief); Line 4 too: the relations reaching the box carry 48 of
# its 51 stations, without the Jinjeop extension's three (Namyangju's finding),
# step 1's report 2026-09-30. In place of the gate, each line's in-city stations
# read against its line table (English Wikipedia, 2026-09-30): Line 1 Seoksu,
# Gwanak, Anyang and Myeonghak (4); Line 4 Indeogwon, Pyeongchon and Beomgye
# (3). Step 1's 7 agree, line by line. Anyang (Regional), read against the same
# tables 2026-10-07: Line 1 adds Geumjeong, Gunpo, Dangjeong and Uiwang (8),
# Line 4 Geumjeong, Sanbon, Surisan and Daeyami (7); step 1's 14 agree.
LINE_STATION_COUNTS = {}
NOT_DRAWN = {"GTX-A": "GTX-A"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
# OSM's English name, where the operator signs it otherwise.
OSM_NAME_EN_OVERRIDES = {}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

CITY_PREFIX = "경기도 안양시"
TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

# The regional map's three municipalities, REGIONAL_RELATIONS above (owner,
# 2026-10-13): the plan's city-alone area left 7 of 14 stations outside.
PLACE_AREA = "(id:3602409161,3602409167,3602409184)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ko",)
PLACE_FOLD = None
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md). Signed
# junctions (junction=yes) named for the building beside them: a road feature,
# not the building (Seoul's precedent, batch 2b).
_JUNCTION = "a signed junction (junction=yes) named for the building beside it: a road feature, not the building"
PLACE_REVIEWED = {name: _JUNCTION for name in (
    "8단지입구사거리", "LG아파트삼거리", "개나리아파트삼거리", "동백아파트앞교차로", "무궁화APT사거리",
    "삼호아파트삼거리", "포은신안아파트삼거리", "대우사원주택앞교차로", "롯데마트사거리", "보우상가사거리",
    "스마트호텔삼거리", "공용주차장앞교차로")}
# Candidate 3 would make the _ESTATE ids redundant, candidate 7 the _EXHIBIT
# ids (docs/decisions_drafts/search-final.md, "Rule candidates").
_ESTATE = "an apartment estate's own garden or playground, run by its management office (operator tag)"
_EXHIBIT = "a Railroad Museum exhibit whose article is its class's or kind's, not the object's own"
_MALL = "a corridor of an underground shopping mall, named for the mall"
_NO_NAME = "a description standing in for a name"
PLACE_DROPPED = {
    # A religious body's meeting halls and branches, and halls named only by a body and a hall type (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "way/1287595059": "a religious body's meeting hall or branch tagged a place of worship is dropped (ruling 2; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    # Codes and numbers beside a type word (the flag read of 2026-10-13, applied on the owner's word;
    # docs/decisions_drafts/search-final.md).
    "way/580706448": "a code or a number beside a type word is no name (CODED_TYPE, owner 2026-10-12; owner 2026-10-13, the flag read's verdicts, all approved)",
    "node/7817073349": "a rail yard (railway=yard) in the index as a station; no passenger tag "
                       "(owner, 2026-10-13)",
    "way/777263833": _ESTATE, "way/777264096": _ESTATE, "way/777262929": _ESTATE,
    "way/777263610": _ESTATE, "way/746342781": _ESTATE,
    "way/1464246217": "a diocese's vicariate office, tagged a place of worship",
    "way/453505500": "a building's own name, tagged a place of worship; the church has its own row",
    "way/544121611": _NO_NAME, "way/471352325": _NO_NAME, "way/634086695": _NO_NAME,
    "node/5932343049": "a name cut short (a monument named only for the forces it honors)",
    "way/829939493": _EXHIBIT, "way/829939495": _EXHIBIT, "way/829939494": _EXHIBIT,
    "way/829939499": _EXHIBIT, "way/829939487": _EXHIBIT, "way/829939488": _EXHIBIT,
    "way/829939503": _EXHIBIT, "way/829939489": _EXHIBIT,
    "way/1339371333": "a footbridge link from a station to a department store, named for the store",
    "way/682618785": _NO_NAME, "way/682618787": _NO_NAME, "way/696843589": _NO_NAME,
    **{f"way/{i}": _MALL for i in (
        837760800, 837760801, 837760802, 837760805, 837760806, 837760808, 837760809, 837760810,
        837760812, 837760813, 837760814, 837760815, 837760816, 837760817, 837760818, 843067493,
        844174049, 844174050, 844174051)},
}
# Kept by id: admitted as rows although a rule passes them over (owner, 2026-10-13;
# docs/decisions_drafts/search-final.md).
PLACE_KEPT = {
    "way/156206585": "'의왕조류생태과학관', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
}
