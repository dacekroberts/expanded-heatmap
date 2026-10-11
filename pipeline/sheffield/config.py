"""Sheffield-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/sheffield.md) on Manchester (Regional)'s contract: the shared
steps are pipeline/countries/uk.py and uk_fetch.py.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

SLUG = "sheffield"
CITY_NAME = "Sheffield"
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
# Scope: the city, without the Rotherham Tram-Train (owner, 2026-10-01). The FSA's bulk XML per authority, named by CODE
# (Rotherham (420) is out with the Tram-Train), exactly 1 asserted.
FSA_AUTHORITIES = {"425": "Sheffield"}
FSA_AUTHORITY_COUNT = 1
FSA_FILE_URL = "https://ratings.food.gov.uk/OpenDataFiles/FHRS{code}en-GB.xml"
FSA_RAW_DIR = DATA_RAW / "fsa"

# Postcode centroids: OS Code-Point Open, London's file and edition (copied,
# not downloaded again), kept to the scope's GSS codes.
CODEPOINT_ZIP = DATA_RAW / "codepo_gb.zip"
CODEPOINT_SOURCE = ROOT / "data" / "london" / "raw" / "codepo_gb.zip"
CODEPOINT_CRS = "EPSG:27700"   # British National Grid eastings / northings
CODEPOINT_DISTRICTS = ("E08000039",)
# London's centroid tier (owner, 2026-09-28; the UK six's kit, 2026-10-01).
PLACE_AT_CENTROIDS = True

# The scope's OSM boundary relations, each polygonised from its outer ways
# and unioned; gated on the union's area so a truncated answer cannot pass.
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
BOUNDARY_OSM_RELATIONS = {106956: "Sheffield"}
BOUNDARY_AREA_KM2 = (350, 385)   # the city, about 368 km2

# Rail: Sheffield Supertram, OpenStreetMap. One query (uk_fetch.osm_query): the bbox's
# route=tram relations and the boundaries with geometry, the routes' member
# ways' tags and member nodes. The lead runs it; agents read the cache.
OSM_BBOX = (53.33, -1.55, 53.47, -1.3)
OSM_ROUTES = ("tram",)
OSM_JSON = DATA_RAW / "osm.json"
SCOPE_LABEL = "the City of Sheffield"

# NaPTAN (DfT, OGL v3): gate 3's second independent source (owner,
# 2026-10-01). ATCO area 940 is the national tram and metro area, where every
# tram stop is filed; step 1 reads the active MET records with these ATCO
# prefixes inside the scope.
NAPTAN_PREFIXES = ("9400ZZSY",)
NAPTAN_ATCO_AREAS = ("940",)
NAPTAN_RAW_DIR = DATA_RAW / "naptan"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-1.47) falls in the -6 to 0 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson. London's,
# Glasgow's and Newcastle's distance CRS too; British National Grid is only
# Code-Point's own CRS (CODEPOINT_CRS above).
CRS_PROJECTED = "EPSG:32630"

# --- Ring geometry ---------------------------------------------------------
# Halved (Aarhus's): tram stops at a 444 m median gap (MEDIAN_GAP_BOUNDS_M).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Business filtering ------------------------------------------------

CITY_KEEP = "the City of Sheffield"

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: the scope's extent plus a margin. The polygon does the
# filtering; this catches a CRS or axis error.
BUSINESS_BBOX = {"lat_min": 53.29, "lat_max": 53.51, "lon_min": -1.81, "lon_max": -1.32}

# --- Step 1: lines and stations -------------------------------------------

# OSM's 8 tram relations (network "Travel South Yorkshire", operator "South
# Yorkshire Future Trams") carry 4 refs, two relations each, one per
# direction. The three Supertram routes are drawn; the Tram-Train is not.
OSM_REFS = ("BLUE", "YELL", "PURP")
NOT_DRAWN = {
    9701871: ("TT: the Tram-Train to Rotherham: every 30 minutes on Network Rail track "
              "beyond Tinsley, which fails the converted-railway frequency gate (Aarhus "
              "L1's precedent; owner, 2026-10-01)"),
    9701872: ("TT: the Tram-Train to Rotherham: every 30 minutes on Network Rail track "
              "beyond Tinsley, which fails the converted-railway frequency gate (Aarhus "
              "L1's precedent; owner, 2026-10-01)"),
}
# The Yellow route's two directions spell one stop two ways (relation 165852
# "Carbrook/Ikea", 9701823 "Carbrook/IKEA"); one station, IKEA as the store
# writes it.
STATION_NAME_ALIASES = {"Carbrook/Ikea": "Carbrook/IKEA"}

# OSM's relations match the operator's three routes one for one, so each line
# is its relations merged by London's branch rule (no LINE_STOPS).
# Purple runs about hourly on purpose-built track: drawn, with the wait on the
# page (Buffalo's rule; owner, 2026-10-01). It alone serves 2 of the 48 stops
# (Herdings Park, Herdings / Leighton Road).
LINE_OSM_REFS = {"Blue": ("BLUE",), "Yellow": ("YELL",), "Purple": ("PURP",)}
LINE_ORDER = list(LINE_OSM_REFS)
# The on-map label is the route's public name, "<Colour> route". The legend
# row reads "<label> <legend name>" (map_common.build_legend), so the legend
# name is the route's ends, as OSM's from/to tags write them.
LINE_NAMES = {k: f"{k} route" for k in LINE_ORDER}
LEGEND_NAMES = {
    "Blue": "(Halfway - Malin Bridge)",
    "Yellow": "(Middlewood - Meadowhall Interchange)",
    "Purple": "(Herdings Park - Cathedral)",
}
# OSM's colour tags; LINE_COLOURS below is what is drawn, after
# scripts/line_colour_search.py.
OSM_COLOURS = {"Blue": "#0000FF", "Yellow": "#FFFF00", "Purple": "#800080"}
LINES = {k: {"hue": v} for k, v in OSM_COLOURS.items()}
# `python scripts/line_colour_search.py sheffield`, run 2026-10-02: each OSM
# hue's nearest feasible colour, 45.4 or more from every pin, 3:1 on both
# pages; closest pair within 500 m 55.1 (Blue, Purple); the three dark-mode
# labels distinct. Yellow's #FFFF00 fails 3:1 on the light page and is
# darkened to #989800 (light 3.08), as Tours's and Dijon's were; Blue's
# #0000FF (about 2.2:1 on the dark page) moves to #8018F8.
#
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search, and
# #989800 sat 15.7 from it, under the owner's floor of 20 (2026-10-07). Yellow
# moves to #B48C00, a dark gold: the colour nearest OSM's #FFFF00, held to a
# yellow hue (LCh 85-103 degrees), that reads 3:1 on both pages (light 3.14)
# and clears 20 from both pins. Olive 25.8, an accepted trade between 20 and
# 45 (owner, 2026-10-07); a re-run of the search at 45 turns it green, which
# is not the line's colour. Blue 97.3 and Purple 45.4 from the pins.
LINE_COLOURS = {"Blue": "#8018F8", "Yellow": "#B48C00", "Purple": "#A030A0"}

# GATE 3 - NaPTAN only. Supertram's own site (supertram.com) serves a Radware
# CAPTCHA to a script and Stagecoach's Supertram page returns 403, both
# 2026-10-02; neither is passed. NaPTAN is then the only independent source
# (owner, 2026-10-01), run name by name in step 1.
OPERATOR_STATION_COUNTS = None
OPERATOR_COUNTS_GAP = ("supertram.com serves a Radware CAPTCHA to scripts and "
                       "Stagecoach's Supertram page returns 403 (2026-10-02); neither "
                       "is passed, so NaPTAN is the only independent source (owner, "
                       "2026-10-01)")
OPERATOR_COUNTS_SOURCE = None
# The tram floor for the station gates (Odense's 350 m, Kansas City's 150 m):
# a collapsed set under it is still platforms.
SPACING_MIN_M = 350.0
# Halved rings: the median gap in scope is 444 m (2026-10-02; min 145 m,
# Castle Square to Fitzalan Square / Ponds Forge, two stops NaPTAN also
# holds), under the spacing rule's 550 m (docs/ring_rules.md). Step 1 stops
# outside this band.
MEDIAN_GAP_BOUNDS_M = (390.0, 500.0)
NAPTAN_EXPLAINED = {}
# NaPTAN's spelling -> the built (OSM) station, for the same stop under a
# shorter or newer name, each paired by its NaPTAN record's position
# (measured 2026-10-02, distance to the OSM stop positions):
NAPTAN_NAME_ALIASES = {
    "Carbrook": "Carbrook/IKEA",                                       # 4 m
    "Fitzalan Sq - Ponds Forge": "Fitzalan Square / Ponds Forge",      # 1-3 m
    "Granville Rd - Sheffield College": "Granville Road / The Sheffield College",  # 68-72 m
    "Manor Top": "Manor Top / Elm Tree",                               # 14-16 m
    "Sheffield Stn - Hallam Uni": "Sheffield Station / Sheffield Hallam University",  # 3-4 m
    # The same stop renamed: ATCO 9400ZZSYSHL (Shalesmoor's code), 3 m from
    # OSM's Shalesmoor, its street "Shalesmoor", revised 2025-05-08. The map
    # keeps OSM's name, Shalesmoor (owner, 2026-10-02).
    "Kelham Island": "Shalesmoor",
}
