"""Boston settings.

Three registries, two buckets, and two station rules - the most assembled city
here after New York. See pipeline/taxonomies/boston_licensecat.py for why the
coverage is what it is, and docs/data_sources.md, "Boston - Step 0 findings",
for the endpoints and the traps.

WHAT THIS CITY CANNOT SHOW, STATED UP FRONT
-------------------------------------------
Boston licenses food and alcohol and essentially no other trade. There is no
personal-service licence anywhere reachable as data - Massachusetts licenses
cosmetology and barbering at STATE level and publishes no address-bearing
export - so **Personal services is ABSENT, not thin**, exactly as in
Philadelphia. Retail exists but is narrow: retail FOOD (groceries, convenience
stores, bodegas) plus package stores and cannabis dispensaries. A clothes shop,
a bookshop or a hardware store needs no licence any of these three registries
issues, so it is simply not here.

The honest summary is that this map shows **food-and-drink density with a
retail-food edge**, not general commercial density, and the city page says so.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "boston" / "raw"
DATA_PROCESSED = ROOT / "data" / "boston" / "processed"
OUTPUTS = ROOT / "outputs" / "boston"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Every station this build drops, with the reason and what it is nearest to
# instead. Boston needs this more than most cities: it loses stations BOTH to
# the boundary (the network is regional) and to the Green Line thinning, so the
# file carries two different kinds of exclusion and names which is which.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
BUSINESSES_PREFILTER_CSV = DATA_PROCESSED / "businesses_prefilter.csv"

# Every raw read passes this rather than relying on pandas' default - see
# docs/data_sources.md, "Declare the source encoding".
SOURCE_ENCODING = "utf-8"

# --- Raw inputs (see pipeline/boston/fetch_sources.py) --------------------

# Boston's open-data portal is CKAN, not Socrata. datastore_search_sql takes
# SQL directly, which is how the aggregate work below is done server-side.
CKAN_SQL_URL = "https://data.boston.gov/api/3/action/datastore_search_sql"

# 1. Inspectional Services food establishments. THE INSPECTION HISTORY, not the
#    "Active Food Establishment Licenses" extract - that extract holds only
#    FS+FT and drops the entire RF (Retail Food) category, which is Boston's
#    whole Retail bucket. 902,651 violation-level rows; step 2 filters to
#    active and collapses to one row per property_id.
ISD_FOOD_RESOURCE = "4582bec6-2b4f-4f9e-bc55-cbaa73117f4c"

# 2. Licensing Board Licenses - used ONLY for package stores. Its 2,578 Common
#    Victualler licences are the same restaurants as source 1 and are excluded
#    to avoid double-counting. Coordinates here are gpsx/gpsy in EPSG:2249,
#    NOT lat/lon.
LICENSING_BOARD_RESOURCE = "04dc653b-1789-4374-9669-b07df7233344"

# 3. Cannabis Active Licenses - 43 rows, same gpsx/gpsy convention.
CANNABIS_RESOURCE = "e395fd88-0f81-4399-a57a-3e94a74b145c"

# The state plane the Licensing Board and cannabis sets use. NAD83 /
# Massachusetts Mainland in US SURVEY FEET. Verified 2026-09-21 by
# transformation, not assumed: it places Copley Square at (42.34860,
# -71.07882) and 122 Brighton Ave in Allston correctly, while EPSG:26986 - the
# metre-based sibling of the same state plane, and the plausible wrong answer -
# lands every point near 60 degrees north.
GPS_XY_CRS = "EPSG:2249"

# MBTA GTFS. feed_info.txt exists but declares NO licence field, so the terms
# come from the MassDOT Developers License Agreement instead - stored at
# docs/licenses/mbta-massdot-develop-license-agreement.pdf. It requires ONE
# notice: "Clearly acknowledge MassDOT as the provider of the Data" (§4.1).
GTFS_URL = "https://cdn.mbta.com/MBTA_GTFS.zip"

# MassGIS municipal boundaries, layer 1 ("Areas"): 351 polygons, one per
# Massachusetts municipality, with a TOWN field.
#
# A MULTI-TOWN layer is the point, and it does two jobs at once. Boston's own
# "water excluded" outline would filter but could not NAME the towns the
# network runs through, and this map loses 54 of 125 stations to other
# municipalities - a scale of exclusion that has to be citable, as it is for
# San Diego's 16 and Los Angeles' 54. Downloaded with a spatial envelope around
# the rapid-transit network rather than all 351 towns statewide.
BOUNDARY_SERVICE_URL = (
    "https://services1.arcgis.com/hGdibHYSPO59RG1h/arcgis/rest/services/"
    "Massachusetts_Municipalities/FeatureServer/1"
)
BOUNDARY_TOWN_FIELD = "TOWN"
CITY_BOUNDARY_NAME = "BOSTON"
# Envelope around MBTA rapid transit, padded. Keeps the boundary download to
# the ~40 towns that can possibly matter.
BOUNDARY_ENVELOPE = "-71.35,42.15,-70.90,42.50"

GTFS_ZIP = DATA_RAW / "gtfs.zip"
ISD_FOOD_CSV = DATA_RAW / "isd_food_active.csv"
LICENSING_BOARD_CSV = DATA_RAW / "licensing_board.csv"
CANNABIS_CSV = DATA_RAW / "cannabis.csv"
TOWN_BOUNDARIES_GEOJSON = DATA_RAW / "ma_municipalities.geojson"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 19N: the longitude (~-71.06) falls in the -72 to -66 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson. Note this is
# NOT the same as GPS_XY_CRS above, which is the state plane two of the three
# source files happen to publish in.
CRS_PROJECTED = "EPSG:32619"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# MBTA rapid transit, by route_id in its own feed. Grouped because the Green
# Line's four branches are one public line sharing a central subway, the same
# way Philadelphia's five subway-surface trolley branches are one group.
#
# The 14 `CR-*` Regional Rail routes are commuter rail and are NOT included, as
# commuter rail is excluded in every other city here. Ferries likewise.
ROUTE_GROUPS = {
    "Red": ["Red"],
    "Orange": ["Orange"],
    "Blue": ["Blue"],
    "Green": ["Green-B", "Green-C", "Green-D", "Green-E"],
    "Mattapan": ["Mattapan"],
}

# group -> (real public name, colour). MBTA's own colours, which are
# unambiguous, distinct from each other and famous enough that substituting
# them would make the map harder to read. Note the project-wide open question
# on official route colours (docs/data_sources.md, item 5c) applies here too.
LINE_NAMES = {
    "Red": ("Red Line", "#DA291C"),
    "Orange": ("Orange Line", "#ED8B00"),
    "Blue": ("Blue Line", "#003DA5"),
    "Green": ("Green Line", "#00843D"),
    # MBTA gives the Mattapan trolley the Red Line's colour, which would make
    # two separately-labelled lines identical on the map. Darkened to stay
    # recognisably in the same family while remaining distinguishable - the
    # same treatment Staten Island Railway got in New York, and for the same
    # legibility reason.
    "Mattapan": ("Mattapan Trolley", "#8C1810"),
}

# Force the Blue Line's label to the Bowdoin (downtown) end of its shape.
#
# Automatic placement puts it at the Wonderland (north-east) end, which lands
# in the top-right corner of the frame - exactly where the map's own fixed
# "Light mode" and "All cities" buttons sit. Measured 2026-09-21 while
# verifying all nine maps before the first deploy: at a frame width of 854px,
# the width a 1024px browser window gives the app's column, the label
# overlapped that button box by 16x15px and rendered as "Blue Li". Confirmed
# by screenshot, not by rects alone. Clean at 1000px and 1280px, so the fault
# is specific to frames NARROWER than the map's own 1000px layout width.
#
# Note "start" and the automatic choice are the SAME end here - setting it
# changed nothing, which is worth knowing before trying it on another line.
# "end" is the one that moves this label.
LINE_LABEL_ENDS = {"Blue": "end"}

# One representative shape per group, read from real trip counts. A tuple is
# one line whose physical extent needs several shapes, which both branching
# lines need: the Red Line splits to Ashmont and Braintree, and the Green Line
# is four branches on a shared subway.
#
# The single-track and short-turn variants are deliberately not drawn (Orange
# has 8 shapes, Blue 8, Green 37) - they are the same track. Mattapan's
# `canonical-899_0005` is a 1-trip artefact and is avoided.
LINE_SHAPES = {
    "Red": ("933_0020", "931_0009"),        # Braintree branch, Ashmont branch
    "Orange": ("903_0026",),                # Oak Grove <-> Forest Hills
    "Blue": ("946_0013",),                  # Wonderland <-> Bowdoin
    "Green": ("8000008", "8000018",         # D (Riverside), E (Heath St)
              "8000013", "8000006"),        # B (Boston College), C (Cleveland Circle)
    "Mattapan": ("899_0005",),              # Ashmont <-> Mattapan
}

# Which groups get the sub-transit-line thinning (docs/sub_transit_line_filters.md).
#
# Boston needs TWO station rules at once, as Philadelphia does. Red, Orange and
# Blue are grade-separated heavy rail on their own right-of-way and keep every
# in-city station. The Green Line is a central subway plus four STREET-RUNNING
# surface branches - San Francisco's exact shape - and is thinned. Mattapan is
# a street-running trolley too, and the obvious guess was that it needed
# thinning as well. MEASURED instead: its 8 stops sit 433-804 m apart, median
# **518 m**, which is comparable to New York's 482 m and nowhere near San
# Francisco's 134 m trolley median. Only about half of it is in Boston anyway,
# so thinning a 4-station in-city segment would leave almost nothing. Left
# unthinned, on the measurement rather than on the street-running label.
THINNED_GROUPS = frozenset({"Green"})

# Target spacing for filter 3, measured along the line's real path.
STATION_SPACING_MILES = 0.5

# Filter 1: the Green Line's central subway, never thinned. These are the
# grade-separated stations between Lechmere and the branch portals, read from
# the feed rather than guessed - see step1_stations.py, which asserts every one
# of them is actually present.
#
# Green Line only - this set feeds filter 1, and filter 1 only runs on
# THINNED_GROUPS. "South Station" was briefly added here and removed: it is a
# Red Line station, not a Green Line one, so it would never match and the
# validator flagged it as absent from the feed on every run.
SUBWAY_STATION_NAMES = frozenset({
    "Lechmere", "Science Park/West End", "North Station", "Haymarket",
    "Government Center", "Park Street", "Boylston", "Arlington", "Copley",
    "Hynes Convention Center", "Kenmore", "Prudential", "Symphony",
})

# GTFS stop names are clean here, unlike Miami's: `parent_station` is populated
# for every rapid-transit stop, so platforms collapse without name surgery.
#
# NOTE WHAT IS *NOT* STRIPPED. An earlier version of this pattern also removed
# a trailing " Station", which is wrong in Boston and was caught by validating
# the configured subway list against the feed: it turned **"North Station"**
# into "North", so filter 1 stopped recognising one of the Green Line's own
# central-subway stations and would have thinned it as a surface stop. "North
# Station" and "South Station" are the stations' real names, not a name plus a
# suffix. Only the direction suffixes are removed here.
STATION_SUFFIX_PATTERN = r"\s*-\s*(Inbound|Outbound)\s*$"

STATION_NAME_ALIASES = {}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "boston_licensecat"

# Each source's own category column, renamed to the taxonomy's VALUE_COLUMN by
# step 2 before classification.
RAW_CLASSIFICATION_COLUMNS = {
    "isd_food": "licensecat",
    "licensing_board": "license_type",
    "cannabis": "license_type",
}

# The premises key per source. ISD publishes a real one; the other two do not,
# so they fall back to name-plus-address as Miami does.
ISD_PREMISES_KEY = "property_id"
PREMISES_KEY = ["business_name", "address"]

# Sanity bounds for coordinates: Greater Boston, since the business registries
# are city-only but the transit network is not.
BOSTON_BBOX = {
    "lat_min": 42.15,
    "lat_max": 42.50,
    "lon_min": -71.35,
    "lon_max": -70.90,
}
