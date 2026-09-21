"""San Francisco-specific settings. Same shape as pipeline/san_diego/config.py
- see that file's docstring for why this is per-city rather than a shared
registry loader (San Diego was city #1, proving the pattern; this is city
#2, still not enough to safely generalize from two data points).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "san_francisco" / "raw"
DATA_PROCESSED = ROOT / "data" / "san_francisco" / "processed"
OUTPUTS = ROOT / "outputs" / "san_francisco"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Documents every surface stop the sub-transit-line-filters process cut,
# with which line it belonged to and why - see
# docs/sub_transit_line_filters.md. Committed (outputs/, not
# data/processed/) since it's a citable record of a real scope decision.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs. Download commands (all public); also in docs/data_sources.md.
# This block was added 2026-09-21, after writing that file found San
# Francisco's boundary endpoint recorded nowhere at all - the layer was in the
# gitignored raw folder with no way to re-fetch it. Identified from the file's
# own fields (objectid / fipsstco / county, FIPS 06075) and confirmed to
# reproduce it byte-for-byte, 38,822 bytes with identical geometry.
#   gtfs.zip  SFMTA Muni. The official host (sfmta.com/reports/gtfs-transit-data)
#     timed out from this environment; this mirror is linked from that page:
#       curl -sL https://muni-gtfs.apps.sfmta.com/data/muni_gtfs-current.zip
#   sf_business_locations.csv  Socrata "Registered Business Locations"
#     (g8m3-pdis), filtered to San Francisco at download:
#       curl -sG https://data.sf.gov/resource/g8m3-pdis.csv
#   sf_county_boundary.geojson  Socrata "Bay Area County Polygons"
#     (wamw-vt4s) - a nine-county Bay Area layer, so it MUST be filtered to
#     the one county:
#       curl -sG https://data.sfgov.org/resource/wamw-vt4s.geojson
#         --data-urlencode "$where=county='San Francisco'"
#         --data-urlencode '$limit=10'
GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "sf_business_locations.csv"
COUNTY_BOUNDARY_GEOJSON = DATA_RAW / "sf_county_boundary.geojson"
COUNTY_BOUNDARY_URL = (
    "https://data.sfgov.org/resource/wamw-vt4s.geojson"
    "?$where=county%3D%27San%20Francisco%27&$limit=10"
)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 10N. San Francisco's longitude (~-122.4) falls in the -126 to
# -120 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32610"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# Muni Metro proper: J Church, K Ingleside, L Taraval, M Ocean View,
# N Judah, T Third Street - route_type "0" (tram/light rail) in the GTFS
# feed. Deliberately excludes the F Market & Wharves heritage streetcar
# (also route_type 0, but a separate branded service - different rolling
# stock, not part of "Muni Metro" in SFMTA's own naming) and the CA/PH/PM
# cable cars (route_type 5, a different mode entirely). Same real-world-
# name-grounded scoping as San Diego's Trolley - include the system riders
# actually call by this name, not everything technically rail-adjacent.
MUNI_METRO_ROUTE_IDS = ["J", "K", "L", "M", "N", "T"]

# Real public-facing names (confirmed against route_long_name in the GTFS
# feed itself, which matches common usage/signage - "J Church" etc.).
MUNI_METRO_LINE_NAMES = {
    "J": "J Church",
    "K": "K Ingleside",
    "L": "L Taraval",
    "M": "M Ocean View",
    "N": "N Judah",
    "T": "T Third Street",
}

# Raw GTFS stop names that are the SAME physical station but were named
# inconsistently by different lines' own trips (not a direction-suffix
# pattern step1_stations.py's regex can catch generally - these needed a
# real proximity check to find: 2026-09-18, checked every pair
# of selected stations for physical distance, found these 4 pairs each
# under 200 feet apart). Left side merges into the right side's name.
STATION_NAME_ALIASES = {
    "Van Ness Station": "Metro Van Ness Station",
    "Church St & Market St": "Metro Church Station",
    "Forest Hill Station": "Metro Forest Hill Station",
    "King St & 4th St": "4th St & King St",
}

# Canonical-name substrings identifying a stop as underground/grade-
# separated Muni Metro subway (as opposed to surface street-running) -
# the Twin Peaks Tunnel corridor (Embarcadero through West Portal) plus
# the Chinatown Central Subway extension, plus the two BART-interchange
# stops. These are always kept in step1_stations.py's station selection,
# exempt from the surface-stop thinning filter - see that file's module
# docstring for the full reasoning (a real check found subway-only scope
# would miss three whole districts the surface network reaches).
SUBWAY_STATION_KEYWORDS = [
    "Metro ",
    "Forest Hill Station",
    "West Portal Station",
    "Union Square/Market St",
    "Yerba Buena/Moscone",
    "Chinatown - Rose Pak",
    "Balboa Park BART",
    "San Jose Ave/Glen Park",
]

# Target spacing (miles, measured along each line's real stop-to-stop
# path, not airline distance) for thinning surface stops - chosen
# specifically because Muni Metro's
# street-running stops (every 1-2 blocks) are far denser than this
# project's ring geometry assumes; unthinned, nearly every point in the
# west/south city would read as "within 0.1mi of a station."
STATION_SPACING_MILES = 0.5

# San Francisco is a consolidated city-county, so its own county boundary
# IS its city boundary - one polygon, not a "pick the right one out of a
# regional layer" step like San Diego's Municipal_Boundaries.geojson
# needed. Muni Metro is also entirely an SFMTA (city) service, unlike San
# Diego's Trolley which crosses into six other cities - so this spatial
# filter is expected to keep every Muni Metro station, not narrow the
# list the way San Diego's did. Still run for real rather than assumed -
# see the add-city skill's Step 0.
COUNTY_BOUNDARY_NAME = "San Francisco"

# --- Business filtering ------------------------------------------------

CITY_KEEP = "San Francisco"
# NAICS catch-all codes excluded for THIS city (the verdict is per city - see
# NAICS_CATCHALL_CODES_TO_CHECK in pipeline/taxonomies/naics.py). Applied as its
# own printed filter in step 2.
#
#   812990  In San Francisco's own licence data this code is labelled "SOLO
#     MASSAGE ESTABLISHMENT", not the generic "All Other Personal Services".
#     Sampled 2026-09-21: 414 mapped pins, of which 31 (7%) carried a
#     person-like name at an address with a residential indicator - the highest
#     residential share of any category in this city. A sole operator working
#     from home is a sensitive thing to pin on a public map, and the category is
#     a small share of the total, so it is excluded here.
NAICS_EXCLUDE_CODES = {"812990"}

TAXONOMY_SYSTEM = "naics"
# The raw export's own classification column (self-reported by the
# business). Step 2 renames it to the taxonomy's VALUE_COLUMN, then
# filters via pipeline.taxonomies.
RAW_CLASSIFICATION_COLUMN = "self_reported_naics_code"

# Sanity bounds - San Francisco county's own bounds extend far offshore
# (the Farallon Islands are part of the county), so this is tighter than
# the county polygon itself: the developed city proper, not the full
# county extent, to catch any genuinely bad geocode.
SAN_FRANCISCO_BBOX = {
    "lat_min": 37.70,
    "lat_max": 37.83,
    "lon_min": -122.52,
    "lon_max": -122.35,
}
