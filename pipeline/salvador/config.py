"""Salvador: settings for one Brazilian city on the national CNEFE modules
(.claude/skills/brazil-city/). Brief: docs/build_briefs/salvador.md.

Metrô de Salvador (CCR Metrô Bahia) from OpenStreetMap, whose four relations
carry no colour at all. The operator names its lines by colour - Linha
1-Vermelha and Linha 2-Azul (trilhos.motiva.com.br/metrobahia, read 2026-09-24) -
and publishes no hex, so the names are resolved through the CSS named-colour table,
Guadalajara's precedent for OSM's colour=orange.
"""

from pathlib import Path

SLUG = "salvador"
NAME = "Salvador"

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
# One zip per município (IBGE code prefix). Salvador alone; the brief measured every station inside it.
CNEFE_FILES = [('29_BA', '2927408_SALVADOR.zip')]
CNEFE_ZIPS = tuple(DATA_RAW / name for _, name in CNEFE_FILES)
SCOPE_CODES = ('2927408',)
IBGE_MUNICIPIO = SCOPE_CODES[0]
SCOPE_AREA_KM2 = (550, 800)   # gate on the union's area
BBOX = (-13.05, -38.6, -12.7, -38.25)   # s, w, n, e - the fetch's OSM box
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
# L1 and L2 by relation id; nothing else is in the cache. Acesso Norte is the interchange.
SYSTEM = "Metrô"
MAP_TITLE = "Salvador Metrô Business Density Heatmap"
LINE_RELATIONS = {'1': (4511874, 6774703), '2': (6771624, 7857257)}
LEFT_OUT = {}
LINE_ORDER = ('1', '2')
LINE_NAMES = {'1': 'Linha 1-Vermelha', '2': 'Linha 2-Azul'}
# The operator's colour NAMES through the CSS table: vermelha 'red' #FF0000, azul 'blue' #0000FF.
LINE_COLOURS = {'1': '#FF0000', '2': '#0000FF'}
STATION_NAME_ALIASES = {}
# Stop positions OSM leaves unnamed, named from their wikidata item's label.
NODE_NAMES = {}
GATE3 = {'lines': {'1': 10, '2': 12}, 'network': None, 'source': "the operator (trilhos.motiva.com.br/metrobahia) and pt.wikipedia 'Metrô de Salvador', read 2026-09-24: Linha 1 10 stations, Linha 2 12"}
SPACING_MIN_M = 300.0
COLLAPSE_MAX_SPREAD_M = 400

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600362362)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("pt",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "Rua Pousada da Jaqueira": "a residential street's own name (the São Paulo precedent, Rua Pousada dos Tucanos); tags read 2026-10-13",
    "Rua dos Colibris": "a residential street, access=yes; its other name is for the shopping centre beside it (the São Paulo precedent, Rua do Shopping); tags read 2026-10-13",
}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/salvador.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # Worship named only by its body or chain (owner, 2026-10-13)
    "node/11159800173": "'Aseembleia de Deus': Assembleia de Deus alone, misspelt (Aseembleia), so the denomination rule missed it",
    "node/7835233926": "'Bola de Neve': named only by the chain (Bola de Neve)",
    "node/7830623876": "'Casa da Benção': named only by the chain (Casa da Benção)",
    "node/5268057426": "'Igreja Casa da Benção': named only by the chain (Igreja Casa da Benção), one of two rows",
    "node/7832892612": "'Igreja Casa da Benção': named only by the chain (Igreja Casa da Benção), one of two rows",
    "node/4516436690": "'Igreja Cristã Maranata': named only by the chain (Igreja Cristã Maranata), one of three rows",
    "node/6525702709": "'Igreja Cristã Maranata': named only by the chain (Igreja Cristã Maranata), one of three rows",
    "node/8318960077": "'Igreja Cristã Maranata': named only by the chain (Igreja Cristã Maranata), one of three rows",
    "node/6438697685": "'Igreja Lagoinha': named only by the chain (Igreja Lagoinha)",
    "node/7810717841": "'Igreja Paz e Vida': named only by the chain (Igreja Paz e Vida)",
    "node/13914404487": "'Paz e Vida': named only by the chain (Paz e Vida)",
    "node/13736089815": "'Renascer': named only by the chain (Renascer)",
    "way/836175062": "'Igrea Mundial do Poder de Deus': named only by the chain (Igreja Mundial do Poder de Deus), with Igreja misspelt Igrea",
    "way/288355043": "'Igreja Evangélica Luterana do Brasil': named only by the body (Igreja Evangélica Luterana do Brasil)",
    "way/557097190": "'Igreja Luterana': named only by the denomination (Igreja Luterana)",
    "node/612539370": "'Igreja Seicho No Ie do Brasil': named only by the body (Seicho-No-Ie do Brasil)",
    "way/381985537": "'Igreja de Jesus Cristo do Santos do Últimos Dias': named only by the body (the Latter-day Saints' church name, with typos)",
    "node/619006951": "'Igreja do Evangelho Quarangular': named only by the body (Igreja do Evangelho Quadrangular, misspelt Quarangular)",
    "node/13588471888": "'Igrecia Pentecostal Unida do Brasil': named only by the body (Igreja Pentecostal Unida do Brasil), with Igreja misspelt Igrecia",
    "way/674120293": "'Igreja Batista do 7° Dia': named only by the denomination (Seventh Day Baptist church)",
    "node/6313476830": "'Igreja Adventista (Sede)': named only by the denomination (Igreja Adventista; \"Sede\" is only the alt name)",
    "node/4528696037": "'Templo Adventista do 7º Dia': named only by the denomination and a hall word (Templo Adventista do 7º Dia)",
    "node/7836239991": "'Templo Batista': named only by the denomination and a hall word (Templo Batista)",
    "way/1549396436": "'Igreja Batista Missionária': named only by the denomination (Igreja Batista Missionária)",
    "node/11534923450": "'Comunidade Batista': named only by the denomination (Comunidade Batista)",
    "node/7830463590": "'Missão Batista': named only by the denomination (Missão Batista)",
    "node/7836234098": "'Igreja Missionária': Igreja Missionária, a generic kind of church with no name",
    "node/7830532874": "'Igreja Evangélica Apostólica': Igreja Evangélica Apostólica, a generic kind of church with no name",
    "way/550632889": "'Comunidade Católica Shalom': named only by the body (Comunidade Católica Shalom, a Catholic community with houses in many cities)",
    "way/1566866628": "'LBV': LBV, the acronym of the body (Legião da Boa Vontade) alone",
    "way/1229548421": "'Salão das Testemunhas de Jeová': Jehovah's Witnesses hall named only by the body (\"Salão das\", not \"Salão do Reino das\", so the rule missed it)",
    "node/14264353743": "'Salão do Reino das Testemhnhas de Jeová': Kingdom Hall named only by the body, with Testemunhas misspelt",
    # A religious office (owner, 2026-10-13)
    "node/6496230295": "'Academia Teológica da Graça de Deus': a theological academy (religious education) tagged a place of worship",
    "node/6822730659": "'Centro Social Paroquial Monsenhor Mario Rebuffoni': a parish social centre tagged a place of worship",
    "node/14203599360": "'Convenção Batista Baiana': the state Baptist convention, a denominational office, tagged a place of worship",
    "node/5176807941": "'Instituto Nacinal da Tradiçao e Cultura Afrobrasileira': a national institute (an association's seat) tagged a place of worship; name also misspelt",
    # A school tagged a place of worship (owner, 2026-10-13)
    "node/6782768882": "'Colégio Damazzio': a school (Colégio) whose only feature tag is amenity=place_of_worship; schools are not indexed otherwise",
    "node/6771884082": "'Colégio Estadual Eraldo Tinoco': a state school whose only feature tag is amenity=place_of_worship",
    "node/6828741041": "'Colégio Gênesis': a school (Colégio) whose only feature tag is amenity=place_of_worship",
    "node/6786524151": "'Colégio Municipal Allan Kardec': a municipal school whose only feature tag is amenity=place_of_worship",
    "node/6821259786": "'Colégio Municipal Malê Debalê': a municipal school whose only feature tag is amenity=place_of_worship",
    "node/6822864110": "'Colégio Sophia': a school (Colégio) whose only feature tag is amenity=place_of_worship",
    "node/6828602870": "'Escola Ceama': a school (Escola) whose only feature tag is amenity=place_of_worship",
    "node/6822742396": "'Escola Mundo': a school (Escola) whose only feature tag is amenity=place_of_worship",
    "node/6823095464": "'Escola Municipal Jorge': a municipal school whose only feature tag is amenity=place_of_worship; the name also looks cut short",
    "node/6770439597": "'Escola Santana Barbosa': a school (Escola) whose only feature tag is amenity=place_of_worship",
    "node/6822933465": "'Externato Mater Et Magistra': a day school (Externato) whose only feature tag is amenity=place_of_worship",
    # A bare type word (owner, 2026-10-13)
    "node/13555727919": "'Beach': \"Beach\", the English type word alone",
    "way/681494747": "'Terreiro': \"Terreiro\", the type word alone",
    "way/681513539": "'Terreiro Candomblé': \"Terreiro Candomblé\", the type and the religion, no name",
    # A description standing in for a name (owner, 2026-10-13)
    "node/7830526268": "'Local de Prática Religiosa': \"place of religious practice\", a description",
    "way/580934573": "'Imagem de uma Santa': \"image of a saint\", a description, tagged a place of worship",
    "node/7830588745": "'Contêiner de Lixo não Reciclado': \"non-recycled rubbish container\", tagged a place of worship",
    "way/1304663641": "'Campo de terra': \"dirt pitch\", a description",
    "way/593578137": "'Pequena praça': \"small square\", a description",
    "way/593578139": "'Pé de amendoas': \"almond tree\", a description (the cached description says a wooded spot with bars)",
    "way/592498880": "'Area de Exposição de Arte Cemiterial. (Aberta a Visitação)': \"cemetery art exhibition area (open to visitors)\", a description with a note in the name",
    "node/11159818239": "'Caixa d'água de Águas Claras': \"water tank of Águas Claras\", a utility object tagged a park",
    "node/11159759360": "'Fim de linha novo de áuas claras': \"new end of the line of Águas Claras\", a bus terminus described, tagged a park",
    "node/14110378602": "'Rua Manoel Fernandes, São Caetano, Salvador': a street address as the name, tagged a park",
    "way/1380473357": "'Rua Marquês de Santana': a street's name alone on a recreation ground",
    # A glitched name (owner, 2026-10-13)
    "node/12854011954": "'Não Informado': \"Não Informado\" = \"not given\", a register placeholder as the name",
    "node/12854009925": "'ONZO D': \"ONZO D\", cut short (same register batch as the terreiros)",
    "way/703231525": "'Praça da 3': \"Praça da 3\", cut short (compare Praça da 3ª Etapa, 1.2 km away)",
    "way/360080720": "'Rótula da V': \"Rótula da V\", cut short",
    "node/12153684691": "'RUÍNA DA USINA DA FABRICA DE TECIDOS SÃO BRÁS (FATBRAZ': cut short with an unclosed bracket; the same ruin as node/12153684690 ANTIGA FABRICA DE TECIDOS SÃO BRÁS, about 110 m away",
    "way/1372007966": "'Edf. Conselheiro Joaquim Batista Neves | Poder Legislativo': an office building's name with a pipe and the institution's branding, tagged a park (alt_name repeats it)",
    "way/1375080351": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': a court seat's name written as a web-page title with pipes, tagged a park",
    # A business (owner, 2026-10-13)
    "way/1226625093": "'Embasa R5': a water utility's reservoir code (Embasa R5) tagged place=square",
    "node/12748224944": "'Projeto Sariguês - Associação Casa dos Bichos': an animal-welfare project and association named as such, tagged a park",
    # A second row of one object (owner, 2026-10-13)
    "node/8319015606": "'Maanaim de Salvador-BA': the same Maranata retreat as way/1214559411 \"Maanaim de Salvador\", about 110 m away",
    "node/12854046551": "'ILE ASE ODE OLUAMI': the same terreiro as node/12854094508 \"Ilê Axé Ode Oluami Osoosi\", about 70 m away",
    "node/12854046181": "'ILE AXE ORUM MOGI': the same terreiro as node/12854066351 \"Ilê Axé Orun-Mogi\", about 70 m away",
    "node/12854015095": "'Terreiro de Cosme e Damião da Bela União': the same terreiro as node/12854016018 \"Casa de Cosme e Damião da Bela União de Família\", about 45 m away",
    # Twin round 1 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1372007967": "'Edf. Conselheiro Joaquim Batista Neves | Poder Legislativo': the twin of way/1372007966; A glitched name (owner, 2026-10-13)",
    "way/545024012": "'Igreja Casa da Benção': the twin of node/5268057426; Worship named only by its body or chain (owner, 2026-10-13)",
    "way/1375080352": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
    # Twin round 2 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1372007970": "'Edf. Conselheiro Joaquim Batista Neves | Poder Legislativo': the twin of way/1372007966; A glitched name (owner, 2026-10-13)",
    "way/1375093587": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
    # Twin round 3 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1372007971": "'Edf. Conselheiro Joaquim Batista Neves | Poder Legislativo': the twin of way/1372007966; A glitched name (owner, 2026-10-13)",
    "way/1375093588": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
    # Twin round 4 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1372007972": "'Edf. Conselheiro Joaquim Batista Neves | Poder Legislativo': the twin of way/1372007966; A glitched name (owner, 2026-10-13)",
    "way/1375093589": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
    # Twin round 5 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1372007973": "'Edf. Conselheiro Joaquim Batista Neves | Poder Legislativo': the twin of way/1372007966; A glitched name (owner, 2026-10-13)",
    "way/1375093685": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
    # Twin round 6 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1372007974": "'Edf. Conselheiro Joaquim Batista Neves | Poder Legislativo': the twin of way/1372007966; A glitched name (owner, 2026-10-13)",
    "way/1375093686": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
    # Twin round 7 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1372007975": "'Edf. Conselheiro Joaquim Batista Neves | Poder Legislativo': the twin of way/1372007966; A glitched name (owner, 2026-10-13)",
    "way/1375093687": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
    # Twin round 8 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1372007977": "'Edf. Conselheiro Joaquim Batista Neves | Poder Legislativo': the twin of way/1372007966; A glitched name (owner, 2026-10-13)",
    "way/1375443919": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
    # Twin round 9 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1372007978": "'Edf. Conselheiro Joaquim Batista Neves | Poder Legislativo': the twin of way/1372007966; A glitched name (owner, 2026-10-13)",
    "way/1375443926": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
    # Twin round 10 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1372016637": "'Edf. Conselheiro Joaquim Batista Neves | Poder Legislativo': the twin of way/1372007966; A glitched name (owner, 2026-10-13)",
    "way/1375443927": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
    # Twin round 11 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1375443928": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
    # Twin round 12 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1375879044": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
    # Twin round 13 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1375879046": "'Tribunal De Justiça Do Estado Da Bahia | Sede Oficial | TJBA | Poder Judiciário': the twin of way/1375080351; A glitched name (owner, 2026-10-13)",
}
# Why this index reaches more than 25 km past the map's stations
# (scripts/check_place_scope.py, rule D): a far corner of the municipality itself.
PLACE_SCOPE_REACH_REASON = "2026-10-13: the bay islands of the municipality (Ilha de Bom Jesus dos Passos) are inside its boundary (owner)"
