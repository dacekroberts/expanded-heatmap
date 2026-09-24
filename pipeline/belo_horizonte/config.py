"""Belo Horizonte: settings for one Brazilian city on the national CNEFE modules
(.claude/skills/brazil-city/). Brief: docs/build_briefs/belo-horizonte.md.

Metrô BH from OpenStreetMap. Linha 2 opened 2026-07-03 with two stations and
weekday peak hours only - DRAWN on the owner's call of 2026-09-24, the page notes
the hours. Prodabel's Linha 1 file is a cross-check the build does not read.
"""

from pathlib import Path

SLUG = "belo_horizonte"
NAME = "Belo Horizonte"

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
# One zip per município (IBGE code prefix). Belo Horizonte alone: the brief measured every station inside it, bar Linha 1's western end in Contagem, which step 1 records as excluded.
CNEFE_FILES = [('31_MG', '3106200_BELO_HORIZONTE.zip')]
CNEFE_ZIPS = tuple(DATA_RAW / name for _, name in CNEFE_FILES)
SCOPE_CODES = ('3106200',)
IBGE_MUNICIPIO = SCOPE_CODES[0]
SCOPE_AREA_KM2 = (300, 360)   # gate on the union's area
BBOX = (-20.1, -44.15, -19.75, -43.8)   # s, w, n, e - the fetch's OSM box
SANITY_BBOX = {"lat_min": BBOX[0], "lat_max": BBOX[2], "lon_min": BBOX[1], "lon_max": BBOX[3]}

# --- Coordinate reference systems -----------------------------------------
CRS_GEOGRAPHIC = "EPSG:4326"
# UTM 23S: longitude ~-43.9 lies in the -48 to -42 band.
CRS_PROJECTED = "EPSG:32723"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail (OpenStreetMap, osm-rail; pipeline/countries/brazil_rail.py) --------
# Linha 1 and Linha 2 by relation id. Left out: the Vitoria-Minas passenger train (Vale) - intercity, not urban rail.
SYSTEM = "Metrô BH"
MAP_TITLE = "Belo Horizonte Metrô Business Density Heatmap"
LINE_RELATIONS = {'1': (420605, 6087652), '2': (21075860, 21075861)}
LEFT_OUT = {3331630: 'Estrada de Ferro Vitória a Minas passenger train - intercity (Vale)', 7831016: 'Estrada de Ferro Vitória a Minas passenger train - intercity (Vale)'}
LINE_ORDER = ('1', '2')
LINE_NAMES = {'1': 'Linha 1', '2': 'Linha 2'}
# OSM's colours: Linha 1 #FF7400 (one direction's relation carries none), Linha 2 #2F1F85.
LINE_COLOURS = {'1': '#FF7400', '2': '#2F1F85'}
STATION_NAME_ALIASES = {}
# Stop positions OSM leaves unnamed, named from their wikidata item's label.
NODE_NAMES = {}
GATE3 = {'lines': {'1': 21, '2': 2}, 'network': 22, 'source': "pt.wikipedia 'Metrô de Belo Horizonte', read 2026-09-24 - secondary; its text: 22 stations in operation. Its table's Linha 1 '20 (+1 being built)' is stale: the +1, Nova Suíça, opened with Linha 2 on 2026-07-03 as the interchange, so Linha 1 21, Linha 2 2"}
SPACING_MIN_M = 300.0
COLLAPSE_MAX_SPREAD_M = 400
