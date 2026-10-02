"""Edinburgh-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/edinburgh.md) on Manchester (Regional)'s contract: the shared
steps are pipeline/countries/uk.py and uk_fetch.py.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

SLUG = "edinburgh"
CITY_NAME = "Edinburgh"
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
# Scope: the City of Edinburgh council area (owner, 2026-10-01). The FSA's bulk XML per authority, named by CODE
# (Scotland's FHIS (SchemeType 2), in the same FSA files), exactly 1 asserted.
FSA_AUTHORITIES = {"773": "Edinburgh (City of)"}
FSA_AUTHORITY_COUNT = 1
FSA_FILE_URL = "https://ratings.food.gov.uk/OpenDataFiles/FHRS{code}en-GB.xml"
FSA_RAW_DIR = DATA_RAW / "fsa"

# Postcode centroids: OS Code-Point Open, London's file and edition (copied,
# not downloaded again), kept to the scope's GSS codes.
CODEPOINT_ZIP = DATA_RAW / "codepo_gb.zip"
CODEPOINT_SOURCE = ROOT / "data" / "london" / "raw" / "codepo_gb.zip"
CODEPOINT_CRS = "EPSG:27700"   # British National Grid eastings / northings
CODEPOINT_DISTRICTS = ("S12000036",)
# London's centroid tier (owner, 2026-09-28; the UK six's kit, 2026-10-01).
PLACE_AT_CENTROIDS = True

# The scope's OSM boundary relations, each polygonised from its outer ways
# and unioned; gated on the union's area so a truncated answer cannot pass.
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
BOUNDARY_OSM_RELATIONS = {1920901: "City of Edinburgh"}
# The relation measures 272.9 km2 in UTM 30N (the fetch, 2026-10-02).
BOUNDARY_AREA_KM2 = (260, 285)

# Rail: Edinburgh Trams, OpenStreetMap. One query (uk_fetch.osm_query): the bbox's
# route=tram relations and the boundaries with geometry, the routes' member
# ways' tags and member nodes. The lead runs it; agents read the cache.
OSM_BBOX = (55.9, -3.4, 55.99, -3.15)
OSM_ROUTES = ("tram",)
OSM_JSON = DATA_RAW / "osm.json"
SCOPE_LABEL = "the City of Edinburgh"

# OSM's three tram relations carry no ref, network or operator tag. The two
# through relations (Newhaven => Airport, 23 stops; Airport => Newhaven, 22,
# ending at Ocean Terminal) are the one line, given a ref by id.
REF_BY_RELATION = {2632877: "Tram", 4116776: "Tram"}
OSM_REFS = ("Tram",)
# Relation 11819309 ("Tram Extension to Newhaven", start_date 2023-06-07, the
# council's extension project page as its website): no stop members, and 100%
# of its 9.3 km lies within 15 m of both through relations' track (measured
# 2026-10-02). A leftover of the extension's construction mapping.
NOT_DRAWN = {
    11819309: "Tram Extension to Newhaven: no stops; a duplicate of the through "
              "relations' track (100% within 15 m)",
}
LINE_OSM_REFS = {"Tram": ("Tram",)}
LINE_ORDER = list(LINE_OSM_REFS)
# The operator's own name for the service; the legend row reads "<label>
# <legend name>" (map_common.build_legend), so the legend name is the ends as
# the timetables page writes them ("Between Newhaven and Airport").
LINE_NAMES = {"Tram": "Edinburgh Trams"}
LEGEND_NAMES = {"Tram": "(Airport - Newhaven)"}
# OSM records no colour and the operator publishes none, so the project's own
# hue (Odense's and Kansas City's dark goldenrod); LINE_COLOURS below is what
# is drawn, after scripts/line_colour_search.py.
LINES = {"Tram": {"hue": "#b8860b"}}
# `python scripts/line_colour_search.py edinburgh`, run 2026-10-02: the hue's
# nearest feasible colour, 73.6 from every pin, 5.86:1 on the dark page and
# 3.20:1 on the light; one line, so no pair to separate.
LINE_COLOURS = {"Tram": "#B88810"}

# GATE 3 - the whole line against the operator's own stop list: the route map
# on edinburghtrams.com/timetables names 23 stops, Edinburgh Airport to
# Newhaven (read 2026-10-02). One line, so the network count is the line's.
OPERATOR_STATION_COUNTS = {"network": 23}
OPERATOR_COUNTS_SOURCE = ("Edinburgh Trams, edinburghtrams.com/timetables (the route "
                          "map's stop list): 23 stops (read 2026-10-02)")
# The tram floor for the station gates (Manchester's 350 m): a collapsed set
# under it is still platforms.
SPACING_MIN_M = 350.0
NAPTAN_EXPLAINED = {}
# The standard rings: the median gap in scope is 614 m (2026-10-02; min 338,
# max 1,199), over the spacing rule's 550 m and clear of its 540-570 m owner
# band (docs/ring_rules.md). Step 1 stops outside this band, whose floor is
# that band's top.
MEDIAN_GAP_BOUNDS_M = (570.0, 700.0)

# NaPTAN (DfT, OGL v3): gate 3's second independent source (owner,
# 2026-10-01). ATCO area 940 is the national tram and metro area, where every
# tram stop is filed; step 1 reads the active MET records with these ATCO
# prefixes inside the scope.
# The eight Newhaven-extension stops (Picardy Place to Newhaven, opened 2023)
# are filed under the Tyne and Wear prefix 9400ZZTW, the other 15 under
# 9400ZZED (measured 2026-10-02); the scope polygon keeps Tyne and Wear's own
# out. Inside the city: 23 active MET records, one per stop.
NAPTAN_PREFIXES = ("9400ZZED", "9400ZZTW")
# NaPTAN's "West End - Princes Street" is the stop OSM and the operator call
# "West End" (the operator's route map, 2026-10-02).
NAPTAN_NAME_ALIASES = {"West End - Princes Street": "West End"}
NAPTAN_ATCO_AREAS = ("940",)
NAPTAN_RAW_DIR = DATA_RAW / "naptan"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-3.19) falls in the -6 to 0 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson. London's,
# Glasgow's and Newcastle's distance CRS too; British National Grid is only
# Code-Point's own CRS (CODEPOINT_CRS above).
CRS_PROJECTED = "EPSG:32630"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: the scope's extent plus a margin. The polygon does the
# filtering; this catches a CRS or axis error.
BUSINESS_BBOX = {"lat_min": 55.8, "lat_max": 56.02, "lon_min": -3.48, "lon_max": -3.05}

# ===========================================================================
# STEP 1 - filled by the city's build (Manchester's config is the model):
# OSM_REFS, NOT_DRAWN, REF_BY_RELATION (a relation with no ref),
# LINE_OSM_REFS or LINE_STOPS, LINE_ORDER, LINE_NAMES, LEGEND_NAMES, LINES
# (hues), LINE_COLOURS, OPERATOR_STATION_COUNTS, OPERATOR_COUNTS_SOURCE,
# SPACING_MIN_M, MEDIAN_GAP_BOUNDS_M, NAPTAN_EXPLAINED, the ring edges.
# ===========================================================================
