"""New Orleans-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

NEW ORLEANS, on Philadelphia's template (a US register with its own text
taxonomy, `pipeline/taxonomies/nola_businesstype.py`) and the shared
`pipeline/osm_tram.py` (the tram-city skill). The register is the City's
Active Occupational Licenses, Socrata `iqay-p646`, CC0, updated daily, with a
point on every row. Rail from OpenStreetMap: RTA's GTFS is unread and not used.
"""

from pathlib import Path

SLUG = "new_orleans"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "new_orleans" / "raw"
DATA_PROCESSED = ROOT / "data" / "new_orleans" / "processed"
OUTPUTS = ROOT / "outputs" / "new_orleans"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Streetcar stops outside the city, with the reason. Every stop is inside, so
# today it is header-only.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) ----------------

# Active Occupational Licenses (data.nola.gov iqay-p646, CC0). Taken by an
# explicit column list. ⚠ COLUMNS NEVER TO LOAD: `ownername` (often a person's
# own name; the brief: never shown) and `businessphone` (contact details). The
# download names its columns and step 2 asserts neither arrived.
REGISTER_DOMAIN = "data.nola.gov"
REGISTER_VIEW = "iqay-p646"
REGISTER_URL = f"https://{REGISTER_DOMAIN}/resource/{REGISTER_VIEW}.json"
REGISTER_META_URL = f"https://{REGISTER_DOMAIN}/api/views/{REGISTER_VIEW}.json"
REGISTER_FIELDS = ("businesslicensenumber", "businessname", "businesstype", "businessaddress",
                   "suite", "zip", "businessstartdate", "the_geom")
FORBIDDEN_COLUMNS = ("ownername", "businessphone")
REGISTER_CSV = DATA_RAW / "occupational_licenses.csv"

# THE CENSUS BUREAU'S PLACE POLYGON (TIGERweb, current Incorporated Places,
# GEOID 2255000, New Orleans city - coextensive with Orleans Parish; public
# domain) - Houston's layer.
CITY_BOUNDARY_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
                     "Places_CouSub_ConCity_SubMCD/MapServer/4/query")
CITY_GEOID = "2255000"
CITY_BOUNDARY_QUERY = {"where": f"GEOID='{CITY_GEOID}'",
                       "outFields": "GEOID,NAME,AREALAND,AREAWATER",
                       "outSR": "4326", "f": "geojson"}
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary_tiger.geojson"
# The polygon, land and water (Census: about 439 km2 land, 468 water); step 1
# stops outside these bounds.
CITY_AREA_KM2 = (860.0, 950.0)

# OSM: every tram relation in the streetcars' box (the brief's check box).
RAIL_BBOX = (29.90, -90.14, 30.00, -90.03)        # south, west, north, east
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 15N: the longitude (~-90.07) falls in the -96 to -90 band. Derived
# per city, not copied.
CRS_PROJECTED = "EPSG:32615"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the 106 stations' 186 m median gap (build, 2026-09-30; the brief
# read 164 m over its 110 with the old Riverfront; the owner's spacing rule), and
# NO THINNING (owner, call 13). Step 1 prints the median again and stops outside
# 120-220 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (120.0, 220.0)

# --- Station scope: EVERY STOP of the five lines RTA runs ----------------------
#
# THE BRIEF'S LINES WERE OUT OF DATE, and the owner re-took the call at build
# (2026-09-30, "draw what runs"). RTA's service-changes page (Fall '26 schedules,
# effective 2026-09-20) says 46 Rampart/UPT "will officially reopen for
# service" (Summer '25), and that 49 Riverfront "will now run along the river
# from the French Market to Julia Street ... no longer service Canal Street,
# Loyola Avenue, or Union Passenger Terminal". So the map draws 12, 46, 47, 48
# and 49. OSM's two ref-2 relations are the old Riverfront routing (Canal at
# Carondelet - French Market) and are not drawn.
ROUTE = "tram"
OPERATOR = None
LINE_REFS = ("12", "46", "47", "48", "49")
NOT_DRAWN = {
    1809582: "OSM's ref 2, the Riverfront's old routing via Canal Street; RTA runs the "
             "Riverfront as 49, French Market - Julia Street, since Summer 2025",
    12340018: "OSM's ref 2, the Riverfront's old routing via Canal Street (the other "
              "direction); superseded by 49",
}
# 46 AND 49 CARRY NO STOP MEMBERS IN OSM: 46's stops are members with no role
# and 49's stand beside its track on no relation. Each is a tagged RTA
# tram_stop, assigned to its line by distance to that line's track (0-10 m;
# 2026-09-30). John Churchill Chase Street (260 m off 49's new track) is not
# served. 46's Loyola Avenue stops (Tulane, Poydras Street, Julia Street) are
# 47's too - OSM's 47 runs Loyola to the terminal - so they keep their names and
# merge with 47's. The riverfront's own Poydras Street and Julia Street, 600 m
# away, take "Riverfront at" names (osm_tram's shown name), or the name collapse
# would join them to Loyola's.
STATION_ADD = {
    # 46 Loyola/Rampart
    4597187933: ("46", "Union Passenger Terminal"),
    8436296823: ("46", "Union Passenger Terminal"),
    2535854754: ("46", "Tulane"),
    2535854769: ("46", "Poydras Street"),
    2535854705: ("46", "Julia Street"),
    4597117789: ("46", "Canal at South Rampart"),
    4597187943: ("46", "North Rampart at Conti"),
    8436279603: ("46", "North Rampart at Conti"),
    4597187934: ("46", "North Rampart at Saint Ann"),
    8436279604: ("46", "North Rampart at Saint Ann"),
    4597187932: ("46", "North Rampart at Ursulines"),
    8436283428: ("46", "North Rampart at Ursulines"),
    4597187936: ("46", "North Rampart at Esplanade"),
    8436283437: ("46", "North Rampart at Esplanade"),
    4597187942: ("46", "Saint Claude at Pauger"),
    8436283443: ("46", "Saint Claude at Pauger"),
    4597187944: ("46", "Saint Claude at Elysian Fields"),
    8436283454: ("46", "Saint Claude at Elysian Fields"),
    # 49 Riverfront
    4821756939: ("49", "French Market"),
    8436263958: ("49", "French Market"),
    8436263959: ("49", "French Market"),
    3360099326: ("49", "Ursulines Avenue"),
    3360099329: ("49", "Ursulines Avenue"),
    3360099319: ("49", "Dumaine Street"),
    4218305286: ("49", "Dumaine Street"),
    3360065425: ("49", "Toulouse Street"),
    8436263939: ("49", "Toulouse Street"),
    4218305284: ("49", "Bienville Street"),
    8436263937: ("49", "Bienville Street"),
    8436263932: ("49", "Canal Street"),
    115996523: ("49", "Poydras Street", "Riverfront at Poydras"),
    4597095916: ("49", "Poydras Street", "Riverfront at Poydras"),
    115997235: ("49", "Julia Street", "Riverfront at Julia"),
    3340628100: ("49", "Julia Street", "Riverfront at Julia"),
}
# ONE STOP, TWO NAMES: on Canal Street and St. Charles Avenue each direction's
# stop is named for the cross street on its own side, 6-26 m apart (2026-09-30)
# - Houston's couplet, merged by explicit alias (Oslo's rule), never a rule.
NAME_ALIASES = {
    "Canal at Elk Place": "Canal at Basin",                    # 6 m
    "Canal at Marais": "Canal at LaSalle",                      # 19 m
    "Saint Charles at Melpomene": "Saint Charles at Martin Luther King Jr.",   # 24 m
    "Canal at South Claiborne": "Canal at North Claiborne",     # 26 m
}
EXPECTED_STATIONS = 106

# GATE 3: the operator's own stops, independent of OSM. RTA's website stop
# list per line and direction (the endpoint its Rider Tools schedule page
# reads, norta.com/RTAStops?routeID=<line>&directionID=<0|1>), the two
# directions merged where stops lie within 60 m (the smallest radius at which
# 46 and 49 each come to one stop a location). 47 and 48 list 25 a direction
# exactly. Read 2026-10-01. THREE LINES DISAGREE, AND THE BUILD IS THE ONE
# SHORT - a station fix for the owner, not reconciled here:
OPERATOR_STATION_COUNTS = {
    # MISMATCH, unexplained: build 62. RTA lists S. Carrollton Ave at Sycamore
    # St (stop 307, both directions); OSM carries no Sycamore stop at all.
    "12": 63,
    "46": 11,
    # MISMATCH, unexplained: build 23. RTA runs 47 down Canal to the Canal St.
    # Ferry Terminal (Canal at N. Rampart, Bourbon/Carondelet, Chartres/Camp,
    # N./S. Peters, Ferry Terminal) and lists the Cemeteries Transit Terminal;
    # the build follows OSM's 47 up Loyola (Canal at Basin, Tulane, Poydras
    # Street, Julia Street), which RTA's 47 does not serve.
    "47": 25,
    # MISMATCH, unexplained: build 20. The same lower-Canal stops, Canal at
    # N. Rampart to the Ferry Terminal (5): the build's 48 ends at LaSalle.
    "48": 25,
    "49": 8,
}
OPERATOR_COUNTS_SOURCE = (
    "New Orleans RTA, website stop lists per line and direction "
    "(https://www.norta.com/RTAStops?routeID=12|46|47|48|49&directionID=0|1, "
    "behind https://www.norta.com/rider-tools?tab=schedules), directions merged "
    "within 60 m; primary; read 2026-10-01")

SPACING_MIN_M = 40.0

DRAWN_LINES = ("12", "46", "47", "48", "49")
# RTA's names (its Fall '25 schedule list): "12 - St. Charles", "46 -
# Loyola/Rampart", "47"/"48" the Canal lines by their ends, "49 - Riverfront".
LINE_NAMES = {"12": "St. Charles", "46": "Loyola/Rampart", "47": "Canal–Cemeteries",
              "48": "Canal–City Park/Museum", "49": "Riverfront"}
# OSM's own colours, CSS keywords resolved by their CSS definitions: 12
# `green` #008000, 47 `red` #FF0000, 48 #90EE90, 49 #5C2E86. 46 carries none,
# so the project's own goldenrod (74.8 from the nearest pin). Against the pins
# (CIE76): 12 37.2, 48 30.5 and 49 37.8 sit under the preferred 45 - recorded,
# not changed, since they are the source's (the tram-city skill's colour rule).
LINE_COLOURS = {"12": "#008000", "46": "#b8860b", "47": "#FF0000", "48": "#90EE90",
                "49": "#5C2E86"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "nola_businesstype"
RAW_CLASSIFICATION_COLUMN = "businesstype"

# Sanity bounds for the register's points: the parish plus a margin.
NEW_ORLEANS_BBOX = {
    "lat_min": 29.85,
    "lat_max": 30.20,
    "lon_min": -90.15,
    "lon_max": -89.60,
}

# A BUSINESS NAMED ONLY AS A PERSON shows the address (Kansas City's rule). Read by
# eye on 2026-09-30 from the 697 shown names residence.py reads as a person's; the
# rest are shop names or brands ("ERIN ROSE", a bar; "KATE SPADE"). Ambiguous names
# are listed, which only shows an address in place of a name.
PERSON_NAMED = (
    "ADAM CLARK", "ALEXANDER CARRE", "ALORA ROOD", "BARBARA CLARK", "DONNA TESI", "FISCHER GAMBINO",
    "GINGER TAYLOR", "GLENDA IVY", "GLYNN BAI", "JANICE HERRON", "JELANI HANKINS", "KYLA BERNBERG",
    "LUCY ROSE", "MAURICE ALVARADO", "MELEAH DRAUGHTER", "NATTY ADAMS", "NEWMAN KEATON", "NISH LEE",
    "PATRICIA JOHNSTON", "PORTER LYON", "PRESTON L PITTS", "PURCELL DANIEL", "STEPHANIE TARRANT",
    "SUZANNE L ORMAND", "TREVA MAY",
)
