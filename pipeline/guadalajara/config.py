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

# INTERCHANGES UNDER TWO NAMES, merged by the owner's call (2026-10-04, via
# Cleanup; DECISIONS.md). Each pair sat 91 m
# apart as two stations: one interchange, one station. Not a spelling, so
# station_name_key cannot merge them; this map does, by exact OSM name.
# The merged Centro station carries both names, since each line's riders know
# it by its own. Step 1 raises if an OSM name here is gone (a stale entry) or
# if a merged station's stops spread past INTERCHANGE_MAX_SPREAD_M.
INTERCHANGE_NAMES = {
    "Juárez II": "Juárez",
    "Guadalajara Centro": "Guadalajara Centro / Plaza Universidad",
    "Plaza Universidad": "Guadalajara Centro / Plaza Universidad",
}
INTERCHANGE_MAX_SPREAD_M = 250.0

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

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3605605820,3605606276,3605606517,3605606660)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("es",)
PLACE_FOLD = None
PLACE_REVIEWED = {
    "Calle G.U.S.A.": "a residential street whose name is an abbreviation, not a company form; the read of 2026-10-13",
}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "way/829874164": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837931377": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/473465228": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837931382": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837931374": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837931388": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837931400": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837931392": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837931399": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837931387": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837931375": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/473465225": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837931383": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837931376": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837931384": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/837251490": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/869762475": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/825218472": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/466223853": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/825218746": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/825032160": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/825032886": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/675578045": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/470802242": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/470802250": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/1248251319": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/1248251291": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/1248251292": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/1248251289": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/552291242": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/1248251293": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/908435689": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/908435555": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/908435949": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/467382416": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/893795875": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/468031609": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/468031620": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/468031624": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/164115842": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/478007070": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/470802273": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/471998923": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/470441442": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/869789156": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/908124543": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/908125067": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/908124177": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/474383371": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/474383372": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/467379607": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/469210959": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/586006756": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/586006755": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/465216461": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/1080966517": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/308501117": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/1562301437": "a residents' amenity inside a gated estate tagged a park (owner, 2026-10-13)",
    "way/1026734452": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/1026734453": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/1026734454": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/1026734476": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/1026734455": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/1026734458": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/1026734472": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/1248251269": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/654322779": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/654322766": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/654322767": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/654322768": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/483270025": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/483270008": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/483270003": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/483270001": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/483270020": "a park named by a planning or stage code (owner, 2026-10-13)",
    "node/9002362743": "a park named by a planning or stage code (owner, 2026-10-13)",
    "node/9002376173": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/691794278": "a code-named private street (owner, 2026-10-13)",
    "way/131882588": "a code-named private street (owner, 2026-10-13)",
    "way/164981933": "a code-named private street (owner, 2026-10-13)",
    "way/696751879": "a code-named private street (owner, 2026-10-13)",
    "way/169924354": "a code-named private street (owner, 2026-10-13)",
    "way/691833115": "a code-named private street (owner, 2026-10-13)",
    "way/678017899": "a code-named private street (owner, 2026-10-13)",
    "way/169924361": "a code-named private street (owner, 2026-10-13)",
    "way/696477195": "a code-named private street (owner, 2026-10-13)",
    "way/703130640": "a code-named private street (owner, 2026-10-13)",
    "way/697188044": "a code-named private street (owner, 2026-10-13)",
    "way/678020199": "a code-named private street (owner, 2026-10-13)",
    "way/466530716": "a code-named private street (owner, 2026-10-13)",
    "way/466530717": "a code-named private street (owner, 2026-10-13)",
    "way/678012249": "a code-named private street (owner, 2026-10-13)",
    "way/678015846": "a code-named private street (owner, 2026-10-13)",
    "way/691833129": "a code-named private street (owner, 2026-10-13)",
    "way/481866121": "a code-named private street (owner, 2026-10-13)",
    "way/823581611": "a code-named private street (owner, 2026-10-13)",
    "way/131882576": "a code-named private street (owner, 2026-10-13)",
    "way/698794010": "a code-named private street (owner, 2026-10-13)",
    "way/482937422": "a code-named private street (owner, 2026-10-13)",
    "way/482937424": "a code-named private street (owner, 2026-10-13)",
    "way/481866122": "a code-named private street (owner, 2026-10-13)",
    "way/823581612": "a code-named private street (owner, 2026-10-13)",
    "way/696520830": "a code-named private street (owner, 2026-10-13)",
    "way/691307529": "a code-named private street (owner, 2026-10-13)",
    "way/691833112": "a code-named private street (owner, 2026-10-13)",
    "way/695703059": "a code-named private street (owner, 2026-10-13)",
    "way/466530713": "a code-named private street (owner, 2026-10-13)",
    "way/466530711": "a code-named private street (owner, 2026-10-13)",
    "way/169924355": "a code-named private street (owner, 2026-10-13)",
    "way/169924353": "a code-named private street (owner, 2026-10-13)",
    "way/122049104": "a code-named private street (owner, 2026-10-13)",
    "way/691307544": "a code-named private street (owner, 2026-10-13)",
    "way/697241059": "a code-named private street (owner, 2026-10-13)",
    "way/466530707": "a code-named private street (owner, 2026-10-13)",
    "way/466530709": "a code-named private street (owner, 2026-10-13)",
    "way/691969483": "a code-named private street (owner, 2026-10-13)",
    "way/691969482": "a code-named private street (owner, 2026-10-13)",
    "way/691305751": "a code-named private street (owner, 2026-10-13)",
    "way/157198009": "a code-named private street (owner, 2026-10-13)",
    "way/157198010": "a code-named private street (owner, 2026-10-13)",
    "way/696510440": "a code-named private street (owner, 2026-10-13)",
    "way/157198011": "a code-named private street (owner, 2026-10-13)",
    "way/689707828": "a code-named private street (owner, 2026-10-13)",
    "way/1081170896": "a code-named private street (owner, 2026-10-13)",
    "way/1081170876": "a code-named private street (owner, 2026-10-13)",
    "way/1081170874": "a code-named private street (owner, 2026-10-13)",
    "way/1081170906": "a code-named private street (owner, 2026-10-13)",
    "way/1081170870": "a code-named private street (owner, 2026-10-13)",
    "way/1081170907": "a code-named private street (owner, 2026-10-13)",
    "way/1081170887": "a code-named private street (owner, 2026-10-13)",
    "way/1081170888": "a code-named private street (owner, 2026-10-13)",
    "way/1081170879": "a code-named private street (owner, 2026-10-13)",
    "way/1081170895": "a code-named private street (owner, 2026-10-13)",
    "way/1081170880": "a code-named private street (owner, 2026-10-13)",
    "way/1081170894": "a code-named private street (owner, 2026-10-13)",
    "way/1081170893": "a code-named private street (owner, 2026-10-13)",
    "way/1081170891": "a code-named private street (owner, 2026-10-13)",
    "way/1081170892": "a code-named private street (owner, 2026-10-13)",
    "way/1081170890": "a code-named private street (owner, 2026-10-13)",
    "way/1081170889": "a code-named private street (owner, 2026-10-13)",
    "way/1081170903": "a code-named private street (owner, 2026-10-13)",
    "way/473467320": "a code-named private street (owner, 2026-10-13)",
    "way/473467321": "a code-named private street (owner, 2026-10-13)",
    "way/473467322": "a code-named private street (owner, 2026-10-13)",
    "way/672177037": "a code-named private street (owner, 2026-10-13)",
    "way/154928280": "a code-named private street (owner, 2026-10-13)",
    "way/155168577": "a code-named private street (owner, 2026-10-13)",
    "way/155168686": "a code-named private street (owner, 2026-10-13)",
    "way/155168700": "a code-named private street (owner, 2026-10-13)",
    "way/155174828": "a code-named private street (owner, 2026-10-13)",
    "way/166180485": "a code-named private street (owner, 2026-10-13)",
    "way/166180488": "a code-named private street (owner, 2026-10-13)",
    "way/166180528": "a code-named private street (owner, 2026-10-13)",
    "way/477704692": "a code-named private street (owner, 2026-10-13)",
    "way/654598333": "a code-named private street (owner, 2026-10-13)",
    "way/700154446": "a code-named private street (owner, 2026-10-13)",
    "way/154789915": "a code-named private street (owner, 2026-10-13)",
    "way/491010190": "a code-named private street (owner, 2026-10-13)",
    "way/166776476": "a code-named private street (owner, 2026-10-13)",
    "way/688243784": "a code-named private street (owner, 2026-10-13)",
    "way/688243785": "a code-named private street (owner, 2026-10-13)",
    "way/688243786": "a code-named private street (owner, 2026-10-13)",
    "way/166776466": "a code-named private street (owner, 2026-10-13)",
    "way/688243783": "a code-named private street (owner, 2026-10-13)",
    "way/491010193": "a code-named private street (owner, 2026-10-13)",
    "way/166776454": "a code-named private street (owner, 2026-10-13)",
    "way/491010192": "a code-named private street (owner, 2026-10-13)",
    "way/166776462": "a code-named private street (owner, 2026-10-13)",
    "way/491010189": "a code-named private street (owner, 2026-10-13)",
    "way/166776477": "a code-named private street (owner, 2026-10-13)",
    "way/491010188": "a code-named private street (owner, 2026-10-13)",
    "way/688243781": "a code-named private street (owner, 2026-10-13)",
    "way/688243782": "a code-named private street (owner, 2026-10-13)",
    "way/154790015": "a code-named private street (owner, 2026-10-13)",
    "way/477704691": "a code-named private street (owner, 2026-10-13)",
    "way/466527094": "a code-named private street (owner, 2026-10-13)",
    "way/166776475": "a code-named private street (owner, 2026-10-13)",
    "way/688243778": "a code-named private street (owner, 2026-10-13)",
    "way/688243779": "a code-named private street (owner, 2026-10-13)",
    "way/688243780": "a code-named private street (owner, 2026-10-13)",
    "way/155206731": "a code-named private street (owner, 2026-10-13)",
    "way/688483491": "a code-named private street (owner, 2026-10-13)",
    "way/698692878": "a code-named private street (owner, 2026-10-13)",
    "way/701204196": "a code-named private street (owner, 2026-10-13)",
    "way/786037662": "a code-named private street (owner, 2026-10-13)",
    "way/786037663": "a code-named private street (owner, 2026-10-13)",
    "way/843293703": "a code-named private street (owner, 2026-10-13)",
    "way/843311264": "a code-named private street (owner, 2026-10-13)",
    "way/893151717": "a code-named private street (owner, 2026-10-13)",
    "way/893151718": "a code-named private street (owner, 2026-10-13)",
    "way/590261320": "a code-named private street (owner, 2026-10-13)",
    "way/590266339": "a code-named private street (owner, 2026-10-13)",
    "way/590266340": "a code-named private street (owner, 2026-10-13)",
    "way/590269775": "a code-named private street (owner, 2026-10-13)",
    "way/590269791": "a code-named private street (owner, 2026-10-13)",
    "way/590273839": "a code-named private street (owner, 2026-10-13)",
    "way/786037664": "a code-named private street (owner, 2026-10-13)",
    "way/590261319": "a code-named private street (owner, 2026-10-13)",
    "way/590266341": "a code-named private street (owner, 2026-10-13)",
    "way/590269773": "a code-named private street (owner, 2026-10-13)",
    "way/590269792": "a code-named private street (owner, 2026-10-13)",
    "way/590273841": "a code-named private street (owner, 2026-10-13)",
    "way/786037665": "a code-named private street (owner, 2026-10-13)",
    "way/590261318": "a code-named private street (owner, 2026-10-13)",
    "way/590261321": "a code-named private street (owner, 2026-10-13)",
    "way/590265375": "a code-named private street (owner, 2026-10-13)",
    "way/590269762": "a code-named private street (owner, 2026-10-13)",
    "way/590269764": "a code-named private street (owner, 2026-10-13)",
    "way/590269769": "a code-named private street (owner, 2026-10-13)",
    "way/590269771": "a code-named private street (owner, 2026-10-13)",
    "way/590269782": "a code-named private street (owner, 2026-10-13)",
    "way/590269783": "a code-named private street (owner, 2026-10-13)",
    "way/590269789": "a code-named private street (owner, 2026-10-13)",
    "way/590273836": "a code-named private street (owner, 2026-10-13)",
    "way/700431505": "a code-named private street (owner, 2026-10-13)",
    "way/700431506": "a code-named private street (owner, 2026-10-13)",
    "way/700431507": "a code-named private street (owner, 2026-10-13)",
    "way/700432448": "a code-named private street (owner, 2026-10-13)",
    "way/843297251": "a code-named private street (owner, 2026-10-13)",
    "way/843297252": "a code-named private street (owner, 2026-10-13)",
    "way/843297255": "a code-named private street (owner, 2026-10-13)",
    "way/843297258": "a code-named private street (owner, 2026-10-13)",
    "way/155025091": "a code-named private street (owner, 2026-10-13)",
    "way/466294417": "a code-named private street (owner, 2026-10-13)",
    "way/689975488": "a code-named private street (owner, 2026-10-13)",
    "way/689975489": "a code-named private street (owner, 2026-10-13)",
    "way/885987674": "a code-named private street (owner, 2026-10-13)",
    "way/590261322": "a code-named private street (owner, 2026-10-13)",
    "way/590266343": "a code-named private street (owner, 2026-10-13)",
    "way/590269777": "a code-named private street (owner, 2026-10-13)",
    "way/590269790": "a code-named private street (owner, 2026-10-13)",
    "way/590273840": "a code-named private street (owner, 2026-10-13)",
    "way/786037666": "a code-named private street (owner, 2026-10-13)",
    "way/590261323": "a code-named private street (owner, 2026-10-13)",
    "way/590266342": "a code-named private street (owner, 2026-10-13)",
    "way/590273837": "a code-named private street (owner, 2026-10-13)",
    "way/786037667": "a code-named private street (owner, 2026-10-13)",
    "way/590266344": "a code-named private street (owner, 2026-10-13)",
    "way/590273846": "a code-named private street (owner, 2026-10-13)",
    "way/590266345": "a code-named private street (owner, 2026-10-13)",
    "way/590269779": "a code-named private street (owner, 2026-10-13)",
    "way/590273845": "a code-named private street (owner, 2026-10-13)",
    "way/590269781": "a code-named private street (owner, 2026-10-13)",
    "way/590273842": "a code-named private street (owner, 2026-10-13)",
    "way/843293704": "a code-named private street (owner, 2026-10-13)",
    "way/590266346": "a code-named private street (owner, 2026-10-13)",
    "way/590273843": "a code-named private street (owner, 2026-10-13)",
    "way/843297253": "a code-named private street (owner, 2026-10-13)",
    "way/590269758": "a code-named private street (owner, 2026-10-13)",
    "way/132297211": "a code-named private street (owner, 2026-10-13)",
    "way/132297239": "a code-named private street (owner, 2026-10-13)",
    "way/1271819724": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1155131257": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1250931515": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1250933525": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/653450233": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1313101761": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1313101762": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1313102077": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/842544455": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1249656192": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1249656193": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/667913331": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/667913333": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1249713184": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1249714070": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1313103275": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1313103277": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1250511656": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1361196833": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1250514641": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1250515117": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/301319790": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/312538668": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1250908977": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1250913736": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1313110423": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1313110424": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1313111012": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1313111013": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1361194507": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1313099337": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1250928870": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1313100090": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1361194508": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1361194509": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1361194510": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1361196832": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/667910826": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1245423425": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1559232437": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1058156145": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1058158747": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1250843757": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1250851499": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1250856068": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1361194505": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/347092651": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/301305760": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/667910828": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1324600327": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/582776014": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/155290404": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/160554533": "a code-named private street (owner, 2026-10-13)",
    "way/827067242": "a code-named private street (owner, 2026-10-13)",
    "way/479396764": "a code-named private street (owner, 2026-10-13)",
    "way/160554512": "a code-named private street (owner, 2026-10-13)",
    "way/160554525": "a code-named private street (owner, 2026-10-13)",
    "way/155218431": "a code-named private street (owner, 2026-10-13)",
    "way/415151330": "a code-named private street (owner, 2026-10-13)",
    "way/415151331": "a code-named private street (owner, 2026-10-13)",
    "way/155074597": "a code-named private street (owner, 2026-10-13)",
    "way/432069404": "a code-named private street (owner, 2026-10-13)",
    "way/828530910": "a code-named private street (owner, 2026-10-13)",
    "way/432069362": "a code-named private street (owner, 2026-10-13)",
    "way/432069395": "a code-named private street (owner, 2026-10-13)",
    "way/828531746": "a code-named private street (owner, 2026-10-13)",
    "way/1078584863": "a code-named private street (owner, 2026-10-13)",
    "way/466805731": "a code-named private street (owner, 2026-10-13)",
    "way/802705846": "a code-named private street (owner, 2026-10-13)",
    "way/802705847": "a code-named private street (owner, 2026-10-13)",
    "way/802705850": "a code-named private street (owner, 2026-10-13)",
    "way/828533928": "a code-named private street (owner, 2026-10-13)",
    "way/479975058": "a code-named private street (owner, 2026-10-13)",
    "way/479975055": "a code-named private street (owner, 2026-10-13)",
    "way/479975071": "a code-named private street (owner, 2026-10-13)",
    "way/834039200": "a code-named private street (owner, 2026-10-13)",
    "way/834039201": "a code-named private street (owner, 2026-10-13)",
    "way/907260687": "a code-named private street (owner, 2026-10-13)",
    "way/907260688": "a code-named private street (owner, 2026-10-13)",
    "way/933075057": "a code-named private street (owner, 2026-10-13)",
    "node/5205025157": "a non-rail object in as a station, a description for a name",
    "node/7310312118": "a non-rail object in as a station (a power utility's service point)",
    "node/7667027131": "a gated cluster's letter box with a phase code for a name",
    "node/7866542124": "a gated cluster's letter box with a phase code for a name",
    "node/7866542126": "a gated cluster's letter box with a phase code for a name",
    "node/7866542125": "a gated cluster's letter box with a phase code for a name",
    "node/7866542127": "a gated cluster's letter box with a phase code for a name",
    "node/7866518707": "a gated cluster's letter box with a phase code for a name",
    "node/14005555282": "a name that says the village is abandoned",
    "node/14088258543": "a rehearsal-room business tagged a park",
    "node/14088101884": "a rehearsal-room business tagged a park",
    "way/555577804": "a company campus's own feature tagged a park, a description for a name",
    "way/555577805": "a company campus's own feature tagged a park, a description for a name",
    "way/555577812": "a company campus's own feature tagged a park, a description for a name",
    "way/555577782": "a company campus's own feature tagged a park, a description for a name",
    "way/555577787": "a company campus's own feature tagged a park, a description for a name",
    "way/555577779": "a company campus's own feature tagged a park, a description for a name",
    "way/555577786": "a company campus's own feature tagged a park, a description for a name",
    "way/787816657": "a funeral home tagged a place of worship",
    "way/550738191": "a health centre tagged a park",
    "way/550738192": "a health centre tagged a park, a misspelled duplicate",
    "way/550738190": "a health centre tagged a park, a misspelled duplicate",
    "node/3802499982": "a preschool tagged a park",
    "way/302468973": "a scout group tagged a park",
    "way/1562302512": "a sports pitch tagged a park",
    "way/899066475": "a sports pitch tagged a park",
    "way/605087481": "a sports pitch tagged a park",
    "way/470726352": "a residential estate's clubhouse tagged a park",
    "way/470401771": "a residential estate's clubhouse tagged a park",
    "way/468455995": "a residential estate's clubhouse tagged a park",
    "way/468456013": "a residential estate's clubhouse tagged a park",
    "way/470356564": "a residential estate's clubhouse tagged a park",
    "way/473155700": "a residential estate's clubhouse tagged a park",
    "way/708334300": "a condominium's own park, by its operator tag",
    "way/1016579247": "a description standing in for a name",
    "way/393296396": "a description standing in for a name",
    "way/839975815": "a description standing in for a name",
    "way/825216780": "a description standing in for a name",
    "way/467379624": "a numbered residents' terrace, a code for a name",
    "way/467379623": "a numbered residents' terrace, a code for a name",
    "way/492680541": "a numbered residents' terrace, a code for a name",
    "way/125709114": "a one or two letter code for a name",
    "node/8086596140": "a one or two letter code for a name",
    "way/179146930": "a stray character glued on the name",
    "node/1705345907": "a description and a year glued on a building's name",
    "node/1481551981": "a misspelled duplicate of a listed church",
    "node/4715305063": "a duplicate of a listed church",
    "node/9768804517": "a duplicate of a listed church",
    "node/3163644357": "a duplicate of a listed church",
    "way/1379363436": "a duplicate of a listed church",
    "way/825216644": "a duplicate of a listed park",
    "node/3802568321": "a duplicate of a listed campus, the weaker node",
    "node/3986687617": "a kiosk survey point inside a listed garden",
    "way/749636577": "a duplicate of a listed river with a misplaced accent",
    "way/749636578": "a duplicate of a listed river with a misplaced accent",
    "way/749636579": "a duplicate of a listed river with a misplaced accent",
    "way/749636580": "a duplicate of a listed river with a misplaced accent",
    "way/749636581": "a duplicate of a listed river with a misplaced accent",
    "way/749636582": "a duplicate of a listed river with a misplaced accent",
    "way/749636583": "a duplicate of a listed river with a misplaced accent",
    "way/749636584": "a duplicate of a listed river with a misplaced accent",
    "way/749636585": "a duplicate of a listed river with a misplaced accent",
    "way/749636586": "a duplicate of a listed river with a misplaced accent",
    "way/749636587": "a duplicate of a listed river with a misplaced accent",
    "node/3144904092": "an animal or object figure tagged a monument, no article",
    "node/3144904091": "an animal or object figure tagged a monument, no article",
    "node/3144904090": "an animal or object figure tagged a monument, no article",
    "node/3144904088": "an animal or object figure tagged a monument, no article",
    "node/3144904089": "an animal or object figure tagged a monument, no article",
    "node/5322586142": "an estate's entrance sign or arch tagged a monument",
    "node/5321002413": "an estate's entrance sign or arch tagged a monument",
    "node/5321010052": "an estate's entrance sign or arch tagged a monument",
    "node/4683530081": "an estate's entrance sign or arch tagged a monument",
    "node/11195093494": "a developer's sign tagged a monument, no article",
    "node/5319660428": "a scale replica tagged a monument, no article",
    "node/14038596085": "a letters sign tagged a monument, no article",
    "node/14049799401": "a letters sign tagged a monument, no article",
    "way/1250512891": "a plaque tagged a monument, a description for a name",
    "way/1250512890": "a plaque tagged a monument, a description for a name",
    "node/6579098404": "a sculpture on a building's upper floor, access no, no article",
    "way/1207647746": "a placeholder standing in for a name",
    "way/1207647747": "a placeholder standing in for a name",
    "way/941980621": "a test label standing in for a name",
    "way/154963148": "a single letter code",
    "way/154963149": "a single letter code",
    "way/154963150": "a single letter code",
    "way/155207304": "a glitched name (glued words, doubled word or typo)",
    "way/701339459": "a glitched name (glued words, doubled word or typo)",
    "way/654737567": "a glitched name (glued words, doubled word or typo)",
    "way/263775336": "a glitched name (glued words, doubled word or typo)",
    "way/906149869": "a glitched name (glued words, doubled word or typo)",
    "way/471896069": "a glitched name (glued words, doubled word or typo)",
    "way/587600066": "a glitched name (glued words, doubled word or typo)",
    "way/698104767": "a glitched name (glued words, doubled word or typo)",
    "way/176845849": "a glitched name (glued words, doubled word or typo)",
    "way/1361194506": "a glitched name (glued words, doubled word or typo)",
    "way/164760297": "an estate, venue or facility gate road",
    "way/934372399": "an estate, venue or facility gate road",
    "way/1141590452": "an estate, venue or facility gate road",
    "way/429335378": "an estate, venue or facility gate road",
    "way/934372395": "an estate, venue or facility gate road",
    "way/164760308": "an estate, venue or facility gate road",
    "way/944791839": "an estate, venue or facility gate road",
    "way/673191288": "an estate, venue or facility gate road",
    "way/429340469": "an estate, venue or facility gate road",
    "way/934372400": "an estate, venue or facility gate road",
    "way/164760296": "an estate, venue or facility gate road",
    "way/934372396": "an estate, venue or facility gate road",
    "way/164760314": "an estate, venue or facility gate road",
    "way/944791840": "an estate, venue or facility gate road",
    "way/157019706": "an estate, venue or facility gate road",
    "way/472815759": "an estate, venue or facility gate road",
    "way/477939823": "an estate, venue or facility gate road",
    "way/1564616494": "an estate, venue or facility gate road",
    "way/1309525741": "a code beside a type on minor firebreak paths",
    "way/1208960185": "a code beside a type on minor firebreak paths",
    "way/1309525744": "a code beside a type on minor firebreak paths",
    "way/1324000836": "a code beside a type on minor firebreak paths",
    "way/1324584260": "a code beside a type on minor firebreak paths",
    "way/908436903": "a description standing in for a name",
    "way/908436904": "a description standing in for a name",
    "way/908436905": "a description standing in for a name",
    "way/1544381391": "a park feature, not a street",
}
