"""Tucson-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

TUCSON, on Houston's template (a US register, the sole-owner name rule) and the
shared `pipeline/osm_tram.py` (the tram-city skill). The register is the City's
BUSLIC business-licence layer (layer 3 of OpenData_EconomicDevelopment, NEVER
layer 1), geocoded points with a NAICS code; the shared naics.py fits
unchanged. Its licence is SILENT, read as permitted by the owner (2026-09-30):
the page credits the City and never calls the pins complete. Rail from
OpenStreetMap.
"""

from pathlib import Path

SLUG = "tucson"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "tucson" / "raw"
DATA_PROCESSED = ROOT / "data" / "tucson" / "processed"
OUTPUTS = ROOT / "outputs" / "tucson"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Sun Link stops outside the city, with the reason. Every stop is inside, so
# today it is header-only.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) ----------------

# BUSLIC, "All current, active business licenses" (the layer's description),
# rebuilt by a daily batch job; NOT layer 1 (ZZ_CPV_BUSLIC, a different table).
# Taken by an explicit field list, active and not a home occupation, at the
# server, paged at the layer's 2,000. LIC_STATUS is padded for "Application",
# so step 2 strips before it compares; "Active" is not padded.
REGISTER_LAYER = ("https://gis.tucsonaz.gov/arcgis/rest/services/PublicMaps/"
                  "OpenData_EconomicDevelopment/MapServer/3")
REGISTER_FIELDS = ("OBJECTID", "ACC_NUM", "ACC_NAME", "OWN_TYPE", "NAIC_CODE", "NAIC_DESC",
                   "LIC_TYPE", "LIC_STATUS", "HOME_OCCUPATION", "DT_START", "ADDRESS", "APT",
                   "CITY", "ZIP_CODE")
REGISTER_WHERE = "LIC_STATUS = 'Active' AND HOME_OCCUPATION = 'F'"
REGISTER_CSV = DATA_RAW / "buslic_active.csv"

# THE CENSUS BUREAU'S PLACE POLYGON (TIGERweb, current Incorporated Places,
# GEOID 0477000 Tucson city; public domain) - Houston's layer. The register's
# CITY field is a postal or jurisdiction name ("PIMA COUNTY", "MARANA"), so the
# polygon decides.
CITY_BOUNDARY_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
                     "Places_CouSub_ConCity_SubMCD/MapServer/4/query")
CITY_GEOID = "0477000"
CITY_BOUNDARY_QUERY = {"where": f"GEOID='{CITY_GEOID}'",
                       "outFields": "GEOID,NAME,AREALAND,AREAWATER",
                       "outSR": "4326", "f": "geojson"}
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary_tiger.geojson"
# Tucson as TIGER draws it (Census: about 627 km2 land); step 1 stops outside.
CITY_AREA_KM2 = (600.0, 660.0)

# OSM: every tram relation in Sun Link's box (the brief's check box).
RAIL_BBOX = (32.20, -110.99, 32.25, -110.93)      # south, west, north, east
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 12N: the longitude (~-110.97) falls in the -114 to -108 band.
# Derived per city, not copied.
CRS_PROJECTED = "EPSG:32612"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the 21 stops' 265 m median gap (the brief, 2026-09-30; the owner's
# spacing rule). Step 1 prints the median again and stops outside 200-340 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (200.0, 340.0)

# --- Station scope: EVERY STOP, 21 --------------------------------------------
#
# Sun Link is one streetcar line, Mercado District - University of Arizona
# Health Sciences: two `route=tram` relations (3920972 and 12426661), ref "Sun
# Link". No metro, no other rail. Every stop is kept (owner: no thinning).
ROUTE = "tram"
OPERATOR = None
LINE_REFS = ("Sun Link",)
NOT_DRAWN = {}
STATION_ADD = {}
EXPECTED_STATIONS = 21

# GATE 3: the operator's own stop count, independent of OSM. Sun Tran's Sun
# Link page says "The 3.9 mile route has 23 stops", and its route map numbers
# 23: 1-3, 4E/4W, 5E-8E and 5W-8W (the downtown couplet), 9-18. Twenty-three
# less two stops counted per direction (the tram-city skill's known reason):
#   - 4E/4W "Granada/Cushing St." - one legend entry on the operator's own map;
#     OSM's two stop positions share the name and lie 41 m apart;
#   - 5E "Broadway/Granada" and 5W "Congress/Granada" - OSM names both
#     "Congress Street & Granada Avenue", 34 m apart where the couplet splits.
# The other 19 match the build by name and place (2026-10-01). The 6E-8E and
# 6W-8W pairs are drawn apart because they stand on two streets, Broadway and
# Congress, 70-95 m apart, under two names.
OPERATOR_STATION_COUNTS = {"Sun Link": 21}   # 23 less the two direction pairs at Granada
OPERATOR_COUNTS_SOURCE = (
    "Sun Tran, 'Sun Link Streetcar' page (https://www.sunlinkstreetcar.com/"
    "routes-services/sunlink/: '23 stops') and its route map "
    "(https://www.suntran.com/wp-content/uploads/2022/10/Sun-Link-Template-map-2022.jpg); "
    "primary; read 2026-10-01")

SPACING_MIN_M = 100.0

DRAWN_LINES = ("Sun Link",)
LINE_NAMES = {"Sun Link": "Sun Link"}
# OSM records no `colour` (the brief), so the project's own palette. Scored
# against the pins (CIE76, 2026-09-30): deep orange 59.7 (worst: Food service);
# teal #00838f was tried first and scored 42.3 against Personal services.
LINE_COLOURS = {"Sun Link": "#e65100"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "naics"
RAW_CLASSIFICATION_COLUMN = "NAIC_CODE"

# THE OWNERSHIP TYPES THAT ARE A PERSON (owner, call 15: Houston's rule): the
# pin shows the address, never ACC_NAME. Sole Proprietorship 4,395, Individual
# 1,857 and Married 131 of the active licences (the brief).
PERSONAL_OWN_TYPES = ("Sole Proprietorship", "Individual", "Married")

# AN ACCOUNT NAME THAT IS ONLY A PERSON'S shows the address too, whatever the
# OWN_TYPE (2,040 storefronts have none): Kansas City's rule, on Bucharest's
# and Denmark's precedent. Read by eye on 2026-09-30 from every shown name
# residence.py's shape test reads as a person's: 642 names, all but these 45
# shop names ("RATHER KEEN", "BLIND PIG") or brands ("SONNY ANGEL"). Step 2
# stops if one of them is no longer shown, so a refresh re-reads the list.
PERSON_NAMED = (
    "ADRIANA AHUMADA", "ARACELI NOLASCO", "CAITLYN COLUSSY", "CELIA L RODRIGUEZ",
    "CHARLENE MELISSA", "CITA SCOTT", "CONNI HOGAN", "CONSEPCION LEON", "COURTNEY PIET",
    "DEIDRA INGRAHAM", "DOREEN M MENNEN", "ELIZA MARTINEZ", "ERIN WELLS", "GREEN CECILIA",
    "HEATHER STROCK", "JACKIE ARTHUR", "JENNIFER MALONEY", "JESSE ZOERNIG", "KARLA ANAYA",
    "KATE MAMMANA", "KL TAFOYA", "KYLE HALEY", "LAURIE SAUNDERS", "LILIANA OCANO",
    "LILLIAN L JIMENEZ", "LYNN M COLE", "LYNN O BJELLAND", "MAGDALENE DRECHSLER",
    "MEGAN HOLLANDER", "MICHAEL D HIGGINS", "NICOLE BROADHEAD", "ORI ALLAN", "PAMELA MAACK",
    "PATRICIA G HUGHES", "PHAM VU", "RICHARD T RODGERS", "ROBYN THWAITS", "SALLY GOLOS",
    "SHAHIDA PARIDES", "SHERRY L CANNON", "STEPHEN DUARTE", "STEVE ORNELAS", "SUSAN MCGILL",
    "TONYA TWINE", "YONG LEE",
)

# Sanity bounds for the register's points: the city's extent plus a margin.
TUCSON_BBOX = {
    "lat_min": 31.95,
    "lat_max": 32.45,
    "lon_min": -111.20,
    "lon_max": -110.65,
}
