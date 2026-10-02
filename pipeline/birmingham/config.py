"""Birmingham (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/birmingham.md) on Manchester (Regional)'s contract: the shared
steps are pipeline/countries/uk.py and uk_fetch.py.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

SLUG = "birmingham"
CITY_NAME = "Birmingham (Regional)"
ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / SLUG / "raw"
DATA_PROCESSED = ROOT / "data" / SLUG / "processed"
OUTPUTS = ROOT / "outputs" / SLUG

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the scope, with where each is (a citable scoping record).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs, all keyless, downloaded by fetch_sources.py ---------------
#
# Scope: the three authorities West Midlands Metro serves today (owner,
# 2026-10-01). Dudley (409) joins only when Line 2 is in passenger service
# (pre-approved); on 2026-10-02 it was not (NOT_DRAWN below). The FSA's bulk
# XML per authority, named by CODE (the FSA's West Midlands region holds many
# more), exactly 3 asserted.
FSA_AUTHORITIES = {"402": "Birmingham", "423": "Sandwell", "436": "Wolverhampton"}
FSA_AUTHORITY_COUNT = 3
FSA_FILE_URL = "https://ratings.food.gov.uk/OpenDataFiles/FHRS{code}en-GB.xml"
FSA_RAW_DIR = DATA_RAW / "fsa"

# Postcode centroids: OS Code-Point Open, London's file and edition (copied,
# not downloaded again), kept to the scope's GSS codes.
CODEPOINT_ZIP = DATA_RAW / "codepo_gb.zip"
CODEPOINT_SOURCE = ROOT / "data" / "london" / "raw" / "codepo_gb.zip"
CODEPOINT_CRS = "EPSG:27700"   # British National Grid eastings / northings
CODEPOINT_DISTRICTS = ("E08000025", "E08000028", "E08000031")
# London's centroid tier (owner, 2026-09-28; the UK six's kit, 2026-10-01).
PLACE_AT_CENTROIDS = True

# The scope's OSM boundary relations, each polygonised from its outer ways
# and unioned; gated on the union's area so a truncated answer cannot pass.
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
BOUNDARY_OSM_RELATIONS = {162378: "Birmingham", 162485: "Sandwell", 173722: "Wolverhampton"}
BOUNDARY_AREA_KM2 = (400, 445)   # the three authorities, about 423 km2

# Rail: West Midlands Metro, OpenStreetMap. One query (uk_fetch.osm_query): the bbox's
# route=tram relations and the boundaries with geometry, the routes' member
# ways' tags and member nodes. The lead runs it; agents read the cache.
OSM_BBOX = (52.45, -2.15, 52.6, -1.85)
OSM_ROUTES = ("tram",)
OSM_JSON = DATA_RAW / "osm.json"
SCOPE_LABEL = "the three Metro authorities (Birmingham, Sandwell and Wolverhampton)"

# OSM's 7 tram relations (2026-10-02): six of ref 1, the service patterns of
# one line (Wolverhampton Station or Wolverhampton St Georges to Edgbaston
# Village, each way, and the Millennium Point branch, each way), and one of
# ref 2. The two light_rail relations in the bbox (the Stourbridge Town
# shuttle, national rail) are outside OSM_ROUTES.
OSM_REFS = ("1",)
LINE2_REASON = "Line 2 (Wednesbury - Dudley), not yet in passenger service; due 2026-11-01"
# Line 2's stops are tagged railway=construction in OSM, and the operator's maps
# page (westmidlandsmetro.com/maps/, read 2026-10-02) lists none of them: its
# 35 stops are all Line 1's. The opening missed its 28 August 2026 date.
NOT_DRAWN = {17248967: LINE2_REASON}

# The four Wolverhampton - Edgbaston Village relations list their stop nodes
# with an EMPTY role (2026-10-02): 118 role-less memberships, 25 stops no
# role-"stop" member of ref 1 carries. uk.elements() reads their named,
# stop-tagged, role-less members as role "stop", and stops once a listed
# relation has none left.
_ROLELESS = "stop members listed with an empty role (2026-10-02)"
ROLELESS_STOP_RELATIONS = {18094029: _ROLELESS, 18094030: _ROLELESS,
                           18094031: _ROLELESS, 18094032: _ROLELESS}
# One stop, two spellings across the two directions (the brief).
STATION_NAME_ALIASES = {"Dudley Street, Guns Village": "Dudley Street Guns Village"}

# One drawn line: the six ref-1 relations merged by London's branch rule, on
# Birmingham's thresholds. Measured 2026-10-02: the Eastside branch adds about
# 415 m of track beyond 30 m of the main relation and the St Georges stub 72 m,
# under the defaults (300 m, 1,000 m), which left Millennium Point 397 m,
# Albert Street 220 m and Wolverhampton St Georges 100 m off the drawn line.
# At 30 m and 50 m, 3 of the 6 relations are drawn (23.8 km) and every station
# is within 4 m of the line.
BRANCH_NEAR_M = 30
BRANCH_MIN_NEW_M = 50
LINE_OSM_REFS = {"1": ("1",)}
LINE_ORDER = list(LINE_OSM_REFS)
# The operator's maps page names no line: it lists one network's stops and
# calls the service "the Metro". With Line 2 not yet open, the label is the
# system's public name, as the one-line precedents (Odense Letbane, Sun Link,
# KC Streetcar). The legend row reads "<label> <legend name>".
LINE_NAMES = {"1": "West Midlands Metro"}
LEGEND_NAMES = {"1": "(Wolverhampton - Edgbaston Village)"}
# OSM's colour on every ref-1 relation; LINE_COLOURS below is what is drawn,
# after scripts/line_colour_search.py.
LINES = {"1": {"hue": "#ec008c"}}
# `python scripts/line_colour_search.py birmingham`, run 2026-10-02: the
# nearest feasible colour to OSM's #ec008c, 45.2 from every pin, 4.81:1 on the
# dark page and 3.89:1 on the light one; one line, so no pair to separate.
LINE_COLOURS = {"1": "#F000B8"}

# GATE 3 - the operator's stop list, counted before the scope split. The maps
# page lists 35 stops (its stop links and its zone list, read 2026-10-02), all
# on Line 1, Albert Street and Millennium Point (the Eastside extension's open
# stops) included.
OPERATOR_STATION_COUNTS = {"1": 35}
OPERATOR_COUNTS_SOURCE = ("West Midlands Metro, westmidlandsmetro.com/maps/: 35 stops "
                          "(read 2026-10-02)")
# The tram floor for the station gates (Odense's 350 m, Kansas City's 150 m):
# a collapsed set under it is still platforms.
SPACING_MIN_M = 350.0
# Halved rings: the median gap in scope is 442 m (2026-10-02, 35 stations),
# under the spacing rule's 550 m (docs/ring_rules.md). Step 1 stops outside
# this band.
MEDIAN_GAP_BOUNDS_M = (390.0, 500.0)

# NaPTAN's names for two built stops: "Centenary Square" is OSM's "Library"
# (6 m apart; the operator writes "Library Centenary Square"), and
# "Wednesbury Central" is OSM's "Wednesbury, Great Western Street" (98 m apart;
# the next stop, Wednesbury Parkway, is 537 m away; the operator writes
# "Wednesbury Great Western Street").
NAPTAN_NAME_ALIASES = {
    "Centenary Square": "Library",
    "Wednesbury Central": "Wednesbury, Great Western Street",
}
EASTSIDE_REASON = ("Eastside extension stop beyond Millennium Point, not yet in passenger "
                   "service (not on the operator's maps page, 2026-10-02)")
# NaPTAN's active MET records inside the scope that no built station matches:
# Line 2's five inside Sandwell, and three Eastside stops not yet open.
NAPTAN_EXPLAINED = {
    "Birmingham New Road": LINE2_REASON,
    "Dudley Port": LINE2_REASON,
    "Great Bridge": LINE2_REASON,
    "Horseley Road": LINE2_REASON,
    "Sedgley Road": LINE2_REASON,
    "Curzon Street": EASTSIDE_REASON,
    "Digbeth High Street": EASTSIDE_REASON,
    "Meriden Street": EASTSIDE_REASON,
}

# NaPTAN (DfT, OGL v3): gate 3's second independent source (owner,
# 2026-10-01). ATCO area 940 is the national tram and metro area, where every
# tram stop is filed; step 1 reads the active MET records with these ATCO
# prefixes inside the scope.
NAPTAN_PREFIXES = ("9400ZZWM",)
NAPTAN_ATCO_AREAS = ("940",)
NAPTAN_RAW_DIR = DATA_RAW / "naptan"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-1.89) falls in the -6 to 0 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson. London's,
# Glasgow's and Newcastle's distance CRS too; British National Grid is only
# Code-Point's own CRS (CODEPOINT_CRS above).
CRS_PROJECTED = "EPSG:32630"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# Halved (the tram-city skill, section 3; Aarhus's): the median gap is 442 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Business filtering ------------------------------------------------

CITY_KEEP = "the three Metro authorities"

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: the scope's extent plus a margin. The polygon does the
# filtering; this catches a CRS or axis error.
BUSINESS_BBOX = {"lat_min": 52.36, "lat_max": 52.66, "lon_min": -2.23, "lon_max": -1.7}
