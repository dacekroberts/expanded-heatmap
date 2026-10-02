"""Nottingham (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/nottingham.md) on Manchester (Regional)'s contract: the shared
steps are pipeline/countries/uk.py and uk_fetch.py.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

SLUG = "nottingham"
CITY_NAME = "Nottingham (Regional)"
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
# Scope: the city, Broxtowe, Rushcliffe and Ashfield (owner, 2026-10-01); never Nottinghamshire (relation 181040). The FSA's bulk XML per authority, named by CODE
# (Gedling (262) has no stop), exactly 4 asserted.
FSA_AUTHORITIES = {"899": "Nottingham City", "261": "Broxtowe", "266": "Rushcliffe", "259": "Ashfield"}
FSA_AUTHORITY_COUNT = 4
FSA_FILE_URL = "https://ratings.food.gov.uk/OpenDataFiles/FHRS{code}en-GB.xml"
FSA_RAW_DIR = DATA_RAW / "fsa"

# Postcode centroids: OS Code-Point Open, London's file and edition (copied,
# not downloaded again), kept to the scope's GSS codes.
CODEPOINT_ZIP = DATA_RAW / "codepo_gb.zip"
CODEPOINT_SOURCE = ROOT / "data" / "london" / "raw" / "codepo_gb.zip"
CODEPOINT_CRS = "EPSG:27700"   # British National Grid eastings / northings
CODEPOINT_DISTRICTS = ("E06000018", "E07000172", "E07000176", "E07000170")
# London's centroid tier (owner, 2026-09-28; the UK six's kit, 2026-10-01).
PLACE_AT_CENTROIDS = True

# The scope's OSM boundary relations, each polygonised from its outer ways
# and unioned; gated on the union's area so a truncated answer cannot pass.
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
BOUNDARY_OSM_RELATIONS = {123292: "City of Nottingham", 154058: "Broxtowe", 77311: "Rushcliffe", 154043: "Ashfield"}
BOUNDARY_AREA_KM2 = (640, 700)   # the four authorities, about 673 km2 (mixed admin levels: the city 6, the districts 8)

# Rail: Nottingham Express Transit, OpenStreetMap. One query (uk_fetch.osm_query): the bbox's
# route=tram relations and the boundaries with geometry, the routes' member
# ways' tags and member nodes. The lead runs it; agents read the cache.
OSM_BBOX = (52.86, -1.3, 53.06, -1.1)
OSM_ROUTES = ("tram",)
OSM_JSON = DATA_RAW / "osm.json"
SCOPE_LABEL = "the four NET authorities (Nottingham, Broxtowe, Rushcliffe and Ashfield)"

# NaPTAN (DfT, OGL v3): gate 3's second independent source (owner,
# 2026-10-01). ATCO area 940 is the national tram and metro area, where every
# tram stop is filed; step 1 reads the active MET records with these ATCO
# prefixes inside the scope.
NAPTAN_PREFIXES = ("9400ZZNO",)
NAPTAN_ATCO_AREAS = ("940",)
NAPTAN_RAW_DIR = DATA_RAW / "naptan"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-1.15) falls in the -6 to 0 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson. London's,
# Glasgow's and Newcastle's distance CRS too; British National Grid is only
# Code-Point's own CRS (CODEPOINT_CRS above).
CRS_PROJECTED = "EPSG:32630"

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: the scope's extent plus a margin. The polygon does the
# filtering; this catches a CRS or axis error. Set from the boundary's bounds
# (lon -1.345 to -0.815, lat 52.789 to 53.171, 2026-10-02): the scaffold's box
# (lon_max -0.93, lat_max 53.16) cut 15 Rushcliffe premises inside the district.
BUSINESS_BBOX = {"lat_min": 52.74, "lat_max": 53.22, "lon_min": -1.40, "lon_max": -0.76}

# --- Step 1: the lines and stations ---------------------------------------
#
# OSM's 4 tram relations (network "NET", operator "Tramlink Nottingham", all
# #003828) are one per line per DIRECTION, each end to end, not half-lines:
# 170076 Line 1 North (Toton Lane - Hucknall), 1984324 Line 1 South, 1984359
# Line 2 North (Clifton South - Phoenix Park), 1984325 Line 2 South (read
# 2026-10-02). All four are kept, so each line's stops are both directions'
# union (Hyson Green's one-way pairs: Noel Street, Beaconsfield Street and
# Shipstone Street northbound; Radford Road and Hyson Green Market southbound).
OSM_REFS = ("1", "2")
NOT_DRAWN = {}
LINE_OSM_REFS = {"1": ("1",), "2": ("2",)}
# London's branch rule keeps one direction only (the other adds 0 m beyond
# 300 m), which leaves Hyson Green's northbound one-way street undrawn and
# Beaconsfield Street 232 m off the line. Beyond 30 m of the first direction the
# second adds 742 m in 8 parts on each line (measured 2026-10-02), so both are
# drawn and every station is within about 60 m of its line (31 m from the two
# directions' union; Birmingham lowers both too).
BRANCH_NEAR_M = 30
BRANCH_MIN_NEW_M = 500
LINE_ORDER = list(LINE_OSM_REFS)
# NET's own line names. The legend row reads "<label> <legend name>"
# (map_common.build_legend), so the legend name is the line's ends.
LINE_NAMES = {"1": "Line 1", "2": "Line 2"}
LEGEND_NAMES = {"1": "(Hucknall - Toton Lane)", "2": "(Phoenix Park - Clifton South)"}
# OSM gives both lines one colour (#003828) and NET's site shows no line
# colours, so two project hues; two lines with one colour are refused
# (Dijon). LINE_COLOURS below is what is drawn, after
# scripts/line_colour_search.py.
LINES = {"1": {"hue": "#00804A"}, "2": {"hue": "#C04020"}}
# `python scripts/line_colour_search.py nottingham`, run 2026-10-02: each hue's
# nearest feasible colour, 45.0 (Line 1) and 45.6 (Line 2) from the pins, 3:1
# on both pages; the pair 70.8 apart; the two dark-mode labels distinct.
LINE_COLOURS = {"1": "#586818", "2": "#D85028"}

# Two northbound stop members that are no stop (uk.elements), each beside a
# real stop the southbound relations carry.
SKIP_MEMBERS = {
    9243041864: "a railway=tram_crossing in the stop role on 170076 and 1984359, about "
                "30 m from Wilkinson Street, which 1984324 and 1984325 carry",
    6711112153: "an untagged node in the stop role on 170076, about 60 m from Bulwell, "
                "which 1984324 carries",
}
# Highbury Vale is one stop with a platform per branch, which OSM names
# "Highbury Vale A" (Line 1) and "Highbury Vale B" (Line 2); one stop to NET
# and NaPTAN (Newcastle's "St. James" precedent). 4 positions, 104 m across.
STATION_RENAMES = {"Highbury Vale A": "Highbury Vale", "Highbury Vale B": "Highbury Vale"}
# Stops on no relation, added by node (the fetch asks for every tram stop in
# the box). Bulwell Forest is on both Line 1 relations with an empty role, so
# not read as a stop; David Lane, between Basford and Highbury Vale, is on no
# relation, and NET lists it on both lines. Both directions' nodes each.
STATION_ADD = {
    502377358: ("1", "Bulwell Forest"),
    454568433: ("1", "Bulwell Forest"),
    502377232: (("1", "2"), "David Lane"),
    506692564: (("1", "2"), "David Lane"),
}
# NaPTAN writes "NTU" for OSM's and NET's "Nottingham Trent University".
NAPTAN_NAME_ALIASES = {"NTU": "Nottingham Trent University"}

# GATE 3 - per line from NET's timetables page (thetram.net/timetables, read
# 2026-10-02): 50 stops, each with its "Towards ..." headings naming the line
# ends it serves; Line 1 (Hucknall, Toton Lane) 36, Line 2 (Phoenix Park,
# Clifton South) 30, an interchange counted on each line.
OPERATOR_STATION_COUNTS = {"1": 36, "2": 30}
OPERATOR_COUNTS_SOURCE = ("NET, thetram.net/timetables: 50 stops, Line 1 36 and Line 2 30 "
                          "by each stop's direction headings (read 2026-10-02)")
# The tram floor for the station gates (Odense's 350 m, Kansas City's 150 m):
# a collapsed set under it is still platforms.
SPACING_MIN_M = 350.0
# Halved rings: the median gap in scope is 432 m (2026-10-02), under the
# spacing rule's 550 m (docs/ring_rules.md). Step 1 stops outside this band.
MEDIAN_GAP_BOUNDS_M = (380.0, 490.0)
NAPTAN_EXPLAINED = {}

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
