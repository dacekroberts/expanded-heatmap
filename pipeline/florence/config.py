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
