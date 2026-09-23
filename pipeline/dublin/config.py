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
