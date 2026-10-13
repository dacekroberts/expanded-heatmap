"""Hong Kong-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/hong-kong.md.

Business leg: FEHD's three licence registers (restaurants, other food, non-food),
one XML each, keyless, regenerated daily and carrying their own GENERATION_DATE
and code lookups. The XML carries an address and no coordinate; each licence is
placed at FEHD's OWN point for it, from the same registers on the CSDI portal,
joined by licence number (see CSDI_LAYERS below for why not ALS).

Rail: MTR's eight urban lines and the Light Rail, from OpenStreetMap. The ground
(osm-rail skill): MTR's open data is station LISTS with no coordinates and no
geometry, and the Transport Department's GTFS (`pt-headway`) carries buses,
minibuses, ferries, the trams and the Peak Tram but NO MTR rail - its agency.txt
has MTR Bus and nothing else of MTR's. MTR's own lists are kept as gate 3.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "hong_kong" / "raw"
DATA_PROCESSED = ROOT / "data" / "hong_kong" / "processed"
OUTPUTS = ROOT / "outputs" / "hong_kong"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Step 1 writes the drawn lines here: MTR's relations as OSM gave them, plus ONE
# synthetic relation for the Light Rail network (the owner's call: drawn as one
# network, since its twelve routes overlap in a small area).
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

FEHD_BASE = "https://www.fehd.gov.hk/english/licensing/license/text/"
FEHD_FILES = {                      # register -> file name (English edition)
    "restaurants": "LP_Restaurants_EN.XML",
    "other_food": "LP_OtherFood_EN.XML",
    "non_food": "LP_NonFood_EN.XML",
}

MTR_BASE = "https://opendata.mtr.com.hk/data/"
MTR_STATIONS_CSV = DATA_RAW / "mtr_lines_and_stations.csv"         # gate 3 only
MTR_LIGHT_RAIL_CSV = DATA_RAW / "light_rail_routes_and_stops.csv"  # gate 3 only

OVERPASS_URLS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
)
# Every name search bounded (osm-rail: an unbounded one is a GLOBAL search).
OSM_BBOX = (22.13, 113.82, 22.57, 114.45)       # S, W, N, E - the whole SAR
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# The SAR's own relation, chosen by its ISO code, never by size.
BOUNDARY_ISO = "HK"
# MEASURED 2,759 km2 (relation 913110): the SAR's OSM boundary includes its
# waters, not the ~1,110 km2 of land. The gate refuses anything else.
BOUNDARY_AREA_KM2 = (2700, 2820)

# WHERE EACH LICENCE IS: FEHD's OWN points. The same three registers are
# published on the Government's Common Spatial Data Infrastructure (CSDI) portal
# with a latitude/longitude per licence, keyed by the same licence number. They
# replaced the brief's plan to geocode every address with ALS (owner,
# 2026-09-24): on 2,000 licences probed, 1,999 matched the XML by number, and
# where ALS's hit passed this build's district and score/content rules the two
# points were a median 12 m apart (89% within 50 m). ALS's own answers are not
# used; ~2,000 cached lookups remain in raw/ only as that cross-check's record.
CSDI_FILE_API = "https://portal.csdi.gov.hk/csdi-webpage/file-api"
CSDI_LAYERS = {                     # register -> (CSDI dataset id, layer)
    "restaurants": ("fehd_rcd_1630036390312_58893", "FEHD_RL"),
    "other_food": ("fehd_rcd_1630036111498_75446", "FEHD_FL"),
    "non_food": ("fehd_rcd_1630036520303_61763", "FEHD_TL"),
}
CSDI_LICENCE_NO = "SEARCH02_EN"     # the licence number, as the XML's LICNO
CSDI_TYPE = "NSEARCH02_EN"          # the licence type code, as the XML's TYPE

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 50N: the longitude (~114.17) falls in the 114 to 120 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32650"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# The owner's call (2026-09-24): MTR's eight urban lines and the Light Rail.
# NOT drawn: Airport Express (it adds only the airport island), the Disneyland
# Resort Line, the high-speed rail, the Peak Tram, and Hong Kong Tramways (within
# a few hundred metres of the Island Line nearly all the way). The bbox also
# catches Shenzhen's metro, which the network tag keeps out.
#
# Matched on the RELATION's network and ref (osm-rail: relation-level network
# filtering is safe; a node-level one is not), after printing the table.
MTR_NETWORK = "港鐵 MTR"
LIGHT_RAIL_NETWORK = "輕鐵 Light Rail"
LINE_ORDER = ["ISL", "TWL", "KTL", "TKL", "SIL", "TCL", "TML", "EAL", "LR"]
LINE_NAMES = {
    "ISL": "Island Line", "TWL": "Tsuen Wan Line", "KTL": "Kwun Tong Line",
    "TKL": "Tseung Kwan O Line", "SIL": "South Island Line", "TCL": "Tung Chung Line",
    "TML": "Tuen Ma Line", "EAL": "East Rail Line", "LR": "Light Rail",
}
NOT_DRAWN = {"AEL": "Airport Express", "DRL": "Disneyland Resort Line"}
# MTR's own colours as OSM carries them on each relation; the Light Rail has one
# per ROUTE, so the network drawn as one line takes this project's own colour.
LIGHT_RAIL_COLOUR = "#b8860b"
# A line is drawn from its longest relation plus only the track another
# relation adds (a branch): a way whose midpoint is further than this from what
# is already drawn. Both directions share an alignment, so this keeps a line
# from being laid on itself while still reaching East Rail's Lok Ma Chau spur
# and the TKO line's LOHAS Park branch.
BRANCH_MIN_M = 60.0
# OSM's name -> MTR's current one, where the two sources disagree about the SAME
# stop. Tuen Mun Swimming Pool carries MTR stop ID 250 (OSM `ref` 250, MTR code
# TSP) in both sources; MTR's list calls it Hoi Wong Road.
NAME_ALIASES = {"Tuen Mun Swimming Pool": "Hoi Wong Road"}
# In OSM's East Rail relations and not in MTR's station list: served on race
# days only, like Rotterdam's event-day tram 12. Recorded as excluded.
EVENT_ONLY = {"Racecourse": "served only on race days (not in MTR's station list)"}
# Stop nodes of one name further apart than this are not one station.
COLLAPSE_MAX_SPREAD_M = 400.0
# The Light Rail is thinned with the sub-transit-line filters, as Amsterdam's
# and Rotterdam's trams were; every MTR station is kept.
THIN_SPACING_MILES = 0.5
SPACING_MIN_M = 200.0

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "hong_kong_fehd"
NO_SHOP_SIGN = "No shop sign on the license"
# FEHD's DIST code 31: food trucks, filed as a district of their own.
FOOD_TRUCK_DISTRICT = "Food Truck"
RAW_CLASSIFICATION_COLUMN = "licence_type"

HONG_KONG_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}

# ---------------------------------------------------------------------------
# Place search (sample batch 2b, 2026-10-08): pipeline/place_index.py builds
# app/static/places/hong_kong.json from the caches place_index_fetch.py writes.
# The search area is the map's: the SAR's own relation 913110 (admin_level 3, ISO3166-1 HK), the
# map's whole scope, confirmed by id 2026-10-08.
# Overpass area id = 3600000000 + relation id.
PLACE_AREA = "(id:3600913110)"
# NEW file names: data/ is shared by every worktree.
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-08.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-08.json"
# The local language of OSM's names here: Chinese; OSM's `name` here is usually
# bilingual ("彌敦道 Nathan Road"), with name:zh and name:en beside it.
PLACE_LANGUAGES = ("zh",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
PLACE_REVIEWED = {
    "保健路 Clinic Road": "a public street named for a building or institution on it, not a business (batch 2b, _named_street)",
}
# OSM objects a reading by eye found to be a business or a home that no rule
# in place_index.py catches, each with why (place_index.build, `dropped`).
# The read (2026-10-08) covered every landmark and place name without a place
# word; the precedents are the Panama Hotel (a notable building kept) and
# Sydney's Meriton park (a business by name, dropped). Names that describe
# rather than name ("open area with bench") are an owner question, not here.
PLACE_DROPPED = {
    # Businesses tagged as places.
    "node/13178154315": "TakeOut Comedy Club: a comedy venue in a basement, tagged a theatre",
    "way/756672170": "大棠有機生態園 Tai Tong Organic EcoPark: a ticketed leisure farm, tagged a park",
    "way/1490236780": "水邊圍邨羅馬商業平台: a housing estate's shopping podium, tagged a park",
    # Homes and residents-only facilities.
    "way/1498122620": "Nan Fung Sun Chuen Ball Court: a private estate's own court",
    "way/696405913": "公眾休憩用地A Public Recreational Area A: a lettered open space for a development's residents (park:for=resident)",
    "way/776910736": "公眾休憩用地B Public Recreational Area B: as A",
    "way/776910737": "公眾休憩用地C Public Recreational Area C: as A",
    # The owner's answers to 2b's questions (2026-10-11): the Pillar of Shame ("drop by id"), descriptions standing in for names, and religious residences held to the worship precedent (a non-notable one where people live is out; the notable 般若精舍, 清涼法苑 and Chi Lin Nunnery stay).
    "node/1925188564": "a sculpture removed in December 2021 (OSM keeps it as historic=ruins with demolished:end_date): a search would move the map to a place where it is not",
    "way/1556817980": "a description standing in for a name (a sitting-out area)",
    "node/11400928912": "a description standing in for a name (a refuse point tagged a park)",
    "node/10264155125": "a 精舍 (a small hall where its nuns or devotees live), tagged a place of worship, not notable",
    "way/702596982": "a 精舍 (a small hall where its nuns or devotees live), tagged a place of worship, not notable",
    "way/510509951": "a 精舍 (a small hall where its nuns or devotees live), tagged a place of worship, not notable",
    "way/1421939813": "a 精舍 (a small hall where its nuns or devotees live), tagged a place of worship, not notable",
    "way/1421939815": "a 精舍 (a small hall where its nuns or devotees live), tagged a place of worship, not notable",
    "way/429896216": "a 精舍 (a small hall where its nuns or devotees live), tagged a place of worship, not notable",
    "way/859463025": "a 精舍 (a small hall where its nuns or devotees live), tagged a place of worship, not notable",
    "way/191365083": "a 精舍 (a small hall where its nuns or devotees live), tagged a place of worship, not notable",
    "way/467768817": "a 精舍 (a small hall where its nuns or devotees live), tagged a place of worship, not notable",
    "way/787051818": "a 精舍 (a small hall where its nuns or devotees live), tagged a place of worship, not notable",
    "way/787051819": "the same 精舍, a second building",
    "way/781756943": "a 精舍 (a small hall where its nuns or devotees live), tagged a place of worship, not notable",
    "way/429685657": "a friary (方濟會院), a religious residence tagged a place of worship, not notable",
    "way/1493422051": "a nunnery (萬佛堂), a religious residence tagged a place of worship, not notable",
    "way/763924400": "a retreat house (靜修院), a religious residence tagged a place of worship, not notable",
}
# Interchange names are street names here (owner, 2026-10-13: "keep as per-city
# with reasoning"): admitted on purpose on 2026-10-08, the names are how the
# junctions are known and signed in Hong Kong, and sixteen of the 44 rows are
# tagged roundabouts. Every other city drops them (place_index.street_never).
PLACE_KEEP_INTERCHANGES = True
