"""Gwangju-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/gwangju.md) on Daejeon's config (Incheon's SEMAS module and
OSM rail route, keyed on 시군구코드).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "gwangju" / "raw"
DATA_PROCESSED = ROOT / "data" / "gwangju" / "processed"
OUTPUTS = ROOT / "outputs" / "gwangju"

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
# (data/korea/raw/), as every built SEMAS city (owner, 2026-09-29; Band A
# 2026-10-03). The 2026 merger put Gwangju's five 구 in the member
# 전남광주통합특별시 (시도코드 12) with all of South Jeolla, under new codes;
# the old 광주광역시 29xxx codes are gone. Keyed on codes, never names (owner,
# 2026-10-03): 동구, 서구, 남구 and 북구 recur in other cities, and 경기도
# 광주시 is another city.
SEMAS_SIDO = "전남광주통합특별시"
SEMAS_SIGUNGU = None
# 동구 12210, 서구 12240, 남구 12270, 북구 12300, 광산구 12330.
SEMAS_SIGUNGU_CODES = ("12210", "12240", "12270", "12300", "12330")

# --- Rail ------------------------------------------------------------------

OSM_BBOX = (35.03, 126.63, 35.27, 127.04)       # S, W, N, E: the placed extent plus about 2 km
# One Overpass query for the city (osm-rail), split by fetch_sources.py into
# the three files below.
OSM_ALL_JSON = DATA_RAW / "osm_all.json"
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# The boundary may have moved with the merger (the brief): the query asks for
# any relation named 광주광역시 and for the five 구 relations. On 2026-10-04
# no 광주광역시 relation came back, so step 1 takes the UNION of the five 구
# (admin_level 6), each by id and checked by name and by the query box.
BOUNDARY_NAME = "광주광역시"
BOUNDARY_DISTRICTS = ("동구", "서구", "남구", "북구", "광산구")
BOUNDARY_DISTRICT_RELATIONS = {4162635: "동구", 7348759: "서구", 7348741: "남구",
                               7348583: "북구", 7348758: "광산구"}
# The five 구 measured 500 km2 together, 2026-10-04.
BOUNDARY_AREA_KM2 = (490, 510)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude (~126.85) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Gwangju Metro Line 1, 20 stations, all inside the city (녹동 to 평동). NOT
# drawn: Line 2 (not open; phase 1 reported for 2028-12) and Korail/KTX
# (intercity, as everywhere in Korea; the query never asks for route=train).
# key -> (OSM ref, colour, public name, label end).
# The operator's color as OSM tags it on both direction relations.
LINES = {
    "L1": ("1", "#009088", "Line 1", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train", "tram"}
# Gate 3: the operator's own count (grtc.co.kr 운행현황, 역수 20개역; brief
# check gwangju-line1-operator-facts).
LINE_STATION_COUNTS = {"Line 1": 20}
# Line 2's two circle relations (route=light_rail, 36 planned stops each on
# 2026-10-04) are the line under construction.
NOT_DRAWN = {"2": "Line 2 (under construction)"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
# OSM's English name, where it misspells what the operator signs: OSM gives
# 금남로4가 "Geumnamno 4(sa)-ga" but 금남로5가 "Geumnamro 5-ga"; the
# operator's English station list reads Geumnamno4-ga and Geumnamno5-ga
# (grtc.co.kr/subwayeng, read 2026-10-04), spaced here as OSM spaces 4가.
OSM_NAME_EN_OVERRIDES = {
    "금남로5가": "Geumnamno 5-ga",
}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

GWANGJU_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3604162635,3607348759,3607348741,3607348583,3607348758)"
# 북구 holds no station and 12,657 of the map's 47,214 businesses, measured
# 2026-10-13. No 광주광역시 relation exists to name the city as one area.
PLACE_AREA_KEPT = {"relation/7348583": "part of the boundary the map's businesses are cut to; "
                                       "owner, 2026-10-13"}
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ko",)
PLACE_FOLD = None
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
_JUNCTION = 'a signed junction (junction=yes) named for the building beside it: a road feature, not the building'
PLACE_REVIEWED = {name: _JUNCTION for name in (
    "신우아파트사거리", "양림2차사거리", "우미광장사거리", "중흥모아사거리", "청아맨션교차로", "한림장오거리", "호반아파트")}
# Candidate 3 would make way/835704878 redundant, candidate 4 the three
# customers-only service roads, candidate 1 the play-park and plaza rows
# (docs/decisions_drafts/search-final.md, "Rule candidates").
PLACE_DROPPED = {
    # Bare type words and type phrases (the flag read of 2026-10-13, applied on the owner's word;
    # docs/decisions_drafts/search-final.md).
    "way/470162156": "a bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; owner 2026-10-13, the flag read's verdicts, all approved)",
    "way/629024038": "a composer's birthplace, in on the composer's article; no sign it is open to visitors was checked (owner, 2026-10-13)",
    "way/444717696": "the air force unit as a second row for Gwangju Airport (owner, 2026-10-13)",
    "node/6411444468": "a development zone's planning label drawn as a place (owner, 2026-10-13)",
    "way/835704878": "an apartment estate's own garden, plaza or playground",
    "way/469653066": "an apartment estate's own garden, plaza or playground",
    "way/473501622": "an apartment estate's own garden, plaza or playground",
    "way/470099446": "an apartment estate's own garden, plaza or playground",
    "way/863752688": "an apartment estate's own garden, plaza or playground",
    "way/473599632": "an apartment estate's own garden, plaza or playground",
    "way/863752689": "a description standing in for a name",
    "way/863758772": "a description standing in for a name",
    "way/863758774": "a description standing in for a name",
    "way/863758770": "a description standing in for a name",
    "way/863758775": "a description standing in for a name",
    "way/863758771": "a description standing in for a name",
    "way/473237154": "a description standing in for a name",
    "way/473240176": "a description standing in for a name",
    "way/473474720": "a description standing in for a name",
    "way/473471661": "a description standing in for a name",
    "way/636203708": "a description standing in for a name",
    "way/638451657": "a description standing in for a name",
    "way/639079455": "a description standing in for a name",
    "way/1125165997": "a description standing in for a name",
    "way/1123127732": "a description standing in for a name",
    "node/4686235141": "a description standing in for a name",
    "way/468928992": "a description standing in for a name",
    "node/4643409027": "a church's name stone; the church has its own row",
    "way/629868781": "a cafe's name on a historic building, no article",
    "node/4945534269": "a shopping street's name tagged a monument",
    "way/470116012": "a high school tagged a place of worship",
    "way/1136431923": "a sisters' congregation house, tagged a place of worship",
    "way/1126651123": "a retreat house, tagged a place of worship",
    "way/990254300": "the archdiocese's chancery, tagged a place of worship",
    "way/1125516300": "a presbytery's office, tagged a place of worship",
    "way/487746950": "a former church by its own name; no lifecycle tag",
    "node/13052442101": "an artwork admitted by its artist's article, not its own",
    "way/628952569": "a community office admitted by its neighborhood's article",
    "way/1236254153": "a shrine drawn a second time as a place; the landmark row stays",
    "node/11379880372": "a market car park's entrance, tagged a junction",
    "way/1380477166": "a bus platform on a footway, named for the junction",
    "way/106346374": "a placeholder for a name",
    "way/1433958430": "a placeholder for a name",
    "way/547068287": "a placeholder for a name",
    "way/583459748": "a placeholder for a name",
    "way/583459749": "a placeholder for a name",
    "way/583459753": "a placeholder for a name",
    "way/583459755": "a placeholder for a name",
    "way/583459758": "a placeholder for a name",
    "way/610965548": "a placeholder for a name",
    "way/720257544": "a description standing in for a name",
    "way/554449628": "a description standing in for a name",
    "way/1213764352": "a school's internal road",
    "way/1213764353": "a school's internal road",
    "way/1213764354": "a school's internal road",
    "way/1213764355": "a school's internal road",
    "way/469936971": "a school's internal road",
    "way/863506122": "a school's internal road",
    "way/863506123": "a school's internal road",
    "way/863506124": "a school's internal road",
    "way/863506125": "a school's internal road",
    "way/863506126": "a school's internal road",
    "way/987248990": "a description standing in for a name",
    "way/1011110239": "a planning code, not a street name",
    "way/1527824182": "a planning code, not a street name",
    "way/105243409": "a street name with a house number; the street has its own row",
    "way/471772549": "a description standing in for a name",
    "way/470163403": "a description standing in for a name",
    "way/470162153": "a description standing in for a name",
    "way/470162157": "a description standing in for a name",
    "way/470164017": "a description standing in for a name",
    "way/470164912": "a description standing in for a name",
    "way/1373352638": "a description standing in for a name",
    "way/1377370198": "a description standing in for a name",
    "way/1210473557": "a description standing in for a name",
    "way/947400344": "an access ramp, named by a description",
    "way/946752294": "an access ramp, named by a description",
    "way/946752295": "an access ramp, named by a description",
    "way/946752298": "an access ramp, named by a description",
    "way/946752302": "an access ramp, named by a description",
    "way/586284995": "an access ramp, named by a description",
}
