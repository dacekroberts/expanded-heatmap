"""Montpellier-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_france_batch.py (the France tram batch) from the
2026-09-27 screen's inputs and the station table in `data/_staging_scratch_2026-09-27/second_cities/france/stations_pure_2026-09-30`.
Read `.claude/skills/france-tram-city/SKILL.md` and
`docs/build_briefs/montpellier.md` before filling anything. Every to-do marker is a value
only the build-day feed or the owner can supply; none may ship.
"""

from pathlib import Path

# The national facts, shared with every French city (see pipeline/rennes/config.py).
from pipeline.countries.france import (  # noqa: F401
    COMMUNE_COLUMN,
    DIFFUSION_COLUMN,
    DIFFUSION_PUBLIC_VALUE,
    EMPLOYEE_BAND_COLUMN,
    ENSEIGNE_COLUMNS,
    GEO_EPSG_COLUMN,
    GEO_LAT_COLUMN,
    GEO_LON_COLUMN,
    GEO_QUALITY_COLUMN,
    GEOLOC_DATASET_SLUG,
    GEOLOC_PARQUET,
    GEOLOC_RESOURCE_TITLE_CONTAINS,
    JOIN_KEY,
    METROPOLITAN_EPSG,
    NAF_COLUMN,
    SIRENE_DATASET_SLUG,
    SIRENE_PARQUET,
    SIRENE_RESOURCE_TITLE_PREFIX,
    STATE_ACTIVE_VALUE,
    STATE_COLUMN,
    USUAL_NAME_COLUMN,
)

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "montpellier" / "raw"
DATA_PROCESSED = ROOT / "data" / "montpellier" / "processed"
OUTPUTS = ROOT / "outputs" / "montpellier"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the commune, each with the commune it IS in.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

GTFS_ZIP = DATA_RAW / "gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# Every commune of the EPCI(s) the network runs in, with contours: the naming
# layer for excluded stations (commune scope) or the scoping layer (regional).
METRO_COMMUNES_GEOJSON = DATA_RAW / "metropole_communes.geojson"

# --- The feed ------------------------------------------------------------

# ⚠ ROLLING. French tram feeds run four to twelve weeks ahead, so the build
# FETCHES THIS FRESH on every run and never trusts a cached copy - including the
# screen's 2026-09-27 copy that may sit in data/montpellier/raw/ already.
GTFS_URL = "https://www.data.gouv.fr/api/1/datasets/r/93a29ce2-cfc8-44ff-b712-bcfd814b7f00"
GTFS_DATASET = "Réseau urbain TaM"
# The licence the NAP declares for this dataset. ODbL under the NAP's
# Conditions Particulières: the §4.3 notice in app/components.py, and the
# station table a PURE extract (read 2026-09-29).
GTFS_LICENCE = "odc-odbl"
# Measured 2026-09-30 by the kit session: no feed_info.txt and NO shapes.txt:
# line geometry from another source, read first (licence read 2026-09-29).
# TODO: re-read at build - does the build-day zip carry feed_info.txt with a
# feed_end_date? True means the page can quote the operator's own window.
GTFS_SELF_ATTESTS = None
# The NAP dataset: fetch_sources.py reads the resource's date and window from it.
GTFS_NAP_ID = "662ba9a3f7d9ff84a3060d0a"

BOUNDARY_COMMUNE_CODE = "34172"
# ⚠ `geometry=contour`, NOT `fields=contour` (a 120-byte POINT, no error).
BOUNDARY_URL = ("https://geo.api.gouv.fr/communes/34172"
                "?geometry=contour&format=geojson")
METROPOLE_EPCI_CODES = ["243400017"]
METROPOLE_COMMUNES_URLS = [
    f"https://geo.api.gouv.fr/epcis/{code}/communes"
    "?fields=nom,code&geometry=contour&format=geojson"
    for code in METROPOLE_EPCI_CODES
]

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# LAMBERT-93, as every French city takes it: one national grid for one national
# register, where a per-city UTM rule would split France across zones 30-32.
CRS_PROJECTED = "EPSG:2154"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# Median nearest-neighbour gap 416 m across the 88 in-scope stations (min 69
# m), Lambert-93, measured from the kit's station table - under ~550 m, so the
# half-size rings every French city takes (docs/ring_rules.md). Step 1 re-
# measures.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# APPROVED by the owner 2026-09-30, as docs/build_briefs/montpellier.md recommended:
#   scope    commune - the worst line, 2, keeps 15 of 28 stations (54%) in
#            commune 34172; half or more stays commune-only (Toulouse 52%,
#            Rennes 73%)
#   mode     tram (the macro map's dot colour: what step 1 keeps, never the
#            feed's route_type flag)
#   coverage full (SIRENE: all three buckets)
SCOPE = "commune"
MAP_MODE = "tram"
MAP_COVERAGE = "full"

# What the feed types the kept lines as. Matched together with the line list,
# never alone: a type flag is not a mode decision (Reims and Rouen type theirs 1).
ROUTE_TYPES_RAIL = ("0",)
# The kept lines, by the feed's route_short_name.
LINE_KEYS = ["1", "2", "3", "4", "5"]
# TODO: the build-day feed's route_id(s) for each key in LINE_KEYS. Read them
# fresh: a rolling feed may renumber. Several route_ids per key is allowed
# (Le Havre, Valenciennes) - they collapse onto the key.
ROUTE_IDS = []

# Station rule (owner, 2026-09-29 and 09-30): the feed's own parent_station
# row, else the FIRST platform in stops.txt order per unchanged stop_name.
# Never a mean, never a rename. On a Licence Ouverte feed ONLY, a same-name
# pair (case and accents ignored) within 150 m keeps its first row; on an ODbL
# feed, never. Fictitious FIC_ stops are not stations.
# Measured 2026-09-30: 112 stations network-wide.
# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope
# decision is checkable. If these move, the decision is being re-taken.
EXPECTED_INSIDE_PER_LINE = {"1": 31, "2": 15, "3": 20, "4": 18, "5": 25}
EXPECTED_STATIONS_PER_LINE = {"1": 31, "2": 28, "3": 29, "4": 18, "5": 27}

# GATE 3: an independent per-line count, from outside the feed.
# TODO: the operator's own stop list or OpenStreetMap's route relations.
OPERATOR_STATION_COUNTS = {}
OPERATOR_COUNTS_SOURCE = "TODO"

# route_short_name -> the name riders use. Proposed; verify each against the
# operator's own naming before it goes on the map and in the legend.
LINE_NAMES = {"1": "Tram 1", "2": "Tram 2", "3": "Tram 3", "4": "Tram 4", "5": "Tram 5"}  # TODO verify
# TODO: each line's colour, from the build-day feed's route_color where it has
# one and it is unambiguous; pipeline/linecolour.py decides a clash.
LINE_COLOURS = {}

# The map's layer and title prefix for the lines.
MAP_SYSTEM_NAME = "Tram"
# Where the line GEOMETRY comes from: "gtfs" (the feed's shapes.txt) or "osm".
# Stations come from the feed either way.
LINE_GEOMETRY = "osm"
# OpenStreetMap route relations, for the LINE GEOMETRY and gate 3's count: ONE query per city, cached by
# fetch_sources.py (the owner's Overpass rule). TODO: check the relations'
# `network` tag and refs at build and narrow the query to the operator's.
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:120];"
    'relation["type"="route"]["route"~"^(tram|light_rail)$"]'
    "(43.55,3.79,43.67,3.96);"
    "out geom;")
# line key -> the relations' `ref` tag. TODO verify against the fetched file.
# Line 4 is a circle, which OpenStreetMap maps as 4A and 4B (one relation per
# direction of the same loop); 4A draws its geometry.
OSM_REFS = {"1": "1", "2": "2", "3": "3", "4": "4A", "5": "5"}

# --- Business filtering ------------------------------------------------

# EXACT INSEE codes, from the station table's own commune placement.
# Legacy codes checked 2026-09-30 against geo.api.gouv.fr's communes associées
# and déléguées (Lille's 59298 and 59355 the control): none in this scope.
COMMUNE_PREFIXES = ("34172",)

CITY_KEEP = "MONTPELLIER"   # scaffold field; COMMUNE_PREFIXES is the filter

# The French precedent (Paris, Marseille, Toulouse, Lille, Rennes): both
# catch-alls excluded on INSEE's own labels. A share is a fact about a city, so
# step 2 prints this city's; a share far from the siblings' goes to the owner.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
RAW_CLASSIFICATION_COLUMN = "naf_label"

# Sanity bounds: the commune's extent plus ~0.02 deg, from the EPCI
# contours. They catch a corrupt coordinate; the commune filter scopes.
MONTPELLIER_BBOX = {"lat_min": 43.55, "lat_max": 43.67, "lon_min": 3.79, "lon_max": 3.96}
