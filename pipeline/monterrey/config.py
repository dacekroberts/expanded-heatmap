"""Monterrey (Regional) settings - Mexico's third city, on the national modules
Mexico City and Guadalajara built (DENUE, scian.py, INEGI's licence and notice).
Guadalajara is the shape copied: a regional build over several municipios, rail
from OpenStreetMap, and the operator's own station counts as gate 3.

REGIONAL, owner's call 2026-09-27 ("regional scope yes"). Monterrey, San
Nicolás de los Garza, Guadalupe and General Escobedo - exactly the municipios a
0.6-mile ring reaches. A Monterrey-only build would cut Línea 2 to 8 of its 13
stations (62%, below Rennes' 11 of 15, the lowest kept commune-only) and lose
its northern leg, Universidad included.

OPENSTREETMAP IS THE RAIL GROUND, owner's call 2026-09-27 ("OSM ok"), on the
same grounds as Mexico City's per-city exception: Nuevo León publishes no
Metrorrey feed, `metrorrey.gob.mx` does not resolve, the state GIS
(`mapas.nl.gob.mx`) times out, and `datos.nl.gob.mx` is a brochure site. It was
recorded as "a real negative" on 2026-09-22 for exactly that reason, which
stopped mattering once OSM was approved as a rail source (see osm-rail).

GATE 3 RUNS IN FULL HERE, unlike Guadalajara's partial one: the operator's
network map names every station on all three lines.
"""

from pathlib import Path

from pipeline.countries.mexico import (  # noqa: F401
    DENUE_ACTIVITY_COLUMN,
    DENUE_CODE_COLUMN,
    DENUE_INTERIOR_COLUMN,
    DENUE_MUNICIPIO_CODE_COLUMN,
    DENUE_MUNICIPIO_COLUMN,
    DENUE_NAME_COLUMN,
    DENUE_STATE_COLUMN,
    FORBIDDEN_COLUMNS,
    OSM_NEVER_A_STATION,
    OVERPASS_HOSTS,
    OVERPASS_USER_AGENT,
    PREMISES_TYPE_COLUMN,
    PREMISES_TYPE_KEEP,
    RAW_CLASSIFICATION_COLUMN,
    SOURCE_ENCODING,
    TAXONOMY_SYSTEM,
    denue_member,
    denue_url,
)

# Re-exported rather than redefined, as Guadalajara's config does: each is a
# fact about DENUE or OpenStreetMap, not about this city.

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "monterrey" / "raw"
DATA_PROCESSED = ROOT / "data" / "monterrey" / "processed"
OUTPUTS = ROOT / "outputs" / "monterrey"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
# Which municipio each kept station lies in - the regional-build record, as
# Guadalajara's and Miami's are.
STATION_MUNICIPIOS_CSV = OUTPUTS / "station_municipios.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs -----------------------------------------------------------
#
# 19 = Nuevo León. As in Jalisco, the entidad is NOT the city: 211,349 units
# statewide, so the scope is finished by MUNICIPIOS below.
DENUE_STATE_CODE = "19"
DENUE_URL = denue_url(DENUE_STATE_CODE)
DENUE_MEMBER = denue_member(DENUE_STATE_CODE)
DENUE_ZIP = DATA_RAW / f"denue_{DENUE_STATE_CODE}_csv.zip"

OSM_STATIONS_JSON = DATA_RAW / "osm_stations.json"
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"

# The operator's network map, read for gate 3 and for Línea 3's colour only -
# never republished (the nl.gob.mx site terms are unread, and nothing from the
# PDF is shown). Dated 2026-05-08 in its own file name.
OPERATOR_MAP_URL = (
    "https://www.nl.gob.mx/sites/default/files/repositorio/Dependencias/"
    "Sistema%20de%20Transporte%20Colectivo%20%28Metrorrey%29/Repositorios/"
    "20260508_mapa_red_metrorrey.pdf"
)
OPERATOR_MAP_PDF = DATA_RAW / "20260508_mapa_red_metrorrey.pdf"

# --- The regional scope ---------------------------------------------------
#
# KEYED ON INEGI'S MUNICIPIO CODE, not on the name - the first Mexican city to
# do so. OSM's `INEGI:MUNID` equals DENUE's cve_ent + cve_mun, so the register
# and the boundaries join on the same code and no spelling can drift between
# them ("San Nicolás de los Garza" vs "San Nicolás"). The names are kept only to
# be ASSERTED against DENUE's own `municipio` column, so a wrong code fails
# loudly instead of scoping to some other municipio.
MUNICIPIOS = {
    "039": "Monterrey",
    "046": "San Nicolás de los Garza",
    "026": "Guadalupe",
    "021": "General Escobedo",
}
MUNIDS = tuple(DENUE_STATE_CODE + code for code in MUNICIPIOS)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 14N: the centre (~-100.31) and the whole extent (-100.47 to
# -100.12) fall in the -102 to -96 band. Mexico City is 14N too, Guadalajara
# 13N - derived per city, never copied.
CRS_PROJECTED = "EPSG:32614"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- OpenStreetMap fetch --------------------------------------------------

# south, west, north, east - the brief's bbox, which holds all four municipios.
OSM_BBOX = "25.55,-100.55,25.90,-100.05"
OSM_NETWORK = "Metrorrey"

# STATIONS COME FROM ROUTE MEMBERSHIP, AND MEMBERS COME IN TWO TYPES. 36 of the
# members are `railway=station` nodes; Cuauhtémoc and General Anaya are members
# only as `railway=stop` stop positions. So both are accepted - but only as
# members of a Metrorrey route relation, never by tag. A tag whitelist in the
# Mexico City style would admit the 11 unbuilt monorail stations below.
OSM_STATION_RAILWAY = ("station", "stop")

# 🚨 LÍNEAS 4 AND 6 ARE UNDER CONSTRUCTION, and OSM already carries 11 of their
# monorail stations as `railway=station` + `construction=yes`. They are not
# route members today, so membership keeps them out - and step 1 RAISES if a
# member ever carries a construction tag, or if a monorail route relation
# appears, because either means Línea 4 or 6 may have opened and the map must
# be re-checked rather than quietly redrawn.
OSM_CONSTRUCTION_TAGS = ("construction", "construction:railway")

# --- Station scope ----------------------------------------------------------

LINE_NAMES = {
    "1": "Línea 1",
    "2": "Línea 2",
    "3": "Línea 3",
}
# Líneas 1 and 2 are OSM's `colour` tags, checked against the operator's
# 2026-05-08 map, where they agree in hue (a yellow and a green).
#
# LÍNEA 3 IS THE OPERATOR'S RED, owner's call 2026-09-27 ("use operator's
# red"). OSM tags it #FF8000, but on the operator's map orange is Línea 6, a
# line under construction and not drawn here - so OSM's colour would have
# drawn Línea 3 in another line's colour. The PDF carries CMYK, not a hex:
# its only red, CMYK (0, 0.914, 0.726, 0), converts to #FF1646 by the device
# formula R=(1-C)(1-K) and so on. It was identified by the path it draws - the
# red runs from Línea 2's southern terminal north-east to its own terminus,
# Línea 3's route - not by hue alone. Read 2026-09-27; the PDF is not shown.
LINE_COLOURS = {
    "1": "#FEC04F",
    "2": "#6BC069",
    "3": "#FF1646",
}

# GATE 3, IN FULL. The operator's 2026-05-08 network map names exactly these
# (OPERATOR_MAP_URL above), and OSM route membership matched all three at the
# 2026-09-27 screen.
PUBLISHED_STATIONS_PER_LINE = {
    "Línea 1": 19,
    "Línea 2": 13,
    "Línea 3": 9,
}

# OSM's spelling of two names is wrong against the operator's. Applied after the
# accent-folded collapse, so they fix the displayed name only.
PUBLIC_NAME_FIXES = {
    "Ruiz Cortinez": "Ruiz Cortines",
    "Niños Heroes": "Niños Héroes",
}

# --- Business filtering ------------------------------------------------

MONTERREY_BBOX = {
    "lat_min": 25.55,
    "lat_max": 25.90,
    "lon_min": -100.55,
    "lon_max": -100.05,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3605605805,3605605824,3605606060,3605606272)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("es",)
PLACE_FOLD = None
# A named private street stays (owner, 2026-10-13; DECISIONS.md, "a named
# private street stays in Guadalajara and Monterrey"): the shared rule took
# 124 named streets of gated neighborhoods out of this index. A private
# street whose name is a code beside a type word still goes.
PLACE_KEEP_NAMED_PRIVATE_STREETS = True
# Rows a reader held that the owner ruled to keep (2026-10-13;
# docs/decisions_drafts/search-final.md). A record only: no code reads it.
# A street is listed by name, a place by OSM id with its name. Not in
# PLACE_REVIEWED, which check E holds to names carrying a leak word.
PLACE_RULED_KEPT = {
    "Callejón Calle del Cacique": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle Andrés Quntana Roo": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle Frida Khalo": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle Vicent Van Gogh": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle Michelángelo Bonarroti": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle José Joaquín Hererra": "a misspelled street is still that street (owner, 2026-10-13)",
    "Ottowa": "a misspelled street is still that street (owner, 2026-10-13)",
    "Montepellier": "a misspelled street is still that street (owner, 2026-10-13)",
    "Perpiñan": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle las Rubrlitas": "a misspelled street is still that street (owner, 2026-10-13)",
    "Privada Logroña": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle Sandra Botticelli": "a misspelled street is still that street (owner, 2026-10-13)",
    "Cerrada Cumbre Segobia": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle Diamante Excelcior": "a misspelled street is still that street (owner, 2026-10-13)",
    "Paseo de Luxenburgo": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle Crisól Marrón": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle Fray Angélico De Fiejole": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle Fray Angélico de Fiejole": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle Rafael Sanziu De Urbino": "a misspelled street is still that street (owner, 2026-10-13)",
    "Calle Rafaél Sanziu de Urbino": "a misspelled street is still that street (owner, 2026-10-13)",
    "Privada Cerrada Forua": "a misspelled street is still that street (owner, 2026-10-13)",
    "Autopista de Peaje Cadereyta-Monterrey": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Autopista de Peaje Monterrey-Cadereyta": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Autopista de Peaje Monterrey-Saltillo": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Avenida La Rioja": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Avenida Privadas de Anáhuac": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Avenida San Nicolas": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Calle Palacio De Justicia": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Calzada San Pedro": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Hermosillo": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Retorno Bello Amanecer": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Retorno Constitución": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "San Rafael": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Sierra de lampazos": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Via Rapida a Monterrey": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Via Rapida al Aeropuerto": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Vía Rápida a Monterrey": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Vía Rápida al Aeropuerto": "an avenue or motorway name, kept though link ways carry it (owner, 2026-10-13)",
    "Calle Paseo Ginebra": "a street name with two type words in a row, kept (owner, 2026-10-13)",
    "Calle Paseo de Los Alpes": "a street name with two type words in a row, kept (owner, 2026-10-13)",
    "Calle Paseo de la Plata": "a street name with two type words in a row, kept (owner, 2026-10-13)",
    "Calle Paseo de los Alpes": "a street name with two type words in a row, kept (owner, 2026-10-13)",
    "Calle Paseo de los Olivos": "a street name with two type words in a row, kept (owner, 2026-10-13)",
    "Calle Paseo del Ciprés": "a street name with two type words in a row, kept (owner, 2026-10-13)",
    "Privada Paseo San Sebastián": "a street name with two type words in a row, kept (owner, 2026-10-13)",
    "Privada Paseo de la Montaña": "a street name with two type words in a row, kept (owner, 2026-10-13)",
    "Privada Paseo de las Lajas": "a street name with two type words in a row, kept (owner, 2026-10-13)",
    "Privada Paseo de las Minas": "a street name with two type words in a row, kept (owner, 2026-10-13)",
    "Privada Paseo las Villas": "a street name with two type words in a row, kept (owner, 2026-10-13)",
    "Balcones 3": "a series name ending in a number, kept (owner, 2026-10-13)",
    "Balcones n°2": "a series name ending in a number, kept (owner, 2026-10-13)",
    "Privada Balcones Número 3": "a series name ending in a number, kept (owner, 2026-10-13)",
    "Privada del Rincón 1": "a series name ending in a number, kept (owner, 2026-10-13)",
    "Privada del Rincón 2": "a series name ending in a number, kept (owner, 2026-10-13)",
    "Privada del Rincón 3": "a series name ending in a number, kept (owner, 2026-10-13)",
    "Privada del Rincón 4": "a series name ending in a number, kept (owner, 2026-10-13)",
    # Held rows kept by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    # A home, family or person row is listed by id alone.
    "node/8250250879": "'Campestre El Barro', housing estates tagged as places are kept in the nine built cities (14 answers no. 6)",
    "node/8250268960": "'Campestre Los Cristales', housing estates tagged as places are kept in the nine built cities (14 answers no. 6)",
    "node/3256518880": "'Privada Roma', housing estates tagged as places are kept in the nine built cities (14 answers no. 6)",
    "way/375133972": "'CEDECO', admitted by the index rule for its kind; no drop rule or ruling reaches it by tags or name",
    "node/5794653472": "'Estatua Virgen de Rosario', a statue, bust or public memorial is kept, on its subject's article or none (personal-names ruling; seven rulings no. 3)",
    "node/8234930880": "'Virgen de Guadalupe', a statue, bust or public memorial is kept, on its subject's article or none (personal-names ruling; seven rulings no. 3)",
    "node/3521567806": "'La Radiodifusión', a monument is not held to the article rule and nothing in its tags says artwork (measured 2026-10-11, not applied)",
    "node/308521309": "'Arena Monterrey', a drawn or network station is never dropped for its name (owner 2026-10-13, station guard)",
    "node/3788005136": "'Félix U. Gomez', a drawn or network station is never dropped for its name (owner 2026-10-13, station guard)",
    "way/317701104": "'Santa Isael', a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "node/988320548": "'Roma', a named place of worship needs no article; its name is no denomination or hall type alone (NOTABLE_ONLY exception)",
    "Andador U-ERRE": "a named private street is kept in Guadalajara and Monterrey; only a code-named one goes (owner 2026-10-13)",
    "Calle Provensa": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Calzada Iberica": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Calle Acceso": "the description and bare-type street rules never take a street with a way of residential class or above (street_description)",
    "Adàn Hernàndez R.": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Antonio Dìaz Soto y Gama": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Calle Plutòn": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Calle Torreòn": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Dolores Ladròn de Guevara": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Enrique Flores Magòn": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Eucadio de Leòn": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Federico Gonzàlez Garza": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Hèrcules": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Jesùs Flores Magòn": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Penèlope": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Privada Nicolò Paganini": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Ricardo Flores Magòn": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Teòfilo Martìnez Perèz": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Torreòn": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "CROCC": "the description and bare-type street rules never take a street with a way of residential class or above (street_description)",
    "AVENIDA DE LA LUZ": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Privada Envases Del Norte": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Calle Tecnocentro": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Andador DIF": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Banco Central": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Central Park": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Federación de Trabajadores de Nuevo León": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Centro Obrero": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "MEX-40": "numbered roads on larger ways stay (15 answers no. 10)",
    "Acacia Residencial": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Calle Segunda Andador Paz": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Calle Tercero Andador Paz": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
}
PLACE_REVIEWED = {
    "Calle Hotel Río": "a real street name (owner, 2026-10-13)",
}

# Colonias drawn as areas on residential land, kept by id (owner, 2026-10-13):
# the estate rule would drop them. The rows appear once PLACE_KEPT reaches
# that rule (docs/decisions_drafts/search-final.md).
PLACE_KEPT = {
    "way/158750071": "'Pedregal La Silla', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/158890877": "'Lomas de Satélite', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/158890879": "'Villas de La Hacienda', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/158894383": "'Miradores Satélite', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/158894389": "'Privado Villalta', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/159105874": "'Jardin Español', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/159105883": "'Residencial La Española', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/159110480": "'La Herradura', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/159110481": "'Ancón del Huajuco', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/159110483": "'Valles de Chapultepec', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/162986859": "'Pedregal Contry', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/162986860": "'Rincon Colonial La Silla', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/162986862": "'Contry La Escondida', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/163034603": "'Contry Lux', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/163034604": "'Colonial La Silla', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/163034605": "'Las Musas', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/163117258": "'La Pastora', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/346622812": "'Fraccionamiento Valle de San Miguel Residencial', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
    "way/346622818": "'Villas de San Francisco', a colonia of the municipal Plano de Colonias (owner, 2026-10-13)",
}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "way/939133719": "a generic footpath name (owner, 2026-10-13)",
    "way/939133722": "a generic footpath name (owner, 2026-10-13)",
    "way/542617754": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/242114128": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/1420214452": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/156274902": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/468466106": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/655124438": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/617513721": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/175150371": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/175150379": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/531335061": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/679356464": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/79584095": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1513127383": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1322900353": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1322909089": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1322909090": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/510893060": "an office tower tagged a park",
    "way/719014983": "an office complex tagged a park",
    "way/510893061": "a tower of an office complex tagged a park",
    "way/1316485379": "a padel club tagged a park",
    "way/770056932": "a sports club tagged a park",
    "way/404139114": "a paintball field tagged a park",
    "way/549676029": "a soccer pitch tagged a park",
    "way/505412054": "a commercial building at an address tagged a square",
    "node/9634673559": "a factory tagged a place of worship",
    "node/4949497426": "a home tagged a neighbourhood",
    "way/504427048": "a tenement tagged a neighbourhood",
    "node/5157931893": "a private estate's gate, a description",
    "way/531335590": "a residents' park of a private estate",
    "way/531336206": "a residents' park of a private estate",
    "way/531334816": "a residents' park of a private estate",
    "way/531334086": "a residents' park of a private estate",
    "way/551105735": "a residents' park, a description standing in for a name",
    "way/807869442": "an estate park tagged privately operated",
    "way/614988390": "a sentence standing in for a name",
    "way/583548846": "a description standing in for a name",
    "way/175306332": "a location description standing in for a name",
    "node/5852168148": "a description standing in for a name",
    "way/380889203": "a garbled name",
    "way/379469495": "a cut name",
    "way/856461891": "a cut name",
    "way/375464896": "a cut name",
    "way/1210582433": "a placeholder name with junk tags",
    "relation/17347347": "a duplicate row, the weaker one",
    "way/429154281": "a duplicate of the parish row beside it",
    "node/9325616114": "a duplicate node of the plaza it sits in",
    "way/157106744": "a bare type word standing as the whole name",
    "way/99987567": "a bare type word standing as the whole name",
    "way/155894815": "a bare type word standing as the whole name",
    "way/156196756": "a bare type word standing as the whole name",
    "way/358217169": "a bare type word standing as the whole name",
    "way/529808166": "a bare type word standing as the whole name",
    "way/559177872": "a placeholder standing in for a name",
    "way/679373997": "a placeholder standing in for a name",
    "way/754050070": "a placeholder standing in for a name",
    "way/754055434": "a name that says the way is temporary",
    "way/157543489": "a name that says the way is temporary",
    "way/531335990": "an English description standing in for a name",
    "way/648189777": "a description standing in for a name",
    "way/939133724": "a description standing in for a name",
    "way/582053509": "a business's entrance label",
    "way/764269701": "a business's exit label",
    "way/1286342564": "a station corridor and its steps",
    "way/1286342565": "a station corridor and its steps",
    "way/1286342566": "a station corridor and its steps",
    "way/1526126262": "a station corridor and its steps",
    "way/1527823047": "a station corridor and its steps",
    "way/1527823048": "a station corridor and its steps",
    "way/1069600004": "a campus's own paths",
    "way/1069600007": "a campus's own paths",
    "way/1108262221": "a campus's own paths",
    "way/1213187540": "a campus's own paths",
    "way/156336390": "a mall's own service road",
    "way/752833521": "a mall's own service road",
    "way/156336406": "a mall's own service road",
    "way/156272448": "a cut name; the alt name reads Calle Agena",
    "way/155860506": "a mangled foreign name",
    "way/751732085": "three names glued together",
    "way/647061850": "a second name glued on",
    "way/155894764": "a stray character in the name",
    "way/160991759": "a garbled name",
    "way/795421426": "a typo in the way word",
    "way/111415632": "a typo that changes the name",
    "way/171073006": "a typo that changes the name",
    "way/156046178": "a cut name",
    "way/390997158": "a school's own steps, described not named",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "way/482114896": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/13599643841": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/7746808881": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/156274890": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/539303532": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/784115788": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/1375951211": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/200354558": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/141009654": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/155861369": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/764284631": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/11860677398": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/6085857315": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/401098523": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/613570633": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/469292222": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/1100674681": "a description standing in for a name is dropped by id (settled read call; wave 1 precedent); held rows settled 2026-10-13",
    "way/704407951": "a description standing in for a name is dropped by id (settled read call; wave 1 precedent); held rows settled 2026-10-13",
    "way/309104183": "a description standing in for a name is dropped by id (settled read call; wave 1 precedent); held rows settled 2026-10-13",
    "way/668725041": "a description standing in for a name is dropped by id (settled read call; wave 1 precedent); held rows settled 2026-10-13",
    "node/6141585789": "a description standing in for a name is dropped by id (settled read call; wave 1 precedent); held rows settled 2026-10-13",
    "way/653038361": "a pool, club, pitch or office tagged a park is dropped by id (settled read call; third list no. 15); held rows settled 2026-10-13",
    "way/653038374": "a pool, club, pitch or office tagged a park is dropped by id (settled read call; third list no. 15); held rows settled 2026-10-13",
    "node/3521555486": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/3521733686": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/11734561988": "a code beside a type word is dropped (CODED_TYPE; 14 answers no. 4, planning-code parks); held rows settled 2026-10-13",
    "node/11734558350": "a code beside a type word is dropped (CODED_TYPE; 14 answers no. 4, planning-code parks); held rows settled 2026-10-13",
    "way/1262980996": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/1283044560": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/1322919572": "a pool, club, pitch or office tagged a park is dropped by id (settled read call; third list no. 15); held rows settled 2026-10-13",
    "way/345504883": "public art needs a Wikipedia article of its own (owner 2026-10-13, third list no. 16); held rows settled 2026-10-13",
    "node/7616694520": "a religious office, education hall or residence tagged a place of worship, no article of its own (owner, 2026-10-13)",
    "way/815550056": "a religious office, education hall or residence tagged a place of worship, no article of its own (owner, 2026-10-13)",
    "node/4977980090": "a religious office, education hall or residence tagged a place of worship, no article of its own (owner, 2026-10-13)",
    "way/525048573": "a religious office, education hall or residence tagged a place of worship, no article of its own (owner, 2026-10-13)",
    "way/514558657": "a generic path word as the whole name on minor ways is dropped (six answers no. 3); held rows settled 2026-10-13",
}
