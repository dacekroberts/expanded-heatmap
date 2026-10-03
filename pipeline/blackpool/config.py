"""Blackpool (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/blackpool.md) on Manchester (Regional)'s contract: the shared
steps are pipeline/countries/uk.py and uk_fetch.py.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

SLUG = "blackpool"
CITY_NAME = "Blackpool (Regional)"
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
# Scope: Blackpool with Wyre (owner, 2026-10-01); never Lancashire. The FSA's bulk XML per authority, named by CODE
# (NOT Wyre Forest (153), a West Midlands council with a near-identical name), exactly 2 asserted.
FSA_AUTHORITIES = {"898": "Blackpool", "207": "Wyre"}
FSA_AUTHORITY_COUNT = 2
FSA_FILE_URL = "https://ratings.food.gov.uk/OpenDataFiles/FHRS{code}en-GB.xml"
FSA_RAW_DIR = DATA_RAW / "fsa"

# Postcode centroids: OS Code-Point Open, London's file and edition (copied,
# not downloaded again), kept to the scope's GSS codes.
CODEPOINT_ZIP = DATA_RAW / "codepo_gb.zip"
CODEPOINT_SOURCE = ROOT / "data" / "london" / "raw" / "codepo_gb.zip"
CODEPOINT_CRS = "EPSG:27700"   # British National Grid eastings / northings
CODEPOINT_DISTRICTS = ("E06000009", "E07000128")
# London's centroid tier (owner, 2026-09-28; the UK six's kit, 2026-10-01).
PLACE_AT_CENTROIDS = True

# The scope's OSM boundary relations, each polygonised from its outer ways
# and unioned; gated on the union's area so a truncated answer cannot pass.
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
BOUNDARY_OSM_RELATIONS = {148603: "Blackpool", 148604: "Wyre"}
BOUNDARY_AREA_KM2 = (355, 390)   # 372.1 km2 measured 2026-10-02: OSM draws both coastal boundaries to low water (Blackpool 43.1, Wyre 329.0), against about 318 km2 of land

# Rail: Blackpool Tramway, OpenStreetMap. One query (uk_fetch.osm_query): the bbox's
# route=tram relations and the boundaries with geometry, the routes' member
# ways' tags and member nodes. The lead runs it; agents read the cache.
OSM_BBOX = (53.77, -3.07, 53.94, -2.98)
OSM_ROUTES = ("tram",)
OSM_JSON = DATA_RAW / "osm.json"
SCOPE_LABEL = "Blackpool and Wyre"

# NaPTAN (DfT, OGL v3): gate 3's second independent source (owner,
# 2026-10-01). ATCO area 940 is the national tram and metro area, where every
# tram stop is filed; step 1 reads the active MET records with these ATCO
# prefixes inside the scope.
# The prefix also holds one London station (Battersea Power Station, measured 2026-10-02); the scope polygon keeps it out.
NAPTAN_PREFIXES = ("9400ZZBP",)
NAPTAN_ATCO_AREAS = ("940",)
NAPTAN_RAW_DIR = DATA_RAW / "naptan"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-3.05) falls in the -6 to 0 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson. London's,
# Glasgow's and Newcastle's distance CRS too; British National Grid is only
# Code-Point's own CRS (CODEPOINT_CRS above).
CRS_PROJECTED = "EPSG:32630"

# --- Ring geometry ---------------------------------------------------------
# Halved (Aarhus's): tram stops at a 357 m median gap (MEDIAN_GAP_BOUNDS_M).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Business filtering ------------------------------------------------

CITY_KEEP = "Blackpool and Wyre"

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: the scope's extent plus a margin. The polygon does the
# filtering; this catches a CRS or axis error.
BUSINESS_BBOX = {"lat_min": 53.74, "lat_max": 54.0, "lon_min": -3.1, "lon_max": -2.55}

# --- Step 1: lines and stations -------------------------------------------

# OSM's 2 tram relations, both ref T1 (7119569 "Blackpool Tramway Southbound",
# 10841330 "Northbound"; no network, operator or colour tags), one per
# direction, Starr Gate to Fleetwood Ferry. Both carry the Blackpool North
# spur (opened 2024): each runs via North Station, its stop a member of
# both (measured 2026-10-02). Both are kept for their stops; the branch rule
# draws the longer (18.8 km), whose track passes 4.9 m from North Station,
# so the spur survives the default thresholds.
OSM_REFS = ("T1",)
NOT_DRAWN = {}
# North Pier's two stop positions sit either side of Talbot Square, the
# spur's junction stop (northbound north of it, southbound south), 216 m
# apart: one stop, so the collapse limit is Den Haag's 250 m, not 200.
COLLAPSE_MAX_SPREAD_M = 250

# OSM's relations are the operator's one line, so the line is its relations
# merged by London's branch rule (no LINE_STOPS).
LINE_OSM_REFS = {"T1": ("T1",)}
LINE_ORDER = list(LINE_OSM_REFS)
# The on-map label is the operator's public name (the brief; its site refuses
# scripts). The legend row reads "<label> <legend name>"
# (map_common.build_legend), so the legend name is the line's ends, as OSM's
# from/to tags write them.
LINE_NAMES = {"T1": "Blackpool Tramway"}
LEGEND_NAMES = {"T1": "(Starr Gate - Fleetwood Ferry)"}
# OSM records no colour and the operator's site refuses scripts, so the hue
# is the project's own (the tram kit's call 3); LINE_COLOURS below is what is
# drawn, after scripts/line_colour_search.py.
LINES = {"T1": {"hue": "#6A2C91"}}
# `python scripts/line_colour_search.py blackpool`, run 2026-10-02: the hue's
# nearest feasible colour, 45.1 from every pin, 3:1 on both pages (dark 3.24,
# light 5.78); one line, so no pair to separate.
LINE_COLOURS = {"T1": "#9840A8"}

# GATE 3 - NaPTAN only. blackpooltransport.com returns 403 to a script
# (staging's screen, 2026-10-01; one plain request, 2026-10-02); it is not
# passed. NaPTAN is then the only independent source (owner, 2026-10-01), run
# name by name in step 1.
OPERATOR_STATION_COUNTS = None
OPERATOR_COUNTS_GAP = ("blackpooltransport.com returns 403 to a script request "
                       "(2026-10-01 and 2026-10-02); it is not passed, so NaPTAN is "
                       "the only independent source (owner, 2026-10-01)")
OPERATOR_COUNTS_SOURCE = None
# The tram floor for the station gates (Odense's 350 m, Kansas City's 150 m):
# a collapsed set under it is still platforms. Kansas City's, since the
# promenade stops' 357 m median sits too near Manchester's 350.
SPACING_MIN_M = 150.0
# Halved rings: the median gap in scope is 357 m (2026-10-02; min 105 m,
# North Pier to Talbot Square, two stops NaPTAN also holds), under the
# spacing rule's 550 m (docs/ring_rules.md). Step 1 stops outside this band.
MEDIAN_GAP_BOUNDS_M = (315.0, 400.0)
NAPTAN_EXPLAINED = {}
# NaPTAN's spelling -> the built (OSM) station, for the same stop under a
# shorter name, each paired by its NaPTAN record's position (measured
# 2026-10-02, distance to the OSM stop positions' centroid). The map keeps
# OSM's names.
NAPTAN_NAME_ALIASES = {
    "Anchorsholme": "Anchorsholme Lane",   # 4 m
    "St Chad's": "St Chad's Road",         # 4 m
    "Talbot Road": "Talbot Square",        # 3 m; NaPTAN's record created 2024-05-29, with the spur
}
