"""Porto Alegre (Regional): settings for one Brazilian city on the national CNEFE modules
(.claude/skills/brazil-city/). Brief: docs/build_briefs/porto-alegre.md.

Trensurb from OpenStreetMap - the corridor's electric metro. REGIONAL - the
owner's decision of 2026-09-23: Porto Alegre, Canoas, Esteio, Sapucaia do Sul,
Sao Leopoldo and Novo Hamburgo, because the city holds under a third of its own
network. The Aeromovel airport connector is NOT drawn (owner, 2026-09-24).
"""

from pathlib import Path

SLUG = "porto_alegre"
NAME = "Porto Alegre (Regional)"

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / SLUG / "raw"
DATA_PROCESSED = ROOT / "data" / SLUG / "processed"
OUTPUTS = ROOT / "outputs" / SLUG

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"
STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
UNCLASSIFIED_CSV = DATA_PROCESSED / "cnefe_unclassified.csv"
OSM_LINES_JSON = DATA_PROCESSED / "osm_lines.json"
OSM_MUNICIPIOS_JSON = DATA_RAW / "osm_municipios.json"
OSM_RAIL_JSON = DATA_RAW / "osm_rail.json"

TAXONOMY_SYSTEM = "brazil_cnefe"

# --- Scope -------------------------------------------------------------------------
# One zip per município (IBGE code prefix). Six municípios - the owner's regional decision of 2026-09-23.
CNEFE_FILES = [('43_RS', '4314902_PORTO_ALEGRE.zip'), ('43_RS', '4304606_CANOAS.zip'), ('43_RS', '4307708_ESTEIO.zip'), ('43_RS', '4320008_SAPUCAIA_DO_SUL.zip'), ('43_RS', '4318705_SAO_LEOPOLDO.zip'), ('43_RS', '4313409_NOVO_HAMBURGO.zip')]
CNEFE_ZIPS = tuple(DATA_RAW / name for _, name in CNEFE_FILES)
SCOPE_CODES = ('4314902', '4304606', '4307708', '4320008', '4318705', '4313409')
IBGE_MUNICIPIO = SCOPE_CODES[0]
SCOPE_AREA_KM2 = (950, 1150)   # gate on the union's area
BBOX = (-30.3, -51.35, -29.6, -50.95)   # s, w, n, e - the fetch's OSM box
SANITY_BBOX = {"lat_min": BBOX[0], "lat_max": BBOX[2], "lon_min": BBOX[1], "lon_max": BBOX[3]}

# --- Coordinate reference systems -----------------------------------------
CRS_GEOGRAPHIC = "EPSG:4326"
# UTM 22S: longitude ~-51.2 lies in the -54 to -48 band.
CRS_PROJECTED = "EPSG:32722"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail (OpenStreetMap, osm-rail; pipeline/countries/brazil_rail.py) --------
# Trensurb's full and short-working relations by id (step 3 draws the longest). Left out: the Aeromovel.
SYSTEM = "Trensurb"
MAP_TITLE = "Porto Alegre Trensurb Business Density Heatmap"
LINE_RELATIONS = {'1': (420335, 7875374, 7886190, 7886191)}
LEFT_OUT = {5465620: 'Aeromóvel airport connector - not drawn (owner, 2026-09-24)', 7889061: 'Aeromóvel airport connector - not drawn (owner, 2026-09-24)'}
LINE_ORDER = ('1',)
LINE_NAMES = {'1': 'Trensurb Linha 1'}
# OSM's colour: #000080.
LINE_COLOURS = {'1': '#000080'}
STATION_NAME_ALIASES = {}
# Stop positions OSM leaves unnamed, named from their wikidata item's label.
NODE_NAMES = {}
GATE3 = {'lines': {'1': 22}, 'network': None, 'source': "pt.wikipedia 'Trensurb', read 2026-09-24 - secondary; Linha 1 22 stations"}
SPACING_MIN_M = 300.0
COLLAPSE_MAX_SPREAD_M = 400
