"""Minneapolis-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

A REDUCED-BUCKET PAGE (owner, 2026-09-29): the City's food-inspection table
is the only register, so the page carries food service and grocery-type
retail, and no personal services - no salon, barber or laundry register
exists for the city. Rail is OSM's (Buffalo's and Houston's owner choice):
Metro Transit's GTFS licence is unread.
"""

from pathlib import Path

SLUG = "minneapolis"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "minneapolis" / "raw"
DATA_PROCESSED = ROOT / "data" / "minneapolis" / "processed"
OUTPUTS = ROOT / "outputs" / "minneapolis"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, each with the municipality it is in (the Los
# Angeles rule): the Green Line's St. Paul half, the Blue Line's airport,
# Fort Snelling and Bloomington stops.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
EXCLUDED_PREMISES_CSV = OUTPUTS / "excluded_premises.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) --------------

# THE CITY'S FOOD INSPECTIONS (ArcGIS item 4eea8bf452e34f8c9d9ac07c54c0b4ab,
# owner City_of_Minneapolis, CC0 1.0 waiver on the item). One row per
# VIOLATION, 2023 onward; step 2 de-duplicates on HealthFacilityIDNumber. The
# layer serves 16,000 records a page, so the fetch pages by OBJECTID.
FOOD_LAYER_URL = ("https://services.arcgis.com/afSMGVsC7QlRK1kZ/arcgis/rest/services/"
                  "Food_Inspections/FeatureServer/0/query")
# Named fields only. Never InspectorComments or FoodCodeText (free text an
# inspector wrote, which can name a person) and never APN.
FOOD_FIELDS = ("OBJECTID", "HealthFacilityIDNumber", "FacilityCategory", "BusinessName",
               "FullAddress", "City", "ZipCode", "DateOfInspection", "InspectionIDNumber",
               "Latitude", "Longitude")
FOOD_INSPECTIONS_JSON = DATA_RAW / "food_inspections.json"

# The Census Bureau's place polygon (TIGERweb, current Incorporated Places,
# GEOID 2743000) - a US federal work, public domain, Buffalo's source.
CITY_BOUNDARY_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
                     "Places_CouSub_ConCity_SubMCD/MapServer/4/query")
CITY_BOUNDARY_QUERY = {"where": "GEOID='2743000'", "outFields": "GEOID,NAME,AREALAND,AREAWATER",
                       "outSR": "4326", "f": "geojson"}
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary_tiger.geojson"
# TIGER's land 139.9 km2 plus water 9.1 km2 = 148.9 km2, gated in step 1.
CITY_AREA_KM2 = (143.0, 155.0)

# The county subdivisions around the lines (TIGERweb layer 1), so each stop
# outside the city is named with the municipality it is in. Minnesota's
# subdivisions cover the state - cities, townships and unorganized
# territory, the airport's Fort Snelling included.
COUSUB_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
              "Places_CouSub_ConCity_SubMCD/MapServer/1/query")
COUSUB_GEOJSON = DATA_RAW / "county_subdivisions_tiger.geojson"

OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
RAIL_BBOX = (44.80, -93.40, 45.10, -93.05)          # south, west, north, east

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 15N: the longitude (~-93.27) falls in the -96 to -90 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32615"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# METRO Blue (901) and Green (902) light rail, whitelisted on operator + ref +
# route. Every other relation in the box is named in NOT_DRAWN or step 1
# exits. Stops outside the city are measured, then written to
# excluded_stations.csv - not drawn as stations, as Los Angeles's are not.
ROUTE_TYPES = ("light_rail", "subway", "tram")
OPERATOR = "Metro Transit"
LINE_REFS = ("901", "902")
LINE_NAMES = {"901": "METRO Blue Line", "902": "METRO Green Line"}
LINE_COLOURS = {"901": "#0000ff", "902": "#008144"}
# The brief called CHCL the airport's people mover; OSM's relation is the
# Minnesota Streetcar Museum's Como-Harriet heritage line - a museum ride, not
# transit, and not drawn on either reading.
NOT_DRAWN = {6736496: "Como-Harriet Streetcar Line: the Minnesota Streetcar Museum's "
                      "heritage ride, not transit"}
# One stop under two spellings, one per direction of each line - explicit,
# never a rule. Metro Transit writes "U.S. Bank Stadium".
STATION_NAME_ALIASES = {"US Bank Stadium": "U.S. Bank Stadium"}
COLLAPSE_MAX_SPREAD_M = 250
SPACING_MIN_M = 400.0

# GATE 3, the whole lines before the city scope: Metro Transit's own line
# pages state no count, so Wikipedia's (read 2026-09-30).
OPERATOR_STATION_COUNTS = {"METRO Blue Line": 19, "METRO Green Line": 23}
OPERATOR_COUNTS_SOURCE = ("Wikipedia, Blue Line (Minnesota) '19 stations' and Green Line "
                          "(Minnesota) infobox 23, read 2026-09-30")

# --- Business filtering ------------------------------------------------

# The fetch date. A facility counts when inspected within CURRENCY_YEARS
# before it: the table carries no status. Set by fetch_sources.py's run.
AS_OF_DATE = "2026-09-30"
CURRENCY_YEARS = 2

# In-city rows are identified by point-in-boundary against TIGER's polygon,
# never by the `City` field.
CITY_KEEP = None

TAXONOMY_SYSTEM = "minneapolis_inspection"
RAW_CLASSIFICATION_COLUMN = "premises_kind"

# Sanity bounds: the place polygon's extent plus ~0.02 deg.
MINNEAPOLIS_BBOX = {
    "lat_min": 44.87,
    "lat_max": 45.07,
    "lon_min": -93.35,
    "lon_max": -93.17,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3600136712)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {
    "Children's Theatre Company": "a notable theatre (amenity=theatre, Wikipedia); \"Company\" is its name",
    "Emerson-Newton Implement Company": "the historic name of an NRHP-listed building (Wikipedia), not the present hotel's",
}
PLACE_DROPPED = {
    "way/88014647": "'Cru House': a campus ministry's house (building=university) tagged a place of worship, 130 m from a church row; not a congregation's church (lane 4 borderline read; owner, 2026-10-16)",
    "way/56157617": "'1010 Lofts', an NRHP-listed building that is apartments today (building:use=apartments): a home",
    "way/60712042": "'430 Oak Grove', an NRHP-listed building that is 75 flats today, named by its address: a home",
    "way/45581681": "'American Trio Lofts', an NRHP-listed building that is apartments today (building:use=apartments): a home",
    "way/143297651": "'The Historic Bremer', an NRHP-listed former school that is apartments today: a home",
    "way/88039984": "'Sigma Phi Epsilon', a fraternity's house, its members' residence",
    "way/153793175": "'Mansion at Uptown', tagged as an events venue under the business's name; the library it was is its own row",
    "node/11206832547": "'Minneapolis', a city-limit sign named by its inscription, the city's name",
    "node/11206832549": "'Minneapolis', a city-limit sign named by its inscription, the city's name",
    "node/11206832550": "'Minneapolis', a city-limit sign named by its inscription, the city's name",
    "node/11206824503": "'Minneapolis', a city-limit sign named by its inscription, the city's name",
    "node/11206824507": "'Minneapolis: City of Lakes', a city-limit sign named by its inscription",
    "way/469741572": "'Theo Wirth', the name is cut short; the park is its own row (relation/19413892)",
    "node/1722225764": "'42nd St Depot', a streetcar museum's heritage line indexed as a station: not transit (owner, 2026-10-13)",
    "node/1722225703": "'Cottage City Stop', a streetcar museum's heritage line indexed as a station: not transit (owner, 2026-10-13)",
    "node/9892321102": "'Lakewood Cemetery Stop', a streetcar museum's heritage line indexed as a station: not transit (owner, 2026-10-13)",
    "way/1360166213": "'Minneapolis Skyway (Tunnel)', a description as a street's name (owner, 2026-10-13)",
    "way/1026174773": "'Loren L. Chadwick Cottages', home: houses with an article and no home tag: private cottages; HOME_NAME misses the plural, by id (flag check, 2026-10-13)",
    "way/1053667647": "'Stone Path', description: a surface and a type word (flag check, 2026-10-13)",
    # The pattern screen of 2026-10-13: rows that fall squarely in one of the owner's
    # class rulings of that date, each with its ruling.
    "node/13788625447": "'Flagpole Plaza', a stock plaza or square name with no place in it (owner, 2026-10-13, ruling 5 and its follow-up: every plaza name with no place in it; pattern screen)",
    # The Midtown Greenway's street bridges, each a row under the greenway's own Wikidata
    # entry (Q6843083): one object labelled many times; the greenway's row
    # (relation/20711846) stays (owner, 2026-10-13, on the helper screen's call).
    "way/715627914": "'10th Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627915": "'11th Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627916": "'12th Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627917": "'13th Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627918": "'14th Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627919": "'15th Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627921": "'16th Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627922": "'17th Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627923": "'18th Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627904": "'1st Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627894": "'Aldrich Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627920": "'Bloomington Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627892": "'Colfax Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627911": "'Columbus Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627898": "'Grand Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627897": "'Harriet Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627903": "'Nicollet Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627909": "'Oakland Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627900": "'Pillsbury Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627899": "'Pleasant Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
    "way/715627905": "'Stevens Avenue Bridge', a street bridge over the Midtown Greenway under the greenway's entry Q6843083: one object labelled many times (owner, 2026-10-13)",
}
