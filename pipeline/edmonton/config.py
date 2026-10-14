"""Edmonton-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "edmonton" / "raw"
DATA_PROCESSED = ROOT / "data" / "edmonton" / "processed"
OUTPUTS = ROOT / "outputs" / "edmonton"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities). Edmonton's is written but EMPTY: all 30 stations are
# in-city, so the boundary is a check rather than a filter.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
# Stops a rail trip touches that no passenger can board at - see
# NON_REVENUE_STOPS_EXPECTED below. Recorded for the same reason as the
# excluded stations: a silent drop is indistinguishable from a bug.
NON_REVENUE_STOPS_CSV = OUTPUTS / "non_revenue_stops.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all public. The exact download commands:
#
#   GTFS - the AGENCY feed, not the Mobility Database mirror and NOT the eight
#   individual Socrata tables. This URL is not published as a link anywhere
#   readable; it comes from the `accessPoints.DOWNLOAD` field of the catalogue's
#   href-type dataset `urjq-fvmq`, which is why two guessed URLs 404'd during
#   the Canada profile:
#     curl -sL "https://gtfs.edmonton.ca/TMGTFSRealTimeWebService/GTFS/gtfs.zip" -o gtfs.zip
#
#   Business licences - Socrata `qhi4-bdpu`, no server-side filter (the whole
#   file is 43,672 rows; step 2 does the filtering, so the raw capture stays a
#   faithful snapshot):
#     curl -sL "https://data.edmonton.ca/resource/qhi4-bdpu.csv?\$limit=60000" -o business_licences.csv
#
#   Boundary - Socrata `qqvh-dp5m`, "Corporate Boundary (current)". FOUR
#   datasets on this portal are named some variant of "Corporate Boundary" and
#   they are NOT the same polygon: `qqvh-dp5m` and `a62q-eaea` give 783.1 km2,
#   `3trg-p57p` and `gtx5-kghy` give 699.8 km2. The 83.3 km2 difference is
#   Edmonton's 2019 annexation from Leduc County, so the smaller pair is stale.
#   This is the Calgary two-boundary trap with four layers instead of two:
#     curl -sL "https://data.edmonton.ca/api/geospatial/qqvh-dp5m?method=export&format=GeoJSON" -o city_boundary.geojson
GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "business_licences.csv"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"

GTFS_URL = "https://gtfs.edmonton.ca/TMGTFSRealTimeWebService/GTFS/gtfs.zip"
BUSINESS_URL = "https://data.edmonton.ca/resource/qhi4-bdpu.csv"
BUSINESS_LIMIT = 60000          # 43,672 rows on 2026-09-21; headroom for growth
BUSINESS_VIEW = "qhi4-bdpu"     # for the updatedAt / licence probe
CITY_BOUNDARY_URL = ("https://data.edmonton.ca/api/geospatial/qqvh-dp5m"
                     "?method=export&format=GeoJSON")

SOURCE_ENCODING = "utf-8"

# Unlike Vancouver's register (`PhoneNumber`) and Los Angeles' (`owner_name`),
# Edmonton publishes exactly ONE name column and it is the business's. There is
# no registrant, owner or contact field to avoid loading, so Edmonton's privacy
# position is STRUCTURAL: no pin CAN be a person's name, because the register
# holds none to fall back to. Asserted at download rather than assumed, so the
# claim stops being true loudly if the schema ever changes.
FORBIDDEN_COLUMNS = ("owner_name", "owner", "registrant", "registrant_name",
                     "licensee", "licence_holder", "license_holder",
                     "contact_name", "phone", "phonenumber", "email")

# Edmonton's GTFS carries a real validity window, which Calgary's and Toronto's
# do not - and checking it is the whole reason the agency feed is used instead
# of the catalogue mirror or the Socrata tables. Both of those are expired.
GTFS_CHECK_FEED_WINDOW = True

# The boundary layer this project must NOT use, kept so the choice above reads
# as a decision rather than an accident.
STALE_BOUNDARY_IDS = ("3trg-p57p", "gtx5-kghy")
BOUNDARY_AREA_KM2_MIN = 750.0   # the current polygon is 783.1; the stale one 699.8

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 12N: the longitude (~-113.49) falls in the -114 to -108 band.
# Derived per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32612"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# Edmonton's LRT is the whole of its urban rail: three lines, all at
# route_type 0, all inside the city. Matched on route_id, which here is stable
# and self-describing ("021R") rather than versioned as Calgary's is - but
# ROUTE_SHORT_NAMES is recorded too because the short names are what riders see
# and what the legend uses.
ROUTE_IDS = ["021R", "022R", "023R"]
ROUTE_SHORT_NAMES = ["Capital", "Metro", "Valley"]
LINE_NAMES = {
    "021R": "Capital Line",
    "022R": "Metro Line",
    "023R": "Valley Line",
}

# COLOURS ARE THIS PROJECT'S OWN, and the reason is MEASURED rather than
# asserted. ETS signs its lines blue / red / green (`route_color` 0081BC,
# FF0000, 008000) and two of those three collide with the business-category
# palette this map already spends: Capital's blue sits Delta-E 23.9 from
# Retail's #2a78d6, and Valley's green 37.2 from Personal services' #1baf7a.
# The project's own working threshold is ~45 - the figure behind #C2185B's
# selection (49.6) and #FBB878's (44.8) in map_common.
#
# So each line keeps ETS's HUE IDENTITY - Capital reads blue, Metro red, Valley
# green - shifted in lightness until it clears the category colours. Measured
# over a grid of candidates, the best achievable combination is:
#
#            vs the 3 category colours      vs the other two lines
#   Capital  #082F49   min Delta-E 49.2     106.7 / 57.0
#   Metro    #CC0000   min Delta-E 49.3     106.7 / 100.7
#   Valley   #365314   min Delta-E 44.2      57.0 / 100.7
#
# **Valley at 44.2 against Personal services is the binding constraint and is
# marginally under the ~45 figure.** Green-against-green is intrinsically the
# hard pair, and the grid has no combination that clears it without abandoning
# green for the Valley Line altogether. Recognisability was preferred to the
# last 0.8, and it is recorded here so the choice reads as a tradeoff rather
# than an oversight. Dark mode brightens 4px strokes 1.55x, so the dark
# Capital and Valley colours lighten there rather than going muddy.
#
# This is the documented fallback, not a departure: see the add-city skill
# ("use a palette of your own that stays distinct from the business-category
# colours") and Miami, which did the same for the same reason.
#
# **COLOUR SEPARATION IS AN INTRA-CITY CONSTRAINT ONLY, and deliberately so.**
# Every figure above compares a line against the OTHER LINES ON THIS MAP and
# against the category pin colours that map spends. It does not compare against
# any other city's lines, and it should not: each city renders its own map, with
# its own legend and its own on-map labels, so two cities sharing a colour can
# never be confused with one another. `#CC0000` here is essentially Calgary's
# Red Line red, and that is FINE - reuse across cities is expected and costs
# nothing. Trying to keep every line in every city distinct would exhaust the
# usable palette long before the city list does, and would push later cities
# into colours that read badly against their own pins, which is the constraint
# that actually matters. Only the macro map shows all cities at once, and it
# draws city dots, not transit lines.
LINE_COLOURS = {
    "021R": "#082F49",   # Capital Line - ETS signs it blue
    "022R": "#CC0000",   # Metro Line   - ETS signs it red; = Calgary's Red, fine
    "023R": "#365314",   # Valley Line  - ETS signs it green
}

# ONE shape per line, and for TWO of the three it is the most-used trip shape.
#
# **The Metro Line is the exception, and taking its mode would have drawn only
# half the line.** Most Metro trips turn back in the north, so its most-used
# shape (`022R-82-South`, 714 trips, 221 points) spans latitude 53.5180 to
# 53.5664 - NAIT down to about Health Sciences. But the Metro Line genuinely
# serves Century Park at 53.4572, and step 1 lists 14 Metro stations including
# Southgate, University and South Campus. Only `022R-38-North` (156 trips, 358
# points, 53.4572 to 53.5673) draws the whole of it.
#
# So the rule here is EXTENT, not trip count, where the two disagree - the same
# problem Miami's branching Metrorail had. Its southern half shares track with
# the Capital Line, which is drawn too; overlapping trunks are normal (Calgary's
# 7 Avenue mall is the same) and the labels sit at each line's own tail.
#
# SUPERSEDED - the owner's call (2026-10-01): follow ETS's PUBLISHED line.
# ETS publishes the Metro Line as NAIT/Blatchford Market - Health Sciences/
# Jubilee, 10 stations (edmonton.ca/ets/lrt-station-locations); only weekend
# trips (the Saturday and Sunday `022R-38-North`/`39-South`/`40-South`, 308 of
# 1,920 in feed 20260911-20261128) run on to Century Park. So the Metro Line
# is drawn NAIT - Health Sciences, from `022R-27-North` (621 weekday trips,
# 224 points, 53.5180 to 53.5673): the published extent, and the north-bound
# shape, which reaches the NAIT platforms (53.5669) where the mode
# (`022R-82-South`, 714 trips) stops 55 m short of them at 53.5664. Both run
# into the Health Sciences tail track (53.5180), 250 m past the station, under
# the Capital Line. McKernan/Belgravia, South Campus, Southgate and Century
# Park stay on the map as Capital Line stations (LINES_LISTED_FROM_DRAWN_SHAPE).
LINE_SHAPES = {
    "021R": "021R-68-North",   # Capital,  980 trips, 314 pts, full extent
    "022R": "022R-27-North",   # Metro,    621 trips, 224 pts - ETS's published
                               # extent, NAIT - Health Sciences (owner, 2026-10-01)
    "023R": "023R-43-South",   # Valley, 1,340 trips, 308 pts, full extent
}
# Lines whose station list is the stops of their DRAWN shape's trips, not of
# every trip on the route (the owner's call above): a station a line's
# weekend trips alone reach is not listed on it. Step 1 prints what this
# removes and stops if a removed station would be left on no line.
LINES_LISTED_FROM_DRAWN_SHAPE = ("022R",)

# Which end of each line carries its label; None = automatic (the end farthest
# from the other lines). EMPTY, and that was checked rather than assumed.
#
# The Metro Line's automatic label lands at its NAIT end, in the busiest part
# of the map, so the alternative was rendered and measured in the browser
# instead of judged by eye (2026-09-21, when the line was drawn to Century
# Park; since 2026-10-01 its other end is Health Sciences, on the Capital
# Line's track). Total label-on-cluster overlap, at 1000x660:
#     automatic (NAIT, north)        ~905 px2, worst single 23x17
#     forced "start" (Century Park)  2,536 px2, worst single 34x21 - it lands
#                                    on the Century Park cluster stack
# So automatic wins by a factor of nearly three and is kept. The residual
# overlap is a few pixels of a label's descender over a circle's edge, and the
# labels carry a white text-shadow halo and draw above the pins, so they stay
# legible. Calgary's is empty for the same reason.
LINE_LABEL_ENDS = {}

# Platform-to-station collapse. `parent_station` is populated on ALL 65 served
# stops, so it is the first and best of the four mechanisms this project ranks
# (parent_station -> regular suffix -> direction prefix -> nothing), and no
# name munging is needed.
#
# The diagnostic that matters is nearest-neighbour SPACING, not a duplicate-name
# check - a name check passed on Calgary while its 83 "stations" were platforms
# 17 m apart. MEASURED 2026-09-21 in EPSG:32612:
#     65 served stops        median nearest neighbour   66 m  -> platforms
#     33 parent_stations     median nearest neighbour  632 m  -> stations
PLATFORMS_EXPECTED = 65
PARENT_STATIONS_EXPECTED = 33
PLATFORM_SPACING_MEDIAN_M_MAX = 150.0   # raw stops must look like platforms
STATION_SPACING_MEDIAN_M_MIN = 400.0    # collapsed stations must not

# THREE of those 33 are not stations. Every rail trip touches them, but
# `pickup_type` and `drop_off_type` are both 1 on every one of their stop_times
# - nobody can board or alight. Two are garage access points and one is a tail
# track. Every other station is boardable, so the split is unambiguous:
#     Q7020  Andrews Garage Platform   1,947 stop_times, 0 boardable
#     Q7019  DL Macdonald Platform     1,947 stop_times, 0 boardable
#     QHTT   Health Sciences Tail      1,430 stop_times, 0 boardable
# Keeping them inflated the published density figure: 2,520/33 = 76 per
# station against the real 2,445/30 = 82. No other city in this project has
# needed this check, and every one of them should have had it.
NON_REVENUE_STOPS_EXPECTED = 3
IN_CITY_STATIONS_EXPECTED = 30

# --- Gate 3: ETS's own per-line stop lists ------------------------------------
# NOT the 33 -> 30 correction above, which came from the feed's boardability
# flags; this is the check from outside the data. An interchange counts once on
# each line it serves (Churchill's Capital/Metro station and the Valley Line's
# street-level Churchill stop are two places, one on each list). All three
# lines are wholly inside Edmonton, so there is no scope split to count before.
OPERATOR_STATION_COUNTS = {
    "021R": 15,   # Capital: Clareview - Century Park
    # Metro: ETS lists 10, "from NAIT / Blatchford Market in the north to
    # Health Sciences / Jubilee in the south". Until 2026-10-01 the build
    # counted 14: ETS's own feed (20260911-20261128) runs 308 of its 1,920
    # Metro trips, all on Saturday and Sunday service_ids, on to Century
    # Park. The owner's call (2026-10-01) follows ETS's published line, so
    # the four stations past Health Sciences are listed and drawn as Capital
    # Line stations only (LINE_SHAPES, LINES_LISTED_FROM_DRAWN_SHAPE). The
    # station set is unchanged.
    "022R": 10,
    "023R": 12,   # Valley Line Southeast: 102 Street - Mill Woods (11 stops
                  # and the elevated Davies station)
}
OPERATOR_COUNTS_SOURCE = (
    "City of Edmonton / Edmonton Transit Service, 'LRT Stops and Stations' "
    "(edmonton.ca/ets/lrt-station-locations): its per-line stop selector "
    "(Capital 15, Metro 10, Valley 12) and per-line 'Travels from ... to ...' "
    "termini. Read 2026-10-01; primary."
)

# --- Business filtering ------------------------------------------------

# `licencetype` is Edmonton's own premises-or-person marker, and it is why this
# city needs no residence inference. Keeping `Commercial` (25,105 of 43,672)
# drops `Home Based` (14,114), `Non-Resident` (2,108, mobile trade) and the two
# individual-held types, `Massage Practitioner` (1,582) and `Adult Services`
# (763) - people rather than premises, the New York `Individual` distinction.
LICENCE_TYPE_COLUMN = "licencetype"
LICENCE_TYPE_KEEP = "Commercial"

# Several categories per row, `";"`-delimited: 5,340 of 25,105 carry more than
# one. Step 2 splits on this and resolves through the taxonomy's
# BUCKET_PRIORITY. Naive value_counts() on the raw column returns 1,247
# COMBINATIONS; the true vocabulary is 60 categories.
CATEGORY_DELIMITER = ";"
CATEGORIES_EXPECTED = 60

# The publisher's own privacy redaction, not a missing value: `<REDACTED FOR
# PRIVACY>` replaces the address on 4,074 rows (9.3%) overall, and on all 25
# `Health Enhancement Practitioner (Accredited)` rows. Those rows carry no
# coordinates either, so they are lost rather than suppressed - `read-licence`
# step 6b, where the publisher did the privacy work upstream.
REDACTED_ADDRESS = "<REDACTED FOR PRIVACY>"

# In-city identification. All 30 stations are inside the corporate boundary, so
# this is a check; the business rows are scoped by the boundary polygon, since
# the register is municipal and carries no city field to trust.
CITY_KEEP = "EDMONTON"

TAXONOMY_SYSTEM = "edmonton_licencecategory"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "business_licence_category"

# The dataset's real primary key, for deduplication - not the business name
# (chains share names): 25,105 Commercial rows hold 24,658 distinct ids.
PREMISES_KEY = "externalid"

NAME_COLUMN = "business_name"
ADDRESS_COLUMN = "business_address"

# The register publishes current licences rather than a term history, so there
# is no status column - but `expiry_date` is populated on every row and 71
# Commercial rows have already lapsed. Filtering on it is the active flag.
EXPIRY_COLUMN = "expiry_date"
# "Lapsed" is judged AS OF THE SNAPSHOT, not as of the day step 2 runs
# (Chicago's AS_OF_DATE model). Until 2026-09-25 step 2 compared expiry with
# today's date, so the same raw file gave a different map every time a licence
# passed its expiry - the full drift check of 2026-09-25 caught two (JUST COZY,
# JAYGO AUTO LTD., both expiring 2026-09-24). The date is the raw file's own
# download date (business_licences.csv, modified 2026-09-21); update it with
# each re-fetch.
AS_OF_DATE = "2026-09-21"

# Sanity bounds for the supplied lat/lng, tightened to the corporate boundary's
# real extent (lat 53.3374-53.7159, lon -113.7139 to -113.2715) plus a margin.
EDMONTON_BBOX = {
    "lat_min": 53.30,
    "lat_max": 53.75,
    "lon_min": -113.75,
    "lon_max": -113.23,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3602564500)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
# Read and kept, 2026-10-13 (the flag check of wave 1; the owner's ruling
# to settle unsure rows by the existing rules). None carries a leak word,
# so check E takes no PLACE_REVIEWED entry for it; the reason is kept here.
#   way/565123468 'Union Bank Inn': a heritage building with a Wikidata entry, tagged as the building: the Panama Hotel precedent
PLACE_REVIEWED = {
    "Transit Hotel": "a historic building (historic=building, Wikipedia) tagged as the building, not the business: the Panama Hotel precedent",
}
PLACE_DROPPED = {
    "way/632373455": "'Pointe Uptown Courtyard', a condominium complex's courtyard, by its own description: homes",
    "way/325217107": "'Mahamevnawa Buddhist Monastery Edmonton', a monastery tagged a place of worship, not notable: a religious residence, by id",
    "way/325035890": "'Truc Lam Monastery', a monastery tagged a place of worship, not notable: a religious residence, by id",
    "relation/15307341": "'Sisters of Our Lady of Charity', a religious order's house tagged a place of worship, not notable: a religious residence, by id",
    "way/325268748": "'Hangar 11', destroyed in a fire (end_date=2024-04-22): removed",
    "way/325267625": "'Courtyard #1', a numbered courtyard: a code and a type word, unregistered",
    "way/1216140709": "'Courtyard #2', a numbered courtyard: a code and a type word, unregistered",
    "way/325267631": "'Courtyard #3', a numbered courtyard: a code and a type word, unregistered",
    "way/325267628": "'Courtyard #4', a numbered courtyard: a code and a type word, unregistered",
    "way/325267630": "'Courtyard #5', a numbered courtyard: a code and a type word, unregistered",
    "way/325267624": "'Courtyard #6', a numbered courtyard: a code and a type word, unregistered",
    "way/325267629": "'Courtyard #7', a numbered courtyard: a code and a type word, unregistered",
    "node/5262997168": "'Jagre Ridge Golf Course hole # 15 scenic park area north of pond', a sentence describing a spot on a golf course",
    "way/544443569": "'Jagare Ridge Excercise Warm Up Park', a description of an exercise area",
    "way/1545297602": "'Future School Site', a description (a future school site) tagged a park",
    "way/320156860": "'Ellerslie RoadBaptist Church', two words glued in the name: a glitch",
    "way/322564914": "'Jesus Christ of Latter Day Saints 116 St', the name is cut short and carries an address: a glitch",
    "node/14123836433": "a place of worship named for a living person (owner, 2026-10-13: a person's own name goes)",
    "node/13529947384": "'1905 Street', a paid living-history park's ride indexed as a station: not transit (owner, 2026-10-13)",
    "node/13529947382": "'1920 Street', a paid living-history park's ride indexed as a station: not transit (owner, 2026-10-13)",
    "node/7759136178": "'Fort Edmonton', a paid living-history park's ride indexed as a station: not transit (owner, 2026-10-13)",
    "node/12205260322": "'107 Street', a railway society's heritage streetcar indexed as a station: not transit (owner, 2026-10-13)",
    "node/11432449223": "'Government Centre Plaza', a railway society's heritage streetcar indexed as a station: not transit (owner, 2026-10-13)",
    "node/1859336998": "'Old Strathcona', a railway society's heritage streetcar indexed as a station: not transit (owner, 2026-10-13)",
    "node/12205260321": "'Whyte Avenue', a railway society's heritage streetcar indexed as a station: not transit (owner, 2026-10-13)",
    "way/126176089": "'Al Rashid Mosque', a building inside a paid living-history park (owner, 2026-10-13: the venue stays, its buildings go)",
    "way/322271762": "'Anglican Church of St. Michael & All Angels', a building inside a paid living-history park (owner, 2026-10-13)",
    "way/322271977": "'Bellerose School', a building inside a paid living-history park (owner, 2026-10-13)",
    "way/126176098": "'Boat Shed', a building inside a paid living-history park (owner, 2026-10-13)",
    "way/126310518": "'Fire Hall, Town Hall, & Police Station', a building inside a paid living-history park (owner, 2026-10-13)",
    "way/583356195": "'Gyro Park & Playground', a feature inside a paid living-history park (owner, 2026-10-13)",
    "way/126176084": "'J.B. Little Brickyard', a feature inside a paid living-history park (owner, 2026-10-13)",
    "way/583356194": "'Memorial Gardens', a feature inside a paid living-history park (owner, 2026-10-13)",
    "way/322275095": "'Methodist Church', a building inside a paid living-history park (owner, 2026-10-13)",
    "way/322264619": "'Métis Cabin', a building inside a paid living-history park (owner, 2026-10-13)",
    "way/322272371": "'N.W.M.P Jail', a building inside a paid living-history park (owner, 2026-10-13)",
    "way/322272995": "'N.W.M.P. Gun Shed', a building inside a paid living-history park (owner, 2026-10-13)",
    "way/126176103": "'Rundle Chapel', a building inside a paid living-history park (owner, 2026-10-13)",
    "way/1474850843": "'Secord Complex', a building inside a paid living-history park (owner, 2026-10-13)",
    "way/264249452": "'St Anthony's Church', a building inside a paid living-history park (owner, 2026-10-13)",
    "way/583862187": "'Tent City', a feature inside a paid living-history park (owner, 2026-10-13)",
    "way/64842311": "'1885 Street', a street inside a paid living-history park (access=customers) (owner, 2026-10-13)",
    "way/126176114": "'1905 Street', a street inside a paid living-history park (access=customers) (owner, 2026-10-13)",
    "way/64842309": "'1905 Street', a street inside a paid living-history park (access=customers) (owner, 2026-10-13)",
    "way/64842310": "'1920 Street', a street inside a paid living-history park (access=customers) (owner, 2026-10-13)",
    "way/126176088": "'1920 Street', a street inside a paid living-history park (access=customers) (owner, 2026-10-13)",
    "way/126176126": "'1920 Street', a street inside a paid living-history park (access=customers) (owner, 2026-10-13)",
    "way/1018647812": "'Peavey Station', a relocated station building inside a railway museum (owner, 2026-10-13)",
    "way/413765132": "'Saint Albert Canadian National Railway Station', a relocated station building inside a railway museum (owner, 2026-10-13)",
    "way/1452723963": "'Alley Access', a bare type as a street's name (owner, 2026-10-13)",
    "way/934500134": "'Alley Access', a bare type as a street's name (owner, 2026-10-13)",
    "way/844073649": "'Cloverdale Bridge Detour', a detour described (owner, 2026-10-13)",
    "way/1218687582": "'Cloverdale Bridge Detour alt', a detour described (owner, 2026-10-13)",
    "way/1094390587": "'Go Trail Alt', a description as a street's name (owner, 2026-10-13)",
    "way/547299003": "'Off-Leash Path', a description as a street's name (owner, 2026-10-13)",
    "way/1279241230": "'On-Leash Path', a description as a street's name (owner, 2026-10-13)",
    "way/98223790": "'51222 Range Road 260', an address as a street's name (owner, 2026-10-13)",
    "way/614250085": "'Goodwin Park & Benches', glitch: stray words glued to the name: '& Benches' after the park's name, by id; not repaired (flag check, 2026-10-13)",
    "node/11940488893": "'Heritage Mall', business: former shopping mall: a demolished mall, by id (flag check, 2026-10-13)",
    "way/521942121": "'Rehwinkel Parsonage', home: clergy residence with an entry and no home tag: a parsonage; 'parsonage' is not in HOME_NAME (flag check, 2026-10-13)",
    "way/322971597": "'Oblats Maison Provinciale', a religious residence (amenity=monastery); its Wikidata entry is the heritage register's and has no article: a home (wave 1's unsure rows, settled on the Wikidata lookup and the existing rules, 2026-10-13)",
    "way/323353112": "'Ukrainian Orthodox Church of Canada', a place of worship named only by a denomination, a body or a chain, in a form the shared rule's lists do not hold; no wikipedia tag of its own (owner's rulings, 2026-10-13)",
    # The pattern screen of 2026-10-13, the owner's rulings on its open calls: rows that fall squarely in one of the owner's
    # class rulings of that date, each with its ruling.
    "way/478357009": "'Orchards Residents Association Park', a residents' association's own park by its name (owner, 2026-10-13, on the pattern screen's open calls: the estate-facility ruling)",
    "way/1113191734": "'East Lawn', a stock name with no place in it (owner, 2026-10-13, on the pattern screen's open calls: ruling 5)",
}
