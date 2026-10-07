"""Geneva (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/geneva.md). Switzerland's second city: Zurich's tram leg
(the shared `pipeline/osm_tram.py`, LV95, the Gemeinde polygons from OSM)
with a new business leg, the canton's business register (REG, SITG Level A),
classified by `pipeline/taxonomies/geneva_noga.py`. Regional scope: the 12
Swiss communes TPG's trams serve (owner, 2026-10-04).
"""

from pathlib import Path

SLUG = "geneva"
# What the brief's checks compare with (`brief_check.py geneva --vs-config`).
MAP_MODE = "tram"
MAP_COVERAGE = "full"
SCOPE = "regional"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "geneva" / "raw"
DATA_PROCESSED = ROOT / "data" / "geneva" / "processed"
OUTPUTS = ROOT / "outputs" / "geneva"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stops of drawn lines outside the 12 communes (tram 17's French end):
# drawn, not ringed, listed with the commune each lies in.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- The register (fetch_sources.py downloads; no step fetches) --------------
#
# Répertoire des entreprises du canton de Genève (REG), SITG dataset
# REG_ENTREPRISE_ETABLISSEMENT, contributor OCIRT; SITG Level A "Accès libre"
# (licence-read 2026-10-04; the narrow indemnity accepted by the owner the
# same day). The CSV zip, UTF-8 with BOM, ";", 35 fields, LV95 E/N on every
# row. Daily; the build uses one dated extract and the page states its date.
REG_URL = "https://ge.ch/sitg/geodata/SITG/OPENDATA/REG_ENTREPRISE_ETABLISSEMENT-CSV.zip"
REG_ZIP = DATA_RAW / "REG_ENTREPRISE_ETABLISSEMENT-CSV.zip"
REG_MEMBER = "REG_ENTREPRISE_ETABLISSEMENT.csv"
REG_DATE_MEMBER = "DOC/Informations_date.txt"
REG_CONDITIONS_URL = "https://sitg.ge.ch/ressources/conditions-utilisation-donnees"
REG_DATASET_PAGE = "https://sitg.ge.ch/donnees/reg-entreprise-etablissement"
# 100,588 rows on 2026-10-04; a file far below it is a failed fetch.
REG_MIN_ROWS = 90_000
# The columns step 2 reads, by exact name. The phone, fax, e-mail and legal-
# name columns are never written to processed/ (the brief); RAISON_SOCIALE is
# read in memory ONLY to test whether a sole trader's trade name is their own
# name (the owner's call 2, 2026-10-04), and is then dropped.
REG_COLUMNS = ("TYPE_REG", "ID_ETABLISSEMENT", "ID_ENTREPRISE", "NOM", "STATUT_REG",
               "TYPE_LOCAL", "CODE_NOGA", "BRANCHE", "PHYS_RUE", "PHYS_NUMRUE",
               "PHYS_NPA", "PHYS_LOCALITE", "PHYS_COMMUNE", "NATURE_JURID",
               "RAISON_SOCIALE", "E", "N")
# Records: establishment rows only (the brief). Company rows with no
# establishment row are left out and disclosed (owner, call 1, 2026-10-04).
RECORD_TYPE = "Etablissement"
# Premises types dropped before classification: home-based and itinerant
# (the brief) and market stands (owner, call 3, 2026-10-04: R1 and the
# mobile-units row).
DROP_PREMISES = ("Activité à domicile", "Activité itinérante", "Stand ambulant")
SOLE_TRADER = "Entreprise individuelle"

# --- OpenStreetMap: one query for the city (osm-rail) ------------------------

# S, W, N, E: the five lines with tram 17's French end (Annemasse) and
# tram 14's Bernex end, plus a margin.
RAIL_BBOX = (46.15, 6.03, 46.25, 6.26)
OSM_ALL_JSON = DATA_RAW / "osm_all.json"
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_COMMUNES_JSON = DATA_RAW / "osm_communes.json"
BFS_TAG = "swisstopo:BFS_NUMMER"
# The 12 Swiss communes the trams serve (the brief's TPG stop table), by
# swisstopo's BFS number as OSM tags it, with the names step 1 checks.
COMMUNES = {
    "6621": "Genève", "6628": "Lancy", "6630": "Meyrin", "6608": "Carouge",
    "6607": "Bernex", "6643": "Vernier", "6633": "Plan-les-Ouates",
    "6612": "Chêne-Bougeries", "6613": "Chêne-Bourg", "6640": "Thônex",
    "6631": "Onex", "6618": "Confignon",
}
# Their summed area, 77.0 km2 measured 2026-10-07; a polygon that fails to
# close moves it.
REGION_AREA_KM2 = (74.0, 80.0)
# The register's PHYS_COMMUNE labels for the same 12 (the Ville appears as
# five), cross-checked against the polygons in step 2.
REG_COMMUNE_LABELS = {
    "Genève", "Genève-Cité", "Genève-Eaux-Vives", "Genève-Petit-Saconnex",
    "Genève-Plainpalais", "Lancy", "Meyrin", "Carouge", "Bernex", "Vernier",
    "Plan-les-Ouates", "Chêne-Bougeries", "Chêne-Bourg", "Thônex", "Onex", "Confignon",
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# CH1903+ / LV95, in metres: the register's E/N are already in it (Zurich's
# precedent; the tram-city skill, section 3). The derived UTM zone would be
# 32N (EPSG:32632).
CRS_PROJECTED = "EPSG:2056"
CRS_REGISTER = "EPSG:2056"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
# HALVED: the median nearest-neighbour gap among the 81 in-scope stops is
# 330 m (measured 2026-10-07; the spacing rule's line is about 550 m). Step 1
# stops outside 290-370 m.
MEDIAN_GAP_BOUNDS_M = (290.0, 370.0)

# --- Station scope: TPG's five trams, every stop in the 12 communes -----------

ROUTES = ("tram", "light_rail")
OPERATOR = None
LINE_REFS = ("12", "14", "15", "17", "18")
NOT_DRAWN = {}
STATION_ADD = {}
NAME_ALIASES = {}
# OSM names many of Geneva's stop positions with TPG's platform letter,
# "Bel-Air (A)", "Bel-Air (B)": one stop, two names, so the collapse counted
# it twice (gate 3 caught it: 102 stations against TPG's 85, 30 pairs within
# 40 m, 2026-10-07). Step 1 strips a trailing platform letter before the
# collapse, which then merges by name within MAX_SPREAD_M as usual; TPG's line
# pages name each stop once. osm_tram's NAME_ALIASES cannot do it, since it
# requires the target spelling to be present and here none is. The stops it
# applies to are listed, and step 1 stops if the list and OSM disagree (a
# letter added or fixed in OSM), so a stale fold cannot outlive the gap.
PLATFORM_LETTER_STOPS = {
    "Acacias", "Avanchets-Étang", "Balexert", "Bel-Air", "Bois-du-Lan", "Coutance",
    "Forumeyrin", "Gare Cornavin", "Industrielle", "Jardin-Alpin-Vivarium",
    "Meyrin-Village", "Place de Neuve", "Plainpalais", "Uni-Mail",
}
# The build of 2026-10-07: 85 stops, 81 in the 12 communes, tram 17's 4 in
# France (Gaillard 2, Ambilly 1, Annemasse 1), the brief's figures exactly.
EXPECTED_IN_SCOPE = 81
EXPECTED_OUTSIDE = 4
# Gate 3: TPG's own line pages, both directions, distinct stop names, the
# whole line before the scope split (tram 17's French stops included).
OPERATOR_STATION_COUNTS = {"12": 25, "14": 30, "15": 22, "17": 26, "18": 31}
OPERATOR_COUNTS_SOURCE = (
    "TPG (Transports publics genevois), line pages https://www.tpg.ch/fr/lignes/<n>, "
    "both directions, distinct stop names; timetable valid 2025-12-14 to 2026-12-12; "
    "read 2026-10-04 (the brief).")
SPACING_MIN_M = 80.0
MAX_SPREAD_M = 200
DRAWN_LINES = LINE_REFS
LINE_NAMES = {ref: f"Tram {ref}" for ref in LINE_REFS}
# TPG's colours as OSM tags them on both relations of each line (read
# 2026-10-07); step 3 asserts they are still OSM's and pipeline/linecolour.py
# measures them against the pins.
OSM_COLOURS = {"12": "#F5A300", "14": "#5A1E82", "15": "#84471C", "17": "#00ACE7",
               "18": "#B82F89"}
LINE_COLOURS = dict(OSM_COLOURS)

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "geneva_noga"
RAW_CLASSIFICATION_COLUMN = "activity_label"
