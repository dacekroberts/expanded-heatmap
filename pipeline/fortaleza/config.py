"""Fortaleza (Regional): settings for one Brazilian city on the national CNEFE modules
(.claude/skills/brazil-city/). Brief: docs/build_briefs/fortaleza.md.

Metrofor from OpenStreetMap: Linha Sul (electric), and three diesel lines -
Linha Oeste, the Parangaba-Mucuripe VLT and the Aeroporto-Castelao branch (opened
2026-02-06). REGIONAL - the owner's decision of 2026-09-23: Fortaleza, Caucaia,
Maracanau and Pacatuba. The diesel lines run every 30-60 minutes (pt.wikipedia)
and went through the rail test (below): Linha Sul is drawn; Linha Oeste and the
branch fail it; the Parangaba-Mucuripe VLT is borderline and out pending the owner.
"""

from pathlib import Path

SLUG = "fortaleza"
NAME = "Fortaleza (Regional)"

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
# One zip per município (IBGE code prefix). Four municípios - the owner's regional decision of 2026-09-23.
CNEFE_FILES = [('23_CE', '2304400_FORTALEZA.zip'), ('23_CE', '2303709_CAUCAIA.zip'), ('23_CE', '2307650_MARACANAU.zip'), ('23_CE', '2309706_PACATUBA.zip')]
CNEFE_ZIPS = tuple(DATA_RAW / name for _, name in CNEFE_FILES)
SCOPE_CODES = ('2304400', '2303709', '2307650', '2309706')
IBGE_MUNICIPIO = SCOPE_CODES[0]
SCOPE_AREA_KM2 = (1650, 1950)   # gate on the union's area
BBOX = (-4.05, -38.8, -3.68, -38.4)   # s, w, n, e - the fetch's OSM box
SANITY_BBOX = {"lat_min": BBOX[0], "lat_max": BBOX[2], "lon_min": BBOX[1], "lon_max": BBOX[3]}

# --- Coordinate reference systems -----------------------------------------
CRS_GEOGRAPHIC = "EPSG:4326"
# UTM 24S: longitude ~-38.5 lies in the -42 to -36 band.
CRS_PROJECTED = "EPSG:32724"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail (OpenStreetMap, osm-rail; pipeline/countries/brazil_rail.py) --------
# THE RAIL TEST (the owner's standing call for this batch), measured 2026-09-24 with
# scripts/measure_rail_backbone.py and pt.wikipedia's headways: Linha Oeste (diesel) 2,059 m
# median, every 60 min - a CLEAR FAIL, out; the Aeroporto-Castelao branch (diesel) 2 stops,
# every 30 min - FAIL, out; the Parangaba-Mucuripe VLT (diesel) 1,228 m, 9 of 11 stops with
# no metro within 800 m, every 40 min - BORDERLINE, out pending the owner (the metro itself
# runs every 20). Caucaia's only stations were Linha Oeste's; the owner's regional scope is
# kept, so Caucaia contributes storefronts and no station - Guadalajara's precedent.
SYSTEM = "Metrofor"
MAP_TITLE = "Fortaleza Metrofor Business Density Heatmap"
LINE_RELATIONS = {'Sul': (4511593, 6113027)}
LEFT_OUT = {4511795: 'Linha Oeste - diesel, 2.1 km apart, every 60 min: fails the rail test', 9963936: 'Linha Oeste - diesel, 2.1 km apart, every 60 min: fails the rail test', 20187272: 'Ramal Aeroporto-Castelão - diesel, every 30 min: fails the rail test', 20189724: 'Ramal Aeroporto-Castelão - diesel, every 30 min: fails the rail test', 4511811: 'VLT Parangaba-Mucuripe - diesel, 1.2 km, every 40 min: BORDERLINE, out pending the owner', 9963933: 'VLT Parangaba-Mucuripe - diesel, 1.2 km, every 40 min: BORDERLINE, out pending the owner'}
LINE_ORDER = ('Sul',)
LINE_NAMES = {'Sul': 'Linha Sul'}
# OSM's colour: Sul #FF0000 (Parangaba-Mucuripe's would be #6B297E if drawn).
LINE_COLOURS = {'Sul': '#FF0000'}
STATION_NAME_ALIASES = {}
# Stop positions OSM leaves unnamed, named from their wikidata item's label.
NODE_NAMES = {}
GATE3 = {'lines': {'Sul': 20}, 'network': None, 'source': "pt.wikipedia 'Metrô de Fortaleza', read 2026-09-24 - secondary; Sul 20, Oeste 10, Parangaba-Mucuripe 11, Aeroporto-Castelao 2"}
SPACING_MIN_M = 300.0
COLLAPSE_MAX_SPREAD_M = 400
