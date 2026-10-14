"""Caen-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_france_batch.py (the France tram batch) from the
2026-09-27 screen's inputs and the station table in `data/_staging_scratch_2026-09-27/second_cities/france/stations_pure_2026-09-30`.
Read `.claude/skills/france-tram-city/SKILL.md` and
`docs/build_briefs/caen.md` before filling anything. Every to-do marker is a value
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
DATA_RAW = ROOT / "data" / "caen" / "raw"
DATA_PROCESSED = ROOT / "data" / "caen" / "processed"
OUTPUTS = ROOT / "outputs" / "caen"

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
# screen's 2026-09-27 copy that may sit in data/caen/raw/ already.
GTFS_URL = "https://transport.data.gouv.fr/resources/81942/download"
GTFS_DATASET = "Agrégat des réseaux urbains et interurbains de Normandie"
# The licence the NAP declares for this dataset. Licence Ouverte 2.0: credit
# the producer and the date.
GTFS_LICENCE = "lov2"
# The aggregate carries several networks: keep this agency only.
GTFS_AGENCY_ID = "ATOUMOD029:Network:029:LOC"
# Measured 2026-09-30 by the kit session: no feed of its own: the Normandie
# aggregate, agency Twisto; credit its Concédant, Syndicat mixte Atoumod; the
# aggregate's shapes are stop-to-stop (AUTO_), so geometry from OpenStreetMap.
# Read at build: the zip declares no dated window, so the page quotes the
# NAP's reading of it, recorded at fetch.
GTFS_SELF_ATTESTS = False
# The NAP dataset: fetch_sources.py reads the resource's date and window from it.
GTFS_NAP_ID = "5ced52ed8b4c4177b679d377"

BOUNDARY_COMMUNE_CODE = "14118"
# ⚠ `geometry=contour`, NOT `fields=contour` (a 120-byte POINT, no error).
BOUNDARY_URL = ("https://geo.api.gouv.fr/communes/14118"
                "?geometry=contour&format=geojson")
METROPOLE_EPCI_CODES = ["200065597"]
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
# Median nearest-neighbour gap 311 m across the 29 in-scope stations (min 12
# m), Lambert-93, measured from the kit's station table - under ~550 m, so the
# half-size rings every French city takes (docs/ring_rules.md). Step 1 re-
# measures.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# APPROVED by the owner 2026-09-30, as docs/build_briefs/caen.md recommended:
#   scope    commune - the worst line, T1, keeps 19 of 25 stations (76%) in
#            commune 14118; half or more stays commune-only (Toulouse 52%,
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
LINE_KEYS = ["T1", "T2", "T3"]
# The build-day feed's route_ids (read by scripts/france_fill_build_day.py).
# A rolling feed may renumber: step 1 exits if they change.
ROUTE_IDS = ["ATOUMOD029:Line:T1:LOC", "ATOUMOD029:Line:T2:LOC", "ATOUMOD029:Line:T3:LOC"]

# Station rule (owner, 2026-09-29 and 09-30): the feed's own parent_station
# row, else the FIRST platform in stops.txt order per unchanged stop_name.
# Never a mean, never a rename. On a Licence Ouverte feed ONLY, a same-name
# pair (case and accents ignored) within 150 m keeps its first row; on an ODbL
# feed, never. Fictitious FIC_ stops are not stations.
# Measured 2026-09-30: 38 stations network-wide.
# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope
# decision is checkable. If these move, the decision is being re-taken.
# T2 counts one fewer than the kit's table: the Licence Ouverte same-name rule
# (owner, 2026-09-30) keeps "Presqu'île" and drops "Presqu'Ile" 12 m away.
EXPECTED_INSIDE_PER_LINE = {"T1": 19, "T2": 16, "T3": 13}
EXPECTED_STATIONS_PER_LINE = {"T1": 25, "T2": 17, "T3": 15}

# GATE 3: an independent per-line count, from outside the feed. Recorded
# as OpenStreetMap has it, even where it disagrees: step 1 prints any
# MISMATCH, and the build log says why.
OPERATOR_STATION_COUNTS = {"T1": 24, "T2": 17, "T3": 15}
OPERATOR_COUNTS_SOURCE = (
    "OpenStreetMap route relations, stop members of each ref's most "
    "complete relation, read 2026-09-30")

# route_short_name -> the name riders use: Twisto names its tram lines T1, T2 and T3.
LINE_NAMES = {"T1": "Tram T1", "T2": "Tram T2", "T3": "Tram T3"}
# Each line's route_color from the build-day feed (the most-used route_id's
# where a line has several); pipeline/linecolour.py decides a clash.
LINE_COLOURS = {"T1": "#23A638", "T2": "#E73132", "T3": "#009ADF"}

# The map's layer and title prefix for the lines.
MAP_SYSTEM_NAME = "Tram"
# Where the line GEOMETRY comes from: "gtfs" (the feed's shapes.txt) or "osm".
# Stations come from the feed either way.
LINE_GEOMETRY = "osm"
# OpenStreetMap route relations, for the LINE GEOMETRY and gate 3's count: ONE query per city, cached by
# fetch_sources.py (the owner's Overpass rule). Checked: the relations'
# `network` tag and refs: read at build, the query returns this network.
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:120];"
    'relation["type"="route"]["route"~"^(tram|light_rail)$"]'
    "(49.13,-0.43,49.24,-0.31);"
    "out geom;")
# line key -> the relations' `ref` tag, checked against the fetched file.
OSM_REFS = {"T1": "T1", "T2": "T2", "T3": "T3"}

# --- Business filtering ------------------------------------------------

# EXACT INSEE codes, from the station table's own commune placement.
# Legacy codes checked 2026-09-30 against geo.api.gouv.fr's communes associées
# and déléguées (Lille's 59298 and 59355 the control): none in this scope.
COMMUNE_PREFIXES = ("14118",)

CITY_KEEP = "CAEN"   # scaffold field; COMMUNE_PREFIXES is the filter

# The French precedent (Paris, Marseille, Toulouse, Lille, Rennes): both
# catch-alls excluded on INSEE's own labels. A share is a fact about a city, so
# step 2 prints this city's; a share far from the siblings' goes to the owner.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
RAW_CLASSIFICATION_COLUMN = "naf_label"

# Sanity bounds: the commune's extent plus ~0.02 deg, from the EPCI
# contours. They catch a corrupt coordinate; the commune filter scopes.
CAEN_BBOX = {"lat_min": 49.13, "lat_max": 49.24, "lon_min": -0.43, "lon_max": -0.31}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600149197)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("fr",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "Rue du Magasin à Poudre": "a public street named for a building or institution on it, not a business (tertiary class; batch 2b precedent, _named_street); tags read 2026-10-13",
}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/caen.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # Worship named only by a body or a denomination (owner, 2026-10-13)
    "way/155677465": "'Église Réformée de France': the whole name is the national body's ('Reformed Church of France'), no place or dedication; the French word lists of worship_only do not hold 'réformée'",
    # A school's or an organisation's ground tagged a park (owner, 2026-10-13)
    "way/1434177332": "'Scouts et Guides de France (Territoire Basse-Normandie)': the name is the scout association and its regional branch, the operator the same body: its grounds, not a public park",
    # A description standing in for a name (owner, 2026-10-13)
    "node/12437436718": "'Ancien souterrain': 'former underground passage': a label on a spot inside the castle, no name",
    "node/12437436717": "'Ancienne maison médiévale': 'former medieval house': as above, same run of nodes in the castle",
    "node/12437436719": "'Anciennes forges et écuries': 'former forges and stables': as above",
    # A glitched name (owner, 2026-10-13)
    "node/2428836194": "'Temple Gallo-Roman _Fanum': a stray underscore in the name, and 'Roman' for 'romain'; no wikidata, no clean name in another tag",
    # A duplicate of one object (owner, 2026-10-13)
    "node/3119272607": "'L'Abbaye aux Hommes': the abbey again, about 80 m from its own row Abbaye aux Hommes (way/155629494, wikidata=Q376932); the leading article kept the two names apart",
    "way/794839194": "'Vestiges de l'ancienne église Saint-Gilles': the same ruin as Église Saint-Gilles (way/205610832, the same Q3581709 and article), about 10 m away",
    # A bare type word (owner, 2026-10-13)
    "node/13076197526": "'Hôtel de Ville': 'town hall' alone, admitted by the abbey's article, at the same point as the abbey's own row (way/155629494)",
}
