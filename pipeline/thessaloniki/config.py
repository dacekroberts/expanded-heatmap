"""Thessaloniki-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/thessaloniki.md, 6/6 checks, owner calls 1-8 answered
2026-10-04). Greece's first city.

The business leg is the City of Thessaloniki's active-shop-licence layer
(GeoServer WFS, CC BY 4.0 on data.gov.gr): a point and a licensed activity on
every row, no name field, so a dot shows its activity (Florence's no-name
precedent; pipeline/taxonomies/thessaloniki_adeies.py). Three layers, Food
service, Food shops and Personal services, Matsuyama's shape. Rail from
OpenStreetMap (osm-rail): no GTFS was probed, and the operator publishes none
on its site.
"""

from pathlib import Path

SLUG = "thessaloniki"

# The macro map's two keys and the scope (the brief's checks compare these).
MAP_MODE = "metro"
MAP_COVERAGE = "narrowed"
SCOPE = "city"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "thessaloniki" / "raw"
DATA_PROCESSED = ROOT / "data" / "thessaloniki" / "processed"
OUTPUTS = ROOT / "outputs" / "thessaloniki"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Line 1's five Kalamaria-branch stations, outside the city (owner,
# 2026-10-04): not drawn, not ringed, listed with the municipality each lies in.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- The business layer (fetch_sources.py; no step fetches) -----------------

# Ενεργές Άδειες Καταστημάτων, the City's point layer of shops holding an
# active licence. ONLY from sdi.thessaloniki.gr's GeoServer, never the copy on
# maps.thessaloniki.gr, whose portal splash forbids redistribution (owner,
# 2026-10-04). One WFS 2.0.0 GetFeature returns every row; fetch_sources.py
# refuses an answer whose numberReturned is under numberMatched.
WFS_ENDPOINT = "https://sdi.thessaloniki.gr/geoserver/wfs"
WFS_TYPENAME = "saloniki:tsp_poi_energes_adeies_katastimaton"
WFS_URL = (f"{WFS_ENDPOINT}?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature"
           f"&TYPENAMES={WFS_TYPENAME}&OUTPUTFORMAT=application/json&SORTBY=gid")
DATASET_PAGE = ("https://data.gov.gr/dataset/"
                "gis-thessaloniki-wms-saloniki-tsp_poi_energes_adeies_katastimaton")
LICENCE_URL = "https://creativecommons.org/licenses/by/4.0/"
LICENCES_GEOJSON = DATA_RAW / "tsp_poi_energes_adeies_katastimaton.geojson"
LICENCES_META = DATA_RAW / "tsp_poi_energes_adeies_katastimaton.geojson.json"
# 8,103 rows on 2026-10-04; the brief check fails outside 8,100-8,199.
LICENCES_ROWS = (8100, 8199)
# The layer serves EPSG:2100 (GGRS87 / Greek Grid), in the GeoJSON's own `crs`
# member; reprojected on read. pyproj's always_xy order for 2100 is (x east,
# y north), which is also the GeoJSON's coordinate order (the layer's own `x`
# and `y` fields agree on every row that carries them).
LAYER_CRS = "EPSG:2100"
# The only fields step 2 reads. NEVER read into processed/: address, street,
# number, zip, city (the brief's privacy list).
LAYER_FIELDS = ("kodikos_katasthmatos", "antikeimeno", "dimotiki_koinotita")
# The six community labels; every row with an activity carries one.
COMMUNITIES = ("Α' ΔΗΜΟΤΙΚΗ ΚΟΙΝΟΤΗΤΑ", "Β' ΔΗΜΟΤΙΚΗ ΚΟΙΝΟΤΗΤΑ", "Γ' ΔΗΜΟΤΙΚΗ ΚΟΙΝΟΤΗΤΑ",
               "Δ' ΔΗΜΟΤΙΚΗ ΚΟΙΝΟΤΗΤΑ", "Ε' ΔΗΜΟΤΙΚΗ ΚΟΙΝΟΤΗΤΑ", "ΔΗΜΟΤΙΚΗ ΕΝΟΤΗΤΑ ΤΡΙΑΝΔΡΙΑΣ")

# --- OpenStreetMap (fetch_sources.py; ONE query for the city) ---------------

# The whole of Line 1, Mikra included, and the municipalities around the city.
OSM_BBOX = (40.54, 22.87, 40.68, 23.02)          # S, W, N, E
OSM_ALL_JSON = DATA_RAW / "osm_all.json"
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundaries.json"
# Municipalities (δήμοι) are admin_level 7 in Greek OSM and municipal units
# 8; both are fetched, so step 1 can name where an outside station lies.
BOUNDARY_ADMIN_LEVELS = ("7", "8")
# Δήμος Θεσσαλονίκης, the municipality (its five communities and Triandria).
# Official area 19.307 km2 (ELSTAT); OSM's relation 1770680 measures 20.82
# km2 in EPSG:32634 (2026-10-07). Step 1 stops outside this range. Nomarchia
# station's stop positions sit 4 m outside its line (in Kalamaria) and Nea
# Elvetia's 289 m inside it: the polygon decides both, as owner call 6 set.
BOUNDARY_NAME = "Δήμος Θεσσαλονίκης"
BOUNDARY_ADMIN_LEVEL = "7"
BOUNDARY_RELATION = 1770680
BOUNDARY_AREA_KM2 = (17.5, 21.5)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 34N: the longitude (~22.94) falls in the 18 to 24 band. Derived per
# city, not copied - see docs/project_context.md's CRS lesson. Not EPSG:2100:
# check_provenance.py's CRS invariant accepts UTM zones and its listed
# national grids only; both are metric and their scale error here is under
# 0.03% (the brief).
CRS_PROJECTED = "EPSG:32634"

# --- Ring geometry ---------------------------------------------------------
# THE SHARED EDGES: the 13 in-city stations' median nearest-station gap is
# 573 m (step 1, 2026-10-07; min 449, max 738), over the ~550 m line
# (docs/ring_rules.md), as Palma's 583 m and Buffalo's 594 m. The brief's
# desk figure was 506 m and expected halved rings; the measurement decides.
# Step 1 stops outside MEDIAN_GAP_BOUNDS_M: under 550 m the halved edges apply.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]
MEDIAN_GAP_BOUNDS_M = (550.0, 620.0)

# --- Station scope ----------------------------------------------------------
# ONE LINE, "Line 1", as the operator names it: THEMA's station page
# (thessmetro.gr/en/metro-stations/, read 2026-10-07 with the project's own
# user agent, owner call 8) heads all 18 stations "Line 1", its home page's
# station map "Thessaloniki Metro Stations (M1)", and its service notice
# speaks of "the entire length of the Line 1". OSM maps the Kalamaria branch
# as a second route (ref 2, "Γραμμή Μετρό Καλαμαριάς", relations 7898293 and
# 7898294) beside the base line (ref 1, relations 6152448 and 7885077);
# both are drawn as the one Line 1 (owner call 4: the operator's name). The
# branch is CUT at the city line, and its five stations (Nomarchia to Mikra,
# all in Kalamaria) are out of scope (owner, 2026-10-04).
# key -> (OSM ref of the relation step 1 writes, colour, public name, label end)
LINES = {"M1": ("1", "#FF0000", "Line 1", None)}
LINE_NAMES = {k: v[2] for k, v in LINES.items()}
# OSM ref -> the drawn line each relation belongs to. Every relation the query
# returns must be placed here, or step 1 stops.
DRAWN_REFS = {"1": "M1", "2": "M1"}
LINES_ROUTE_TYPES = {"subway"}
# OSM's colour tag on the ref 1 relations, #FF0000 (the ref 2 relations carry
# #0070FF); step 1 stops if it moves. The operator's own map draws its line
# in its brand navy #0F0A68, which reads 1.13:1 on the dark page, so OSM's
# red is drawn: CIE76 62.3 from Food service (the nearest pin colour),
# contrast 4.00:1 on the light page and 4.68:1 on the dark one (measured
# 2026-10-07).
OSM_COLOUR = {"1": "#FF0000"}
# A way another relation adds counts as branch track only beyond this
# distance from the track already drawn (Gimhae's figure).
BRANCH_MIN_M = 60.0
# Stop positions of one station (one per direction and per route) sit within
# a platform's length; a same-named pair farther apart than this stops step 1.
COLLAPSE_MAX_SPREAD_M = 300.0
# After the cut at the city line, every kept station must still sit on the
# drawn track (its stop positions are on the track; widest spread 18 m).
STATION_ON_TRACK_M = 50.0
# Gate 1's floor: the shared 400 m (pipeline/stations.py).

# GATE 3, from Elliniko Metro, the state company that built and owns the
# metro (owner call 5): its base line page lists 13 stations, New Railway
# Station to Nea Elvetia, and its Kalamaria extension page 5, Nomarchia to
# Mikra (read 2026-10-04 and re-read by brief_check.py 2026-10-07). The
# operator's station page lists the same 18 under Line 1. The in-city count
# is the base line's 13 because the polygon puts Nea Elvetia in and Nomarchia
# out; step 1 also checks the 13 names one by one.
OPERATOR_STATION_COUNTS = {"Line 1": 18, "Line 1 in Thessaloniki": 13}
OPERATOR_COUNTS_SOURCE = (
    "Elliniko Metro's station pages (emetro.gr/?page_id=15008, the base line's 13; "
    "emetro.gr/?page_id=15499, the Kalamaria extension's 5), read 2026-10-04; THEMA's "
    "station page (thessmetro.gr/en/metro-stations/) lists the same 18 under Line 1, "
    "read 2026-10-07.")
# Elliniko Metro's 13 base-line names, as its page writes them (capitals,
# accents folded by station_name_key). OSM writes Αναλήψεως as Ανάληψη.
OPERATOR_IN_CITY_EL = ("ΝΕΟΣ ΣΙΔΗΡΟΔΡΟΜΙΚΟΣ ΣΤΑΘΜΟΣ", "ΔΗΜΟΚΡΑΤΙΑΣ", "ΒΕΝΙΖΕΛΟΥ", "ΑΓΙΑΣ ΣΟΦΙΑΣ",
                       "ΣΙΝΤΡΙΒΑΝΙ", "ΠΑΝΕΠΙΣΤΗΜΙΟ", "ΠΑΠΑΦΗ", "ΕΥΚΛΕΙΔΗΣ", "ΦΛΕΜΙΓΚ",
                       "ΑΝΑΛΗΨΕΩΣ", "25ΗΣ ΜΑΡΤΙΟΥ", "ΒΟΥΛΓΑΡΗ", "ΝΕΑ ΕΛΒΕΤΙΑ")
OPERATOR_NAME_ALIASES = {"ΑΝΑΛΗΨΗ": "ΑΝΑΛΗΨΕΩΣ", "ΦΛΕΜΙΝΓΚ": "ΦΛΕΜΙΓΚ"}
# THEMA's English station names, in its order (the station page, 2026-10-07).
# Each station's label is OSM's name:en, which must be one of these; the one
# OSM spelling that differs is replaced by the operator's below.
OPERATOR_STATIONS_EN = ("New Railway Station", "Dimokratias", "Venizelou", "Agias Sofias",
                        "Sintrivani", "Panepistimio", "Papafi", "Efkleidis", "Fleming",
                        "Analipsi", "25th Martiou", "Voulgari", "Nea Elvetia", "Nomarchia",
                        "Kalamaria", "Aretsou", "Nea Krini", "Mikra")
EN_NAME_OVERRIDES = {"Thessaloniki New Railway Station": "New Railway Station"}

# Headway, from THEMA's FAQ (thessmetro.gr/en/frequent-asked-questions-faq/,
# read 2026-10-07): New Railway Station to 25th Martiou every 2:55 min from
# 07:30 Monday to Saturday (3:25 Sundays and holidays), 5:00 before 07:30
# Monday to Friday and 10:00 at weekends; 25th Martiou to Nea Elvetia every
# 8:45 (10:15 Sundays; 15:00 or 30:00 before 07:30). Well inside the
# 20-minute floor in the day; recorded, not computed.
HEADWAY_SOURCE = "THEMA's FAQ, thessmetro.gr/en/frequent-asked-questions-faq/ (2026-10-07)"

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "thessaloniki_adeies"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "activity"

# Sanity bounds for the reprojected points: the layer's extent (X 407,485 to
# 414,256, Y 4,493,154 to 4,500,381 in EPSG:2100) with a margin. The boundary
# does the filtering; this catches an axis or CRS error.
THESSALONIKI_BBOX = {
    "lat_min": 40.57,
    "lat_max": 40.68,
    "lon_min": 22.88,
    "lon_max": 23.00,
}
