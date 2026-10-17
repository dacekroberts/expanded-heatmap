"""Dublin-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Step 0 evidence and its checks: docs/build_briefs/dublin.md (6/6).

Dublin is a REGIONAL build - four local authorities, not one municipality -
which is the Vancouver + Surrey shape. The rail network runs through all four
and the register is queried per authority, so a city-only scope would have cut
Luas Red at Tallaght and DART at Howth. What that costs is recorded honestly on
the city page: 36% of the region's storefronts sit near no rail at all, against
22% for Dublin City alone, because Fingal's largest town (Swords) has no rail
station of any type.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "dublin" / "raw"
DATA_PROCESSED = ROOT / "data" / "dublin" / "processed"
OUTPUTS = ROOT / "outputs" / "dublin"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the four authorities, with where each is (a citable scoping
# record, as in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all downloaded by fetch_sources.py - deliberately NOT named
# step*.py, so drift_check.py never runs it and a drift check can never ask
# "does the CURRENT UPSTREAM still produce this" instead of "does the
# COMMITTED CODE".
BUSINESSES_RAW_JSON = DATA_RAW / "valuations.json"
BOUNDARY_GEOJSON = DATA_RAW / "local_authorities.geojson"
# The NTA's national feed is 158 MB and its shapes.txt is 372 MB over 8.0M
# rows - too heavy to re-parse on every step and every drift check. So
# fetch_sources.py trims it ONCE to the three drawn routes and writes a small
# zip; the steps read only that.
GTFS_ALL_ZIP = DATA_RAW / "gtfs_all.zip"
GTFS_ZIP = DATA_RAW / "gtfs_dublin_rail.zip"
# OSM is kept as the CROSS-CHECK, not as the source. Madrid's three sources
# agreeing on 13 lines while landing at 243 / 236 / 230 stations is what showed
# its GTFS feed was undercounting; a second opinion is worth one cached file.
RAIL_OSM_JSON = DATA_RAW / "rail_osm.json"

# --- Sources ---------------------------------------------------------------

# Tailte Eireann's rateable valuation register. Keyless, accountless. The API
# has NO documentation page - opendata.tailte.ie/ is itself a 404, and so are
# /swagger, /docs and /robots.txt - and states its contract only in its error
# body: {"message":"Use either Property Number or Local Authority"}.
#
# TWO PREDECESSOR HOSTS ARE DEAD AND NEITHER REDIRECTS: api.valoff.ie is
# NXDOMAIN and www.valoff.ie answers 000. An earlier screen recorded the whole
# country as negative on the strength of those two corpses.
VALUATION_API = "https://opendata.tailte.ie/api/Property/GetProperties"

# Tailte Eireann, "Local Authorities - National Statutory Boundaries -
# Ungeneralised - 2026", layer 3. Use the FeatureServer, NOT the resource that
# data.gov.ie lists: that one is the ArcGIS Hub async download endpoint, which
# answers HTTP 202 with a job id (the Surrey trap in the add-country skill).
BOUNDARY_SERVICE = (
    "https://services-eu1.arcgis.com/FH5XCsx8rYXqnjF5/arcgis/rest/services/"
    "National_Statutory_Boundaries_-_Local_Authorities__Ungeneralised_-_2026"
    "/FeatureServer/3"
)
BOUNDARY_NAME_FIELD = "ENG_NAME_VALUE"

# --- The four local authorities ---------------------------------------------

# THE TWO SOURCES SPELL ONE AUTHORITY DIFFERENTLY, AND THE REGISTER MATCHES
# EXACTLY. Asking the register for "DUN LAOGHAIRE RATHDOWN COUNTY COUNCIL"
# returns HTTP 200 WITH ZERO ROWS - a silent empty answer, not an error. So the
# join is this explicit table and never string equality.
#
# Row counts measured 2026-09-22; they are the drift baseline, not a filter.
AUTHORITIES = {
    # register spelling                boundary spelling
    "DUBLIN CITY COUNCIL": "DUBLIN CITY COUNCIL",
    "FINGAL COUNTY COUNCIL": "FINGAL COUNTY COUNCIL",
    "SOUTH DUBLIN COUNTY COUNCIL": "SOUTH DUBLIN COUNTY COUNCIL",
    "DUN LAOGHAIRE RATHDOWN CO CO": "DUN LAOGHAIRE-RATHDOWN COUNTY COUNCIL",
}

# THE BOUNDARY LAYER IS MULTIPART and must be dissolved before any
# point-in-polygon test. Fingal returns 46 polygons and Dun Laoghaire-Rathdown
# 42 - islands and coastal outcrops, most under 0.1 km2 - so a query that takes
# the first polygon per authority gets a rock (Lambay Island, in Fingal's case).
BOUNDARY_PARTS_EXPECTED = 90

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# EPSG:2157, Irish Transverse Mercator - a NATIONAL GRID, not a UTM zone, and
# a deliberate departure from this project's per-city-UTM invariant.
#
# Derived, not copied: the register publishes Xitm/Yitm and the boundary layer
# reports wkid 2157, so BOTH SOURCES ARE ALREADY IN THIS CRS, in metres. Using
# UTM 29N (EPSG:32629, which Dublin's longitude implies) would mean
# transforming every point and polygon out of the CRS the publisher measured
# them in, to buy nothing - and Dublin sits at -6.26, within a quarter-degree
# of zone 29's eastern edge at -6.0, where UTM scale distortion is at its worst
# for the zone. ITM's scale factor is optimised for the island instead.
#
# check_provenance.py's UTM invariant was extended to admit documented national
# grids rather than relaxed: see NATIONAL_GRIDS there, which still checks that
# this city's longitude falls inside the grid's own domain.
CRS_PROJECTED = "EPSG:2157"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# RAIL COMES FROM THE AGENCY FEED, NOT OSM - and the first version of this
# build had it the other way round. The osm-rail skill's order is agency GIS
# layers, then agency GTFS, then OSM ON A RECORDED GROUND, and this city's
# brief asserted "OpenStreetMap, not a feed" without running either of the
# first two. Both pass:
#   - The NTA publishes a Feature Service - 14,079 stops, 6,507 route
#     polylines, already EPSG:2157 - at
#     services-eu1.arcgis.com/p0UmGrpumWZYhF0p/.
#   - The NTA's national GTFS is CURRENT: feed_info.txt declares
#     feed_end_date 20270922, a year out, and it carries Woodbrook
#     (8220WBROK), a station that opened in 2025 - so it is maintained, not a
#     re-uploaded archive.
# This is Madrid's failure in its general form: "the GTFS is stale or absent"
# is a different question from "the agency route is closed", and here the
# second was never asked.
GTFS_URL = "https://www.transportforireland.ie/transitData/Data/GTFS_All.zip"

# What is DRAWN. Each entry: GTFS route_id -> (real public name, colour).
#
# THE COLOURS ARE CHOSEN, NOT INHERITED, AND HERE THAT IS FORCED: `route_color`
# is EMPTY for all three routes, in both routes.txt and the feature service.
# There is no agency colour to be faithful to.
#
# The first render used OpenStreetMap's community values and map_common's
# separation check reported all three below the preferred CIE76 of 45 against
# the category pins they are drawn under - DART 21.7 and Luas Green 24.3 from
# Personal services, Luas Red 27.5 from Food service. The project keeps AGENCY
# colours that score badly, as a branding decision; these were not agency
# colours, so that exemption did not apply and the palette was re-measured
# instead.
#
#   Luas Red    #CD5C5C -> #8B0000   27.5 -> 39.5
#   Luas Green  #008531 -> #006400   24.3 -> 37.4
#   DART        #68C56B -> #F57C00   21.7 -> 72.4
#
# THE TWO LUAS LINES STAY UNDER 45 ON PURPOSE. Nothing red clears it (the best
# measured was 39.5) and nothing green does either (37.4), because red sits
# near the magenta food pin and green near the teal personal-services pin by
# construction. A line named "Luas Red Line" cannot be drawn in purple, so the
# choice is the best available red and green rather than a different hue - and
# the shades above are the measured best, not the inherited ones.
#
# DART MOVES OFF GREEN ALTOGETHER because it is the one line whose name is not
# a colour, so it is free - and moving it fixes a second problem the numbers do
# not show: with OSM's palette the map had TWO green lines.
#
# ITS COLOUR IS SCORED TWICE, against the pins AND against the other two
# lines, because a line only has to be legible against both. #E65100 scored
# 59.7 on pins and was rejected at 36.0 from Luas Red - two dark warm lines
# crossing in the city centre. #F57C00 is 72.4 / 48.9 / 94.0, the only
# candidate measured that clears every pairing.
#
# DART'S LABEL IS `DART`, NOT ITS route_long_name. The feed says
# "Bray - Howth", which understates a line whose own stops run Malahide to
# Greystones; route_short_name is what riders call it.
ROUTES = {
    "10000 GREEN g a": ("Luas Green Line", "#006400"),
    "10000 RED g a": ("Luas Red Line", "#8B0000"),
    "BRAY-HOWTH-I": ("DART", "#F57C00"),
}

# Gate 3: the operators' own per-line stop counts, keyed as ROUTES. Whole
# lines, BEFORE the four-authority cut (DART's Greystones, in Wicklow, counts
# here). An interchange counts once on each line it serves (Connolly is on the
# Red Line's list and on DART's).
OPERATOR_STATION_COUNTS = {
    # "The line has 35 operating stops with 2 future stops which may be
    # brought into use when there is development in those areas" - the two
    # future stops are not built or served, so 35.
    "10000 GREEN g a": 35,
    "10000 RED g a": 32,        # "The line has 32 stops."
    # Iarnrod Eireann's two DART routes: Malahide - Greystones, 29 stations,
    # and Howth - Greystones, which adds Howth, Sutton and Bayside before
    # joining at Howth Junction. 29 + 3 = 32, Woodbrook (opened 2025) included.
    "BRAY-HOWTH-I": 32,
}
OPERATOR_COUNTS_SOURCE = (
    "Luas: Transport Infrastructure Ireland, 'Luas Red and Green Lines' "
    "(tii.ie/en/public-transport/luas/red-and-green-lines/), the stated stop "
    "count of each line. DART: Iarnrod Eireann, 'Accessible details for "
    "Dublin City and Commuter Zone Train and Tram Map' (irishrail.ie/en-ie/"
    "travel-information/station-and-route-maps/accessible-details-dublin-"
    "area), the DART station list of each route. Both read 2026-10-01; "
    "primary (TII owns the Luas network; Iarnrod Eireann runs DART)."
)

# COMMUTER AND INTERCITY ARE EXCLUDED, and the agency feed separates them more
# cleanly than OSM did: they are other route_ids under the same route_type 2,
# with no tag to misread. Commuter rail is out in every built city and eight
# record it explicitly (Boston's CR-*, Chicago's Metra, Madrid's Cercanias,
# Miami's Tri-Rail, Philadelphia's Regional Rail, Vancouver's West Coast
# Express; Montreal and Washington DC note they have none). Measured here, it
# is also worth only 4.4% of the region - 619 storefronts, and zero in Dun
# Laoghaire-Rathdown, which DART already serves end to end.

# The OSM cross-check still runs. Keeping a second opinion is what showed
# Madrid's feed undercounting, and it costs one cached file.
RAIL_BBOX = (53.15, -6.55, 53.65, -6.02)   # south, west, north, east
OSM_REFS = ("Luas Red Line", "Luas Green Line", "DART")

# DART IS KEPT ON A JUDGMENT CALL, NOT BY THE RULE ABOVE. By the letter of it -
# national railway operator, OSM route=train, GTFS route_type 2 - DART would go
# with the rest. It is kept on Philadelphia's precedent, where SEPTA's
# Market-Frankford and Broad Street lines are drawn and Regional Rail is not,
# the line between them being station spacing rather than which company runs
# the trains: DART's in-city spacing (Connolly, Tara Street, Pearse, Grand
# Canal Dock, Lansdowne Road, Sandymount) is about a kilometre, where the
# Commuter services it shares track with run to Dundalk and Portlaoise.
# See DECISIONS.md, 2026-09-22. IF THAT RULE IS EVER TIGHTENED TO ADMIT NO
# route_type 2, DUBLIN LOSES ITS PRINCIPAL LINE and must be re-scoped rather
# than shipped as a two-tram-line map.

# One stop recorded under two names. Found by the shared spacing gate, which
# printed "11 station(s) within 200 m, minimum 4 m" and said to go and look -
# the median (586 m) cannot see a handful of uncollapsed names, which is
# exactly how Barcelona shipped Catalunya twice.
#
# THE LINE DRAWN, because Dublin's centre genuinely is this dense: same mode,
# same line, metres apart = one stop under two names, collapse it. Different
# modes = a real interchange with separate platforms, keep both.
#   - Fortunestown / Fortunestown Tram Stop: both Luas Red `tram_stop`, 4 m.
#     One stop. Collapsed.
#   - Connolly (Luas `tram_stop`) / Connolly Station (DART `stop`): 251 m and
#     two different modes - the tram stop on the street, the rail platforms
#     inside. KEPT SEPARATE, on the same reasoning that keeps Abbey Street
#     (Red Line) and Marlborough (Green Line) 70 m apart: they are distinct
#     boarding points, and the map assigns each business to its nearest
#     station so nothing is double-counted.
#   - Heuston here is the LUAS stop. Dublin Heuston's mainline platforms are
#     not in the drawn set because no DART calls there.
STATION_ALIASES = {
    "Fortunestown Tram Stop": "Fortunestown",
}

# --- Business filtering ------------------------------------------------

# In-region rows are identified by the register's own LocalAuthority field
# (the AUTHORITIES keys above), then confirmed against the dissolved boundary.
# There is no city-name field to mis-trust here, unlike Los Angeles' postal
# community names.
CITY_KEEP = tuple(AUTHORITIES)

TAXONOMY_SYSTEM = "dublin_uses"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "Uses"

# A SECOND PASS OVER MIXED-USE ROWS, not the main exclusion. The taxonomy
# already lists VACANT, RIGHT OF TRADING and ATM as non-storefront segments, so
# a row whose only use is one of those never reaches here - of the 117, 150 and
# 88 such rows region-wide, this filter sees 6. Those 6 are the mixed ones:
# "VACANT, SHOP" classifies as Retail on its SHOP half while the premises is
# half empty, and a vacant unit should not be a pin.
#
# Measured 2026-09-22: 13,133 -> 13,127. Kept because the mixed case is real
# and would otherwise be invisible, and because a filter that stops dropping
# anything is a signal the taxonomy changed underneath it.
EXCLUDE_USES_CONTAINING = (
    "VACANT",
    "RIGHT OF TRADING",
    "ATM",
)

# THE REGISTER CARRIES NO BUSINESS NAME OF ANY KIND - no trade name, no
# occupier, no ratepayer, no owner. 19 fields, checked against
# name|occupier|tenant|owner|ratepayer|proprietor|person|contact with zero
# matches; the Irish valuation list records premises and is non-domestic by
# statute. So Los Angeles' failure mode (a blank trade name falling back to a
# registrant's own name at their home) CANNOT OCCUR HERE, structurally rather
# than by a filter. The pin label is the address instead.
NAME_COLUMN = "Address1"

# EIRCODE IS DROPPED AT LOAD, NOT FILTERED AFTERWARDS. The Eircode database is
# third-party IP (An Post / OSi via GeoDirectory, licensed through Capita), and
# both the PSI licence and data.gov.ie/license carve out third-party database
# rights the Information Provider is not authorised to license. The build never
# needs it - it has Xitm/Yitm and five address lines - so the column is dropped
# rather than the question answered. See DECISIONS.md, 2026-09-22.
DROP_COLUMNS = ("Eircode",)

# Sanity bounds for the four authorities' real extent: Balbriggan in the north,
# the Wicklow border in the south, Lambay Island in the east.
DUBLIN_BBOX = {
    "lat_min": 53.15,
    "lat_max": 53.70,
    "lon_min": -6.60,
    "lon_max": -5.95,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3601109531,3601114164,3601115720,3601117469)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {
    "Store Street": "a public street (ref L1049) with an Irish name of its own",
    "T2 Parking Road": "a public airport road, no access tag",
}
PLACE_DROPPED = {
    "way/474813985": "'The Green': tagged leisure=park and nothing else, named by a type word alone (73 m from Glasmore Abbey in Swords); the type-word park ruling drops it; in an... (lane 4 borderline read; owner, 2026-10-16)",
    "way/32205818": "'The Green': tagged leisure=park and nothing else, named by a type word alone, no landmark or place row within 250 m (lane 4 borderline read; owner, 2026-10-16)",
    "way/1316674035": "'College Chapel': a chapel named only by a type, inside the All Hallows campus (38 m from the campus row, relation/5467501); its description says it carries a room... (lane 4 borderline read; owner, 2026-10-16)",
    "node/13677383001": "'Hardwicke Street Flats', council flats mapped as a neighbourhood: homes",
    "node/3326702964": "'Bremore Cottages', a row of cottages mapped as a locality: homes",
    "node/3152506221": "'Dubber Cottages', a row of cottages mapped as a locality: homes",
    "node/3326644314": "'Dunsoghly Cottages', a row of cottages mapped as a locality: homes",
    "node/3329360876": "'Lancaster Cottages', a row of cottages mapped as a locality: homes",
    "node/3152506220": "'Meakstown Cottages', a row of cottages mapped as a locality: homes",
    "node/2493161146": "'Johnstown House', a single house mapped as a locality: a home",
    "node/8108546137": "'New House', a single house mapped as a locality: a home",
    "way/94874697": "'Martello Tower No.7 Killiney - Killiney Hill', its description says it is now part of a residence: a home",
    "way/257155934": "'Bridgeview Halting Site', a halting site's own road: homes",
    "way/257155935": "'Bridgeview Halting Site', a halting site's own road: homes",
    "way/440823836": "'Citywest Business Park', a business park tagged a park",
    "way/177562856": "'Docklands Innovation Park - Central Building', a business park's building tagged a park",
    "relation/4546404": "'Profile Park', a business park tagged a locality",
    "node/2956395537": "'Ballinteer Business Park', a business park tagged a locality",
    "way/675737984": "'FoodCentral', a business park tagged a locality",
    "way/674251614": "'Grange Castle Business Park', a business park tagged a locality",
    "way/992980618": "'Dublin Inland Port', an industrial site of the port company tagged a locality",
    "way/669995931": "'Block 503', a business park's numbered block tagged a locality",
    "way/671320058": "'Block 532', a business park's numbered block tagged a locality",
    "way/671859995": "'Block 613', a business park's numbered block tagged a locality",
    "way/668626898": "'Blue Zone', a business park's colour zone tagged a locality",
    "way/668626900": "'Green Zone', a business park's colour zone tagged a locality",
    "way/668626901": "'Orange Zone', a business park's colour zone tagged a locality",
    "way/668626902": "'Red Zone', a business park's colour zone tagged a locality",
    "way/668626899": "'Yellow Zone', a business park's colour zone tagged a locality",
    "node/14090745363": "'Imaal Mart', a terrace of shops tagged a locality",
    "node/10556690863": "'Omni centre Oratory', an oratory inside a shopping centre, under the centre's name",
    "node/10751721512": "'Anchor', a bare type word, unregistered",
    "way/513392167": "'The Anchor', a bare type word, unregistered",
    "node/1976319808": "'Ice Houses', a bare type word, unregistered",
    "way/322713307": "'Church (in ruins)', a type word and a status note",
    "way/546295439": "'Pavilion Ruins', a description on a ruin",
    "way/628317444": "'Pavilion Ruins', a description on a ruin",
    "node/8879621806": "'Rockwork Feature', a description standing in for a name",
    "node/2625918843": "'Abandoned Cottages', a description standing in for a name",
    "node/2688933710": "'Kenure estate storage room', a description of a storage room",
    "node/4631122184": "'IADT Sign', a sign described",
    "way/556856623": "'Triangle Seating Park area', a description of a seating area",
    "way/461226974": "'Redcourt Oaks Amenity Green area', a housing estate's green described",
    "way/34892576": "'Redcourt Oaks Green Area (Fountain)', a housing estate's green described",
    "way/461434299": "'Redcourt Oaks Green area', a housing estate's green described",
    "node/11816365456": "'Aviva Stadium Entrance M - O', a stadium entrance's letters on a node",
    "node/12173751970": "'Telegraph Cable Marker', a description of a marker",
    "way/468601467": "'Quadrangle Courtyard', a description standing in for a name",
    "node/3425117454": "'Mortuary Chapel of Repose', a hospital's mortuary chapel described",
    "node/2570048897": "'Confined Spaces Training', a training facility's label on a locality node",
    "node/2570048898": "'Leakage Training Rig', a training facility's label on a locality node",
    "node/3153262650": "'Emergency Rendevous Point B', an emergency assembly point's label on a locality node",
    "node/5384578630": "'Collins Avenue Entrance', an entrance described on a locality node",
    "node/9943789195": "'T9', a bare code on a locality node",
    "node/653535739": "'Grace', the name is cut short: a glitch",
    "way/89405856": "'Blackrock Baths (closed)', closed since 1987 (end_date), with the status in its name",
    "node/13260437635": "'W18539', a wreck with access=no under a bare code",
    "way/548116412": "'Former Moravian Church', a former church that is offices today (building:use=office)",
    "relation/19322044": "'Nally Stand', a stadium stand tagged a locality",
    "way/374959239": "'Dominican Convent', a convent, not notable: a religious residence, by id",
    "way/60541923": "'Our Lady's Convent (old)', a convent, not notable: a religious residence, by id",
    "node/264698492": "'Gort Muire', a religious house tagged a place of worship, not notable: a religious residence, by id",
    "node/7020297702": "a plaque to a private person, named for them (owner, 2026-10-13: a person's own name goes)",
    "node/5071696221": "a grave tagged an attraction and admitted on the article of the person buried there (owner, 2026-10-13)",
    "node/5071682622": "a grave tagged an attraction and admitted on the article of the person buried there (owner, 2026-10-13)",
    "relation/7523707": "'Rathdown Poor Law Union', an abolished administrative boundary (owner, 2026-10-13: a search must not land where the thing is not)",
    "relation/6340790": "'Suburban District of Dublin 1861 Census', an abolished census district (owner, 2026-10-13)",
    "relation/10569993": "'Fitzwilliam Land South Dublin', a historic estate boundary, no longer a place (owner, 2026-10-13)",
    "relation/11840660": "'Dublin Townships', an abolished constituency (owner, 2026-10-13)",
    "node/3958839458": "'African Savanna', a zone inside the zoo, a paid venue, mapped as a place (owner, 2026-10-13: the venue stays, its zones go)",
    "node/3950726154": "'Asian Forests', a zone inside the zoo, a paid venue, mapped as a place (owner, 2026-10-13)",
    "node/3958839466": "'Orangutan Forest', a zone inside the zoo, a paid venue, mapped as a place (owner, 2026-10-13)",
    "node/3958839469": "'Sea lion cove', a zone inside the zoo, a paid venue, mapped as a place (owner, 2026-10-13)",
    "node/3950828684": "'Family Farm', a zone inside the zoo, a paid venue, mapped as a place (owner, 2026-10-13)",
    "node/1902288302": "'Marlay Station', a miniature railway in a park indexed as a station: not transit (owner, 2026-10-13)",
    "node/632939835": "'Kerlin Gallery', a dealer's gallery is the business itself, whatever its article (owner, 2026-10-11)",
    "way/586138064": "'Bus Terminus', a bare type as a street's name (owner, 2026-10-13)",
    "way/1562600502": "'Footpath (Under Construction)', a description as a street's name (owner, 2026-10-13)",
    "way/459633756": "'entrance path #3', a description as a street's name (owner, 2026-10-13)",
    "way/459633757": "'entrance path 4-12', a description as a street's name (owner, 2026-10-13)",
    "way/26150001": "'James's Street Exit', a description as a street's name (owner, 2026-10-13)",
    "way/461012279": "'Entrance to Grand Canal Way', a description as a street's name (owner, 2026-10-13)",
    "way/1147200630": "'Cycle Link at Drummartin Link Road via Salt Barn to Bracken Road', a description as a street's name (owner, 2026-10-13)",
    "way/77006401": "'Station Access', a bare type as a street's name (owner, 2026-10-13)",
    "way/199651933": "'(Flood Road)', a bracketed note as a street's name (owner, 2026-10-13)",
    "way/476060876": "'r122', a runway construction note as a street's name (owner, 2026-10-13)",
    "way/26491461": "'7A', a code as a street's name (owner, 2026-10-13)",
    "way/1333616549": "'7A', a code as a street's name (owner, 2026-10-13)",
    "way/1333616550": "'7A', a code as a street's name (owner, 2026-10-13)",
    "way/236891739": "'Kaziranga Forest Trail', a trail inside the zoo, a paid venue (owner, 2026-10-13)",
    "node/13687138236": "'18th Century Stone Architrave', description: historic=ruins; ruins=Architrave; no wikidata (name describes the object) (flag check, 2026-10-13)",
    "node/916893779": "'1916 volunteers meeting point', description: historic=monument; lowercase descriptive name; no wikidata (a description standing in for a name) (flag check, 2026-10-13)",
    "way/1189826856": "'Balrothery Union Workhouse, site of', not there: historic=workhouse; name ends \", site of\" (a site-of name: nothing stands) (flag check, 2026-10-13)",
    "node/886520168": "'Bunchloch (Foundation Stone)', description: historic=monument; name is \"(Foundation Stone)\" (a foundation stone under a type word) (flag check, 2026-10-13)",
    "node/10040750611": "'CIIC 137 / TCBKD A', code: historic=ogham_stone; moved=yes; name is a corpus code (catalogue code; stone moved (moved_to:wikidata)) (flag check, 2026-10-13)",
    "node/10563395863": "'CIIC 185 / TCBKD B', code: historic=ogham_stone; moved=yes; name is a corpus code (catalogue code; stone moved (moved_to:wikidata)) (flag check, 2026-10-13)",
    "node/3834809157": "'Crimean War cannon', description: historic=monument; lowercase type word; no wikidata (cannon under a description) (flag check, 2026-10-13)",
    "way/568711652": "'Dome-Shaped Temple', description: historic=monument; no wikidata (name describes the object) (flag check, 2026-10-13)",
    "way/340537785": "'Memorial Garden', description: leisure=garden; wikipedia is the event's (bare type name; article not the garden's own) (flag check, 2026-10-13)",
    "node/2578153247": "'Norman Motte', description: historic=castle; no wikidata (period + type word) (flag check, 2026-10-13)",
    "node/1359917267": "'Norman Tower', description: historic=ruins; no wikidata (period + type word) (flag check, 2026-10-13)",
    "way/1189827843": "'Rathdown Union Workhouse, site of', not there: historic=workhouse; name ends \", site of\" (a site-of name) (flag check, 2026-10-13)",
    "node/3562604733": "'W&R Jacob & Co. Limited', business: historic=building; note=Carved stone sign from factory (a company's name on a carved sign) (flag check, 2026-10-13)",
    "node/3804149636": "'Saint Vincent's Graveyard (site of)', not there: place=locality; name ends \"(site of)\" (a site-of name) (flag check, 2026-10-13)",
    # The pattern screen of 2026-10-13: rows that fall squarely in one of the owner's
    # class rulings of that date, each with its ruling.
    "way/136549341": "'Central Square', a stock plaza or square name with no place in it (owner, 2026-10-13, ruling 5 and its follow-up: every plaza name with no place in it; pattern screen)",
    # The pattern screen of 2026-10-13, the owner's rulings on its open calls: rows that fall squarely in one of the owner's
    # class rulings of that date, each with its ruling.
    "way/719011797": "'Village Green', a park named only by a type word (owner, 2026-10-13, on the pattern screen's open calls)",
    # The helper screens of 2026-10-13 (duplicates, parts in a church's grounds): rows that
    # fall squarely in an owner ruling, each with its ruling.
    "node/3950323926": "'Kilmainham Jail Museum', one object under two rows within 300 m; the other row stays (owner, 2026-10-13, the duplicates class of the pattern screen and the Three Soldiers ruling; helper screen): the museum point of Kilmainham Gaol, 34 m from the gaol's own row (way/41662413, alt name Kilmainham Jail), under the same Wikidata entry (Q1049842) and the same article: one sight twice",
}

# Places of worship kept by the owner's word against the denomination rule
# (place_index, worship_only; owner, 2026-10-13: "keep all four by id").
PLACE_KEPT = {
    "way/230568525": "'Unitarian Church', the St Stephen's Green church (denomination=unitarian, building=church, heritage=4, no wikidata or wikipedia tag): a known building under its denomination's name (owner, 2026-10-13)",
    "relation/289528": "'General Post Office', one of the city's best-known sights, in the cache with no row (tourism=attraction, building=retail, wikidata=Q1339254 and its own article; held out by the rules all the same): a famous place the rules pass over (owner, 2026-10-13; pattern screen)",
    "relation/4547344": "'Custom House', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "node/332211029": "'Forty Foot', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "node/1740224383": "'Gaelic Athletic Association Museum', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "node/9683454002": "'Guinness Brewery Gate', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "node/660711306": "'Liberty Hall Theatre', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "way/1418111967": "'National Museum of Ireland, Collins Barracks', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "way/109491574": "'Papal Cross', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "way/661187320": "'Richmond Barracks', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
}
