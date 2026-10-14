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

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600302547,3600302588,3600302620)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("pt",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "Rua Sâmia Carla": "a residential street; 'cafe' is a surname in its other name; tags read 2026-10-13",
}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read of this
# index (rule passes 5 and 6), each id read with its cached name and its index
# row; grouped by the reader's class.
PLACE_DROPPED = {
    # A station row that is no working passenger station (reader's drop; owner, 2026-10-13)
    "way/727761853": "'FTL - Pátio Aracapé'",
    "way/446935983": "'Estação de Monguba'",
    # Worship named only by a body, a denomination or a chain (reader's drop; owner, 2026-10-13)
    "node/6416376621": "'Igreja Adventista do 7° dia'",
    "way/543806720": "'Igreja Adventista do 7° dia'",
    "node/4496129029": "'Igreja Adventista do Sétimo Dia Movimento de Reforma'",
    "way/1123925274": "'Igreja dos Santos dos Últimos Dias'",
    "node/4476080648": "'Igreja Batista Independente'",
    "node/4495031627": "'Igreja Presbiteriana Renovada'",
    "node/6387149526": "'Igreja Batista de Sétimo dia'",
    "way/588818682": "'Igreja do Evangelho Pleno'",
    "way/436927651": "'Igreja de Cristo no Brasil'",
    "way/358213535": "'Igreja de Deus no Brasil'",
    "way/377731871": "'Igreja Bola de Neve'",
    "way/715650244": "'Igreja Verbo da Vida'",
    "way/626527275": "'Sara Nossa Terra'",
    "way/549606836": "'Videira'",
    "node/6852345795": "'Igreja da Videira'",
    "way/762392031": "'Racionalismo Cristão'",
    "node/6777943032": "'Missão Evangélica Pentecostal do Brasil'",
    "way/1108285128": "'Missão Evangélica Pentacostial do Brasil'",
    "node/5258136927": "'Assembleia De Deus Templo Central'",
    "node/11077009782": "'Assembleia de Deus Templo Central'",
    "node/10169822782": "'Assembléia de Deus Templo Central'",
    "node/4464954390": "'Assembléia de Deus Templo Central'",
    "node/4493490220": "'Assembléia de Deus Templo Central'",
    "way/658749872": "'Assembléia de Deus Templo Central'",
    "node/10600099403": "'Assembéia de Deus Templo Central'",
    # A bare type word standing alone (reader's drop; owner, 2026-10-13)
    "node/11435681134": "'Centro de Umbanda'",
    "way/683454161": "'Congregação pentecosteal'",
    "way/243918639": "'Altar'",
    "node/4464369963": "'Estátuas'",
    "node/4238442170": "'Cruzeiro'",
    "way/1264357030": "'Campo de pouso'",
    "way/1408797230": "'Pista skate'",
    "way/719536291": "'Society'",
    # A religious office, hall or residence tagged a place of worship (reader's drop; owner, 2026-10-13)
    "node/4495743938": "'Mitra Arquidiocesana de Fortaleza'",
    "way/553291804": "'Centro Pastoral PIO XII'",
    # An exhibit or object kept on another's entry or article (reader's drop; owner, 2026-10-13)
    "way/563470715": "'Trator'",
    "node/6393748959": "'Vagão de Carga'",
    # A description standing in for a name (reader's drop; owner, 2026-10-13)
    "node/6411508241": "'Placa de inauguração da praça Bosque dos Ferroviaros'",
    "relation/9089271": "'Area de Convivencia - Bloco 804'",
    "way/552219993": "'Area de Convivencia - Engenharia Civil'",
    "relation/9089245": "'Area de Convivencia - Engenharia Eletrica'",
    "node/13189039371": "'MUDANDO REFLORESTAR'",
    "way/686480774": "'Praça da paróquia'",
    "way/721488428": "'Praça na Parangaba'",
    "way/719519028": "'Praça no Demócrito Rocha'",
    # Unsure in the read, dropped by the estate ruling, a facility of an estate named for a block or run by the estate itself (owner, 2026-10-13)
    "way/1288617799": "'Parque Jardim Alvorada'",
    "way/1288617518": "'Área verde do Jardim Alvorada'",
    "way/723568022": "'Praça II - Jathaí'",
    # A second row for one object (the surviving row named in each note) (reader's drop; owner, 2026-10-13)
    "node/14039871939": "'Torre da Vida': the same tower as way/1543028408 (Monumento Torre da Vida), 0 m apart",
    "way/499578851": "'Praça do João XXIII': the same square as way/720109743 (Praca Joao XXIII), 0 m apart",
    "node/9776212032": "'Igreja Deus é Amor | Paupina (Anexo)': the same hall as way/1097099286 (Deus e Amor Paupina), 44 m apart",
    # Twin round 1 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/377731874": "'Igreja Bola de Neve': the twin of way/377731871; Worship named only by a body, a denomination or a chain (reader's drop; owner, 2026-10-13)",
}
