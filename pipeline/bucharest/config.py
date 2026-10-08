"""Bucharest-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/bucharest.md), Staging's measurements and London's
OSM-rail build.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "bucharest" / "raw"
DATA_PROCESSED = ROOT / "data" / "bucharest" / "processed"
OUTPUTS = ROOT / "outputs" / "bucharest"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- The register --------------------------------------------------------
#
# DSVSA București (the sanitary-veterinary and food safety directorate): one
# XLSX per unit category, each listing registered units "active and closed" -
# the rows below a row reading ANULATE are cancelled. No status column, no
# coordinates. The hosts sit behind a browser challenge, so THE OWNER FETCHES
# THE FILES in their own browser (the Band C memo's condition); nothing here
# downloads them, and a cookie is never replayed. Files dated 25.08.2026.
DSVSA_PAGE_ANIMAL = "https://bucuresti.dsvsa.ro/"
# file -> what it holds. The taxonomy buckets each file, and reads the
# category text for the exceptions (labs, kiosk carts, vending machines).
# The animal-origin list (in data/bucharest/raw/):
ANIMAL_FILES = {
    "01-CARMANGERIE.xlsx": "pork butcher",
    "02.-MACELARIE.xlsx": "butcher",
    "11-MAGAZIN-DE-DESFACERE-PESTE-PESCARIE.xlsx": "fishmonger",
    "16-MAGAZIN-DE-DESFACERE-A-MIERII-DE-ALBINE-SI-A-ALTOR-PRODUSE-APICOLE.xlsx": "honey shop",
    "19-UNITATE-DE-ALIMENTATIE-PUBLICA.xlsx": "restaurants, cafés, bars",
    "20-PIZZERIE.xlsx": "pizzeria",
    "23-COFETARIE-PATISERIE.xlsx": "confectioner and pastry shop",
    "25-MAGAZIN-ALIMENTAR.xlsx": "food shop",
    "26-HIPERMARKET-SUPERMARKET.xlsx": "supermarket and hypermarket",
}
# The non-animal-origin list (in data/bucharest/raw/non-animal/):
NON_ANIMAL_FILES = {
    "01.-FABRICAREA-PAINII.xlsx": "bakery",
    "02.-FABRICAREA-PRAJITURILOR-A-PRODUSELOR-PROASPETE-DE-PATISERIE.xlsx": "pastry shop",
    "03.-FABRICAREA-PAINII-FABRICAREA-PRAJITURILOR-A-PRODUSELOR-PROASPETE-DE-PATISERIE.xlsx":
        "bakery and pastry shop",
    "24.-FABRICAREA-INGHETATEI.xlsx": "ice-cream maker",
    "33.-COMERT-CU-AMANUNTUL-EXCLUSIV-SUPERMARKETURI-HIPERMARKETURI.xlsx": "retail (not supermarkets)",
    "34.-SUPERMARKET-HIPERMARKET.xlsx": "supermarket (empty)",
    "36.-BARURI.xlsx": "bars and cafés",
    "42.-UNITATI-DE-COMERCIALIZARE-A-PRODUSELOR-ALIMENTARE-DE-ORIGINE-NONANIMALA-CONGELATE-REFRIGERATE.xlsx":
        "frozen and chilled food counters",
}
# Left out by the owner (2026-09-28) and never fetched: canteens (21), pastry
# labs (22), catering (31), local producers (34), internet-only sales, mobile
# stalls, vending machines, warehouses, fairs, farm and processing units.
REGISTER_DATE = "2026-08-25"   # the date printed on every file

# --- Addresses -----------------------------------------------------------
#
# OSM address objects inside the municipality (relation 377733) with both
# addr:street and addr:housenumber - the JOIN target (address-join): ANCPI's
# national nomenclature has no reachable geospatial service. Fetched
# 2026-09-28 with the owner's OK (9,523,237 bytes); the query is recorded
# here so fetch_sources.py can reproduce it into a new dated file.
OSM_ADDRESSES_CSV = DATA_RAW / "osm_addresses_2026-09-28.csv"
OSM_ADDRESSES_QUERY = (
    '[out:csv(::type,::id,::lat,::lon,"addr:street","addr:housenumber","addr:postcode")][timeout:300];'
    'area(3600377733)->.a;nwr["addr:street"]["addr:housenumber"](area.a);out center;')

# The six sectors (admin_level 9), fetched to test each register row's own
# Sector against where its OSM address lies: Bucharest reuses street names
# across sectors, and Staging's sector-free key put 11.2% of its first-pass
# matches on an address with points more than 300 m apart (2026-09-29).
SECTORS_QUERY = ('[out:json][timeout:180];rel(377733);map_to_area->.a;'
                 'rel["boundary"="administrative"]["admin_level"="9"](area.a);out geom;')
SECTORS_OSM_CACHE = DATA_RAW / "osm_sectors.json"
SECTORS_GEOJSON = DATA_RAW / "sectors.geojson"
# One matched address is ONE place when its OSM points link hop to hop within
# ADDRESS_HOP_M and span no more than SITE_SPREAD_MAX_M (a shopping centre or
# an industrial site); otherwise it is two places and the row is left
# unplaced rather than guessed. Measured 2026-09-29: a plain 150 m spread
# test left 3,177 rows "ambiguous", of which 1,701 of the 2,655 read were one
# continuous site (Casa Presei, Bucur Obor).
ADDRESS_HOP_M = 150
SITE_SPREAD_MAX_M = 600
# An OSM address counts for a sector it lies in or within this distance of:
# boulevards are often the boundary, with numbers on both sides.
SECTOR_EDGE_M = 100

# --- Rail ----------------------------------------------------------------
#
# Metrorex M1-M5 from OpenStreetMap's route relations (osm-rail): no GTFS for
# the metro is published that this project can use.
OSM_BBOX = "44.33,25.95,44.55,26.25"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:180];("
    f'rel["type"="route"]["route"="subway"]({OSM_BBOX});'
    ");out geom;")
OSM_ROUTES_JSON = DATA_RAW / "osm_rail_routes.json"
# Stop AND named platform members (Stockholm's lesson), out center.
OSM_STOPS_QUERY = OSM_ROUTES_QUERY.replace(
    ");out geom;",
    ')->.r;(node(r.r:"stop");node(r.r:"stop_entry_only");node(r.r:"stop_exit_only");'
    'node(r.r:"platform");node(r.r:"platform_entry_only");node(r.r:"platform_exit_only");'
    'way(r.r:"platform");way(r.r:"platform_entry_only");way(r.r:"platform_exit_only");'
    'rel(r.r:"platform"););out center;')
OSM_STOPS_JSON = DATA_RAW / "osm_rail_stops.json"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
BRANCH_NEAR_M = 100
BRANCH_MIN_NEW_M = 300
# A kept station further than this from its own drawn line stops step 1.
STATION_OFF_LINE_MAX_M = 100
STATION_CLUSTER_M = 400
UNNAMED_PLATFORM = r"(?i)^(track|linia|peron|platform)\s*\d+$"
# OSM's one station name carrying its line; Metrorex signs it "Basarab 1".
# The numbered interchange pairs (Basarab 1/2, Dristor 1/2, Eroilor/Eroilor 2,
# Nicolae Grigorescu 1/2, Piața Unirii 1/2, Piața Victoriei 1/2, Gara de Nord
# 1/2) stay two stations each: Metrorex counts them so, which is how 64 is
# reached.
STATION_NAME_ALIASES = {"Basarab 1 - M1": "Basarab 1"}

CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# Municipiul București, OSM relation 377733, polygonised from its outer ways
# and gated on its area: 238.9 km2 in UTM 35N on 2026-09-29, exactly the six
# sectors' sum.
BOUNDARY_OSM_RELATION = 377733
BOUNDARY_OSM_NAME = "București"
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_bucuresti.json"
BOUNDARY_AREA_KM2 = (234, 244)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 35N: the longitude (~26.10) falls in the 24 to 30 band. Derived per
# city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32635"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

CITY_LABEL = "the Municipality of Bucharest"
# On-map label: Metrorex's line code; the legend adds the line's termini.
# Hues are OSM's route colours (Metrorex's own); the drawn colour is
# scripts/line_colour_search.py's nearest feasible one.
LINES = {"M1": {"hue": "#FFFF00"}, "M2": {"hue": "#003399"}, "M3": {"hue": "#BC1725"},
         "M4": {"hue": "#347C11"}, "M5": {"hue": "#FF8040"}}
LINE_ORDER = list(LINES)
LINE_NAMES = {k: k for k in LINES}
# The legend row reads "<label> <this>" (build_legend).
LEGEND_NAMES = {"M1": "Dristor – Pantelimon", "M2": "Pipera – Tudor Arghezi",
                "M3": "Preciziei – Anghel Saligny", "M4": "Gara de Nord – Străulești",
                "M5": "Eroilor – Valea Ialomiței / Râul Doamnei"}
# `python scripts/line_colour_search.py bucharest`, run 2026-09-29: every line
# >= 45.0 from the pins of that run, closest pair within 500 m 20.1 (M1's
# olive-yellow against M4's green, which meet only at Basarab), five distinct
# dark-mode labels. M1's yellow darkens to read on the light page; M2's blue
# takes a violet beside the Food shops pins (Stockholm's Blue line precedent).
#
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search, and two
# lines sat under the owner's floor of 20 from it (2026-10-07): M4 #608000 at
# 11.6 and M1 #989800 at 15.7. Each moved to the colour nearest its OSM hue
# that reads 3:1 on both pages, clears 20 from both pins and 18 from every
# other line, taking a wider margin where it cost little: M4 #247810 (olive
# 30.0), M1 #B48C00, a dark gold held to a yellow hue (olive 25.8). Both sit
# between 20 and 45 from olive, an accepted trade (owner, 2026-10-07); closest
# pair now 26.0 (M3, M5), five distinct dark-mode labels. DECISIONS, "Lines
# within 20 of the olive and violet pins recoloured".
LINE_COLOURS = {"M1": "#B48C00", "M2": "#7840D0", "M3": "#C02008", "M4": "#247810", "M5": "#E87030"}
# Five lines, one key each; M5's two branches (to Valea Ialomiței and Râul
# Doamnei) are one line, as Metrorex presents it.
LINE_OSM_REFS = {r: (r,) for r in ("M1", "M2", "M3", "M4", "M5")}
RELATIONS_SKIPPED = {}
STATION_ADDITIONS = {}
OSM_ADDITIONS_JSON = DATA_RAW / "osm_station_additions.json"
# GATE 3 - the network against English Wikipedia's Bucharest Metro infobox
# (64 stations), read 2026-09-29, a SECONDARY source (Prague's precedent). No
# per-line count is published there, so the gate is network-level (Oslo's).
OPERATOR_STATION_COUNTS = {"Metrorex (network)": 64}
OPERATOR_COUNTS_SOURCE = "en.wikipedia: Bucharest Metro infobox, 64 stations - secondary, read 2026-09-29"
# The naming layer for stations outside the municipality (none expected).
NAMING_GEOJSON = DATA_RAW / "naming_layer.geojson"

# --- Business filtering ------------------------------------------------

CITY_KEEP = "București"
TAXONOMY_SYSTEM = "romania_dsvsa"
RAW_CLASSIFICATION_COLUMN = "Categorie"

# The municipality's polygon extent (44.3342-44.5414 N, 25.9667-26.2256 E,
# measured 2026-09-29) plus ~0.02 deg. Placement is by OSM address and the
# polygon does the filtering; this records the frame.
BUCHAREST_BBOX = {
    "lat_min": 44.31,
    "lat_max": 44.56,
    "lon_min": 25.94,
    "lon_max": 26.25,
}
