"""Orléans-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_france_batch.py (the France tram batch) from the
2026-09-27 screen's inputs and the station table in `data/_staging_scratch_2026-09-27/second_cities/france/stations_pure_2026-09-30`.
Read `.claude/skills/france-tram-city/SKILL.md` and
`docs/build_briefs/orleans.md` before filling anything. Every to-do marker is a value
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
DATA_RAW = ROOT / "data" / "orleans" / "raw"
DATA_PROCESSED = ROOT / "data" / "orleans" / "processed"
OUTPUTS = ROOT / "outputs" / "orleans"

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
# screen's 2026-09-27 copy that may sit in data/orleans/raw/ already.
GTFS_URL = "https://www.data.gouv.fr/api/1/datasets/r/b2dfbaa3-47e9-4749-b6a4-750bebd760e7"
GTFS_DATASET = "Réseau urbain TAO"
# The licence the NAP declares for this dataset. Licence Ouverte 2.0: credit
# the producer and the date.
GTFS_LICENCE = "lov2"
# Measured 2026-09-30 by the kit session: feed_info.txt self-attests;
# parent_station on 9 of 103 platforms only.
# Read at build: the zip's feed_info.txt carries a feed_end_date, so the
# page quotes the operator's own window.
GTFS_SELF_ATTESTS = True
# The NAP dataset: fetch_sources.py reads the resource's date and window from it.
GTFS_NAP_ID = "61fb1b864ba517c310952886"

BOUNDARY_COMMUNE_CODE = "45234"
# ⚠ `geometry=contour`, NOT `fields=contour` (a 120-byte POINT, no error).
BOUNDARY_URL = ("https://geo.api.gouv.fr/communes/45234"
                "?geometry=contour&format=geojson")
METROPOLE_EPCI_CODES = ["244500468"]
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
# Median nearest-neighbour gap 383 m across the 32 in-scope stations (min 202
# m), Lambert-93, measured from the kit's station table - under ~550 m, so the
# half-size rings every French city takes (docs/ring_rules.md). Step 1 re-
# measures.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# APPROVED by the owner 2026-09-30, as docs/build_briefs/orleans.md recommended:
#   scope    commune - the worst line, B, keeps 15 of 25 stations (60%) in
#            commune 45234; half or more stays commune-only (Toulouse 52%,
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
LINE_KEYS = ["A", "B"]
# The build-day feed's route_ids (read by scripts/france_fill_build_day.py).
# A rolling feed may renumber: step 1 exits if they change.
ROUTE_IDS = ["ORLEANS:Line:A", "ORLEANS:Line:B"]

# Station rule (owner, 2026-09-29 and 09-30): the feed's own parent_station
# row, else the FIRST platform in stops.txt order per unchanged stop_name.
# Never a mean, never a rename. On a Licence Ouverte feed ONLY, a same-name
# pair (case and accents ignored) within 150 m keeps its first row; on an ODbL
# feed, never. Fictitious FIC_ stops are not stations.
# Measured 2026-09-30: 51 stations network-wide.
# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope
# decision is checkable. If these move, the decision is being re-taken.
EXPECTED_INSIDE_PER_LINE = {"A": 18, "B": 15}
EXPECTED_STATIONS_PER_LINE = {"A": 27, "B": 25}

# GATE 3: an independent per-line count, from outside the feed. Recorded
# as OpenStreetMap has it, even where it disagrees: step 1 prints any
# MISMATCH, and the build log says why.
OPERATOR_STATION_COUNTS = {"A": 27, "B": 25}
OPERATOR_COUNTS_SOURCE = (
    "OpenStreetMap route relations, stop members of each ref's most "
    "complete relation, read 2026-09-30")

# route_short_name -> the name riders use: TAO names its lines A and B, and the map
# spells out the mode, as Le Mans's and Toulouse's do.
LINE_NAMES = {"A": "Tram A", "B": "Tram B"}
# Each line's route_color from the build-day feed (the most-used route_id's
# where a line has several); pipeline/linecolour.py decides a clash.
LINE_COLOURS = {"A": "#E2121A", "B": "#762A80"}

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
    "(47.79,1.86,47.95,1.97);"
    "out geom;")
# line key -> the relations' `ref` tag, checked against the fetched file.
OSM_REFS = {"A": "A", "B": "B"}

# --- Business filtering ------------------------------------------------

# EXACT INSEE codes, from the station table's own commune placement.
# Legacy codes checked 2026-09-30 against geo.api.gouv.fr's communes associées
# and déléguées (Lille's 59298 and 59355 the control): none in this scope.
COMMUNE_PREFIXES = ("45234",)

CITY_KEEP = "ORLÉANS"   # scaffold field; COMMUNE_PREFIXES is the filter

# The French precedent (Paris, Marseille, Toulouse, Lille, Rennes): both
# catch-alls excluded on INSEE's own labels. A share is a fact about a city, so
# step 2 prints this city's; a share far from the siblings' goes to the owner.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
RAW_CLASSIFICATION_COLUMN = "naf_label"

# Sanity bounds: the commune's extent plus ~0.02 deg, from the EPCI
# contours. They catch a corrupt coordinate; the commune filter scopes.
ORLEANS_BBOX = {"lat_min": 47.79, "lat_max": 47.95, "lon_min": 1.86, "lon_max": 1.97}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600147558,3600147559)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("fr",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "Hôtel Brachet et jardin de la Vieille Intendance": "a historic mansion tagged an attraction, a hôtel in the French sense (tourism=attraction, wikidata Q22997019): the building's historic name, not a hotel business (the Paris precedent); tags read 2026-10-13",
    "Hôtel Cabu - Musée historique et archéologique de l'Orléanais": "a historic mansion tagged an attraction, a hôtel in the French sense (tourism=attraction, Wikipedia): the building's historic name, not a hotel business (the Paris precedent); tags read 2026-10-13",
    "Hôtel Groslot": "a historic mansion tagged an attraction, a hôtel in the French sense (tourism=attraction, Wikipedia): the building's historic name, not a hotel business (the Paris precedent); tags read 2026-10-13",
    "Hôtel Groslot, actuellement Hôtel de ville pour la célébration des mariages": "a listed Renaissance mansion in use as a town hall (amenity=townhall, ref:mhs, Wikipedia); the long name is OSM's; tags read 2026-10-13",
    "Hôtel Sanxerre": "a historic mansion tagged an attraction, a hôtel in the French sense (tourism=attraction, wikidata Q22944450): the building's historic name, not a hotel business (the Paris precedent); tags read 2026-10-13",
    "Hôtel Toutin": "a historic mansion tagged an attraction, a hôtel in the French sense (tourism=attraction, wikidata Q22944559): the building's historic name, not a hotel business (the Paris precedent); tags read 2026-10-13",
    "Hôtel des Créneaux": "a historic mansion tagged an attraction, a hôtel in the French sense (tourism=attraction, Wikipedia): the building's historic name, not a hotel business (the Paris precedent); tags read 2026-10-13",
}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/orleans.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # A second row of one object (owner, 2026-10-13)
    "node/2136003267": "'Guy Marie Robié': the second platform node of the stop Guy Marie Riobé (node/1576849093, 20 m away), with the name misspelt Robié",
    "node/1914487530": "'Cathédrale': one platform of the stop \"Cathédrale Hôtel de Ville\" (node/1865589193, 65 m away; both carry the stop area code TCAHDV), under a shortened name",
    "way/1518765969": "'Hôtel Groslot, actuellement Hôtel de ville pour la célébration des mariages': the same building as node/6894974505 \"Hôtel Groslot\" (same Wikidata entry, 25 m away), under a register title with a description in it",
    "node/9677370119": "'Notre Dame de Recouvrance': the same church as way/113997491 \"Église Notre-Dame-de-Recouvrance\" (same Wikidata entry, 30 m away)",
    "node/11752236683": "'Église Saint-Euverte d'Orléans': the same church as way/113692150 \"Église Saint-Euverte\" (same Wikidata entry, 35 m away)",
    "node/6895191699": "'Temple protestant d'Orléans': the same temple as way/152140295 \"Église Réformée d'Orléans\" (same Wikidata entry, under 10 m away); either row could be the one kept, the node's name is the article's title",
    "node/11389672570": "'Parc Floral': a node \"Parc Floral\" inside way/491694575 \"Parc Floral de la Source\", which carries the article",
    "way/491692199": "'Parc du square Poursine': the same square as way/1149849950 \"Square Poursine\", same spot",
    # A monument-register entry named only by type and house number (owner, 2026-10-13)
    "relation/1026963": "'Immeuble n°1': \"Immeuble n°1\": a listed residential building of the rue Royale row named by type and house number only (23 such rows; each has its own Wikidata entry, which is why the rules kept them)",
    "way/66182556": "'Immeuble n°3': \"Immeuble n°3\", type and house number only",
    "way/113978057": "'Immeuble n°11': \"Immeuble n°11\", type and house number only",
    "way/113703665": "'Immeuble n°12': \"Immeuble n°12\", type and house number only",
    "way/113977920": "'Immeuble n°13': \"Immeuble n°13\", type and house number only",
    "way/113703576": "'Immeuble n°14': \"Immeuble n°14\", type and house number only",
    "way/113978004": "'Immeuble n°15': \"Immeuble n°15\", type and house number only",
    "way/113977906": "'Immeuble n°17': \"Immeuble n°17\", type and house number only",
    "way/113978227": "'Immeuble n°19': \"Immeuble n°19\", type and house number only",
    "way/113704116": "'Immeuble n°20': \"Immeuble n°20\", type and house number only",
    "way/113977374": "'Immeuble n°21': \"Immeuble n°21\", type and house number only",
    "way/113978190": "'Immeuble n°25': \"Immeuble n°25\", type and house number only",
    "way/113704415": "'Immeuble n°26': \"Immeuble n°26\", type and house number only",
    "way/113977714": "'Immeuble n°27': \"Immeuble n°27\", type and house number only",
    "way/113704539": "'Immeuble n°28': \"Immeuble n°28\", type and house number only",
    "way/113978295": "'Immeuble n°29': \"Immeuble n°29\", type and house number only",
    "way/113703636": "'Immeuble n°30': \"Immeuble n°30\", type and house number only",
    "way/113977934": "'Immeuble n°31': \"Immeuble n°31\", type and house number only",
    "way/113703873": "'Immeuble n°32': \"Immeuble n°32\", type and house number only",
    "way/113977597": "'Immeuble n°33': \"Immeuble n°33\", type and house number only",
    "way/113703701": "'Immeuble n°34': \"Immeuble n°34\", type and house number only",
    "way/113998175": "'Immeuble n°45': \"Immeuble n°45\", type and house number only",
    "way/113978280": "'Immeuble et maison n°2-4': \"Immeuble et maison n°2-4\", type and house numbers only",
    # A bare type word (owner, 2026-10-13)
    "node/9813839781": "'Jardins ouvriers': \"Jardins ouvriers\" = allotment gardens, the type alone (operator=AOJOF)",
    "node/10200585078": "'Campus Universitaire': \"Campus Universitaire\", the type alone, tagged place=hamlet",
    # Worship named only by its body or chain (owner, 2026-10-13)
    "node/9480618626": "'Église néo-apostolique': \"Église néo-apostolique\", the denomination alone",
    # A religious office (owner, 2026-10-13)
    "node/9480671086": "'Évêché': \"Évêché\" = the bishop's house and offices, a bare type word, tagged a place of worship",
    # A glitched name (owner, 2026-10-13)
    "node/8388112099": "'All de Mistigris': \"All de Mistigris\": Allée cut to \"All\"; a street's name on a place=locality node",
    "node/8388112102": "'All de la Loire': \"All de la Loire\": Allée cut to \"All\"; a street's name on a place=locality node",
    "node/8388112098": "'Res La Mouchetière': \"Res La Mouchetière\": Résidence cut to \"Res\"; a housing residence on a place=locality node",
}
