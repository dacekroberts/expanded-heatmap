"""Pittsburgh-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

A REDUCED-BUCKET PAGE (owner, 2026-09-29): Allegheny County's food-facility
register is the only premises register, so the page carries food service and
food-selling retail, and no personal services - the City's own licences are
signs, amusements and peddlers. Rail is OSM's (Buffalo's, Houston's and
Minneapolis's owner choice): PRT's GTFS licence is unread.
"""

from pathlib import Path

SLUG = "pittsburgh"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "pittsburgh" / "raw"
DATA_PROCESSED = ROOT / "data" / "pittsburgh" / "processed"
OUTPUTS = ROOT / "outputs" / "pittsburgh"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, each with the municipality it is in (the Los
# Angeles rule): the T's South Hills branches.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
EXCLUDED_PREMISES_CSV = OUTPUTS / "excluded_premises.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) --------------

# ALLEGHENY COUNTY HEALTH DEPARTMENT'S GEOCODED FOOD FACILITIES, on WPRDC
# (package allegheny-county-restaurant-food-facility-inspection-violations,
# resource 112a3821-334d-4f3f-ab40-4de1220b1a0a, "as of 2025", last modified
# 2025-08-27; CC0). One row per facility, county-wide. `status` 1 is active
# and 7 out of business (the resource's own description).
FACILITIES_URL = "https://data.wprdc.org/datastore/dump/112a3821-334d-4f3f-ab40-4de1220b1a0a"
FACILITIES_CSV = DATA_RAW / "geocoded_food_facilities.csv"
# The file's own vintage: the resource's last modification. The page states it.
REGISTER_DATE = "2025-08-27"
# Named columns only; the file carries no owner or person column.
FACILITY_COLUMNS = ["id", "facility_name", "num", "street", "city", "zip", "municipal",
                    "category_cd", "description", "bus_st_date", "bus_cl_date", "status",
                    "x", "y"]

# The Census Bureau's place polygon (TIGERweb, current Incorporated Places,
# GEOID 4261000) - a US federal work, public domain, Buffalo's source.
CITY_BOUNDARY_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
                     "Places_CouSub_ConCity_SubMCD/MapServer/4/query")
CITY_BOUNDARY_QUERY = {"where": "GEOID='4261000'", "outFields": "GEOID,NAME,AREALAND,AREAWATER",
                       "outSR": "4326", "f": "geojson"}
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary_tiger.geojson"
# TIGER's land 143.4 km2 plus water 7.7 km2 = 151.1 km2, gated in step 1.
CITY_AREA_KM2 = (145.0, 157.0)

# The county subdivisions around the lines (TIGERweb layer 1), so each stop
# outside the city is named with the municipality it is in (Pennsylvania's
# boroughs and townships cover the county).
COUSUB_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
              "Places_CouSub_ConCity_SubMCD/MapServer/1/query")
COUSUB_GEOJSON = DATA_RAW / "county_subdivisions_tiger.geojson"

OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
RAIL_BBOX = (40.28, -80.15, 40.50, -79.90)          # south, west, north, east

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 17N: the longitude (~-80.00) falls in the -84 to -78 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32617"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the in-city stations' ~445 m median gap (the brief; the spacing
# rule, docs/ring_rules.md: the halved edges where the median is 341-541 m).
# Step 1 prints the median again.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------
#
# PRT's light rail (the T), whitelisted on route + ref, set from the build's
# read of the cache. Every other relation in the box is named in NOT_DRAWN or
# step 1 exits. Stops outside the city are measured, then written to
# excluded_stations.csv - not drawn as stations.
ROUTE_TYPES = ("light_rail", "subway", "tram")
# On NETWORK, not operator: the Red Line's four relations say "PRT", the
# others "Pittsburgh Regional Transit". Red has two services (the Overbrook
# short working and the full run to South Hills Village), so a line may have
# more than two relations; step 1 draws its longest.
NETWORK = "Pittsburgh Regional Transit"
LINE_REFS = ("Red", "Blue", "Silver")
# The brief's labels: the agency on the first, as Minneapolis's "METRO".
LINE_NAMES = {"Red": "PRT Red Line", "Blue": "PRT Blue Line", "Silver": "PRT Silver Line"}
# OSM's colours, scored by render_heatmap's shared check, except Blue: OSM's #77b6e4
# is Delta-E 37.8 from the Retail pins this page draws, so it moves the
# least that clears 46 against every bucket (#59bcde, 11.8 from #77b6e4,
# slightly more cyan; Toronto's precedent of adjusting one agency colour).
LINE_COLOURS = {"Red": "#ec1b24", "Blue": "#59bcde", "Silver": "#BCBDC0"}
NOT_DRAWN = {}
STATION_NAME_ALIASES = {}
COLLAPSE_MAX_SPREAD_M = 250
SPACING_MIN_M = 300.0

# GATE 3, the whole lines before the city scope: Wikipedia's infoboxes (read
# 2026-09-30); PRT's own line pages were not read for a count.
OPERATOR_STATION_COUNTS = {"PRT Red Line": 31, "PRT Blue Line": 24, "PRT Silver Line": 31}
OPERATOR_COUNTS_SOURCE = ("Wikipedia, Red / Blue / Silver Line (Pittsburgh) infoboxes 31 / 24 / "
                          "31, read 2026-09-30")

# --- Business filtering ------------------------------------------------

# The fetch date. Currency is the register's own status (1, no closing date),
# not an inspection window: the file carries one.
AS_OF_DATE = "2026-09-30"

# In-city rows: the County's own `municipal` (Pittsburgh-NNN, the city's
# wards) AND a point inside TIGER's polygon.
CITY_KEEP = "Pittsburgh-"

TAXONOMY_SYSTEM = "pittsburgh_inspection"
RAW_CLASSIFICATION_COLUMN = "premises_kind"

# Sanity bounds: the place polygon's extent plus ~0.02 deg.
PITTSBURGH_BBOX = {
    "lat_min": 40.34,
    "lat_max": 40.52,
    "lon_min": -80.12,
    "lon_max": -79.84,
}
