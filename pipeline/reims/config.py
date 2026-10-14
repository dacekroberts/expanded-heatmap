"""Reims-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_france_batch.py (the France tram batch) from the
2026-09-27 screen's inputs and the station table in `data/_staging_scratch_2026-09-27/second_cities/france/stations_pure_2026-09-30`.
Read `.claude/skills/france-tram-city/SKILL.md` and
`docs/build_briefs/reims.md` before filling anything. Every to-do marker is a value
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
DATA_RAW = ROOT / "data" / "reims" / "raw"
DATA_PROCESSED = ROOT / "data" / "reims" / "processed"
OUTPUTS = ROOT / "outputs" / "reims"

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
# screen's 2026-09-27 copy that may sit in data/reims/raw/ already.
GTFS_URL = "https://transport.data.gouv.fr/resources/80594/download"
GTFS_DATASET = "Réseau urbain Grand Reims Mobilités"
# The licence the NAP declares for this dataset. Licence Ouverte 2.0: credit
# the producer and the date.
GTFS_LICENCE = "lov2"
# Measured 2026-09-30 by the kit session: the feed types its tram route_type 1
# (metro); it is a tram - mode 'tram'.
# Read at build: the zip's feed_info.txt carries a feed_end_date, so the
# page quotes the operator's own window.
GTFS_SELF_ATTESTS = True
# The NAP dataset: fetch_sources.py reads the resource's date and window from it.
GTFS_NAP_ID = "63b4c3d200fbf8e5ed9dde9a"

BOUNDARY_COMMUNE_CODE = "51454"
# ⚠ `geometry=contour`, NOT `fields=contour` (a 120-byte POINT, no error).
BOUNDARY_URL = ("https://geo.api.gouv.fr/communes/51454"
                "?geometry=contour&format=geojson")
METROPOLE_EPCI_CODES = ["200067213"]
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
# Median nearest-neighbour gap 370 m across the 21 in-scope stations (min 247
# m), Lambert-93, measured from the kit's station table - under ~550 m, so the
# half-size rings every French city takes (docs/ring_rules.md). Step 1 re-
# measures.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# APPROVED by the owner 2026-09-30, as docs/build_briefs/reims.md recommended:
#   scope    commune - the worst line, TRAM, keeps 21 of 24 stations (88%) in
#            commune 51454; half or more stays commune-only (Toulouse 52%,
#            Rennes 73%)
#   mode     tram (the macro map's dot colour: what step 1 keeps, never the
#            feed's route_type flag)
#   coverage full (SIRENE: all three buckets)
SCOPE = "commune"
MAP_MODE = "tram"
MAP_COVERAGE = "full"

# What the feed types the kept lines as. Matched together with the line list,
# never alone: a type flag is not a mode decision (Reims and Rouen type theirs 1).
ROUTE_TYPES_RAIL = ("1",)
# The kept lines. ⚠ THE BRIEF SAID ONE LINE, and it was out of date: since
# 2025-11-24 Grand Reims Mobilités runs TWO public lines, T1 (Neufchâtel -
# Hôpital Debré, 21 stops) and T2 (Neufchâtel - Gare Champagne TGV, 22 stops),
# the former lines A and B (fr.wikipedia "Tramway de Reims", checked
# 2026-09-30; OpenStreetMap's relations say the same). The feed still carries
# ONE route, "TRAM", so ROUTE_BRANCHES splits its trips by the terminus each
# serves; a trunk short-working counts for both lines.
LINE_KEYS = ["T1", "T2"]
ROUTE_BRANCHES = {"TRAM": {"T1": "HOPITAL DEBRE",
                           "T2": "GARE CHAMP. TGV"}}  # platform names
# The build-day feed's route_ids (read by scripts/france_fill_build_day.py).
# A rolling feed may renumber: step 1 exits if they change.
ROUTE_IDS = ["TRAM"]

# Station rule (owner, 2026-09-29 and 09-30): the feed's own parent_station
# row, else the FIRST platform in stops.txt order per unchanged stop_name.
# Never a mean, never a rename. On a Licence Ouverte feed ONLY, a same-name
# pair (case and accents ignored) within 150 m keeps its first row; on an ODbL
# feed, never. Fictitious FIC_ stops are not stations.
# Measured 2026-09-30: 24 stations network-wide.
# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope
# decision is checkable. If these move, the decision is being re-taken.
EXPECTED_INSIDE_PER_LINE = {"T1": 20, "T2": 19}
EXPECTED_STATIONS_PER_LINE = {"T1": 21, "T2": 22}

# GATE 3: the published stop counts, 21 and 22 (fr.wikipedia's line articles),
# which OpenStreetMap's four relations reproduce exactly (T1 21, T2 22,
# 2026-09-30). The relations carry no `ref`, so OSM_REFS is empty and the
# counts are recorded here by hand.
OPERATOR_STATION_COUNTS = {"T1": 21, "T2": 22}
OPERATOR_COUNTS_SOURCE = (
    "fr.wikipedia's Ligne T1 and Ligne T2 articles (21 and 22 stops), matched by "
    "OpenStreetMap's relations 10544852/3 and 18349763/4, read 2026-09-30")

# The public names T1 and T2, with the mode spelt out as Le Mans's are.
LINE_NAMES = {"T1": "Tram T1", "T2": "Tram T2"}
# The feed's one route_color, #E0001B, is T1's red (OpenStreetMap tags T1
# #ed2625). T2 takes OpenStreetMap's #00AEF0: the feed cannot tell the two
# lines apart, and OSM's colour tag is data under the OpenStreetMap notice.
LINE_COLOURS = {"T1": "#E0001B", "T2": "#00AEF0"}

# The map's layer and title prefix for the lines.
MAP_SYSTEM_NAME = "Tram"
# Where the line GEOMETRY comes from: "gtfs" (the feed's shapes.txt) or "osm".
# Stations come from the feed either way.
LINE_GEOMETRY = "gtfs"
# OpenStreetMap route relations (geometry is the feed's): ONE query per city,
# cached by fetch_sources.py. Read 2026-09-30: the bbox returns exactly Grand
# Reims Mobilités' four tram relations, which carry names but no ref.
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:120];"
    'relation["type"="route"]["route"~"^(tram|light_rail)$"]'
    "(49.18,3.97,49.32,4.14);"
    "out geom;")
# The relations carry no ref (see gate 3 above).
OSM_REFS = {}

# --- Business filtering ------------------------------------------------

# EXACT INSEE codes, from the station table's own commune placement.
# Legacy codes checked 2026-09-30 against geo.api.gouv.fr's communes associées
# and déléguées (Lille's 59298 and 59355 the control): none in this scope.
COMMUNE_PREFIXES = ("51454",)

CITY_KEEP = "REIMS"   # scaffold field; COMMUNE_PREFIXES is the filter

# The French precedent (Paris, Marseille, Toulouse, Lille, Rennes): both
# catch-alls excluded on INSEE's own labels. A share is a fact about a city, so
# step 2 prints this city's; a share far from the siblings' goes to the owner.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
RAW_CLASSIFICATION_COLUMN = "naf_label"

# Sanity bounds: the commune's extent plus ~0.02 deg, from the EPCI
# contours. They catch a corrupt coordinate; the commune filter scopes.
REIMS_BBOX = {"lat_min": 49.18, "lat_max": 49.32, "lon_min": 3.97, "lon_max": 4.14}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600036458)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("fr",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "Hôtel Ponsardin": "a listed historic mansion or public building, a hôtel in the French sense (ref:mhs PA00078793, Wikipedia): the building's historic name, not a hotel business (the Paris precedent); tags read 2026-10-13",
    "Hôtel de Bézannes": "a listed historic mansion or public building, a hôtel in the French sense (ref:mhs PA00078790, Wikipedia): the building's historic name, not a hotel business (the Paris precedent); tags read 2026-10-13",
    "Jardin du Musée-hôtel Le Vergeur": "a public garden named for the museum-mansion beside it (leisure=park, Wikipedia); tags read 2026-10-13",
    "Musée Hôtel le Vergeur": "a museum in a hôtel particulier (tourism=museum, Wikipedia); tags read 2026-10-13",
}
# Dropped by id on the full read of 2026-10-13 under the owner's rulings of the
# same day, each id read with its cached name (docs/decisions_drafts/search-rollout.md).
PLACE_DROPPED = {
    # description: dropped in the full read (owner, 2026-10-13)
    "way/741215757": "'parc et residence': \"park and residence\" in lower case: a mapper's note on the grounds of a housing block, tagged leisure=park (full read, description)",
    "way/222784804": "'jardin du couvent': \"the convent's garden\" in lower case: a description, and the garden of a religious residence (full read, description)",
    "way/625755903": "'Terrain rue de la Maladrerie': \"plot on rue de la Maladrerie\": a description of a city-owned plot, tagged leisure=park (full read, description)",
    "node/6944372085": "'Les grands magasins (art déco)': \"the department stores (art deco)\": a description with a mapper's style note in brackets, historic=monument on a node (full read, description)",
    "node/7036857830": "'Restitution d'un tumulus Gaulois': \"reconstruction of a Gaulish tumulus\", access=no: a description of an exhibit that cannot be entered (full read, description)",
    "node/7036921358": "'Restitution d'une tombe à char gauloise': \"reconstruction of a Gaulish chariot tomb\", access=no, 60 m from the row above (full read, description)",
    "way/90719109": "'Ateliers de fabrication': \"manufacturing workshops\": the function of a building in an industrial site, building=industrial (full read, description)",
    "way/90730629": "'Ateliers de réparation': \"repair workshops\": as above, 200 m away (full read, description)",
    "node/10178870778": "'Îlot A': \"Block A\": a planning block's letter as a quarter's name (full read, description)",
    "way/934172282": "'Îlot G': \"Block G\": a block's letter; the description says detached housing built about 1972 (full read, description)",
    "node/8655840209": "'Îlot H': \"Block H\": a block's letter; the alt name (Secteur Tourangeaux) is the real one (full read, description)",
    "node/10557477903": "'Îlot I': \"Block I\": a block's letter (full read, description)",
    "way/1112303723": "'Îlot J': \"Block J\": a block's letter, 200 m from Block I (full read, description)",
    # bare type: dropped in the full read (owner, 2026-10-13)
    "way/904713009": "'Cour d'honneur': \"Cour d'honneur\" (court of honour), the type alone on place=square (full read, bare type)",
    "node/6942475486": "'Ancienne fontaine': \"Ancienne fontaine\" (old fountain), the type alone (full read, bare type)",
    "node/5326108648": "'Monument de guerre': \"Monument de guerre\" (war monument), the type alone (full read, bare type)",
    "way/741060562": "'Secteur pavillonnaire': \"detached-housing sector\": a housing type as the name of a neighbourhood (description tag says the same) (full read, bare type)",
    "way/659405177": "'Secteur collectif': \"collective-housing sector\": a housing type as the name; the description names the real district (ZAC de la Bonne Femme) (full read, bare type)",
    # worship body: dropped in the full read (owner, 2026-10-13)
    "way/92308609": "'Mission chrétienne': \"Christian mission\": no congregation's name, denomination=evangelical only (full read, worship body)",
    "way/92294275": "'Association de la Mosquée et du Centre Islamique de Reims': named for the association that runs it (\"Association of the Mosque and Islamic Centre of Reims\"), a body's name (full read, worship body)",
    "node/7456690318": "'Maison Diocesaine Saint-Sixte': the diocesan house, a religious office tagged a place of worship (full read, worship body)",
    # business: dropped in the full read (owner, 2026-10-13)
    "relation/8823000": "'Champagne Henriot': a champagne house under its trade name (website and description say it trades), tagged historic=industrial on a site relation; no wikidata (full read, business)",
    "way/633476015": "'Forbo Sarlino': a working factory under its company name (operator is the company, an S.A.S.), tagged historic=industrial (full read, business)",
    # vanished: dropped in the full read (owner, 2026-10-13)
    "way/633713396": "'Anciens Établissements Taillet': the description says the site was demolished in 2013 (full read, vanished)",
    # duplicate: dropped in the full read (owner, 2026-10-13)
    "way/629186116": "'Ancienne église Saint-Michel': the doorway of the former Saint-Michel church, at the same point as Église Saint-Michel de Reims node/8189738891, which has the wikidata (full read, duplicate)",
    "node/6985672067": "'Cité Warnier-David': the Warnier-David garden city as a node, 10 m from the relation Cité-Jardin Warnier-David relation/10308807 (full read, duplicate)",
    "node/6939127890": "'SIR 1': \"SIR 1\", an abbreviation; same alt name as the quarter Wilson 1 way/659403552, 100 m away (full read, duplicate)",
    # home: dropped in the full read (owner, 2026-10-13)
    "way/640089704": "'Tours Naudin': one apartment complex listed as a neighbourhood: the description says three residential towers, the operator is the landlord (full read, home)",
    "way/650768925": "'Maison blanche Centre commercial': one landlord's 13 flats around a shopping centre (description), named for the shopping centre (full read, home)",
    "way/764274824": "'Murigny Simon Courbet Forestier': one landlord's 44 dwellings (description), named for its three streets (full read, home)",
    # estate marketing: dropped in the full read (owner, 2026-10-13)
    "way/751139188": "'Plein R': a developer's programme name: the description says a housing programme on a former school site, carried by a developer (full read, estate marketing)",
    # a duplicate of a row that stays, dropped though it carries a wikipedia tag (owner, 2026-10-13)
    "node/7388163831": "'Cathédrale de Reims': the cathedral again as an archaeological-site node with the cathedral's own wikidata Q206823, 40 m from Cathédrale Notre-Dame way/92294792 (full read, duplicate)",
    "node/7073407675": "'Ancien Collège des Jésuites': the Jesuit college again as a node with the same wikidata Q2983815, 45 m from Collège des Jésuites way/629160734 (full read, duplicate)",
}
