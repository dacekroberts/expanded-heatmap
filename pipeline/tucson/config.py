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
#
# 5E/5W and 4E/4W RE-TESTED ON GEOMETRY (2026-10-01), because the operator
# names 5E and 5W after two streets, as it does 6-8: they are one stop each.
#   - OSM's track (ways 188426734 eastbound, 245869213 westbound) comes north
#     up Granada on two parallel tracks and turns east; at Granada the
#     eastbound (Broadway) track runs 13 m south of the westbound (Congress)
#     one, the two streets meeting there, and they part only towards Church
#     (72 m apart at 6E/6W). 5E is node 2986100986 on the eastbound track,
#     5W node 2986100987 on the westbound, 34 m apart (platform ways 915513296
#     and 915513295, side by side), and the only stop nodes on either track
#     between 4 and 6 - there is no separate Broadway stop to add.
#   - The operator's map draws 5E and 5W as two circles touching at one spot,
#     as it does 4E and 4W, where it draws 6E/6W, 7E/7W and 8E/8W a street
#     apart.
#   - 4E/4W are nodes 8501663123 and 2986100983 on the two Granada tracks
#     just north of Cushing, 41 m apart, one legend entry.
# So 21 stands: a direction pair 34-41 m apart is one stop, the 70-95 m pairs
# on two streets are two.
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
# Keys, not names (pipeline/name_keys.py): a new name's key is its output.
PERSON_NAMED = (
    "36651ae5975449dc", "308b00601e27e289", "291d5a29ac6c15b9", "e9b97b19c5386482",
    "0fd3a051bce2c666", "4232ed74cbd043fe", "33bf32e76cd51b18", "6ef6df70ca05a30f",
    "e0e8a0cca8c78ff2", "949f958e43b918ca", "7888b7d166847338", "c2fe9d692d897a1e",
    "3fcd721329f6a90c", "ca9cb27362eaacef", "b2abd0eedec6a09e", "aa966ea85a7f6586",
    "b8df5d2b41cc7c26", "7ebef3b7607ac47c", "8785cd4d72ef2397", "6a68bd6a9cd11f31",
    "ccfc332fb6169373", "4c60a73621368c34", "37967b401da1f259", "ffd9c57c35fcb5bc",
    "031fd687c73ef6d9", "26921be07797a09f", "b0eeb4d525a87d5a", "694cd3329660a4c7",
    "512ba652061321d0", "2b578e4527ba6212", "28a22c4e835a0eea", "733c87b88279a68b",
    "ff9c8fafa0f4b126", "d835ebd2293e3354", "504a42aec6e8d621", "18924cd80f2bc93e",
    "27b10d6082fc1658", "12db90d2c70a5f33", "d3b1ec46df57bbd7", "8726eea746621d69",
    "13b02cf5e5fb6cfb", "4c03b642bb417549", "0254478dfa4c24a2", "362f1a6223a390d9",
    "e92e14f046052efd",
)

# Sanity bounds for the register's points: the city's extent plus a margin.
TUCSON_BBOX = {
    "lat_min": 31.95,
    "lat_max": 32.45,
    "lon_min": -111.20,
    "lon_max": -110.65,
}
