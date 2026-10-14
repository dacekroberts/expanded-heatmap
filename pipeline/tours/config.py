"""Tours-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_france_batch.py (the France tram batch) from the
2026-09-27 screen's inputs and the station table in `data/_staging_scratch_2026-09-27/second_cities/france/stations_pure_2026-09-30`.
Read `.claude/skills/france-tram-city/SKILL.md` and
`docs/build_briefs/tours.md` before filling anything. Every to-do marker is a value
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
DATA_RAW = ROOT / "data" / "tours" / "raw"
DATA_PROCESSED = ROOT / "data" / "tours" / "processed"
OUTPUTS = ROOT / "outputs" / "tours"

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
# screen's 2026-09-27 copy that may sit in data/tours/raw/ already.
GTFS_URL = "https://www.data.gouv.fr/api/1/datasets/r/198b7602-5e74-4d88-b6bc-483af85a2430"
GTFS_DATASET = "Réseau urbain et périurbain Fil Bleu"
# The licence the NAP declares for this dataset. Licence Ouverte 2.0: credit
# the producer and the date.
GTFS_LICENCE = "lov2"
# Measured 2026-09-30 by the kit session: ships feed_infos.txt (sic), so no
# feed_info.txt.
# Read at build: the zip declares no dated window, so the page quotes the
# NAP's reading of it, recorded at fetch.
GTFS_SELF_ATTESTS = False
# The NAP dataset: fetch_sources.py reads the resource's date and window from it.
GTFS_NAP_ID = "638157af7f6b7cd00e2908e1"

BOUNDARY_COMMUNE_CODE = "37261"
# ⚠ `geometry=contour`, NOT `fields=contour` (a 120-byte POINT, no error).
BOUNDARY_URL = ("https://geo.api.gouv.fr/communes/37261"
                "?geometry=contour&format=geojson")
METROPOLE_EPCI_CODES = ["243700754"]
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
# Median nearest-neighbour gap 377 m across the 22 in-scope stations (min 272
# m), Lambert-93, measured from the kit's station table - under ~550 m, so the
# half-size rings every French city takes (docs/ring_rules.md). Step 1 re-
# measures.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# APPROVED by the owner 2026-09-30, as docs/build_briefs/tours.md recommended:
#   scope    commune - the worst line, A, keeps 22 of 29 stations (76%) in
#            commune 37261; half or more stays commune-only (Toulouse 52%,
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
LINE_KEYS = ["A"]
# The build-day feed's route_ids (read by scripts/france_fill_build_day.py).
# A rolling feed may renumber: step 1 exits if they change.
ROUTE_IDS = ["TTR:LINE:A"]

# Station rule (owner, 2026-09-29 and 09-30): the feed's own parent_station
# row, else the FIRST platform in stops.txt order per unchanged stop_name.
# Never a mean, never a rename. On a Licence Ouverte feed ONLY, a same-name
# pair (case and accents ignored) within 150 m keeps its first row; on an ODbL
# feed, never. Fictitious FIC_ stops are not stations.
# Measured 2026-09-30: 29 stations network-wide.
# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope
# decision is checkable. If these move, the decision is being re-taken.
EXPECTED_INSIDE_PER_LINE = {"A": 22}
EXPECTED_STATIONS_PER_LINE = {"A": 29}

# GATE 3: an independent per-line count, from outside the feed. Recorded
# as OpenStreetMap has it, even where it disagrees: step 1 prints any
# MISMATCH, and the build log says why.
OPERATOR_STATION_COUNTS = {"A": 29}
OPERATOR_COUNTS_SOURCE = (
    "OpenStreetMap route relations, stop members of each ref's most "
    "complete relation, read 2026-09-30")

# route_short_name -> the name riders use: Fil Bleu names its line A ("ligne A du tram"), and the map
# spells out the mode, as Le Mans's and Toulouse's do.
LINE_NAMES = {"A": "Tram A"}
# Fil Bleu's route_color is #BD074E, Delta-E 5.5 from the Food service pins -
# under the hard floor of 10, so pipeline/linecolour.py refuses it. The same
# hue darkened 16% of HSL lightness: 29.5 from the pins, where Lille's Tram T
# landed (29.3 and 34.4) on the same rule.
LINE_COLOURS = {"A": "#6E042E"}

# The map's layer and title prefix for the lines.
MAP_SYSTEM_NAME = "Tram"
# Where the line GEOMETRY comes from: "gtfs" (the feed's shapes.txt) or "osm".
# Stations come from the feed either way.
LINE_GEOMETRY = "gtfs"
# OpenStreetMap route relations, for gate 3's independent per-line count (geometry is the feed's): ONE query per city, cached by
# fetch_sources.py (the owner's Overpass rule). Checked: the relations'
# `network` tag and refs: read at build, the query returns this network.
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:120];"
    'relation["type"="route"]["route"~"^(tram|light_rail)$"]'
    "(47.33,0.63,47.46,0.76);"
    "out geom;")
# line key -> the relations' `ref` tag, checked against the fetched file.
OSM_REFS = {"A": "A"}

# --- Business filtering ------------------------------------------------

# EXACT INSEE codes, from the station table's own commune placement.
# Legacy codes checked 2026-09-30 against geo.api.gouv.fr's communes associées
# and déléguées (Lille's 59298 and 59355 the control): none in this scope.
COMMUNE_PREFIXES = ("37261",)

CITY_KEEP = "TOURS"   # scaffold field; COMMUNE_PREFIXES is the filter

# The French precedent (Paris, Marseille, Toulouse, Lille, Rennes): both
# catch-alls excluded on INSEE's own labels. A share is a fact about a city, so
# step 2 prints this city's; a share far from the siblings' goes to the owner.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
RAW_CLASSIFICATION_COLUMN = "naf_label"

# Sanity bounds: the commune's extent plus ~0.02 deg, from the EPCI
# contours. They catch a corrupt coordinate; the commune filter scopes.
TOURS_BBOX = {"lat_min": 47.33, "lat_max": 47.46, "lon_min": 0.63, "lon_max": 0.76}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600076306)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("fr",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "Ancien hôtel du Doyenné de Saint-Gatien": "a listed historic mansion or public building, a hôtel in the French sense (ref:mhs PA00098169, Wikipedia): the building's historic name, not a hotel business (the Paris precedent); tags read 2026-10-13",
    "Hôtel Goüin": "a listed historic mansion or public building, a hôtel in the French sense (ref:mhs PA00098170, tourism=museum, Wikipedia): the building's historic name, not a hotel business (the Paris precedent); tags read 2026-10-13",
    "Hôtel des ducs de Touraine": "a listed historic mansion or public building, a hôtel in the French sense (ref:mhs PA00098168, Wikipedia): the building's historic name, not a hotel business (the Paris precedent); tags read 2026-10-13",
    "Portail de l'hôtel des trésoriers de Saint-Martin": "a listed gateway tagged an attraction (barrier=sally_port, heritage=2, ref:mhs, wikidata): a monument, not a hotel; tags read 2026-10-13",
    "Ruines de l'Hôtel de Beaune-Semblançay": "the listed ruins of a Renaissance mansion (historic=ruins, ref:mhs, Wikipedia); tags read 2026-10-13",
}
# Dropped by id on the full read of 2026-10-13 under the owner's rulings of the
# same day, each id read with its cached name (docs/decisions_drafts/search-rollout.md).
PLACE_DROPPED = {
    # duplicate: dropped in the full read (owner, 2026-10-13)
    "node/2439033646": "'Gare de Tours 2': the tram stop at the railway station twice, at the same point: platform 2 of the stop whose platform 1 is node/2380890444; the platform number is part of the name (local_ref=2) (full read, duplicate)",
    "node/2439033652": "'Jean Jaurès 2': the Jean Jaurès tram stop twice, 60 m apart: the second platform, numbered in the name (full read, duplicate)",
    "way/69469160": "'Pavillon de l'Octroi': one of the two toll pavilions, 35 m from the site relation that has the article and the listing (relation/7603658) (full read, duplicate)",
    # bare type: dropped in the full read (owner, 2026-10-13)
    "way/49357257": "'Centre Commercial': \"shopping centre\", the type words alone, on a hedged park polygon (full read, bare type)",
    # description: dropped in the full read (owner, 2026-10-13)
    "node/11111659905": "'Ancien pressoir à vin': \"old wine press\", a description of the object (historic=pressoir, not a known tag value) (full read, description)",
    "node/5132993446": "'Deux Caves du 10e et du 15e Siècle': the heritage register's description of the listing (\"two cellars of the 10th and 15th century\"), a room inside a building (full read, description)",
    "relation/7610969": "'Maisons du 15e siècle': the heritage register's description (\"15th-century houses\"); the houses are homes with no name of their own (full read, description)",
    "way/868720179": "'parc paysager société crématiste': lower-case mapper's description: the landscaped grounds of a cremation society (full read, description)",
    # estate facility: dropped in the full read (owner, 2026-10-13)
    "way/1209385863": "'Parc de la Cité Bords de Loire': access=customers: the grounds of one residence, not a public park (full read, estate facility)",
    # religious residence: dropped in the full read (owner, 2026-10-13)
    "way/74370359": "'Presbytère (Paroisse St Maurice)': a presbytery (priests' house) tagged a place of worship, named for the parish (full read, religious residence)",
    "way/143581025": "'Presbytère Saint-François de Paule': a presbytery tagged a place of worship; the church of that name is its own row (full read, religious residence)",
    # worship body: dropped in the full read (owner, 2026-10-13)
    "way/73676398": "'Église Adventiste du Septième Jour': denomination name alone (full read, worship body)",
    "way/315316288": "'Association Culturelle Turque de Tours': named only for the association that runs it; the prayer room has no name of its own (full read, worship body)",
    # business: dropped in the full read (owner, 2026-10-13)
    "way/1551359567": "'Excelia Business School': a private business school (operator:type=private); the article is the school group's, not this building's (full read, business)",
}
