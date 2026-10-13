"""Washington D.C. settings.

The ninth city, and the first in the project whose transit feed is behind an
API key. See docs/data_sources.md, "Washington D.C. - Step 0 findings", for the
endpoints and the traps, and pipeline/taxonomies/dc_businessactivity.py for
what the single registry can and cannot show.

WHAT IS DIFFERENT ABOUT THIS CITY
---------------------------------
1. **One registry, all three buckets.** D.C.'s Basic Business License register
   is the first non-NAICS source in the project that covers Retail, Food
   service AND Personal services on its own, so there is no multi-source
   assembly here - unlike New York's four sources or Boston's three.
2. **The feed expires.** WMATA's `feed_info.txt` declares a TEN-DAY validity
   window, the shortest of any feed here, so `fetch_sources.py` refuses to
   reuse a stored copy once `feed_end_date` has passed. Every other city's feed
   can sit in `data/<city>/raw/` for months.
3. **The published latitude and longitude are useless.** `LATITUDE` and
   `LONGITUDE` are literally `39` and `-77` on every one of the 76,107 active
   rows - 0 of them inside the District. The real coordinates are
   `X_COORDINATE`/`Y_COORDINATE` in EPSG:26985, which step 2 reprojects.
4. **Half the storefront rows have no trade name**, which is the Los Angeles
   trap at half LA's severity, so the display-name rule is stricter here than
   anywhere else: see DISPLAY_NAME_PLACEHOLDER below.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "washington_dc" / "raw"
DATA_PROCESSED = ROOT / "data" / "washington_dc" / "processed"
OUTPUTS = ROOT / "outputs" / "washington_dc"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Every station this build drops, with the reason and what it is nearest to
# instead. D.C. loses stations only to the boundary - there is no thinning -
# so unlike Boston's this file carries one kind of exclusion.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
BUSINESSES_PREFILTER_CSV = DATA_PROCESSED / "businesses_prefilter.csv"

# 452 of the 6,504 storefront rows (6.9%) carry no coordinates at all, and the
# same rows carry no MAR_ID either - so Step 0's expectation that the Master
# Address Repository id would recover them was wrong: they are the rows the
# District's own geocoder already failed on, which is also why 409 of them have
# a blank WARD. All 452 do have a street address, and the loss is even across
# the three buckets (Retail 7.7%, Food service 6.4%, Personal services 6.6%),
# so it distorts nothing - but it is ~450 real premises on a dense map, and the
# Census geocoder is already built, cached and deterministic. Recovered in
# step 3, which makes the map step 4, exactly as in Los Angeles.
BUSINESSES_GEOCODED_CSV = DATA_PROCESSED / "businesses_geocoded.csv"
GEOCODE_CACHE_DIR = DATA_PROCESSED / "geocode_cache"

# Every raw read passes this rather than relying on pandas' default - see
# docs/data_sources.md, "Declare the source encoding". The ArcGIS download is
# written by this project's own fetch script, so it is UTF-8 by construction.
SOURCE_ENCODING = "utf-8"

# --- Raw inputs (see pipeline/washington_dc/fetch_sources.py) -------------

# 1. WMATA Rail GTFS Static. THE ONLY FEED IN THIS PROJECT BEHIND A KEY:
#    unauthenticated requests return 401. The key is the owner's, is WMATA's
#    property under §5 of the Transit Data Terms of Use, and must never enter
#    this repo - fetch_sources.py reads it from the WMATA_API_KEY environment
#    variable and refuses to run without it.
#
#    Take the `Rail GTFS Static` operation, NOT `Rail & Bus Combined GTFS
#    Static` (which carries bus routes this project never draws) and not any
#    `RT` feed. Verified 2026-09-21: 6 routes, all route_type 1, network_id
#    Metrorail, 98 parent stations all with coordinates, no bus contamination.
GTFS_URL = "https://api.wmata.com/gtfs/rail-gtfs-static.zip"
GTFS_API_KEY_ENV = "WMATA_API_KEY"

# The ten-day window. fetch_sources.py reads feed_info.txt out of the zip and
# exits rather than let a step build a map from an expired feed - the failure
# mode being a quietly stale station set, which nothing downstream would catch.
GTFS_FEED_INFO_MEMBER = "feed_info.txt"

# 2. Basic Business Licenses, DCRA/DLCP via the District's ArcGIS server.
#    278,747 rows, 76,107 Active, 61,329 Active and in the District.
BUSINESS_SERVICE_URL = (
    "https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/DCRA/FeatureServer/0"
)

# Only these columns are ever downloaded, and the omissions are the point.
# BUSINESSOWNERFIRSTNAME, BUSINESSOWNERLASTNAME, BUSINESSOWNERMIDDLENAME,
# AGENTFIRSTNAME, AGENTLASTNAME, AGENTMIDDLENAME, AGENTENTITY and
# BILLINGADDRESS all exist in this layer and are populated on tens of
# thousands of rows. They are people's names and their mailing addresses, so
# they are excluded at the download boundary rather than dropped later - the
# same discipline Boston's SQL uses. step 2 asserts they never arrive.
BUSINESS_OUT_FIELDS = (
    "OBJECTID", "CUSTOMERNUMBER", "LICENSESTATUS", "BUSINESSACTIVITY",
    "CATEGORYSERVICETYPE", "ENTITYNAME", "ENTITYTRADENAME", "ENTITYTYPE",
    "PRIMARYACTIVITYFLAG", "PREMISEADDRESS", "PREMISEINDC", "WARD",
    "MAR_ID", "SSL", "X_COORDINATE", "Y_COORDINATE",
)

# Columns that must never appear in any D.C. dataframe. Asserted in step 2.
FORBIDDEN_COLUMNS = (
    "BUSINESSOWNERFIRSTNAME", "BUSINESSOWNERLASTNAME",
    "BUSINESSOWNERMIDDLENAME", "AGENTFIRSTNAME", "AGENTLASTNAME",
    "AGENTMIDDLENAME", "AGENTENTITY", "BILLINGADDRESS",
)

# Scope, applied server-side at download.
#
# PREMISEINDC = 'Yes' (61,329 rows), NOT `WARD`. WARD is null on 16,806 rows
# and mixes "Ward 2" with "2", so it cannot carry the scope filter - though it
# is still downloaded, because it is a useful cross-check.
BUSINESS_WHERE_ACTIVE = "LICENSESTATUS='Active' AND PREMISEINDC='Yes'"

# The residential rentals, dropped at download. 37,195 of the 61,329 in-District
# active rows - 61% - are somebody's home being let out: One Family Rental
# 25,557, Apartment 6,081, Two Family Rental 2,558, Short Term Rental 2,196,
# Vacation Rental 803. This is the Philadelphia pattern, where 79% of the
# register was landlord registrations, and the reason a raw row count means
# nothing until the distribution is read.
#
# Lodging (Hotel, Inn and Motel, Bed and Breakfast, Rooming House, Boarding
# House) is NOT excluded here - it is excluded by the taxonomy instead, so that
# step 2 prints it as a category decision rather than hiding it in a URL.
BUSINESS_RENTAL_ACTIVITIES = (
    "One Family Rental", "Apartment", "Two Family Rental",
    "Short Term Rental", "Vacation Rental",
)

# 3. DC Boundary, layer 10 of the District's administrative-boundaries service:
#    a single clean polygon. Only ONE station is even arguably marginal
#    (Southern Av, 40.1 m outside), and the next two are 111 m and 130 m out,
#    so no multi-jurisdiction layer is needed to disambiguate - the contrast
#    with Boston, where four stations sat within 60 m of the line and a MassGIS
#    town layer had to name them.
BOUNDARY_SERVICE_URL = (
    "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/"
    "Administrative_Other_Boundaries_WebMercator/MapServer/10"
)

# 4. Census TIGERweb state polygons, for NAMING the excluded stations rather
#    than only counting them. 58 of 98 Metrorail stations are outside the
#    District - the second-largest station exclusion in the project after San
#    Diego's - and at that scale it has to be citable, as San Diego's 16 and Los
#    Angeles' 54 are. D.C.'s own boundary layer can say "outside" and nothing
#    more, so this adds the one fact a reader needs: Maryland or Virginia.
#
#    Three polygons only, requested by name. Census TIGER products are US
#    federal government works and carry no copyright.
STATES_SERVICE_URL = (
    "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
    "State_County/MapServer/0"
)
STATES_WHERE = "NAME IN ('Maryland', 'Virginia', 'District of Columbia')"
STATES_NAME_FIELD = "NAME"

GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESS_CSV = DATA_RAW / "basic_business_licenses.csv"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
STATES_GEOJSON = DATA_RAW / "states.geojson"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 18N: the longitude (~-77.02) falls in the -78 to -72 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32618"

# The CRS the register's own X_COORDINATE/Y_COORDINATE are in: NAD83 / Maryland
# state plane, METRES (not the US-survey-feet variant Boston's sources use).
# Verified 2026-09-21 by transformation rather than assumed - it places 312
# Pennsylvania Ave SE at (38.88715, -77.00153). Note this is a third CRS,
# distinct from both of the above.
SOURCE_XY_CRS = "EPSG:26985"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# WMATA Metrorail, by route_id in its own feed. Six lines, one group each -
# none of them branches, so none needs Boston's or Philadelphia's grouping.
# There is no commuter rail here to exclude: MARC and VRE are separate
# agencies with separate feeds, and the D.C. Streetcar is a single 2.4 km line
# that WMATA does not publish.
ROUTE_GROUPS = {
    "Red": ["RED"],
    "Blue": ["BLUE"],
    "Green": ["GREEN"],
    "Yellow": ["YELLOW"],
    "Orange": ["ORANGE"],
    "Silver": ["SILVER"],
}

# group -> (real public name, colour).
#
# ALL SIX ARE WMATA'S OWN route_color VALUES, exactly as the feed publishes
# them. Here the colour IS the line's name - drawing the Red Line in anything
# but red would be actively misleading, which is not true of San Francisco's
# lettered Muni lines or Miami's numbered ones. Measured against the three
# business-bucket colours in CIE76 Delta-E before accepting them: the closest
# pair is Blue vs Retail pins at 26.0, and Boston already ships tighter pairs
# (its Green is 20.1 from Personal services, its Red 21.4 from Food service)
# and verified clean in the browser.
#
# THE SILVER LINE IS WHERE THIS GOT DECIDED TWICE, and the second measurement
# is the one that counts. WMATA's #919D9D is a grey line, and against the LIGHT
# basemap it is the weakest colour here: Delta-E 31.4 from OSM's land fill,
# 36.5 from its road fill, 22.0 from its unpaved-track fill. So it was darkened
# to #5F6A6A, which lifts those to 51.0 / 56.3 / 41.0 - the treatment New
# York's Staten Island Railway and Boston's Mattapan Trolley already carry.
#
# That measurement was against the wrong basemap. This map OPENS IN DARK MODE,
# where map_common.py does not invert the line strokes but brightens them
# (`brightness(1.55) saturate(0.9)`) while inverting the tiles underneath. Both
# sides of the comparison move, and in opposite directions:
#
#                        dark mode (default)    light mode (the toggle)
#   #919D9D official          75.4                    22.0
#   #5F6A6A darkened          47.2                    41.0
#   for scale: Blue           81.7                    54.3
#
# Darkening therefore made the Silver Line the worst-contrast line in the city
# in the mode every reader sees first, to fix the mode they have to ask for -
# and in the render it was untraceable, legend swatch included. A dozen
# hue-shifted slates were measured too; the ones that beat #5F6A6A's worst case
# did it by drifting towards the Blue Line's hue (Delta-E 30.7 from Blue against
# the official colour's 42.0), which trades one confusion for a worse one.
#
# So the published colour stands, and the residual is recorded honestly rather
# than engineered around: in LIGHT mode the Silver Line is harder to trace than
# the other five. Its worst case there is against OSM's unpaved-track fill,
# which is nearly absent from an urban view; against land and road fill it is
# 31.4 and 36.5.
LINE_NAMES = {
    "Red": ("Red Line", "#C80F2D"),
    "Blue": ("Blue Line", "#009CDE"),
    "Green": ("Green Line", "#00B140"),
    "Yellow": ("Yellow Line", "#FFD100"),
    "Orange": ("Orange Line", "#ED8B00"),
    "Silver": ("Silver Line", "#919D9D"),
}

LINE_LABEL_ENDS = {}

# One representative shape per line, chosen from real trip counts - but with a
# wrinkle the other cities do not have. WMATA publishes 26 to 101 shapes per
# route (short turns, single-tracking variants, both directions), so "the
# most-used shape" could easily have been a partial run: the Yellow Line's
# second-most-used shape stops at Mt Vernon Square, nine stations short of
# Greenbelt. Each of these is the most-used shape AMONG those serving the
# route's full stop count, checked rather than assumed.
LINE_SHAPES = {
    "Red": ("RRED_10",),      # Shady Grove <-> Glenmont, 27 stops
    "Blue": ("RBLU_58",),     # Franconia-Springfield <-> Downtown Largo, 28
    "Green": ("RGRN_103",),   # Branch Ave <-> Greenbelt, 21
    "Yellow": ("RYEL_135",),  # Huntington <-> Greenbelt, 22
    "Orange": ("RORG_174",),  # Vienna <-> New Carrollton, 26
    "Silver": ("RSLV_257",),  # Ashburn <-> New Carrollton, 34
}

# No thinning. Metrorail is entirely grade-separated heavy rail with no
# street-running segment anywhere, which is San Diego's and New York's shape
# rather than San Francisco's - and step1_stations.py measures the in-city
# spacing and prints it, so this stays a finding rather than an assumption.
THINNED_GROUPS = frozenset()
STATION_SPACING_MILES = 0.5
SUBWAY_STATION_NAMES = frozenset()

# GTFS stop names need no surgery here: `parent_station` is populated on all
# 125 platforms, so the 98 stations collapse cleanly, and no parent name
# carries a direction or platform suffix.
#
# NOTHING IS STRIPPED, deliberately. "Union Station" and "Metro Center" are two
# of the 98 names, and Boston's bug was a pattern that removed a trailing
# " Station" and turned "North Station" into "North". A station's name is its
# name.
STATION_SUFFIX_PATTERN = None
STATION_NAME_ALIASES = {}

# Gate 3: WMATA's own station list on each line's page, keyed as ROUTE_GROUPS
# and counted over every station the line's trips serve, before the District
# cut. Silver's 39 is both its branches since the June 2025 split (Ashburn to
# Downtown Largo and to New Carrollton), as WMATA's page lists them.
OPERATOR_STATION_COUNTS = {
    "Red": 27,
    # WMATA lists 28 (Franconia-Springfield to Downtown Largo). The cached feed
    # (2026-09-15 to 09-25) also runs Blue trains to Huntington, through
    # Eisenhower Av, on the weekend service ids 23_R and 27_R (Sat 19/26 and
    # Sun 20/27 September): weekend planned work. 28 + those 2 = 30.
    "Blue": 30,
    "Green": 21,
    "Yellow": 22,
    "Orange": 26,
    "Silver": 39,
}
OPERATOR_COUNTS_SOURCE = ("WMATA 'Rail Line Stations' pages, "
                          "https://www.wmata.com/ridertools/line/<colour> for "
                          "all six lines (read 2026-10-01)")

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "dc_businessactivity"

RAW_CLASSIFICATION_COLUMN = "BUSINESSACTIVITY"

# The premises key. MAR_ID is the District's Master Address Repository
# identifier - a real address id rather than address text, which is better than
# anything Boston or Miami had. It is not unique on its own (a mall, an office
# building and a market hall each hold many licensees at one MAR_ID), so the
# key pairs it with the licensee: CUSTOMERNUMBER is the register's own
# per-licensee identifier, and one licensee holding three licence types at one
# address is exactly the duplicate this collapses.
PREMISES_KEY = ["CUSTOMERNUMBER", "MAR_ID"]

# Sanity bounds for coordinates: the District plus a margin. The business
# register is District-only, and unlike Boston's the transit network's
# out-of-District reach does not matter here, because no station outside the
# boundary is kept.
DC_BBOX = {
    "lat_min": 38.78,
    "lat_max": 39.01,
    "lon_min": -77.13,
    "lon_max": -76.89,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3600162069)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {
    "United Brick Corporation Brick Company": "a registered historic site with its own article (the brick complex), not a company",
}
PLACE_DROPPED = {
    "relation/7945929": "'L'Enfant Plaza (Blue/Orange/Silver)', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/67260444": "'Building 101', a single building's own way, named for the building",
    "way/67260470": "'Building 108', a single building's own way, named for the building",
    "way/67260361": "'Building 176', a single building's own way, named for the building",
    "way/67260425": "'Building 201', a single building's own way, named for the building",
    "way/67260293": "'Building 212', a single building's own way, named for the building",
    "way/1134277416": "'Building 44', a single building's own way, named for the building",
    "way/67260354": "'Building 58', a single building's own way, named for the building",
    "way/67260112": "'Building 59', a single building's own way, named for the building",
    "way/1138154744": "'Band Hall', a single building's own way, named for the building",
    "way/55331749": "'Barrack Building', a single building's own way, named for the building",
    "way/67260519": "'Commandant's Office', a single building's own way, named for the building",
    "way/67266273": "'Chapel two annex', a description standing in for a name (owner, 2026-10-13)",
    "way/1133990742": "'Marine Railway', a type word standing in for a name (owner, 2026-10-13)",
    "way/67260466": "'Quarters C', a housing estate's own way, named for the estate",
    "way/67260151": "'Quarters D', a housing estate's own way, named for the estate",
    "way/67260590": "'Quarters E', a housing estate's own way, named for the estate",
    "way/67260417": "'Quarters F', a housing estate's own way, named for the estate",
    "way/67260190": "'Quarters G', a housing estate's own way, named for the estate",
    "relation/15348308": "'Quarters H', a housing estate's own way, named for the estate",
    "way/67260412": "'Quarters L', a housing estate's own way, named for the estate",
    "relation/15348309": "'Quarters N', a housing estate's own way, named for the estate",
    "way/67260316": "'Quarters O', a housing estate's own way, named for the estate",
    "way/67260372": "'Quarters R', a housing estate's own way, named for the estate",
    "way/67260144": "'Quarters V', a housing estate's own way, named for the estate",
    "way/55331764": "'Lenox School lofts', a home",
    "way/66693632": "'Phillips School', a home",
    "node/367142191": "'Convent Carmelite Sisters', a religious residence",
    "node/367142188": "'Immaculate Conception Convent', a religious residence",
    "node/367142185": "'Notre Dame Convent', a religious residence",
    "way/297739331": "'Marian Scholasticate', a religious residence",
    "node/13186828250": "'DC General Hospital (historic)', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/13186767884": "'Eastern Methodist Cemetery (historic)', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/367143953": "'The Seven Buildings', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/367142907": "'MacArthur Theater', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "way/234100086": "'Reservoir District Construction', a description standing in for a name (owner, 2026-10-13)",
    "way/893887248": "'Emancipation Hall', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "node/13852079385": "'Supreme Council-the Hse-jacob', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1131619243": "'TURNING HEARTS CHURCH;ST THOMAS MORE CHURCH', a type or model word standing in for a name (owner, 2026-10-13)",
    "node/9525437752": "'Corinthian Capital', a religious residence",
    "node/11583132469": "'The Chinese Community Church', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "relation/5396194": "'Washington', the city boundary's center as a second place row beside the city's own: a duplicate (owner, 2026-10-13)",
    "node/10568796370": "'Anna J. Cooper Circle', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/10568811905": "'Grant Circle', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/105823176": "'Entrance 4', a description standing in for a name (owner, 2026-10-13)",
    "way/1176510923": "'Entrance 4', a description standing in for a name (owner, 2026-10-13)",
    "way/238487269": "'Entry Road', a description standing in for a name (owner, 2026-10-13)",
    "way/384199753": "'Entry Road', a description standing in for a name (owner, 2026-10-13)",
    "way/484888848": "'Entry Road', a description standing in for a name (owner, 2026-10-13)",
    "way/859164329": "'Entry Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1527572265": "'Entry Road', a description standing in for a name (owner, 2026-10-13)",
    "way/50712483": "'Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/405691441": "'Support Building Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/50431280": "'Virginia Avenue Northwest Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/246556623": "'Robert Clifton Weaver', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/627181822": "'Robert Clifton Weaver', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/120907204": "'Springhouse Roadw', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/232949249": "'Capital Beltway (Local)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/899962512": "'Capital Beltway (Local)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/899962515": "'Capital Beltway (Local)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1230739478": "'Capital Beltway (Local)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/232949248": "'Capital Beltway (Thru)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/899962513": "'Capital Beltway (Thru)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/899962514": "'Capital Beltway (Thru)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1230739479": "'Capital Beltway (Thru)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/49077527": "'395 Express Lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/49077542": "'395 Express Lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/121980301": "'395 Express Lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/374376244": "'395 Express Lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/1182629696": "'395 Express Lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/1182629699": "'395 Express Lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/1182629701": "'395 Express Lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/1176510913": "'McDonough Bus Turnaround', not a street: another kind of object indexed as one",
    "way/1176510915": "'McDonough Bus Turnaround', not a street: another kind of object indexed as one",
    "way/1112147248": "'Chain Bridge Ramp', a ramp described, not a street's name",
    "way/130225881": "'Navy and Marine Memorial Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/288513981": "'Navy and Marine Memorial Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/288513982": "'Navy and Marine Memorial Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1031846179": "'Navy and Marine Memorial Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1492384120": "'Navy and Marine Memorial Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/375442224": "'Icre Cream Access Trail', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/375441675": "'Pliushsh Trail', a glitched name, not repaired (owner, 2026-10-13)",
    "way/102417253": "'Museum Foot Trail', a description standing in for a name (owner, 2026-10-13)",
    "way/102639686": "'Picnic Loop Road', a description standing in for a name (owner, 2026-10-13)",
    "way/102675772": "'Garden Loop Road', a description standing in for a name (owner, 2026-10-13)",
    "way/375443010": "'Garden Loop Road', a description standing in for a name (owner, 2026-10-13)",
    "way/457558491": "'Scale Gate Road', a description standing in for a name (owner, 2026-10-13)",
    "way/457558493": "'Scale Gate Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1347780259": "'Scale Gate Road', a description standing in for a name (owner, 2026-10-13)",
    "way/50758306": "'Scale Gate Road Northeast', a description standing in for a name (owner, 2026-10-13)",
    "way/50758311": "'Scale Gate Road Northeast', a description standing in for a name (owner, 2026-10-13)",
    "way/457558482": "'Scale Gate Road Northeast', a description standing in for a name (owner, 2026-10-13)",
    "way/457558485": "'Scale Gate Road Northeast', a description standing in for a name (owner, 2026-10-13)",
    "way/1050915725": "'20th Street Southeast', not built: highway=proposed",
    "way/1050915726": "'20th Street Southeast', not built: highway=proposed",
    "way/1050915729": "'20th Street Southeast', not built: highway=proposed",
    "way/1050915722": "'Burke Street Southeast', not built: highway=proposed",
    "way/1050915723": "'C Street Southeast', not built: highway=proposed",
    "way/1050915731": "'Massachusetts Avenue Southeast', not built: highway=proposed",
    "way/708677189": "'Potomac Avenue Southeast', not built: highway=proposed",
    "way/904354637": "'Library of Congress Passage', not a street: an indoor corridor indexed as one",
    "way/1043291917": "'15th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/49298978": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931247285": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931247289": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931247290": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931247291": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931247298": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931247300": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931247301": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931247302": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931247303": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931247304": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1075230958": "'17th Street Southeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1095474058": "'19th Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1075234303": "'19th Street Southeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469854805": "'19th Street Southeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469854806": "'19th Street Southeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1352158751": "'19th st NE protected bike lane', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469816274": "'19th st NE protected bike lane', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469816275": "'19th st NE protected bike lane', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469816276": "'19th st NE protected bike lane', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469816277": "'19th st NE protected bike lane', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/633517785": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931274364": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931274365": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931274367": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931274368": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931274369": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931274370": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1022778364": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1336959835": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1396718473": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1396718474": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1396834194": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1403226956": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1403226957": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1409326235": "'1st Street Northeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/977379780": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/977379781": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238608": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238609": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238610": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238611": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238615": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238616": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238617": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238618": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238619": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238620": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238621": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238622": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238623": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238624": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238625": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238626": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238630": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238631": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315350464": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315350465": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315350466": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315350467": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529480": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529481": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529482": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529483": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529490": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529491": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529492": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529493": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529538": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529539": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529540": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529541": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529542": "'1st Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/994133429": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1193466108": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771831": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771834": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771835": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771836": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771837": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771839": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771840": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771841": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771842": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771843": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771844": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771845": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771846": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771851": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771852": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771853": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771854": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771855": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771856": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771857": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771858": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771860": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771861": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771863": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771864": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771865": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771866": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771867": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314771868": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1329680039": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1329680040": "'20th Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1112169574": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764603": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764604": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764605": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764606": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764607": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764608": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764609": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764610": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764611": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764612": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764618": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764619": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1329682645": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1329710595": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1329710596": "'21st Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/710054725": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667653": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667654": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667655": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667656": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667657": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667659": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667660": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667661": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667662": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667663": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667664": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/992781620": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315750098": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315750099": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315750105": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315754918": "'2nd Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/359869182": "'41st Street NE Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1525647522": "'41st Street NE Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/807874686": "'4th Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931282968": "'4th Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1248943467": "'4th Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584547": "'4th Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584550": "'4th Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584551": "'4th Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584552": "'4th Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584553": "'4th Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584554": "'4th Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584563": "'4th Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934527261": "'4th Street Northwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934531382": "'4th Street Northwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934531383": "'4th Street Northwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934531384": "'4th Street Northwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934531385": "'4th Street Northwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934531386": "'4th Street Northwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934531388": "'4th Street Northwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1215599098": "'4th Street Northwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1363190224": "'4th Street Northwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1363190225": "'4th Street Northwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1248943502": "'4th Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584532": "'4th Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584533": "'4th Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584535": "'4th Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584536": "'4th Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584537": "'4th Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/845188203": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934531387": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934531389": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533673": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533674": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533675": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533676": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533677": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533678": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533679": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533680": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533681": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533682": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533683": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533684": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934533685": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/987859216": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/987859217": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1101853778": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1101853779": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1289708777": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1289708778": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295096935": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295096936": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109286": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109287": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109288": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109289": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109290": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109291": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109292": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109293": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109294": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109295": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109296": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109297": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109298": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109299": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109300": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109301": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109302": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109303": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109304": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109305": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109306": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109307": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109308": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109309": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109310": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109311": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109312": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109313": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109314": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109315": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109316": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109317": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109318": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109319": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109320": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109321": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109322": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109323": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109324": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109325": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295109326": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295119966": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1295119968": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1324851546": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1333495849": "'4th Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1086571836": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1097434484": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1097434485": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1156851690": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1156851692": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1156851693": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1156851694": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1156851695": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1156851696": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1156851697": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1156851698": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1388084394": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1388084395": "'9th Street NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1061126844": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1063796061": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1193466107": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761745": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761746": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761747": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761748": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761749": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761750": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761751": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761752": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761753": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761754": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761756": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761757": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761761": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761762": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761766": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761767": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761769": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761770": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761772": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761773": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761774": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761775": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761778": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761779": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761781": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761782": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761783": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761784": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761785": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761786": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761787": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761788": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761789": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314761790": "'G Street Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/703923692": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1075240578": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1134681355": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1134681357": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1134681358": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1134681360": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1134681361": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1134681362": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1134681365": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1208595688": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529517": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529518": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529519": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529520": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529521": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529522": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529523": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529524": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529525": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529526": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529527": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529543": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529544": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529547": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529548": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529549": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529551": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1330991100": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1330991106": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1471730237": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1471730238": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1497379567": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1497379569": "'I Street Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/323320155": "'M Street Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1134677463": "'M Street Southeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1337734278": "'M Street Southeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1044427353": "'Maine Avenue SW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825654": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825656": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825658": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825660": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825661": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825662": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825663": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825664": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825665": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825666": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825667": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825668": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305825669": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305836908": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305836911": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305836912": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305836913": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305836914": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305836915": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305836916": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305836917": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305836918": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305836919": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305837417": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1305837418": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1329456825": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1329456826": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1329489633": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1329490751": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1329655813": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1329655814": "'Minnesota Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1198436010": "'Morse Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584560": "'Morse Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315584562": "'Morse Street Northeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1004612316": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1004612317": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1134681359": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1134681363": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1134681364": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1137669747": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1137669748": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1137669749": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238643": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315238644": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315516227": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315516228": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315516229": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315516230": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529486": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529487": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529488": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529489": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529500": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529501": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529502": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529503": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529505": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529506": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529507": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529508": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529509": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529510": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529511": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315529512": "'New Jersey Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1103983081": "'New Mexico Avenue NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667652": "'P Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1046062197": "'P Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1046062198": "'P Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1101853776": "'P Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315754913": "'P Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315754914": "'P Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315754915": "'P Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1355230958": "'Penn Avenue Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1355230959": "'Penn Avenue Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1355230960": "'Penn Avenue Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/194820208": "'Pennsylvania Avenue Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/910190948": "'Pennsylvania Avenue Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/910190954": "'Pennsylvania Avenue Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934125950": "'Pennsylvania Avenue Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/992781624": "'Pennsylvania Avenue Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/992781625": "'Pennsylvania Avenue Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/992781626": "'Pennsylvania Avenue Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1215423876": "'Pennsylvania Avenue Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1215423877": "'Pennsylvania Avenue Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1215423879": "'Pennsylvania Avenue Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1215423882": "'Pennsylvania Avenue Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1215599102": "'Pennsylvania Avenue Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/488788119": "'Pennsylvania Avenue Sidepath', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1075234636": "'Potomac Avenue Southeast Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/710054732": "'Potomac Avenue Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931671056": "'Potomac Avenue Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931671057": "'Potomac Avenue Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931671058": "'Potomac Avenue Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931671059": "'Potomac Avenue Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/985356412": "'Potomac Avenue Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/993190313": "'Potomac Avenue Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931667658": "'R Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931671055": "'R Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315606896": "'R Street Southwest Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/381551116": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/381552108": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/381552109": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/381552110": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1355230260": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1355230262": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469844958": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469847024": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469847025": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1223261757": "'Tunlaw Road NW Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1020958895": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1056345183": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1056345184": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1056345186": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1056345188": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1058949165": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1058949169": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1063796060": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1063796062": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756412": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756413": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756414": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756418": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756419": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756423": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756424": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756425": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756426": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756427": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756428": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756439": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314756440": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759890": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759891": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759892": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759893": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759894": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759895": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759896": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759897": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759898": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759899": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759900": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759901": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759902": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759903": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759905": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759906": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759907": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759908": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759914": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759915": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759916": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759917": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759918": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759919": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759923": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759924": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759925": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759926": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314759927": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764613": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314764614": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1499644906": "'Virginia Avenue Northwest Cycletrack', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934643159": "'Virginia Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934643166": "'Virginia Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934643167": "'Virginia Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934648605": "'Virginia Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/934648610": "'Virginia Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315567780": "'Virginia Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315567781": "'Virginia Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315578829": "'Virginia Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1315578830": "'Virginia Avenue Southeast Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/231968509": "'Sacred Heart Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968487": "'Saint Anthony's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968501": "'Saint Benedict's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968495": "'Saint Bernard's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/778570551": "'Saint Catherine Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1394978890": "'Saint Cecelia's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1394978902": "'Saint Cyprian's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1394978894": "'Saint Dominic's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1394978903": "'Saint Elizabeth's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1394978904": "'Saint Francis' Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968492": "'Saint Ignatius' Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968512": "'Saint James Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968498": "'Saint James' Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1394978895": "'Saint Jerome's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/680961332": "'Saint John's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968490": "'Saint Mary's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968507": "'Saint Mary's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968491": "'Saint Matthew's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968499": "'Saint Matthew's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968514": "'Saint Matthew's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/127292258": "'Saint Michael's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1394978892": "'Saint Patrick's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968503": "'Saint Paul's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968516": "'Saint Peter's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968486": "'Holy Name Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1217675336": "'Holy Nativity Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968488": "'Immaculate Conception Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/231968489": "'Olivet Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1394978899": "'Olivet Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1394978900": "'Olivet Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/191053766": "'Church House Lane', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/67829158": "'Number One Observatory Circle', a home with no sign of visiting, whatever its article (owner, 2026-10-13)",
    "way/295652629": "'Tregaron Estate', a home with no sign of visiting, whatever its article (owner, 2026-10-13)",
    "way/1361163002": "'Eighteen Hundred Block Park Road Buildings', a home with no sign of visiting, whatever its article (owner, 2026-10-13)",
    "node/367141563": "'Towpath Row', a home with no sign of visiting, whatever its article (owner, 2026-10-13)",
}
