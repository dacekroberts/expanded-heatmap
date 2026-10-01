"""Bordeaux (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_france_batch.py (the France tram batch) from the
2026-09-27 screen's inputs and the station table in `data/_staging_scratch_2026-09-27/second_cities/france/stations_pure_2026-09-30`.
Read `.claude/skills/france-tram-city/SKILL.md` and
`docs/build_briefs/bordeaux.md` before filling anything. Every to-do marker is a value
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
DATA_RAW = ROOT / "data" / "bordeaux" / "raw"
DATA_PROCESSED = ROOT / "data" / "bordeaux" / "processed"
OUTPUTS = ROOT / "outputs" / "bordeaux"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# The communes the network serves, and their union: the regional
# scope's own record and the map's boundary (Lille's pattern).
SERVED_COMMUNES_CSV = OUTPUTS / "served_communes.csv"
SERVED_BOUNDARY_GEOJSON = DATA_PROCESSED / "served_boundary.geojson"

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
# screen's 2026-09-27 copy that may sit in data/bordeaux/raw/ already.
GTFS_URL = "https://www.data.gouv.fr/api/1/datasets/r/10b87ffe-e6bb-494d-93df-bb6019e223d9"
GTFS_DATASET = "Réseau urbain et scolaire TBM"
# The licence the NAP declares for this dataset. Licence Ouverte 1.0: credit
# Bordeaux Métropole and the feed's own date (read 2026-09-29).
GTFS_LICENCE = "fr-lo"
# Measured 2026-09-30 by the kit session: Licence Ouverte 1.0: credit Bordeaux
# Métropole and the feed's own date; feed_info.txt self-attests (publisher
# Mecatran).
# Read at build: the zip's feed_info.txt carries a feed_end_date, so the
# page quotes the operator's own window.
GTFS_SELF_ATTESTS = True
# The NAP dataset: fetch_sources.py reads the resource's date and window from it.
GTFS_NAP_ID = "67f5bad303325228295b7dff"

BOUNDARY_COMMUNE_CODE = "33063"
# ⚠ `geometry=contour`, NOT `fields=contour` (a 120-byte POINT, no error).
BOUNDARY_URL = ("https://geo.api.gouv.fr/communes/33063"
                "?geometry=contour&format=geojson")
METROPOLE_EPCI_CODES = ["243300316"]
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
# Median nearest-neighbour gap 425 m across the 140 in-scope stations (min 3
# m), Lambert-93, measured from the kit's station table - under ~550 m, so the
# half-size rings every French city takes (docs/ring_rules.md). Step 1 re-
# measures.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# APPROVED by the owner 2026-09-30, as docs/build_briefs/bordeaux.md recommended:
#   scope    regional - the worst line, A, keeps 17 of 47 stations (36%) in
#            commune 33063; under half goes regional (Lille's precedent)
#   mode     tram (the macro map's dot colour: what step 1 keeps, never the
#            feed's route_type flag)
#   coverage full (SIRENE: all three buckets)
SCOPE = "regional"
MAP_MODE = "tram"
MAP_COVERAGE = "full"

# What the feed types the kept lines as. Matched together with the line list,
# never alone: a type flag is not a mode decision (Reims and Rouen type theirs 1).
ROUTE_TYPES_RAIL = ("0",)
# The kept lines, by the feed's route_short_name.
LINE_KEYS = ["A", "B", "C", "D", "E", "F"]
# The build-day feed's route_ids (read by scripts/france_fill_build_day.py).
# A rolling feed may renumber: step 1 exits if they change.
ROUTE_IDS = ["163", "164", "59", "60", "61", "62"]

# Station rule (owner, 2026-09-29 and 09-30): the feed's own parent_station
# row, else the FIRST platform in stops.txt order per unchanged stop_name.
# Never a mean, never a rename. On a Licence Ouverte feed ONLY, a same-name
# pair (case and accents ignored) within 150 m keeps its first row; on an ODbL
# feed, never. Fictitious FIC_ stops are not stations.
# Measured 2026-09-30: 140 stations network-wide.
# THE SERVED COMMUNES, asserted rather than trusted: every commune holding
# a kept station, placed in the official contours. A change is a decision.
EXPECTED_SERVED_COMMUNES = {"33039": "Bègles", "33056": "Blanquefort", "33063": "Bordeaux", "33069": "Le Bouscat", "33075": "Bruges", "33119": "Cenon", "33162": "Eysines", "33167": "Floirac", "33200": "Le Haillan", "33249": "Lormont", "33281": "Mérignac", "33318": "Pessac", "33522": "Talence", "33550": "Villenave-d'Ornon"}
# Per line, network-wide (the regional scope keeps every station). Each is one
# to two fewer than the kit's table: the Licence Ouverte same-name rule (owner,
# 2026-09-30) keeps the first row of Hôtel de Ville (73 m), Les Aubiers (10 m),
# Pessac Centre / PESSAC CENTRE (3 m), Porte de Bourgogne (11 m) and Stade
# Chaban Delmas (104 m).
EXPECTED_STATIONS_PER_LINE = {"A": 46, "B": 37, "C": 31, "D": 24, "E": 41, "F": 34}

# GATE 3, recorded as OpenStreetMap has it (2026-09-30): each ref's most
# complete relation. Line B's relations carry no ref (named "Tram B"), so its
# 35 is read by name. The lines that branch read low, since each relation
# covers one branch: A (40, forks east and west), B (35 on the France Alouette
# branch, 32 on Pessac Centre), E (29 against the feed's 41: the feed's E
# includes trips that overlap A and C).
OPERATOR_STATION_COUNTS = {"A": 40, "B": 35, "C": 30, "D": 24, "E": 29, "F": 35}
OPERATOR_COUNTS_SOURCE = (
    "OpenStreetMap route relations, stop members of each line's most complete "
    "relation (line B's by name), read 2026-09-30")

# route_short_name -> the name riders use: TBM lettered lines A to F (the feed's own long names read "Tram A" to "Tram F").
LINE_NAMES = {"A": "Tram A", "B": "Tram B", "C": "Tram C", "D": "Tram D", "E": "Tram E", "F": "Tram F"}
# Each line's route_color from the build-day feed (the most-used route_id's
# where a line has several); pipeline/linecolour.py decides a clash.
LINE_COLOURS = {"A": "#831F82", "B": "#E50040", "C": "#D35098", "D": "#9262A3", "E": "#967651", "F": "#F08700"}

# The map's layer and title prefix for the lines.
MAP_SYSTEM_NAME = "Tram"
# Where the line GEOMETRY comes from: "gtfs" (the feed's shapes.txt) or "osm".
# Stations come from the feed either way.
LINE_GEOMETRY = "gtfs"
# OpenStreetMap route relations, for gate 3's count (geometry is the feed's):
# ONE query per city, cached by fetch_sources.py. Read 2026-09-30: the bbox
# returns TBM's sixteen tram relations; line B's carry a name but no ref.
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:120];"
    'relation["type"="route"]["route"~"^(tram|light_rail)$"]'
    "(44.72,-0.78,44.97,-0.47);"
    "out geom;")
# line key -> the relations' `ref` tag, checked against the fetched file (B has
# none; its gate 3 count above is read by name).
OSM_REFS = {"A": "A", "B": "B", "C": "C", "D": "D", "E": "E", "F": "F"}

# --- Business filtering ------------------------------------------------

# EXACT INSEE codes, from the station table's own commune placement.
# Legacy codes checked 2026-09-30 against geo.api.gouv.fr's communes associées
# and déléguées (Lille's 59298 and 59355 the control): none in this scope.
COMMUNE_PREFIXES = ("33039", "33056", "33063", "33069", "33075", "33119", "33162", "33167", "33200", "33249", "33281", "33318", "33522", "33550")

CITY_KEEP = "BORDEAUX"   # scaffold field; COMMUNE_PREFIXES is the filter

# The French precedent (Paris, Marseille, Toulouse, Lille, Rennes): both
# catch-alls excluded on INSEE's own labels. A share is a fact about a city, so
# step 2 prints this city's; a share far from the siblings' goes to the owner.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
RAW_CLASSIFICATION_COLUMN = "naf_label"

# Sanity bounds: the served communes' extent plus ~0.02 deg, from the EPCI
# contours. They catch a corrupt coordinate; the commune filter scopes.
BORDEAUX_BBOX = {"lat_min": 44.72, "lat_max": 44.97, "lon_min": -0.78, "lon_max": -0.47}
