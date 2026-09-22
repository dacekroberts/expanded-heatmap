"""Mexico City-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

MEXICO CITY IS THE FIRST CITY HERE WHOSE RAIL DOES NOT COME FROM GTFS, and the
reason is not a preference. Every `*.cdmx.gob.mx` host - the city open-data
portal, STC Metro, and STE (Tren Ligero) - returns ConnectTimeout, on `www.`
and bare, http and https, re-confirmed 2026-09-22. No block page prints an IP,
so this is a dead host from here rather than a client refusal, and the browser
does not help. The feed's S3 `direct_download` returns 403.

So the geometry comes from OpenStreetMap, approved by the owner on 2026-09-22
as a documented per-city exception rather than a new default. What that costs
is recorded honestly in two places: the city page says where the geometry came
from, and `STATION_COUNT_GATE_3` below records that the operator's published
station count CANNOT be checked, because the operator is unreachable.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "mexico_city" / "raw"
DATA_PROCESSED = ROOT / "data" / "mexico_city" / "processed"
OUTPUTS = ROOT / "outputs" / "mexico_city"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities). Lines A and B run into Estado de Mexico, where this
# build has no business data, so their stations there must be cut rather than
# left to anchor rings over a blank.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs -----------------------------------------------------------
#
# BUSINESSES: INEGI DENUE, bulk CSV per entidad federativa. Keyless, no token,
# no CAPTCHA - verified 2026-09-22, 45,439,249 bytes, real ZIP by magic bytes.
#   curl -L -o denue_09_csv.zip \
#     https://www.inegi.org.mx/contenidos/masiva/denue/denue_09_csv.zip
# The DENUE API at /app/api/denue/v1/consulta/ 404s without a token; the bulk
# download is both keyless and more complete, so the API is not used.
#
# RAIL + BOUNDARY: OpenStreetMap via Overpass, fetched by step1 (see above for
# why not the agency).
DENUE_ZIP = DATA_RAW / "denue_09_csv.zip"
DENUE_URL = "https://www.inegi.org.mx/contenidos/masiva/denue/denue_09_csv.zip"
# The member inside the ZIP. INEGI also ships a data dictionary and a metadata
# file; reading the dictionary by mistake returns 43 rows of column
# documentation, which is a confusing near-miss rather than an error.
DENUE_MEMBER = "conjunto_de_datos/denue_inegi_09_.csv"
# 09 = Ciudad de Mexico. The file IS the state, so no city-name filter is
# needed for businesses - the in-city question is answered by the download,
# which is why CITY_KEEP does not exist for this city.
DENUE_STATE_CODE = "09"

OSM_STATIONS_JSON = DATA_RAW / "osm_stations.json"
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"

# LATIN-1, NOT UTF-8. INEGI ships DENUE in latin-1; decoding as UTF-8 raises.
# add-city requires this declared per city rather than guessed.
SOURCE_ENCODING = "latin-1"

# --- OpenStreetMap fetch --------------------------------------------------

# overpass-api.de returned 504 on two of four probes and kumi.systems on one,
# at different times - so more than one host, tried in order. A 504 from one is
# not a fact about the data.
OVERPASS_HOSTS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
)
OVERPASS_USER_AGENT = (
    "expanded-heatmap city profiling (github.com/dacekroberts/expanded-heatmap)"
)
# Wide enough for Line A to La Paz and Line B to Ciudad Azteca, both in Estado
# de Mexico. A tighter box (19.04-19.62) silently returned 159 station nodes
# against 184 - the boundary filter, not the bbox, is what scopes this city.
OSM_BBOX = "18.95,-99.45,19.75,-98.85"

# WHITELIST, NOT A BLACKLIST, and this is not a style preference. OSM carries
# 13 PROPOSED Texcoco light-rail stations in this bbox, and five of them are
# tagged `railway=prpopsed` - misspelled in the source data. Excluding
# `railway=proposed` would have let those five through and drawn rings around
# building sites, which is Israel's STATUS trap. Keeping only railway=station
# is immune to the typo.
OSM_RAILWAY_KEEP = ("station",)
# railway=subway_entrance is 447 nodes against 184 stations - 2.4x. Counting
# entrances as stations is the Israeli entrances trap and would inflate every
# ring. Named here so the exclusion is explicit rather than incidental.
OSM_EXCLUDE_RAILWAY = ("subway_entrance", "proposed", "construction", "prpopsed")

# Both operators are kept: STC Metro (12 lines) and STE Tren Ligero (1 line).
# Tren Ligero is a different operator and a different mode, and it is included
# on the same reasoning that put Metromover on Miami's map and the Valley Line
# on Edmonton's - it is urban rail inside the city, and dropping it would leave
# the whole southern corridor to Xochimilco blank while the register still
# counts its shops. Metrobus is BRT and is NOT rail, so it is out.
OSM_STATION_NETWORKS = ("STC Metro", "Tren Ligero")

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 14N: the longitude (~-99.13) falls in the -102 to -96 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32614"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# GATE 3 IS UNAVAILABLE FOR THIS CITY AND THAT IS RECORDED, NOT WORKED AROUND.
# pipeline/stations.py calls the operator's published count "the one check that
# can see an error every internal check agrees with" - it is what corrected
# Edmonton 33->30 and Toronto 118->110. STC Metro publishes its station counts
# on metro.cdmx.gob.mx, which is unreachable from here (see the module
# docstring). A figure typed in from memory would LOOK like gate 3 and be
# worthless, so none is.
#
# What runs instead: the spacing gate, the railway=station whitelist above, and
# cross-direction agreement inside each route relation (each line has two
# direction relations whose station membership must match). Disclosed on the
# city page.
STATION_COUNT_GATE_3 = None
STATION_COUNT_GATE_3_REASON = (
    "STC Metro's published counts live on metro.cdmx.gob.mx, which returns "
    "ConnectTimeout from this environment on every host and scheme tried "
    "(2026-09-22). No published figure is asserted here."
)

# Measured from OSM on 2026-09-22, BEFORE the boundary filter. These are
# observations of the source, not the operator's figures - the names say so.
OSM_STATIONS_MEASURED = 184          # distinct STC Metro names in OSM_BBOX
OSM_TREN_LIGERO_MEASURED = 15        # distinct Tren Ligero names
OSM_PROPOSED_EXCLUDED = 13           # Texcoco light rail, 5 of them misspelled
OSM_ENTRANCES_EXCLUDED = 447         # railway=subway_entrance, never stations

# Real public line names and the operator's own livery colours, both straight
# from the OSM route relations, where `name`, `ref`, `colour`, `network` and
# `operator` are each 100% populated across all 26 relations. Keyed by `ref`.
LINE_NAMES = {
    "1": "Línea 1",
    "2": "Línea 2",
    "3": "Línea 3",
    "4": "Línea 4",
    "5": "Línea 5",
    "6": "Línea 6",
    "7": "Línea 7",
    "8": "Línea 8",
    "9": "Línea 9",
    "A": "Línea A",
    "B": "Línea B",
    "12": "Línea 12",
    "L1": "Tren Ligero",
}
#
# TWO OF THE THIRTEEN ARE DARKENED FROM OSM'S VALUE, and both are recorded here
# rather than silently adjusted. pipeline/linecolour.py RAISED on this city -
# the first time that check has stopped a build - because two pairs sat below
# the hard floor of Delta-E 10, where two colours are the same colour at a
# glance and a line disappears under its own pins:
#
#   Línea 2 #005EB8 vs Tren Ligero #0554ba   Delta-E  9.8   both blue
#   Línea 3 #AF9800 vs Línea 12    #B0A32A   Delta-E  8.5   both olive-gold
#
# These are LINE-VS-LINE clashes, which no previously built city hit; the
# check was written for line-vs-category. Resolved by the module's own rule -
# keep the agency's hue and change only lightness - and by moving the
# secondary line of each pair, so the more prominent service keeps the colour
# riders know:
#
#   Tren Ligero  #0554ba -> #033574  (lightness -0.14)  now 21.9 from Línea 2
#   Línea 12     #B0A32A -> #877D20  (lightness -0.10)  now 21.3 from Línea 3
#
# LÍNEA 2 IS DELIBERATELY NOT CHANGED, although it measures 10.4 against the
# Retail pin colour - the closest in the project after Calgary's historic 3.3.
# It is above the floor, and the 2026-09-21 branding decision keeps agencies'
# real route colours; fourteen line colours across six cities already sit in
# the 10-45 band and are recorded rather than repainted (New York's green at
# 13.6, Montréal's blue at 16.9). Darkening it to clear Retail was measured
# (-0.08 gives #00498F at 22.1) and rejected as overturning that decision for
# a line that is legible. Revisit only if a render shows it actually vanishing.
LINE_COLOURS = {
    "1": "#F04E98",
    "2": "#005EB8",
    "3": "#AF9800",
    "4": "#6BBBAE",
    "5": "#FFD100",
    "6": "#DA291C",
    "7": "#E87722",
    "8": "#009A44",
    "9": "#512F2E",
    "A": "#981D97",
    "B": "#B1B3B3",
    "12": "#877D20",   # darkened from OSM's #B0A32A - see above
    "L1": "#033574",   # darkened from OSM's #0554ba - see above
}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "scian"
# DENUE's own column names. Step 2 renames these to the taxonomy's columns.
DENUE_NAME_COLUMN = "nom_estab"          # the exterior sign, per INEGI's dictionary
DENUE_ACTIVITY_COLUMN = "nombre_act"     # -> scian_actividad (the tooltip value)
DENUE_CODE_COLUMN = "codigo_act"         # -> scian (what classify() reads)
RAW_CLASSIFICATION_COLUMN = "scian_actividad"

# FIJO ONLY. DENUE distinguishes Fijo (442,146, 95.55%) from Semifijo (20,586,
# 4.45%) - a semi-fixed stall or street post rather than a storefront. This
# project maps storefronts, so the same reasoning that excluded nonstore retail
# and home-based businesses excludes these: 18,264 of them would otherwise have
# classified into a bucket. Owner's decision 2026-09-22, stated on the city
# page and in docs/excluded_categories.md rather than applied silently.
PREMISES_TYPE_COLUMN = "tipoUniEco"
PREMISES_TYPE_KEEP = "Fijo"

# NEVER LOADED, and step 2 asserts they never arrive - New York's pattern,
# which is what lets that city claim structurally that no pin can be a
# registrant's name.
#
#   telefono    35.56% populated - a phone number at a sole trader's premises
#   correoelec  22.64% - likewise an email
#   www         10.60%
#   raz_social  25.87% - the legal entity name. INEGI ALREADY omits it when the
#               owner is a persona fisica, explicitly "para proteger la
#               confidencialidad de la informacion", so what remains is
#               corporate. It is still not loaded: `nom_estab` is populated on
#               99.95% of rows, so no fallback to a legal name is ever needed,
#               and Los Angeles' 4,000 published individual names came from
#               exactly such a fallback. Forbidding the column structurally
#               removes the failure mode rather than relying on the fallback
#               never firing.
FORBIDDEN_COLUMNS = ("telefono", "correoelec", "www", "raz_social")

# Sanity bounds for coordinates, tightened to CDMX's real extent plus the
# Estado de Mexico reach of Lines A and B (cut later by the boundary filter).
MEXICO_CITY_BBOX = {
    "lat_min": 18.95,
    "lat_max": 19.75,
    "lon_min": -99.45,
    "lon_max": -98.85,
}
