"""Tacoma-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

TACOMA, WASHINGTON, on Kansas City's template (a US register on NAICS, the
shared `pipeline/osm_tram.py`, the TIGER place polygon) with Vancouver's name
rule (docs/build_briefs/tacoma.md). The register is the City's "Business
Licenses - Map (Tacoma)" point layer, refreshed daily: active Tax & License
accounts, already placed, so there is no address join and no geocoder. Rail
from OpenStreetMap: Sound Transit's GTFS is not used (owner, 2026-10-02, for
Seattle; the brief).
"""

from pathlib import Path

SLUG = "tacoma"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "tacoma" / "raw"
DATA_PROCESSED = ROOT / "data" / "tacoma" / "processed"
OUTPUTS = ROOT / "outputs" / "tacoma"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# T Line stops outside the city, with the reason (the Los Angeles rule).
# Every stop is inside, so today it is header-only.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) ----------------

# "Business Licenses - Map (Tacoma)", ArcGIS item 2fa3b14b4de44c16b44893fee2cadefd
# (owner IT.OpenDataMgr, credit "City of Tacoma, Tax & License"): the POINT
# layer, never the table item 8efa2724e88a44a286894d33cb5fb331, which carries
# the same rows without geometry (the brief). Published on data.tacoma.gov;
# the item's licenseInfo still links data.cityoftacoma.org, a host that no
# longer resolves, so data.tacoma.gov is what is cited.
REGISTER_ITEM = "2fa3b14b4de44c16b44893fee2cadefd"
REGISTER_URL = ("https://services3.arcgis.com/SCwJH1pD8WSn5T5y/arcgis/rest/services/"
                "BusinessLicenses_Map/FeatureServer/0")
# An explicit column list. The mailing_* fields are NEVER fetched (Den Haag's
# precedent): a mailing address is where the owner gets post, often a home,
# and it never places or labels a pin (the brief).
REGISTER_FIELDS = ("objectid", "license_number", "business_name", "trade_name",
                   "naics_code", "naics_code_description", "business_open_date",
                   "site_street", "site_unit_number", "site_city", "site_state",
                   "site_zip_code", "council_district", "map_status", "x", "y")
REGISTER_CSV = DATA_RAW / "business_licenses.csv"

# THE CENSUS BUREAU'S PLACE POLYGON (TIGERweb, current Incorporated Places,
# GEOID 5370000 Tacoma city; public domain) - Kansas City's and Tucson's layer.
CITY_BOUNDARY_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
                     "Places_CouSub_ConCity_SubMCD/MapServer/4/query")
CITY_GEOID = "5370000"
CITY_BOUNDARY_QUERY = {"where": f"GEOID='{CITY_GEOID}'",
                       "outFields": "GEOID,NAME,AREALAND,AREAWATER",
                       "outSR": "4326", "f": "geojson"}
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary_tiger.geojson"
# The polygon's area, land and water (Census: 128.9 km2 land, 32.9 water; 161.7
# in UTM 10N, 2026-10-04); step 1 stops outside these bounds.
CITY_AREA_KM2 = (150.0, 175.0)

# OSM: the T Line's relations in a box around downtown Tacoma, Hilltop and the
# Tacoma Dome, on either route mode OSM may tag it with (the brief: read
# whether it is route=tram or route=light_rail).
RAIL_BBOX = (47.22, -122.48, 47.28, -122.41)        # south, west, north, east
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 10N: the longitude (~-122.44) falls in the -126 to -120 band.
# Derived per city, not copied. The register's own geometry is EPSG:2927
# (Washington State Plane South, US feet); the fetch asks for outSR=4326.
CRS_PROJECTED = "EPSG:32610"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED on the spacing rule: the 12 stops' median gap is 451 m (2026-10-04;
# the brief's 452-469 m in Sound Transit's feed), under 550 m. Step 1 prints
# the median again and stops outside 400-500 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (400.0, 500.0)

# --- Station scope: EVERY STOP, 12 --------------------------------------------
#
# The T Line is one line, Tacoma Dome to St Joseph with the Hilltop extension
# (opened September 2023): two `route=tram` relations, one per direction, ref
# "T Line", network Link, operator Sound Transit (5705256 and 5705257, read
# 2026-10-04), sharing the same 12 stop nodes. No other tram or light rail in
# the box. Every stop is kept (owner: no thinning on the tram list).
ROUTES = ("tram", "light_rail")
OPERATOR = "Sound Transit"
LINE_REFS = ("T Line",)
NOT_DRAWN = {}
STATION_ADD = {}
EXPECTED_STATIONS = 12

# GATE 3: the operator's own stop count, independent of OSM. Sound Transit's
# T Line page names 12 stations, St Joseph to Tacoma Dome, the same 12 the
# build draws (it writes "S 25th" where OSM writes "S 25th St"). Read for the
# count only; Sound Transit's GTFS is not used (owner).
OPERATOR_STATION_COUNTS = {"T Line": 12}
OPERATOR_COUNTS_SOURCE = (
    "Sound Transit, 'T Line' (https://www.soundtransit.org/ride-with-us/routes-schedules/"
    "t-line): 12 stations; primary; read 2026-10-04")

SPACING_MIN_M = 150.0

DRAWN_LINES = ("T Line",)
# The line's public name (the brief). No Sound Transit logo.
LINE_NAMES = {"T Line": "T Line"}
# OSM's colour on both relations, the T Line's orange (#F38B00): CIE76 77.9
# from the nearest pin color (Food service), its label 4.5:1 in both themes
# (check_map_markup.py, 2026-10-04).
LINE_COLOURS = {"T Line": "#F38B00"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "naics"
RAW_CLASSIFICATION_COLUMN = "naics_code"

# The register's own in-city marker: a council district 1-5. Rows without one
# are outside the city or "Not Mapped" (the brief: 11,812 in the city).
IN_CITY_DISTRICTS = ("1", "2", "3", "4", "5")

# Sanity bounds for the register's points: the city's extent plus a margin.
TACOMA_BBOX = {
    "lat_min": 47.10,
    "lat_max": 47.40,
    "lon_min": -122.65,
    "lon_max": -122.30,
}
