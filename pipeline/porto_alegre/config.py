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

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600242397,3600242399,3600242471,3600242574,3600242616,3600242778)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("pt",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "Rua Arthur da Costa e Silva": "a residential street; 'cafe' is a surname in its other name; tags read 2026-10-13",
    "Rua José Linhares": "a residential street; 'cafe' is a surname in its other name; tags read 2026-10-13",
}
# Dropped by id on the leak-word read of 2026-10-13, each id read with its cached
# name and tags (docs/decisions_drafts/search-rollout.md).
PLACE_DROPPED = {
    "way/374506833": "a number and a description standing in for a name ('2 - restaurant ruins'), no article (2 - Ruínas Restaurante); tags read 2026-10-13",
    "node/9755888551": "a closed business under its own name and the status '(closed)', tagged ruins, no article (the '(geschlossen)' precedent) (Motel Kasulo (FECHADO)); tags read 2026-10-13",
    "node/9758495470": "a closed business under its own name and the status '(closed)', tagged ruins, no article (the '(geschlossen)' precedent) (Motel serra Verde (FECHADO)); tags read 2026-10-13",
    "node/10003286571": "a closed business under its own name and the status '(closed)', tagged ruins, no article (the '(geschlossen)' precedent) (Nacional Supermercado (FECHADO)); tags read 2026-10-13",
    "node/12128874866": "a closed business under its own name and the status '(closed)', tagged ruins, no article (the '(geschlossen)' precedent) (Sasun Indústria de Produtos Termo-Transferíveis Ltda (FECHADO)); tags read 2026-10-13",
    # The entries below: the full read of 2026-10-13 under the owner's rulings of the
    # same day, each id read with its cached name (docs/decisions_drafts/search-rollout.md).
    # home: dropped in the full read (owner, 2026-10-13)
    "node/13686487028": "'Condominio Encosta do Cerro': a gated condominium mapped as a neighbourhood (full read, home)",
    # duplicate: dropped in the full read (owner, 2026-10-13)
    "way/1376631466": "'Carioca (ocupação)': second row for Carioca (node/7906709047, about 180 m), with a mapper's bracket (full read, duplicate)",
    "way/512384395": "'Pasqualine': misspelled second row for Pasqualini (node/7898855163, about 220 m) (full read, duplicate)",
    "way/512369456": "'Vachi': misspelled second row for Vacchi (node/7898855110, about 110 m) (full read, duplicate)",
    "way/377514290": "'Praça Prof. Emilio M. Ripoll': second row for Praça Professor Emilio Mabilde Ripoll (way/38744201, 11 m), abbreviated (full read, duplicate)",
    # bare type: dropped in the full read (owner, 2026-10-13)
    "way/909121471": "'Area Verde Três': \"Green Area Three\": a lot code beside a type word (full read, bare type)",
    "way/1216499868": "'Cachorrodromo': \"dog park\" alone (full read, bare type)",
    "way/217350354": "'Pedalinhos': \"pedal boats\": a ride in Parque Farroupilha tagged a park (full read, bare type)",
    "way/1295815686": "'Praça comunitária': \"community square\" alone (full read, bare type)",
    "way/542275958": "'Praça infantil': \"children's square\" (playground) alone (full read, bare type)",
    "way/340141441": "'praça de lazer': \"leisure square\" alone, lower case (full read, bare type)",
    "way/837405874": "'centro afro': \"afro centre\" alone, lower case (full read, bare type)",
    "node/2442008467": "'Torii': \"Torii\" alone; also barrier=gate (full read, bare type)",
    # worship only: dropped in the full read (owner, 2026-10-13)
    "node/3832738698": "'Assembéia de Deus': denomination alone (Assembleia de Deus, misspelled, so the rule missed it) (full read, worship only)",
    "node/7688082990": "'Capela Luterana': hall word and denomination only (full read, worship only)",
    "node/5351883425": "'Encontros De Fé': the chain's name alone (Encontros de Fé) (full read, worship only)",
    "node/11067493579": "'Encontros de Fé': the chain's name alone (Encontros de Fé) (full read, worship only)",
    "way/805559540": "'Igreja Evangélica Encontros de Fé': hall type and the chain's name alone (full read, worship only)",
    "node/2697121804": "'IURD - Igreja Universal do Reino de Deus': the chain's initials and name alone (IURD) (full read, worship only)",
    "way/424643512": "'IURD - Igreja Universal do Reino de Deus': the chain's initials and name alone (IURD) (full read, worship only)",
    "way/650817283": "'Igreja Universal do Reino de Deus - IURD': the chain's name and initials alone (IURD) (full read, worship only)",
    "way/426621953": "'Igreja Brasil Para Cristo': the body's name alone (O Brasil Para Cristo) (full read, worship only)",
    "node/9509591228": "'Igreja o Brasil para Cristo': the body's name alone (O Brasil Para Cristo) (full read, worship only)",
    "way/693804475": "'Igreja Do Nazareno': denomination alone (Nazarene) (full read, worship only)",
    "node/6537014436": "'Igreja Nazareno': denomination alone (Nazarene) (full read, worship only)",
    "node/5328138286": "'Igreja Nova Apostólica': denomination alone (New Apostolic) (full read, worship only)",
    "node/1220447811": "'Igreja Pentecostal Unida do Brasil': the body's name alone (Igreja Pentecostal Unida do Brasil) (full read, worship only)",
    "node/4430045360": "'Igreja Pentecostal Unida do Brasil': the body's name alone (Igreja Pentecostal Unida do Brasil) (full read, worship only)",
    "way/558634347": "'Igreja do E Qauandrangular': the Foursquare body's name alone, garbled (\"E Qauandrangular\") (full read, worship only)",
    "way/569186273": "'Igreja evangelica luterana do Brasil': the body's name alone (Igreja Evangélica Luterana do Brasil), lower case (full read, worship only)",
    "node/1043931244": "'Salão das Testemunhas de Jeová': Kingdom Hall named by the denomination alone (full read, worship only)",
    "node/431739366": "'Salão de Assembleias das Testemunhas de Jeová': Jehovah's Witnesses assembly hall named by the denomination alone (full read, worship only)",
    "node/6688250944": "'Seicho-No-Ie': the movement's name alone; the wikidata and wikipedia are the movement's, not this hall's (full read, worship only)",
    # zoo content: dropped in the full read (owner, 2026-10-13)
    "way/62009396": "'Avestruzes': zoo enclosure tagged a park, named by the animal (Sapucaia zoo) (full read, zoo content)",
    "way/61109537": "'Aves': zoo enclosure tagged a park, named by the animal (full read, zoo content)",
    "way/62009406": "'Camelos': zoo enclosure tagged a park, named by the animal (full read, zoo content)",
    "way/62009410": "'Capivaras': zoo enclosure tagged a park, named by the animal (full read, zoo content)",
    "way/61109541": "'Cervos': zoo enclosure tagged a park, named by the animal (full read, zoo content)",
    "way/62009393": "'Elefantes': zoo enclosure tagged a park, named by the animal (full read, zoo content)",
    "way/62009409": "'Hipopótamos': zoo enclosure tagged a park, named by the animal (full read, zoo content)",
    "way/62009397": "'Javalis': zoo enclosure tagged a park, named by the animal (full read, zoo content)",
    "way/62009411": "'Leões, Felinos e Ursos': zoo enclosure tagged a park, named by the animals (full read, zoo content)",
    "way/418208793": "'Lhamas': zoo enclosure tagged a park, named by the animal (full read, zoo content)",
    "way/61975486": "'Macacos': zoo enclosure tagged a park, named by the animal (full read, zoo content)",
    "way/62009392": "'Rinocerontes': zoo enclosure tagged a park, named by the animal (full read, zoo content)",
    "way/61109526": "'Répteis': zoo enclosure tagged a park, named by the animal (full read, zoo content)",
    "way/62009395": "'Zebras': zoo enclosure tagged a park, named by the animal (full read, zoo content)",
    # worship office: dropped in the full read (owner, 2026-10-13)
    "node/3779015843": "'Caju Casa Marista da Juventude': a Marist youth house tagged a place of worship (full read, worship office)",
    "way/1250679463": "'Casa de formação coração de jesus': a formation house (seminary residence) tagged a place of worship, no entry (full read, worship office)",
    "way/484442705": "'Franciscanos - Sede Provincial': a Franciscan province's head office tagged a place of worship (full read, worship office)",
    # business: dropped in the full read (owner, 2026-10-13)
    "node/4635195791": "'Plantão MRV obra': a builder's sales stand at a construction site (MRV), tagged a place of worship (full read, business)",
    # description: dropped in the full read (owner, 2026-10-13)
    "node/7183201904": "'Escola Infantil Municipal (obra inacabada - em ruínas)': a mapper's note on an unfinished school building, not a name (full read, description)",
    "node/9010182267": "'Imagem religiosa': \"religious image\": a description, not a name (full read, description)",
    "way/887354383": "'praça da rua de cima': \"square of the street above\": a description (full read, description)",
    "way/1418731209": "'Área de descanso dos funcionários REFAP': \"rest area of the REFAP employees\": a refinery's staff area, tagged a beach (full read, description)",
    # estate facility: dropped in the full read (owner, 2026-10-13)
    "way/197054205": "'Rossi Estilo': a condominium's marketing name (Rossi Estilo) tagged a park (full read, estate facility)",
    # unsure in the full read, dropped by ruling 1: a park named only by a category and an inventory or lot number (owner, 2026-10-13)
    "way/243369444": "'Praça 2': Praça 2, the type and a number alone (my reading; about 60 lot-numbered squares the reader kept are not listed) (unsure in the full read; ruling 1)",
    # Twin round 1 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/61109539": "'Aves': the twin of way/61109537; zoo content: dropped in the full read (owner, 2026-10-13)",
    "way/557349048": "'Igreja Nova Apostólica': the twin of node/5328138286; worship only: dropped in the full read (owner, 2026-10-13)",
    "way/62009408": "'Macacos': the twin of way/61975486; zoo content: dropped in the full read (owner, 2026-10-13)",
    "node/11191618808": "'Torii': the twin of node/2442008467; bare type: dropped in the full read (owner, 2026-10-13)",
}
# Why this index reaches more than 25 km past the map's stations
# (scripts/check_place_scope.py, rule D): a far corner of the municipality itself.
PLACE_SCOPE_REACH_REASON = "2026-10-13: Porto Alegre's far south (Praia do Lami) is inside the municipality, one of the six searched (owner)"
