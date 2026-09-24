"""Rome-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Italy's second city and nothing like its first: Milan reads six premises
registers from its own portal, Rome ONE - Roma Capitale's SUAP register of
productive activities, which records premises by the city's own street code
and civic number with no coordinates - JOINED to ANNCSU, Italy's national
house-number archive, which carries the same street code with WGS84 points.
No geocoder. Brief: docs/build_briefs/rome.md.
"""

from pathlib import Path

SLUG = "rome"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "rome" / "raw"
DATA_PROCESSED = ROOT / "data" / "rome" / "processed"
OUTPUTS = ROOT / "outputs" / "rome"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

SUAP_CSV = DATA_RAW / "opendata_suap_luglio_2025.csv"
ANNCSU_ZIP = DATA_RAW / "indirizzario_lazio.zip"
GTFS_ZIP = DATA_RAW / "rome_static_gtfs.zip"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
OSM_RAIL_JSON = DATA_RAW / "osm_rail.json"
OSM_NEIGHBOURS_JSON = DATA_RAW / "osm_neighbour_comuni.json"
OSM_FOOD_JSON = DATA_RAW / "osm_food_control.json"

# --- Endpoints ---------------------------------------------------------------

# SUAP's "Elenco delle attività produttive", monthly files; JULY 2025 IS THE
# NEWEST and no 2026 dataset exists (brief, measured 2026-09-24).
SUAP_URL = ("https://dati.comune.roma.it/catalog/it/dataset/94848d96-0197-486b-b143-485f00285928/"
            "resource/3fc5fd67-6ed5-428a-88c4-cf5245f9ec0f/download/opendata_suap_luglio_2025.csv")
# ANNCSU's Lazio address list. It refuses HEAD (403) and answers GET; the
# file inside names its own date (indirizzarioLazio<yyyymmdd>.csv).
ANNCSU_URL = "https://anncsu.open.agenziaentrate.gov.it/age-inspire/opendata/anncsu/getds.php?INDIR_LAZI"
GTFS_URL = "https://romamobilita.it/sites/default/files/rome_static_gtfs.zip"

# --- Scope ---------------------------------------------------------------------

ISTAT_COMUNE = "058091"
# OSM relation 41485, "Roma", admin_level 8, ref:ISTAT 058091 - a bounded
# name search's only candidate. The comune is 1,287 km² and includes Ostia.
OSM_BOUNDARY_RELATION = 41485
BOUNDARY_AREA_KM2 = (1250, 1320)

# The comune runs from Ostia (41.7 N) to Cesano (42.1 N); padded slightly.
ROME_BBOX = {"lat_min": 41.60, "lat_max": 42.18, "lon_min": 12.20, "lon_max": 12.90}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 33N: longitude ~12.49 falls in the 12-18 E band. Derived per city.
CRS_PROJECTED = "EPSG:32633"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail ------------------------------------------------------------------------
#
# THE RAIL SOURCE IS OPENSTREETMAP, on a recorded ground (osm-rail's order is
# agency GIS layers, then agency GTFS, then OSM) - PUT TO THE OWNER 2026-09-24:
#   * Roma Mobilità's static GTFS is AMBIGUOUS IN A WAY THAT MATTERS
#     (`licence-read`, 2026-09-24): its own open-data page says the data "possono
#     essere utilizzati ... esclusivamente a titolo di supporto al viaggio" (only
#     as travel support) and reserves action against "utilizzo improprio", and
#     the one file carries five inconsistent licence declarations - CC BY-SA
#     with no version, "Licenza Sconosciuta", CC BY 4.0 by harvest. Not
#     resolved in the project's favour; not used.
#   * RSM's own ArcGIS metro layers are CC BY 4.0 but last edited 2023-05-19:
#     Metro C stops at San Giovanni, missing Porta Metronia and Colosseo - Fori
#     Imperiali (opened 2025-12-16).
#   * OSM (ODbL, notice 1) carries all four lines to the current termini.
RAIL_SOURCE_GROUND = "agency GTFS terms ambiguous; agency GIS layers stale (Metro C)"

# OSM relation ids, both directions per line. B1 is tagged ref "B" in OSM (its
# relations end at Jonio), so lines are keyed on RELATION IDS, never on ref.
LINE_RELATIONS = {
    "A": (207973, 1720955),
    "B": (207926, 1720959),
    "B1": (2172804, 2172805),
    "C": (398053, 2172845),
}
LINE_ORDER = ("A", "B", "B1", "C")
LINE_NAMES = {"A": "Metro A", "B": "Metro B", "B1": "Metro B1", "C": "Metro C"}
# Left out, by default and PUT TO THE OWNER: Metromare (the Roma-Lido railway,
# COTRAL, tagged route=subway in OSM - 208013/1721156) and the Roma-Viterbo
# urban service (COTRAL, light_rail - 387417/1721478): regional railways
# under the commuter-rail rule until the owner says otherwise. Always out:
# OSM's "Metro D" (2703073, a line not yet built - no stops) and Palestrina's
# scala mobile.
LEFT_OUT_RELATIONS = {208013: "Metromare", 1721156: "Metromare",
                      387417: "Roma-Viterbo (urban)", 1721478: "Roma-Viterbo (urban)",
                      2703073: "Metro D (not built)", 2581270: "Palestrina escalator",
                      2581271: "Palestrina escalator"}

# OSM's colours, ATAC's brand colours (A orange, B blue, C green). B and B1
# share one blue, and this project's check refuses two lines under Delta-E
# 10, so B1 moves in HSL lightness only by the smallest step that clears 13 -
# Amsterdam's and Oslo's rule: #3783C6 -> #629ed3 (L +0.11), 13.7 from B.
LINE_COLOURS = {"A": "#F68B1F", "B": "#3783C6", "B1": "#629ed3", "C": "#008751"}

# Step 1 writes the kept relations here for step 3, with B1 relabelled and cut
# to its OWN ways (Bologna to Jonio): OSM tags it ref "B", and its relations
# run the whole trunk to Laurentina, which would lay B1 on top of B.
OSM_LINES_JSON = DATA_PROCESSED / "osm_lines.json"

# One interchange under two names: ATAC's Colosseo (B) and Colosseo - Fori
# Imperiali (C), connected underground. Wikipedia's 74 stations network-wide
# counts it once.
STATION_NAME_ALIASES = {"Colosseo – Fori Imperiali": "Colosseo"}

# Gate 3: English Wikipedia's "Rome Metro" (read 2026-09-24, SECONDARY): A 27,
# B 26 including B1's four, C 24, network 74.
OPERATOR_STATION_COUNTS = {"Metro A": 27, "Metro B + B1": 26, "Metro C": 24,
                           "Metro (network)": 74}
OPERATOR_COUNTS_SOURCE = ("en.wikipedia.org/wiki/Rome_Metro, read 2026-09-24 - secondary; "
                          "A 27, B 26 (with B1), C 24, network 74")
SPACING_MIN_M = 400.0
COLLAPSE_MAX_SPREAD_M = 400

# --- Business filtering ------------------------------------------------------

TAXONOMY_SYSTEM = "rome_suap"
RAW_CLASSIFICATION_COLUMN = "activity"
CITY_KEEP = "ROMA"   # kept for the scaffold's templates; the register is Roma Capitale's own
