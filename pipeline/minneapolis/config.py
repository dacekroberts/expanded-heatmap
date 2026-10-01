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
