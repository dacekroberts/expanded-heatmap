"""Florence-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

FIRENZE, on Milan's and Rome's template (the Comune's own activity layers, an
OSM comune boundary) and the shared `pipeline/osm_tram.py` (the tram-city
skill). The business leg is the Comune di Firenze's four GeoJSON layers
(CC BY 4.0): a point and a type on every row, no name and no address, so a dot
shows its type (`pipeline/taxonomies/florence_attivita.py`). Rail from
OpenStreetMap; GEST's GTFS is not used.
"""

from pathlib import Path

SLUG = "florence"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "florence" / "raw"
DATA_PROCESSED = ROOT / "data" / "florence" / "processed"
OUTPUTS = ROOT / "outputs" / "florence"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# T1's four stops in Scandicci, outside the comune: drawn, not ringed, listed
# here with the comune each lies in (call 17).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) ----------------

# The Comune's four layers (datigis.comune.fi.it/json/, CC BY 4.0; credit the
# Comune di Firenze, state the changes). EPSG:3003 (Monte Mario / Italy 1).
# Layer key -> file. The key is the taxonomy's `source`.
LAYERS = {
    "commercio": "commercio_sede_fissa_od.json",
    "pubblici_esercizi": "pubblici_esercizi_od.json",
    "estetiche": "attivita_estetiche_od.json",
    "tintolavanderie": "tintolavanderie_od.json",
}
LAYER_URL = "https://datigis.comune.fi.it/json/"     # + the file name
LAYER_CRS = "EPSG:3003"
LAYER_MIN_ROWS = {"commercio": 6000, "pubblici_esercizi": 2500, "estetiche": 1000,
                  "tintolavanderie": 100}

# OSM: every tram relation in the network's box, and the comuni around it.
RAIL_BBOX = (43.72, 11.15, 43.84, 11.34)          # south, west, north, east
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_COMUNI_JSON = DATA_RAW / "osm_comuni.json"
# Comune di Firenze, OSM relation 42602, ref:ISTAT 048017; the other comuni in
# the box only name where an outside stop lies.
ISTAT_FIRENZE = "048017"
COMUNE_AREA_KM2 = (95.0, 110.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 32N: the longitude (~11.25) falls in the 6-12 E band. Derived per
# city, not copied.
CRS_PROJECTED = "EPSG:32632"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the 39 in-comune stops' 322 m median gap (the brief, 2026-09-30;
# the owner's spacing rule). Step 1 prints the median again and stops outside
# 270-380 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (270.0, 380.0)

# --- Station scope: T1 and T2, every stop in the comune ------------------------
#
# Tramvia di Firenze: T1 Leonardo (Villa Costanza - Careggi) and T2 Vespucci
# (Aeroporto - Unità). T1 runs on into Scandicci, so its four stops there are
# drawn but not ringed (owner, call 17). The T3 and T4 relations are under
# construction with no stops (filled from the fetch).
ROUTE = "tram"
OPERATOR = None
LINE_REFS = ("T1", "T2")
# Under construction, with track and no stops in OSM (owner, call: T3 not drawn
# until it opens). T3.2.1 Libertà - Bagno a Ripoli is due to open about January
# 2027 (Comune di Firenze; read 2026-09-30). Re-check when it opens.
_BUILDING = "under construction, no stops in OSM; not drawn until it opens (owner)"
NOT_DRAWN = {
    18624687: "T3.2.1 Libertà - Bagno a Ripoli: " + _BUILDING,
    18624725: "T3.2.1 Bagno a Ripoli - Libertà: " + _BUILDING,
    18649601: "T3.2.2 Libertà - Rovezzano (no ref): " + _BUILDING,
    18649602: "T3.2.2 Rovezzano - Libertà (no ref): " + _BUILDING,
    18621862: "T4 Firenze - Le Piagge: " + _BUILDING,
    18622253: "T4 Le Piagge - Firenze: " + _BUILDING,
    18651301: "T2.2 Aeroporto - Sesto Fiorentino: " + _BUILDING,
    18651302: "T2.2 Sesto Fiorentino - Aeroporto: " + _BUILDING,
}
STATION_ADD = {}
EXPECTED_IN_COMUNE = 39
EXPECTED_OUTSIDE = 4

# Gate 3: GEST's own stop counts per line, the whole line before the comune
# split (T1's four Scandicci stops included). Step 1 stops on a mismatch.
#   T1 Villa Costanza - Careggi: 26 stops.
#   T2 Peretola Aeroporto - San Marco Università: 20 stops. GEST's diagram also
#      shows Unità, greyed out: the Comune closed it to regular service on
#      2 January 2025, first and last runs only. It is not drawn, so it is not
#      counted (secondary sources that say 21 include it).
OPERATOR_STATION_COUNTS = {"T1": 26, "T2": 20}
OPERATOR_COUNTS_SOURCE = (
    "GEST's stop diagram 'Sinottico fermate' on its Linee page, "
    "https://www.gestramvia.it/linee/ (image wp-content/uploads/2025/01/"
    "Sinottico-fermate-1.png), read 2026-10-01; Unità's closure from the Comune di "
    "Firenze, 'Linea 2 della tramvia, tratto Fortezza-San Marco' (16 Jan 2025). "
    "Cross-checked against it.wikipedia 'Rete tranviaria di Firenze' (secondary).")

SPACING_MIN_M = 100.0

DRAWN_LINES = ("T1", "T2")
LINE_NAMES = {"T1": "T1 Leonardo", "T2": "T2 Vespucci"}
# OSM's own colours (the brief).
LINE_COLOURS = {"T1": "#254395", "T2": "#5d3988"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "florence_attivita"
RAW_CLASSIFICATION_COLUMN = "tipologiaattivita"

# Sanity bounds for the placed points: the comune plus a margin.
FLORENCE_BBOX = {
    "lat_min": 43.70,
    "lat_max": 43.85,
    "lon_min": 11.13,
    "lon_max": 11.35,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600042602)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("it",)
PLACE_FOLD = None
PLACE_REVIEWED = {}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "node/7325281962": "a library with no article of its own (owner, 2026-10-13)",
    "way/179792589": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281960": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281959": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281958": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281955": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281954": "a library with no article of its own (owner, 2026-10-13)",
    "node/8931185320": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281953": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281951": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281950": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281949": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281948": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281947": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281946": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281945": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281944": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281942": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281941": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281940": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281937": "a library with no article of its own (owner, 2026-10-13)",
    "way/134663645": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281936": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281935": "a library with no article of its own (owner, 2026-10-13)",
    "node/3676426335": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281934": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281931": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281930": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281929": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281928": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281926": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281925": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281932": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281923": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281922": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281920": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281919": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281918": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281916": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281915": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281914": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281913": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281912": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281909": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281908": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281910": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281907": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281906": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281905": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281904": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281903": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281902": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281901": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281900": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281897": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281895": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281894": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281892": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281891": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281890": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281889": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281888": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281887": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281886": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281884": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281885": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281883": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281882": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281880": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281879": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281878": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281877": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281876": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281874": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281873": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281872": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281871": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281870": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281869": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281868": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281867": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281866": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281865": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281864": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281863": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281862": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281861": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281860": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281859": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281858": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281856": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281855": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281854": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281853": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281851": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281850": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281849": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281848": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281847": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281846": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281845": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281843": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281899": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281842": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281841": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281840": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281839": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281838": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281836": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281835": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281834": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281833": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281832": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281831": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281830": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281828": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281826": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281825": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281824": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281823": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281819": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281818": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281817": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281816": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281815": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281814": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281813": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281812": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281811": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281810": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281809": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281808": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281807": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281806": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281805": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281803": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281802": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281801": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281800": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281799": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281798": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281797": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281796": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281795": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281794": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281793": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281792": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281791": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281790": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281789": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281786": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325281785": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280184": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280183": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280180": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280179": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280178": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280176": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280175": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280174": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280172": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280171": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280169": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280168": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280167": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280166": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280165": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280164": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280163": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280162": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280160": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280159": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280158": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280157": "a library with no article of its own (owner, 2026-10-13)",
    "way/1253418328": "a library with no article of its own (owner, 2026-10-13)",
    "way/82646719": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280155": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280154": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280152": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280151": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280149": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280147": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280145": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280144": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280143": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280142": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280141": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280139": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280138": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280137": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280136": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280135": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280133": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280131": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280130": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280128": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280127": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280125": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280124": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280123": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280126": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280122": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280121": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280120": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280117": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280116": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280115": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280114": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280113": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280112": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280111": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280110": "a library with no article of its own (owner, 2026-10-13)",
    "node/7325280109": "a library with no article of its own (owner, 2026-10-13)",
    "node/9687617360": "a freight yard, depot or operating point, not a passenger station (owner, 2026-10-13)",
    "way/1455775297": "a lane named for its mode (owner, 2026-10-13)",
    "way/1455775298": "a lane named for its mode (owner, 2026-10-13)",
    "way/192460803": "a lane named for its mode (owner, 2026-10-13)",
    "way/116487203": "a lane named for its mode (owner, 2026-10-13)",
    "way/162782248": "a lane named for its mode (owner, 2026-10-13)",
    "way/31101494": "a lane named for its mode (owner, 2026-10-13)",
    "way/583788623": "a lane named for its mode (owner, 2026-10-13)",
    "way/595068335": "a lane named for its mode (owner, 2026-10-13)",
    "way/900303357": "a lane named for its mode (owner, 2026-10-13)",
    "way/900303358": "a lane named for its mode (owner, 2026-10-13)",
    "way/1386997977": "a lane named for its mode (owner, 2026-10-13)",
    "way/779503329": "a lane named for its mode (owner, 2026-10-13)",
    "way/1198307081": "a lane named for its mode (owner, 2026-10-13)",
    "way/1201694730": "a lane named for its mode (owner, 2026-10-13)",
    "way/1201694731": "a lane named for its mode (owner, 2026-10-13)",
    "way/1310486871": "a lane named for its mode (owner, 2026-10-13)",
    "way/620127564": "a lane named for its mode (owner, 2026-10-13)",
    "way/890241171": "a lane named for its mode (owner, 2026-10-13)",
    "way/939389473": "a lane named for its mode (owner, 2026-10-13)",
    "way/942741443": "a lane named for its mode (owner, 2026-10-13)",
    "way/942741444": "a lane named for its mode (owner, 2026-10-13)",
    "way/953572027": "a lane named for its mode (owner, 2026-10-13)",
    "way/953572028": "a lane named for its mode (owner, 2026-10-13)",
    "way/953572029": "a lane named for its mode (owner, 2026-10-13)",
    "way/953572030": "a lane named for its mode (owner, 2026-10-13)",
    "way/1198307077": "a lane named for its mode (owner, 2026-10-13)",
    "way/1534919065": "a lane named for its mode (owner, 2026-10-13)",
    "way/623794860": "a lane named for its mode (owner, 2026-10-13)",
    "way/422288184": "a lane named for its mode (owner, 2026-10-13)",
    "way/623794868": "a lane named for its mode (owner, 2026-10-13)",
    "way/620127562": "a lane named for its mode (owner, 2026-10-13)",
    "way/422515715": "a lane named for its mode (owner, 2026-10-13)",
    "way/623794867": "a lane named for its mode (owner, 2026-10-13)",
    "way/637497276": "a lane named for its mode (owner, 2026-10-13)",
    "way/637497278": "a lane named for its mode (owner, 2026-10-13)",
    "way/953570011": "a lane named for its mode (owner, 2026-10-13)",
    "way/953570012": "a lane named for its mode (owner, 2026-10-13)",
    "way/953570013": "a lane named for its mode (owner, 2026-10-13)",
    "way/953570014": "a lane named for its mode (owner, 2026-10-13)",
    "way/1207855202": "a lane named for its mode (owner, 2026-10-13)",
    "way/419950205": "a lane named for its mode (owner, 2026-10-13)",
    "way/993483636": "a lane named for its mode (owner, 2026-10-13)",
    "way/799784923": "a lane named for its mode (owner, 2026-10-13)",
    "way/870882759": "a dog-training club tagged a park",
    "way/472637048": "a farmhouse ruin with no article",
    "way/478064678": "a description standing in for a name",
    "node/8669023184": "a memorial stone's inscription standing in for a name, no article",
    "node/7959956070": "a duplicate row: the same synagogue as way/102979678",
    "node/4713726602": "public art whose Wikipedia link is another subject's article, none of its own",
    "way/1444307352": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444315433": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307356": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307435": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307437": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307354": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307355": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1087438300": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1442609718": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307353": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307439": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444315434": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307438": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/912178164": "a path's variant marked in the name, a description: no street name",
    "way/680667747": "a list of house numbers standing in for a name",
    "way/637311392": "a glitched name: a mistyped street word (Vie for Via)",
}
