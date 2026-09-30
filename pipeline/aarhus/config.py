"""Aarhus-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

SECOND DANISH CITY, on Copenhagen's national modules: CVR's six-file join,
the columns never to load and the sole-trader guard live in
`pipeline/countries/denmark.py` and `denmark_register.py`. What is Aarhus's
own is below: the kommune, the 20-station scope and its halved rings, the
palette, the catch-all verdict - and the PLACEMENT, which is not
Copenhagen's (OSM's DAR address points, keyless, instead of Datafordeler's
per-kommune Adressepunkt file).
"""

from pathlib import Path

SLUG = "aarhus"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "aarhus" / "raw"
DATA_PROCESSED = ROOT / "data" / "aarhus" / "processed"
OUTPUTS = ROOT / "outputs" / "aarhus"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Letbane stations left out, each with its kommune or the reason it is out of
# scope - a citable scoping record (the Los Angeles rule).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# L2 cut to the new tramway by step 1, read by step 3 (Madrid's GeoJSON path).
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# Raw inputs. `fetch_sources.py` downloads them, keyless, from OpenStreetMap;
# no step may fetch. CVR and DAR are the national caches Copenhagen fetched
# (`denmark.SHARED_RAW`), read here and NEVER refreshed by this city: a new
# generation would change Copenhagen's inputs too.
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_KOMMUNER_JSON = DATA_RAW / "osm_kommuner.json"
# OSM's imported Danish address points: (osm id, lat, lon, osak:identifier),
# Overpass CSV. `osak:identifier` IS the DAR Husnummer id (DECISIONS
# 2026-09-27; central-Copenhagen control, median 0.03 m from DAR's own point).
OSM_ADDRESS_POINTS_TSV = DATA_RAW / "osm_osak_points.tsv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Scope: ONE kommune ------------------------------------------------------
#
# Aarhus Kommune, 751 (OSM relation 1784663, 471.2 km2). The business filter is
# CVR's own `CVRAdresse_kommunekode` on the location address, never a polygon;
# the polygon decides only which stations are in the kommune.
KOMMUNER = {"751": "Aarhus"}                 # CVR's unpadded code
OSM_KOMMUNE_RELATION = 1784663

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# ETRS89 / UTM 32N. Aarhus (~10.21 E) is in zone 32 (6-12 E) - derived per
# city, and NOT Copenhagen's 25833. It happens to be DAR's national CRS too.
CRS_PROJECTED = "EPSG:25832"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the 20 in-scope stations' 499 m median gap (brief, 2026-09-29;
# owner confirmed). The halved edges were taken where the median was 341-541
# m (Marseille, Oslo, Lille, Toulouse, Rennes); the shared 0.6 mi outer ring
# would swallow three or four neighbours here. Step 1 prints the median again.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope: THE NEW CITY TRAMWAY, 20 STATIONS ----------------------
#
# ✅ Owner, confirmed 2026-09-29. The Letbane in Aarhus Kommune is three
# pieces of track (41 OSM stop names, 39 stations after the two aliases):
#
#   the new city tramway, Aarhus H - Nørreport - Universitetet - Skejby -
#     Lisbjerg - Lystrup, and L2's Lisbjergskolen branch     20   purpose-built, 2017
#   Odderbanen, Kongsvang - Malling                          12   converted railway
#   Grenaabanen, Østbanetorvet - Løgten                       7   converted railway
#
# THE LIGHT-RAIL TEST MAKES FREQUENCY A GATE ON CONVERTED RAILWAY: 15 min or
# better by day, at the median stop's worst daytime hour (owner, 2026-09-29).
# Read 2026-09-29 from MIDTTRAFIK'S OWN published timetables, weekdays -
# L2 `l2_k26_20261009-20270403_normal-ua.pdf` (the normal plan from 9 October
# 2026) and L1 `l1_k26_20260925-20270320_helaar-ua.pdf` (the year plan from
# 25 September 2026), both linked from midttrafik.dk/rejsemuligheder/:
#
#   new tramway   Aarhus H northbound every 7-8 min              passes
#   Odderbanen    every 30 min; the Mårslet extras run through
#                 the intermediate stops without stopping          fails
#   Grenaabanen   every 30 min (Aarhus H x.18, x.48)              fails
#
# So the two converted railways' 19 stations are NOT counted and their track is
# NOT drawn; each is named in excluded_stations.csv with that reason. Stations
# are named per section below, and step 1 EXITS unless the three sections
# partition the kommune's stations exactly - a new stop, a renamed one or a
# station moved between sections is a scope question, not a config edit.
NEW_TRAMWAY = (
    "Aarhus H", "Dokk1", "Skolebakken", "Nørreport", "Universitetsparken",
    "Aarhus Universitet (Ringgaden)", "Stjernepladsen", "Stockholmsgade",
    "Vandtårnet (Ringvejen)", "Nehrus Allé", "Olof Palmes Allé",
    "Universitetshospitalet", "Gl. Skejby", "Humlehuse", "Klokhøjen",
    "Lisbjerg Bygade", "Lisbjerg-Terp", "Nye", "Lystrup", "Lisbjergskolen",
)
ODDERBANEN = (
    "Kongsvang", "Viby J", "Rosenhøj", "Øllegårdsvej", "Gunnar Clausens Vej",
    "Tranbjerg", "Nørrevænget", "Mølleparken", "Mårslet", "Vilhelmsborg",
    "Beder", "Malling",
)
GRENAABANEN = (
    "Østbanetorvet", "Risskov Strandpark", "Vestre Strandalle", "Torsøvej",
    "Hjortshøj", "Skødstrup", "Løgten",
)
SECTION_REASONS = {
    "Odderbanen": ("Odderbanen, converted railway: every 30 min by day at the "
                   "section's stops (Midttrafik's L2 timetable, read 2026-09-29), "
                   "under the 15-minute light-rail test"),
    "Grenaabanen": ("Grenaabanen, converted railway: every 30 min by day "
                    "(Midttrafik's L1 timetable, read 2026-09-29), under the "
                    "15-minute light-rail test"),
}

# One stop under two names: the two directions' stop nodes are spelled
# differently in OSM. Explicit, never a rule (Oslo's) - each was looked at.
STATION_NAME_ALIASES = {
    "G. Clausens Vej": "Gunnar Clausens Vej",
    "Lisbjerg - Terp": "Lisbjerg-Terp",
}

# A WHITELIST ON THREE TAGS - ref, route and operator - never `network`
# alone (Copenhagen's rule). All six relations: route=light_rail,
# operator=Keolis, network=Midttrafik, refs L1 and L2.
ROUTE = "light_rail"
OPERATOR = "Keolis"
LINE_REFS = ("L1", "L2")

# DRAWN: L2 only, cut to the new tramway (Aarhus H northward, and its
# Lisbjergskolen branch). L1's only in-scope track is the Aarhus H - Skolebakken
# stretch it shares with L2; the rest of it is Grenaabanen, out of scope, so
# L1 is not drawn, and its four in-scope stations (Aarhus H, Dokk1,
# Skolebakken, Lystrup) carry both lines in stations.csv. Step 3 cuts L2 at
# Aarhus H.
DRAWN_LINES = ("L2",)
# The name riders use, with the mode word, as Copenhagen's "S-tog A". OSM
# says "Light rail L2"; riders say Letbanen.
LINE_NAMES = {"L2": "Letbane L2"}
# All six relations carry #30556E. One line is drawn, so it keeps OSM's
# colour; render_heatmap's shared check (pipeline/linecolour.py) scores it.
LINE_COLOURS = {"L2": "#30556E"}

SPACING_MIN_M = 400.0

# GATE 3 - NOT RUN, recorded as such (Bergen's precedent). No operator
# publishes a count for the new-tramway section on its own. Step 1 asserts
# instead that the three section lists partition exactly what OSM carries in
# the kommune, which is the check this scope needs.
OPERATOR_STATION_COUNTS = {}
OPERATOR_COUNTS_SOURCE = ""

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "denmark_db25"
RAW_CLASSIFICATION_COLUMN = "db25_label"
CITY_KEEP = "AARHUS"   # kept for the scaffold's templates; KOMMUNER filters

# Where the Husnummer's point comes from - see pipeline/countries/denmark.py.
PLACEMENT = "osm_osak"

# The per-city catch-all verdict, on Aarhus's own numbers (the screen,
# 2026-09-27, CVR generation 505): 969900 "Andre personlige serviceydelser
# i.a.n." is 165 rows (3.0%), personally owned 78% against 45% overall -
# Copenhagen's and Oslo's home-based signature, dropped as there. The six
# retail catch-alls and 561190 are kept, as in Copenhagen. Step 2 prints the
# figures again.
CATCH_ALL_EXCLUDE = ("969900",)

# Sanity bounds: Aarhus Kommune's OSM polygon (relation 1784663) plus ~0.02
# deg. A corrupt coordinate is caught; the join does the placing.
AARHUS_BBOX = {
    "lat_min": 55.98,
    "lat_max": 56.34,
    "lon_min": 9.93,
    "lon_max": 10.43,
}
