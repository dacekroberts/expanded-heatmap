"""Liège-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

LIEGE, the Ville (INS 62063), on the two shared Belgian modules Charleroi
uses: the tram from TEC's own GTFS (`pipeline/countries/belgium_tec.py`) and
the shops and horeca premises from Wallonia's LoGIC 2024 survey
(`pipeline/countries/belgium_logic.py`). One street tram, T1, opened
2025-04-28 and wholly inside the commune, so a trams-only page (tram-city).
Two categories, Retail and Food service (`narrowed`, "Two"). The brief:
docs/build_briefs/liege.md.
"""

from pathlib import Path

from pipeline.countries import belgium_tec

SLUG = "liege"
NAME = "Liège"
FETCH = "pipeline/liege/fetch_sources.py"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "liege" / "raw"
DATA_PROCESSED = ROOT / "data" / "liege" / "processed"
OUTPUTS = ROOT / "outputs" / "liege"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Written even when empty: every T1 stop is in the commune.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# The owner's "measure first" (2026-10-03), written by step 2.
COVERAGE_JSON = DATA_PROCESSED / "logic_coverage.json"

# --- Raw inputs (fetch_sources.py installs or verifies; no step fetches) ---

GTFS_ZIP = belgium_tec.FEED_ZIP
# Every municipality in the tram's box, from OpenStreetMap (admin_level 8,
# ref:INS), cached by the lead's run of fetch_communes on 2026-10-04: 18
# communes, Liege's polygon 68.5 km2.
OSM_COMMUNES_JSON = DATA_RAW / "osm_communes.json"
COMMUNE_BBOX = (50.56, 5.48, 50.71, 5.68)          # south, west, north, east
NIS = "62063"
COMMUNE_AREA_KM2 = (62.0, 75.0)                    # the OSM polygon: 68.5 km2
LOGIC_INS = 62063

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 31N: the longitude (~5.58) falls in the 0 to 6 band (still zone 31,
# west of 6 E). Derived per city, not copied - see docs/project_context.md's
# CRS lesson. LoGIC's EPSG:3812 is reprojected to it.
CRS_PROJECTED = "EPSG:32631"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the owner's spacing rule (about 550 m or less): the stops' median
# nearest-neighbour gap is 351 m (step 1, 2026-10-04, 23 stops). Step 1 stops
# outside the bounds below.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (300.0, 420.0)

# --- Station scope: the tram, T1, every stop -----------------------------------
#
# TEC's only route_type 0 route (2026-10-04), "Coronmeuse/Expo - St-Lambert -
# Guillemins-Standard". It forks at its northern end (Coronmeuse via Parc
# Reine Astrid; Liege Expo via Droixhe) and runs one way each through the
# centre (Pont Maghin and Feronstree southbound, La Batte and Curtius
# northbound). No stop is thinned (tram-city). Buses and NMBS-SNCB trains are
# not drawn. Matched on route_short_name.
ROUTE_TYPE = "0"
LINES = ("T1",)
# The bare public line name (the owner's open ruling on the TEC name keeps the
# operator's name out of every label until it lands).
LINE_NAMES = {"T1": "T1"}
# Daytime (09-16) headway read on this Tuesday: every 6 minutes, longest gap
# 8-9 (2026-10-04). Street trams have no frequency gate; the figure is for the
# page.
HEADWAY_DAY = "20261013"
HEADWAY_MAX_MIN = None

# Display names are the child stops' own names without TEC's upper-case
# locality prefix and "(Tram)" suffix ("SCLESSIN Standard (Tram)" ->
# "Standard"). One stop carries two parent ids, Liege Expo and "Liege Expo
# quai 0" (a departure quay, 210 trips over the feed): merged into one station
# (owner, 2026-10-03, Belgium build call 5).
NAME_ALIASES = {"Liège Expo quai 0": "Liège Expo"}
MERGED_NAMES = ("Liège Expo",)
COLLAPSE_MAX_SPREAD_M = 250.0
SPACING_MIN_M = 100.0

# Gate 3: the City of Liege's open dataset "Tram - Stations"
# (opendata.liege.be, 23 rows, 2022, CC BY; the brief, 2026-10-03): a public
# authority's list independent of OSM and of the feed, read for the count
# only, never republished. The whole line. Not re-read by this build (no
# download): the lead confirms its rows match the line as opened (2025-04-28).
OPERATOR_STATION_COUNTS = {"T1": 23}
OPERATOR_COUNTS_SOURCE = (
    "Ville de Liège, open dataset 'Tram - Stations' (opendata.liege.be), 23 rows, 2022, "
    "CC BY; counted by the Liège brief, 2026-10-03.")

# T1's drawn shapes, picked by step 1 (belgium_tec.line_shapes, France's rule:
# shapes by trips, one added only where it reaches stops the others miss).
# Three, for the fork and the one-way centre. Step 1 stops if the pick changes.
LINE_SHAPES = {"T1": ("gw:tec:L10000178", "gw:tec:L10000161", "gw:tec:L10000170")}
# The feed's own route_color, TEC yellow, on precedent (an operator's colour
# where it is unambiguous; T1 is the only line). CIE76 nearest pin 88.6
# (Personal services), 108.1 from Food service, 144.5 from Retail
# (pipeline/linecolour.py, 2026-10-04). Contrast against white is 1.5: the
# label's halo is set by linecolour.label_colours, checked by
# scripts/check_map_markup.py.
LINE_COLOURS = {"T1": "#FFCD00"}
FEED_ROUTE_COLOR = "FFCD00"

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "wallonia_logic"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "NATURE"
# Scope is LoGIC's INS; the OSM commune polygon checks it. A point with the
# city's INS further than this outside the polygon stops step 2.
POLYGON_TOLERANCE_M = 100.0

# SIGNS READ AS A PERSON'S OWN NAME, withheld: the pin shows its NATURE class
# instead (owner, 2026-10-03, Belgium build call 10). Keys, never names
# (pipeline/name_keys.py). Proposed by belgium_logic.person_sign on the retail
# and horeca rows, less any sign found at two or more points in Wallonia (a
# brand); 39 rows, 2026-10-04. NOT READ BY EYE (see Charleroi's config).
# Regenerate with
#   python -m pipeline.countries.belgium_logic --person-keys 62063
PERSON_NAMED = (
    "12249e1ba7af5d4c", "124ea924209ca036", "229f533ece3d8f50", "2400df9c16526722",
    "27391aab133ce5d6", "2c295970c838d313", "2e4358b24c2e6030", "2fe499b59a1474df",
    "336119b025983540", "33ba93aa232070ef", "4844cf1ad07158d6", "5927c548a85b359f",
    "6116cf14a47aeee9", "65ae8e2b9f89388e", "701e02cc7659af77", "7a38c9bd42f9a118",
    "7a8d877382ff2cdf", "7ed3027abdf32074", "88f8e8f8a79d03a8", "8ec25daeda03d584",
    "94d214ffdc8d512a", "9b016a5eac5825b8", "9ba4be98137a9968", "a06b13aa8b725626",
    "a339345cdddd2191", "a8776d9c5a714e1f", "abe7f44de5b6f338", "afd4d81cae95aef0",
    "c185d94aa51226a3", "c1e554360d6f3ac4", "c7313ccc4215dda3", "da7585bc0e395a38",
    "e8f0ceba8bd0ff80", "eb589cb15f9ab964", "ebcf5f7a0052c0bd", "f3ea59ddf153827f",
    "f727be878df528b5", "fa8b183cc9896740", "fc3092062e76dac7",
)

# Sanity bounds for the points: the commune plus a margin.
LIEGE_BBOX = {
    "lat_min": 50.55,
    "lat_max": 50.72,
    "lon_min": 5.47,
    "lon_max": 5.70,
}
