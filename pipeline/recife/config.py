"""Recife (Regional): settings for one Brazilian city on the national CNEFE modules
(.claude/skills/brazil-city/). Brief: docs/build_briefs/recife.md.

Metrô do Recife from OpenStreetMap: Linha Centro's two branches and Linha Sul
(electric), drawn; the two diesel VLTs failed the rail test on spacing and are not. REGIONAL - the owner's decision of 2026-09-23: Recife,
Jaboatao dos Guararapes, Cabo de Santo Agostinho and Camaragibe. The city's ODbL
station file is a cross-check only and is never read by a step.
"""

from pathlib import Path

SLUG = "recife"
NAME = "Recife (Regional)"

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
CNEFE_FILES = [('26_PE', '2611606_RECIFE.zip'), ('26_PE', '2607901_JABOATAO_DOS_GUARARAPES.zip'), ('26_PE', '2602902_CABO_DE_SANTO_AGOSTINHO.zip'), ('26_PE', '2603454_CAMARAGIBE.zip')]
CNEFE_ZIPS = tuple(DATA_RAW / name for _, name in CNEFE_FILES)
SCOPE_CODES = ('2611606', '2607901', '2602902', '2603454')
IBGE_MUNICIPIO = SCOPE_CODES[0]
SCOPE_AREA_KM2 = (880, 1080)   # gate on the union's area
BBOX = (-8.4, -35.15, -7.92, -34.83)   # s, w, n, e - the fetch's OSM box
SANITY_BBOX = {"lat_min": BBOX[0], "lat_max": BBOX[2], "lon_min": BBOX[1], "lon_max": BBOX[3]}

# --- Coordinate reference systems -----------------------------------------
CRS_GEOGRAPHIC = "EPSG:4326"
# UTM 25S: longitude ~-34.9 lies in the -36 to -30 band.
CRS_PROJECTED = "EPSG:32725"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail (OpenStreetMap, osm-rail; pipeline/countries/brazil_rail.py) --------
# THE RAIL TEST (the owner's standing call for this batch), measured 2026-09-24 with
# scripts/measure_rail_backbone.py: the VLT to Cabo 3,126 m median, the VLT to Curado 3,941 m -
# CLEAR FAILS on spacing (Metromare, left out, was 2,171), out. Cabo's only stations were
# the VLT's; the owner's regional scope is kept, so Cabo contributes storefronts and no
# station - Guadalajara's precedent.
SYSTEM = "Metrô do Recife"
MAP_TITLE = "Recife Metrô Business Density Heatmap"
LINE_RELATIONS = {'Camaragibe': (420618, 7869351), 'Jaboatao': (420619, 7869333), 'Sul': (4510097, 7869373)}
LEFT_OUT = {9699109: 'VLT Cajueiro Seco-Cabo - diesel, 3.1 km apart: fails the rail test', 4510254: 'VLT Cajueiro Seco-Cabo - diesel, 3.1 km apart: fails the rail test', 4510189: 'VLT Curado-Cajueiro Seco - diesel, 3.9 km apart: fails the rail test', 7945216: 'VLT Curado-Cajueiro Seco - diesel, 3.9 km apart: fails the rail test'}
LINE_ORDER = ('Camaragibe', 'Jaboatao', 'Sul')
LINE_NAMES = {'Camaragibe': 'Linha Centro – Camaragibe', 'Jaboatao': 'Linha Centro – Jaboatão', 'Sul': 'Linha Sul'}
# OSM's colours: Camaragibe #e77405, Jaboatao #D9001C, Sul #1a5ba3.
LINE_COLOURS = {'Camaragibe': '#e77405', 'Jaboatao': '#D9001C', 'Sul': '#1a5ba3'}
STATION_NAME_ALIASES = {}
# Stop positions OSM leaves unnamed, named from their wikidata item's label.
NODE_NAMES = {}
GATE3 = {'lines': {'Camaragibe': 15, 'Jaboatao': 14, 'Sul': 12}, 'network': None, 'source': "pt.wikipedia 'Metrô do Recife', read 2026-09-24 - secondary; Centro-Camaragibe 15, Centro-Jaboatao 14, Sul 12, VLT Cabo 6, VLT Curado 4"}
SPACING_MIN_M = 300.0
COLLAPSE_MAX_SPREAD_M = 400

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600303585,3600303695,3600303709)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("pt",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "Rua do Hotel Pousada do Vale": "tags do not decide; kept (one residential way with no access tag, named whole for a hotel)",
    "Shopping": "a subway station (railway=station), named for the place beside it (the Prague precedent, Hotel Golf); tags read 2026-10-13",
}
# Dropped by id on the full read of 2026-10-13 under the owner's rulings of the
# same day, each id read with its cached name (docs/decisions_drafts/search-rollout.md).
PLACE_DROPPED = {
    # glitch: dropped in the full read (owner, 2026-10-13)
    "way/655804270": "'DA AV ENGENHEIRO JOSÉ ESTELITA': truncated register entry: the park's name minus its first word (\"... of Av. X\"), all caps; a street address standing in for a name (full read, glitch)",
    "way/673701083": "'DA AV NORTE MIGUEL ARRAES DE ALENCAR': truncated register entry, \"of Av. X\" with no head word (full read, glitch)",
    "way/673513091": "'DA AVENIDA MILITAR': truncated register entry, \"of Avenida X\" with no head word (full read, glitch)",
    "way/660887080": "'DA AVENIDA PREFEITO ARTUR LIMA CAVALCANTI': truncated register entry, \"of Avenida X\" with no head word (full read, glitch)",
    "way/673896929": "'DA RUA ARNOLDO MAGALHÃES': truncated register entry, \"of Rua X\" with no head word (full read, glitch)",
    "way/673671219": "'DA RUA DESENHISTA EULINO SANTOS': truncated register entry, \"of Rua X\" with no head word; the square of that name is its own row (way/673671220) (full read, glitch)",
    "way/673677243": "'DA RUA HERCÍLIA DE MEDEIROS': truncated register entry, \"of Rua X\" with no head word (full read, glitch)",
    "way/655715015": "'DA RUA OLIVIA MENELAU': truncated register entry, \"of Rua X\" with no head word (full read, glitch)",
    "way/673701084": "'DA RUA TIJUCAL': truncated register entry, \"of Rua X\" with no head word (full read, glitch)",
    "way/673515352": "'da Rua da Aurora': same class in lower case: \"da Rua da Aurora\", no head word (full read, glitch)",
    "node/5729134436": "'Busto de....': \"Bust of ....\": the mapper never filled in whose (full read, glitch)",
    "way/655365057": "'Praça do S': name cut off after \"Praça do S\" (full read, glitch)",
    # description: dropped in the full read (owner, 2026-10-13)
    "way/666325252": "'Rua Barão de Caiara': a street name alone (\"Rua X\") on a park polygon (full read, description)",
    "way/556302956": "'Laguinho e Arredores': \"small lake and surroundings\", a mapper's description (full read, description)",
    "way/1562587356": "'Pracinha com brinquedos': \"little square with toys\", a mapper's description (full read, description)",
    "way/675046850": "'Área das Piscinas': \"pool area\" on a footway area tagged a square; a facility label, far outside the centre (full read, description)",
    "way/607806652": "'Praça Adotada: Espaço Verde': \"Adopted square: green space\", a sign about an adoption scheme, not a name (full read, description)",
    # bare type: dropped in the full read (owner, 2026-10-13)
    "way/1523863380": "'Feira': \"Feira\" (market), the type word alone, on a park (full read, bare type)",
    "way/678531208": "'Palco': \"Palco\" (stage), the type word alone, on a square (full read, bare type)",
    "node/7750478180": "'Sino': \"Sino\" (bell), the object type alone (full read, bare type)",
    "way/651714244": "'Relógio Solar': \"Relógio Solar\" (sundial), the object type alone; one of the pieces mapped inside Oficina Brennand (full read, bare type)",
    "way/1284272034": "'salão do rei': \"salão do rei\", the hall type cut short and lower case (full read, bare type)",
    "way/1284275854": "'igreja petencostal': \"pentecostal church\", misspelt and lower case, no name (full read, bare type)",
    "node/11914405258": "'Igreja evnagelica': \"evangelical church\", misspelt, no name (full read, bare type)",
    # business: dropped in the full read (owner, 2026-10-13)
    "way/549211982": "'Food Park do Shooping Recife': a mall's food-truck area tagged a park (Shopping Recife) (full read, business)",
    "way/545703562": "'Sport Club do Recife': a members' sports club's grounds tagged a park; the stadium has its own row (full read, business)",
    # estate facility: dropped in the full read (owner, 2026-10-13)
    "way/620659500": "'Conjunto Habitacional Aritana': a housing estate's name (\"Conjunto Habitacional ...\") on its recreation ground (full read, estate facility)",
    "way/560507213": "'Praça do Condominio Maria Amelia': \"square of Condominium X\": a condominium's own facility (full read, estate facility)",
    # worship body: dropped in the full read (owner, 2026-10-13)
    "way/810633429": "'Assembelia de Deus': denomination name alone, misspelt (\"Assembelia\"), so the rule's spelling missed it (full read, worship body)",
    "way/646110066": "'Assembéia de Deus': denomination name alone, misspelt (\"Assembéia\") (full read, worship body)",
    "way/588708253": "'Assembléia de Deus Recife': the regional body's name alone (denomination + city); six rows carry the identical name with no congregation (full read, worship body)",
    "way/593431540": "'Assembléia de Deus Recife': as above (full read, worship body)",
    "way/620395283": "'Assembléia de Deus Recife': as above (full read, worship body)",
    "way/672361663": "'Assembléia de Deus Recife': as above (full read, worship body)",
    "way/895719153": "'Assembléia de Deus Recife': as above (full read, worship body)",
    "way/996906496": "'Assembléia de Deus Recife': as above (full read, worship body)",
    "way/543913231": "'Congregação Cristão do Brasil': denomination name alone (Congregação Cristã no Brasil, misspelt) (full read, worship body)",
    "node/4961603922": "'Igreja Cristã Maranata': denomination name alone (Igreja Cristã Maranata) (full read, worship body)",
    "node/6974922139": "'Igreja Cristã Maranata': denomination name alone (Igreja Cristã Maranata) (full read, worship body)",
    "way/744959187": "'Igreja Maranata': denomination name alone, short form (Maranata) (full read, worship body)",
    "node/11914390400": "'Igreja Presbiteriana do Brasil': national denomination's name alone (full read, worship body)",
    "way/424470021": "'Igreja Presbiteriana do Brasil': national denomination's name alone (full read, worship body)",
    "node/6720139480": "'Igreja Presbiteriana do Brasil': national denomination name alone, the third row of it (full read, worship body)",
    "way/549207073": "'Igreja de Jesus Cristo dos Últimos Dias': denomination name alone (Latter-day Saints, shortened) (full read, worship body)",
    "node/6974046922": "'Salão de Assembléias Testemunhas de Jeová': \"assembly hall of\" the denomination, no place name (full read, worship body)",
    "node/5108575000": "'Vale do Amanhecer': the movement's name alone (Vale do Amanhecer) (full read, worship body)",
    "node/6973937771": "'Vale do Amanhecer': the movement's name alone (Vale do Amanhecer) (full read, worship body)",
    "node/8747225514": "'Verbo Da Vida': a church chain's name alone (Verbo da Vida) (full read, worship body)",
    "way/744959191": "'Igreja Verbo da Vida': a church chain's name alone (Igreja Verbo da Vida) (full read, worship body)",
    "node/2889084347": "'CEBB': an organisation's acronym alone (a Buddhist study centre network) (full read, worship body)",
    # religious residence: dropped in the full read (owner, 2026-10-13)
    "way/537839023": "'Congregação dos Sacerdotes do Sagrado Coração de Jesus': named only for the order of priests, no church or house name; the order's church is its own row (way/539849511) (full read, religious residence)",
    # a duplicate of a row that stays, dropped though it carries a wikipedia tag (owner, 2026-10-13)
    "node/5029162539": "'Museu do Homen do Nordeste': the museum twice, 60 m apart; this node is the misspelt one (\"Homen\"). It carries the article tags, the building way/991346779 carries the correct name (full read, duplicate)",
    # Twin round 1 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/655804298": "'DA AV ENGENHEIRO JOSÉ ESTELITA': the twin of way/655804270; glitch: dropped in the full read (owner, 2026-10-13)",
    "way/673513092": "'DA AVENIDA MILITAR': the twin of way/673513091; glitch: dropped in the full read (owner, 2026-10-13)",
    "way/745098088": "'Igreja Cristã Maranata': the twin of node/4961603922; worship body: dropped in the full read (owner, 2026-10-13)",
    "way/675046851": "'Área das Piscinas': the twin of way/675046850; description: dropped in the full read (owner, 2026-10-13)",
    # Twin round 2 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/673513093": "'DA AVENIDA MILITAR': the twin of way/673513091; glitch: dropped in the full read (owner, 2026-10-13)",
}
