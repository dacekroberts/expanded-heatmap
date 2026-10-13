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
# Read and kept, 2026-10-13 (the flag check of wave 1; the owner's ruling
# to settle unsure rows by the existing rules). None carries a leak word,
# so check E takes no PLACE_REVIEWED entry for it; the reason is kept here.
#   node/367141729 'Twin Oaks': tourism=attraction with a Wikidata entry: a home tagged an attraction is kept
PLACE_REVIEWED = {
    "United Brick Corporation Brick Company": "a registered historic site with its own article (the brick complex), not a company",
}
PLACE_DROPPED = {
    "way/1131619243": "'TURNING HEARTS CHURCH;ST THOMAS MORE CHURCH', a type or model word standing in for a name (owner, 2026-10-13)",
    "way/67266273": "'Chapel two annex', a description standing in for a name (owner, 2026-10-13)",
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
    "node/9525437752": "'Corinthian Capital', a religious residence",
    "node/11583132469": "'The Chinese Community Church', a duplicate beside the same thing's own row (owner, 2026-10-13)",
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
    "way/931247300": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/931247301": "'15th Street Northwest Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/381551116": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/381552108": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/381552109": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/381552110": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1355230260": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1355230262": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469844958": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469847024": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469847025": "'Suitland Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
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
    "way/67260451": "'Commander, Navy Installations Command', non-public facility: an office title as a building's name: a command's title on a Navy Yard building; like Tacoma's job-title drop, by id (flag check, 2026-10-13)",
    "node/3360867538": "'Moishe House', a communal residence tagged a place of worship, no article: a home (flag check, settled by the existing rules, 2026-10-13)",
    "way/640685801": "'Grove 24 Trail', description: an informal trail under a grove number (flag check, 2026-10-13)",
    "way/199920712": "'Leavey Center Entrance bridge', description: a campus footbridge named for a building (flag check, 2026-10-13)",
    "way/199920714": "'Leavey Center Entrance bridge', description: a campus footbridge named for a building (flag check, 2026-10-13)",
}

# Public art kept by the owner's word against the article rule (place_index,
# PLACE_KEPT; owner, 2026-10-13). Each is a known work the Wikidata lookup
# cannot admit; DECISIONS.md of that date lists the works left out.
PLACE_KEPT = {
    "node/358960331": "'Three Servicemen Statue', a known work the article rule drops for want of an article of its own (owner, 2026-10-13)",
}
