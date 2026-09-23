"""Guadalajara (Regional) settings - Mexico's second city, and the one that
shows which of Mexico City's settings were national and which were local.

REGIONAL, on the operator's own description. SITEUR states that Línea 3
"conecta Zapopan, Guadalajara y Tlaquepaque" and that Línea 4 connects
"Tlajomulco de Zúñiga, Tlaquepaque y Guadalajara", so a Guadalajara-municipio
build would truncate two of four lines. Same shape as Miami (42 stations, six
municipalities) and Vancouver (24 stations, two).

THE GTFS FEED WAS FOUND, DOWNLOADED, AND REJECTED - which is a different
finding from Mexico City's unreachable host, and the numbers are recorded so
nobody re-adopts it:

  * The only Guadalajara rail feed in the Mobility Database (mdb 1925, also
    inside the larger 2366) carries `feed_end_date = 20230128` in its own
    `feed_info.txt`. **It expired 2023-01-28**, three and a half years before
    this build.
  * Its `feed_publisher_name` is **Nubenautas** (`gtfs.studio`) - a third
    party, not SITEUR.
  * It contains **three** light-rail routes. SITEUR publishes **four**, because
    **Línea 4 opened on 15 December 2025** - almost three years after the feed
    stopped. Building from it would have drawn a map missing an entire
    operating line, 8 stations and 21 km, while looking complete.

That is the Toronto lesson (a stale mirror missing a mode) with the staleness
declared in the artifact itself, which is exactly the case add-country says to
catch by reading `feed_end_date` rather than by avoiding mirrors. So the
geometry comes from OpenStreetMap, as Mexico City's does - the owner's second
documented exception, granted 2026-09-22 on incompleteness rather than on
unreachability.

AND UNLIKE MEXICO CITY, GATE 3 RUNS HERE. `siteur.gob.mx` answers (HTTP 200),
so the operator's published station counts are readable, and OSM matches them
on both lines where SITEUR states one.
"""

from pathlib import Path

from pipeline.countries.mexico import (  # noqa: F401
    DENUE_ACTIVITY_COLUMN,
    DENUE_CODE_COLUMN,
    DENUE_INTERIOR_COLUMN,
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

# Re-exported above rather than redefined: every one of those names is a fact
# about DENUE or about OpenStreetMap, not about this city, and both Mexican
# cities were measured to agree on all of them before the split. The `noqa`
# is deliberate - these ARE unused here and are imported so that this city's
# step files keep importing them from this module, unchanged.

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "guadalajara" / "raw"
DATA_PROCESSED = ROOT / "data" / "guadalajara" / "processed"
OUTPUTS = ROOT / "outputs" / "guadalajara"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
# Which municipio each kept station lies in - the regional-build record, as
# Miami's station_municipalities.csv and Vancouver's are.
STATION_MUNICIPIOS_CSV = OUTPUTS / "station_municipios.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs -----------------------------------------------------------
#
# 14 = Jalisco. The only per-city part of the download; see
# pipeline/countries/mexico.py for the URL shape and the dictionary near-miss.
#
# UNLIKE MEXICO CITY, the entidad is NOT the city: Jalisco holds 125
# municipios including Puerto Vallarta 300 km away, so this city scopes by
# MUNICIPIOS_KEEP below. That difference is the clearest single reason the
# state code stayed per-city while everything around it moved out.
DENUE_STATE_CODE = "14"
DENUE_URL = denue_url(DENUE_STATE_CODE)
DENUE_MEMBER = denue_member(DENUE_STATE_CODE)
DENUE_ZIP = DATA_RAW / f"denue_{DENUE_STATE_CODE}_csv.zip"

OSM_STATIONS_JSON = DATA_RAW / "osm_stations.json"
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"


# --- The regional scope ---------------------------------------------------
#
# DENUE's `municipio` values, exactly as INEGI spells them - the join is on
# this string, so the spelling is the interface. Measured in state 14:
#   Guadalajara 97,134 · Zapopan 53,311 · San Pedro Tlaquepaque 26,832 ·
#   Tlajomulco de Zúñiga 19,630   (Tonalá's 19,897 is NOT included: no line
#   reaches it, and including a municipio with no station would add businesses
#   that no ring can ever contain.)
#
# NOTE "San Pedro Tlaquepaque", not "Tlaquepaque" - SITEUR's prose says
# Tlaquepaque and INEGI's register says San Pedro Tlaquepaque. Matching the
# operator's wording here would keep zero rows, which is Los Angeles' CITY_KEEP
# trap and Toronto's "former Toronto" trap in one.
MUNICIPIOS_KEEP = (
    "Guadalajara",
    "Zapopan",
    "San Pedro Tlaquepaque",
    "Tlajomulco de Zúñiga",
)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 13N: the longitude (~-103.35) falls in the -108 to -102 band.
# Mexico City is 14N - the CRS is per city and never copied, and these two
# cities are the project's own worked example of why.
CRS_PROJECTED = "EPSG:32613"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- OpenStreetMap fetch --------------------------------------------------

OSM_BBOX = "20.35,-103.60,20.85,-103.15"

# GUADALAJARA'S STATIONS ARE TAGGED DIFFERENTLY FROM MEXICO CITY'S, and this is
# the single most important line in this file. Mexico City has 184
# `railway=station` nodes; Guadalajara has **one**. Its stations are
# `railway=stop` - per-direction stop positions - carrying `network=Mi Tren`:
# **96 nodes, 48 distinct names, exactly 2 per name**, which is one per
# direction with no exceptions.
#
# So Mexico City's whitelist would have found ONE station here and the build
# would have looked like a boundary or scope problem rather than a tagging one.
# This is why pipeline/stations.py shares the CHECKS and leaves the COLLAPSE
# per city: two cities in one country, one register, one taxonomy - and
# different station objects.
OSM_STATION_RAILWAY = ("stop",)
OSM_STATION_NETWORK = "Mi Tren"
# 114 subway entrances in this bbox. Never stations - Israel's trap.
OSM_EXCLUDE_RAILWAY = ("subway_entrance", "proposed", "construction", "prpopsed",
                       "level_crossing", "switch", "crossing", "buffer_stop",
                       "railway_crossing", "milestone", "signal")

# --- Station scope ----------------------------------------------------------

# Real public names and colours from the OSM route relations, keyed by `ref`.
LINE_NAMES = {
    "TL-1": "Línea 1",
    "TL-2": "Línea 2",
    "TL-3": "Línea 3",
    "TL-4": "Línea 4",
}
# OSM carries a hex value for three of the four. Línea 4's `colour` tag is the
# WORD "orange", so it is resolved through the CSS named-colour table
# (orange = #FFA500) rather than invented - a defined mapping, and recorded
# here because it is the one colour on this map that is not a hex value in the
# source.
LINE_COLOURS = {
    "TL-1": "#c5112c",
    "TL-2": "#27be31",
    "TL-3": "#dd0e98",
    "TL-4": "#FFA500",   # OSM's `colour=orange`, via the CSS named-colour table
}

# GATE 3, AND IT RUNS HERE. siteur.gob.mx answers, so these are the operator's
# own published figures, read from
# siteur.gob.mx/index.php/sistemas-de-transporte/mi-tren on 2026-09-22:
#   Línea 2  "recorre el corredor Javier Mina - Juárez a través de 10
#             estaciones subterráneas"                          -> 10
#   Línea 4  "Estaciones: 8"                                    ->  8
# SITEUR publishes no station count for Líneas 1 or 3 on that page, so those
# are left out rather than filled in from anywhere else - a partial gate 3 with
# its gaps named is worth more than a complete-looking one built from memory.
# Measured against OSM route-relation membership on 2026-09-22: both MATCH.
PUBLISHED_STATIONS_PER_LINE = {
    "Línea 2": 10,
    "Línea 4": 8,
}

# --- Business filtering ------------------------------------------------


# Fijo only, and Jalisco is 97.94% Fijo against Ciudad de Mexico's
# 95.55% - street commerce is a smaller share here. Both the column and
# the kept value are shared; only this observation is local.

GUADALAJARA_BBOX = {
    "lat_min": 20.35,
    "lat_max": 20.85,
    "lon_min": -103.60,
    "lon_max": -103.15,
}
