"""Tbilisi-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

One national register (Geostat's Statistical Business Register, a keyless
JSON API) filtered to the FACTUAL address in the city of Tbilisi, and the
metro from OpenStreetMap. Every endpoint and trap is in
docs/georgia_step0_endpoints.md; the build brief is docs/build_briefs/tbilisi.md.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "tbilisi" / "raw"
DATA_PROCESSED = ROOT / "data" / "tbilisi" / "processed"
OUTPUTS = ROOT / "outputs" / "tbilisi"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
PROVENANCE_JSON = OUTPUTS / "provenance.json"
# Every station is inside the city, so this is written with a header and no
# rows (Calgary's precedent): a citable record that nothing was excluded.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
CITY_BOUNDARY_GEOJSON = DATA_PROCESSED / "city_boundary.geojson"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- The register --------------------------------------------------------

AS_OF_DATE = "2026-10-02"

# Geostat's Statistical Business Register. One row per ECONOMIC ENTITY (a
# legal person or an individual entrepreneur), not per premises: a chain is
# one row at one factual address (the undercount the owner accepted,
# disclosed). `factualAddressRegion` filters on where the entity OPERATES;
# `legalAddressRegion` would map registered offices. Both filters were proved
# against a nonsense value (total 0).
GEOSTAT_API = "https://br-api.geostat.ge/api/documents"
GEOSTAT_QUERY = {"factualAddressRegion": "11", "isActive": "true", "lang": "en"}
# 2,000 rows a page: on 2026-10-02 a 2,000-row page took 48 s and a
# 10,000-row page outlasted the gateway (HTTP 502), though Step 0 pulled
# 10,000-row pages the same morning. 32 pages, well inside the 50-request
# window.
GEOSTAT_PAGE_SIZE = 2000
# Measured 2026-10-02: 63,511 active rows. A total outside this band is a
# changed filter or a changed register, not a refresh.
GEOSTAT_TOTAL_RANGE = (60000, 67000)
GEOSTAT_PAGE_PAUSE_S = 3
GEOSTAT_TERMS_URL = "https://www.geostat.ge/en/page/monacemta-gamoyenebis-pirobebi"
BUSINESSES_RAW_CSV = DATA_RAW / f"geostat_br_tbilisi_active_{AS_OF_DATE}.build.csv"

# The only columns written to disk. The API has no column selection, so
# every other key (personal numbers, heads, partners, phone, e-mail, web,
# both address strings) is dropped in memory, page by page, before anything
# is written; step 2 asserts the absence of PERSONAL_COLUMNS.
KEEP_COLUMNS = [
    "Stat_ID", "Legal_Form_ID", "Legal_Form", "Ownership_Type",
    "Region_Code2", "City_Code2", "City_name2",
    "Activity_2_Code", "Activity_2_Name", "ISActive", "Zoma",
    "X", "Y", "Init_Reg_date", "Reg_Date",
]
PERSONAL_COLUMNS = [
    "Legal_Code", "Personal_no", "Head", "Head_PN", "Partner", "Partner_PN",
    "mob", "Email", "web", "Address", "Address2",
]
# Legal form 30 is the individual entrepreneur ("Individual Entreprises",
# sic; Stat_ID_Type 2, a natural person). Their Full_Name is the person's own
# name and is never written: the pin shows the category only (owner,
# 2026-10-01; Taichung's precedent).
INDIVIDUAL_ENTREPRENEUR_FORM = "30"
# Columns derived in memory from the dropped address strings, holding no
# street address: `factual_address_key` is, for a legal entity, its factual
# address when that carries no digit (a bare district or settlement name, the
# placeholder test below), "" when blank, and otherwise "#" plus a 12-hex
# hash of the normalised address, so the commonest address at a point can be
# found without storing one; an individual entrepreneur's is "#" or "".
# `legal_eq_factual` is the only residence proxy the register offers (3.5% of
# kept individual entrepreneurs, measured 2026-10-02: too weak to act on,
# recorded).
DERIVED_COLUMNS = ["Full_Name", "factual_address_key", "legal_eq_factual"]

# X is LATITUDE and Y is LONGITUDE (the register app reads `lat: X, lng: Y`).
LAT_COLUMN = "X"
LON_COLUMN = "Y"

# --- Placeholder coordinates ----------------------------------------------
# 91% of rows carry a coordinate, but some coordinates are district or
# settlement centroids that dozens of businesses share. Rule (owner,
# 2026-10-02, "approve all three"): a point carrying PLACEHOLDER_MIN_ROWS or
# more rows (all active rows, not only storefronts) whose commonest legal-
# entity factual address is a bare district or settlement name, or blank, is
# a placeholder; its rows are dropped and disclosed. Step 2 re-derives the
# set and exits if it differs from this list, so a refresh that moves a
# centroid is seen, not absorbed. Measured at Step 0, 2026-10-02: ten points, 1,295
# kept rows, 805 of them on four metro stations.
#
# ⚠ THE BUILD'S PULL CANNOT TAKE "COMMONEST" IN FULL. It kept every numbered
# address as one marker, so step 2 runs a BOUNDED check on it: every point
# the pull proves qualifies must be listed (it proved one more, Mtatsminda,
# added), and every listed point must still carry 50+ rows. 33 points could
# not be settled that way (1,629 storefronts; at nearly all, the commonest
# bare name appears 1-4 times against dozens of street addresses). The full
# check runs on the next pull, whose fetch keeps a hash per address (owner,
# 2026-10-02: skip the re-pull for this build, run it before the next review).
PLACEHOLDER_MIN_ROWS = 50
PLACEHOLDER_POINTS = {
    (41.68655, 44.840891): "Isani district (77 m from Isani station)",
    (41.749448, 44.779977): "blank addresses (1 m from Didube station)",
    (41.725938, 44.750388): "Saburtalo district centroid",
    (41.685844, 44.853535): "blank addresses (87 m from Samgori station)",
    (41.693803, 44.801517): "seven districts on one point (113 m from Liberty Square)",
    (41.789026, 44.810777): "Nadzaladevi, blank addresses",
    (41.709599, 44.756885): "Vake district centroid",
    (41.72151, 44.762499): "Digomi village centroid",
    (41.695, 44.789167): "three-decimal point, city center",
    (41.613415, 44.908357): "Krtsanisi, blank addresses",
    # Proved by the build's pull: 27 of the point's 28 companies give the bare
    # district name, against one street address.
    (41.695863, 44.792928): "Mtatsminda district, bare addresses",
}
# Coordinates are compared at this many decimals (the register carries 6-7
# or 12-15; two geocoding generations).
PLACEHOLDER_DECIMALS = 6

# --- Rail (OpenStreetMap) ---------------------------------------------------

# ONE Overpass query per city (owner, 2026-09-30): the metro's route
# relations, their route_masters, member nodes, track ways with geometry,
# every station=subway node, and the city's administrative boundary for the
# pin sanity check. The brief's Step 0 cache (osm_metro.json, the same day)
# lacks the boundary, so the build issues this one query once.
OSM_BBOX = (41.60, 44.65, 41.86, 45.05)
OSM_JSON = DATA_RAW / "osm_tbilisi.json"
OSM_BOUNDARY_NAME_EN = "Tbilisi"

LINE_REFS = {"1": "Akhmeteli-Varketili Line", "2": "Saburtalo Line"}
# OSM's colours: line 1 `#FF0000`; line 2 `green`, a CSS keyword rather than
# an operator hex. Its CSS value, #008000, measured CIE76 37.2 against the
# Personal services pins, under the preferred 45 (pipeline/linecolour.py);
# #30A800 is the nearest green that clears it (45.5), as Seattle's line
# colours were moved (DECISIONS drafts, seattle-tbilisi).
LINE_COLOURS = {"1": "#FF0000", "2": "#30A800"}
# Gate 3: "27.3 km with 23 stations on two lines" (Tbilisi Transport Company,
# Stakeholder Engagement Plan, October 2024). Per line, 16 + 7, as OSM's
# relations carry them; the operator states the total.
OPERATOR_STATION_TOTAL = 23
OPERATOR_STATION_COUNTS = {"Akhmeteli-Varketili Line": 16, "Saburtalo Line": 7}
OPERATOR_COUNTS_SOURCE = ("https://ttc.com.ge/sites/default/files/2024-10/"
                          "Tbilisi%20Metro_New%20RS_SEP_09Oct2024_0.pdf")
# Station Square-1 and Station Square-2 are 110 m apart and both are in the
# operator's count: both drawn, under their real names.
SPACING_MIN_M = 100
# OSM writes "Nadzaledevi"; the operator and the register write Nadzaladevi.
STATION_NAME_FIXES = {"Nadzaledevi": "Nadzaladevi"}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 38N: the longitude (~44.79) falls in the 42 to 48 band. Derived per
# city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32638"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "georgia_nace"
RAW_CLASSIFICATION_COLUMN = "activity_label"

# Sanity bounds for the register's coordinates: the city of Tbilisi's extent
# with a margin. Step 2 also tests each pin against OSM's city boundary.
TBILISI_BBOX = {
    "lat_min": 41.55,
    "lat_max": 41.90,
    "lon_min": 44.55,
    "lon_max": 45.15,
}
