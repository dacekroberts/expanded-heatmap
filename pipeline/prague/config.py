"""Prague-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

FIRST CZECH CITY. The national facts - ROS02, RES, RUIAN, the legal forms,
the CRS - live in `pipeline/countries/czechia.py`. What is Prague's own is
below: the obec, the metro, Flora, the palette and the catch-all verdict.
"""

from pathlib import Path

SLUG = "prague"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "prague" / "raw"
DATA_PROCESSED = ROOT / "data" / "prague" / "processed"
OUTPUTS = ROOT / "outputs" / "prague"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the obec, if any - the brief measured all 60 metro
# station-line pairs inside it, so this is expected to be written EMPTY.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs. `fetch_sources.py` downloads them; no step may fetch. ROS02, RES
# and the CZ-NACE codebooks are national (`czechia.SHARED_RAW`); RUIAN is per
# obec, and the rail and boundary are Prague's own.
GTFS_ZIP = DATA_RAW / "pid_gtfs.zip"
RUIAN_ZIP = DATA_RAW / "ruian_adr_554782.csv.zip"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
OSM_RAIL_JSON = DATA_RAW / "osm_rail.json"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# PID - Pražská integrovaná doprava, via ROPID. Keyless, CC BY 4.0, credit
# ROPID and state the changes (pid.cz/o-systemu/opendata/, read 2026-09-24).
# ⚠ Its feed_info declares a TWO-WEEK window - a stale copy means refetch.
GTFS_URL = "https://data.pid.cz/PID_GTFS.zip"

# --- Scope ---------------------------------------------------------------
#
# Obec 554782, Praha - which is also the region, so the city IS its own
# kraj. The businesses are scoped by RUIAN's own address list for the obec
# (ROS02's PKODADM in it), never by a polygon.
OBEC = "554782"
# The boundary, for station scope and label anchoring only: OSM relation
# 435514 ("Praha", admin_level 4, ref:nuts CZ010) - the ONLY relation a
# bbox-bounded name search returns (2026-09-24). ČÚZK's INSPIRE polygon
# measured 496.2 km² in the brief; step 1 gates the OSM one on that.
OSM_BOUNDARY_RELATION = 435514
BOUNDARY_AREA_KM2 = (480.0, 510.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 33N: Prague's longitude (~14.44 E) falls in the 12-18 band. Derived
# per city, not copied. RUIAN's S-JTSK (EPSG:5513) is converted on read and
# never used for this city's geometry.
CRS_PROJECTED = "EPSG:32633"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# THE SHARED EDGES, on measured spacing: the 58 stations' nearest-neighbour
# distances are min 450, median 912, mean 935, max 1,491 m (2026-09-24) -
# sparser than Philadelphia's 711 m and Copenhagen's 708 m, which both keep
# these edges. The halved edges were taken only at medians of 341-541 m.
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# WHAT COUNTS - owner's calls, 2026-09-24 (before the pause, banked in the
# brief): METRO A, B, C ONLY (`route_type 1`). Prague's trams are a dense
# overlay on the metro across the whole centre, not a separate corridor; the
# Petřín funicular, the ferries and the S-trains go on the standing rules,
# as in Paris.
ROUTE_TYPE_METRO = "1"
LINE_NAMES = {"A": "Metro A", "B": "Metro B", "C": "Metro C"}
# The operator's own livery, from the feed's route_color, with ONE colour
# moved. The shared check (pipeline/linecolour.py, Delta-E floor 10) REFUSED
# metro A's #00A562 at 9.2 from the Personal services pins (#1baf7a) - the
# line would vanish under its own dots. Lightened in HSL lightness only, hue
# and saturation kept, by the smallest step that clears the floor with
# Copenhagen's ~13 margin: +0.04 -> #00b96e, 13.1 from the pins and 8.5 from
# DPP's green. Lighter, not darker, for Lille's reason (the dark basemap).
# B #F8B322 is 86.9 from its nearest pin; C #CF003D is 21.2 from Food
# service, below the preferred 45 and recorded rather than moved.
LINE_COLOURS = {"A": "#00b96e", "B": "#F8B322", "C": "#CF003D"}

# FLORA IS DRAWN, DISCLOSED - owner's call 2026-09-24. Line A's Flora is
# CLOSED FOR RECONSTRUCTION (DPP: from 1 February 2026 for about ten months,
# reopening at the turn of November/December 2026), so no metro trip calls
# there and a trip-based station list has A at 16 where it has 17. It is
# located from PID's own stops.txt (parent station U118S1), and step 1 STOPS
# the build once the feed serves Flora again, so this override cannot outlive
# the closure.
FLORA_PARENT = "U118S1"
FLORA_NAME = "Flora"
FLORA_LINE = "A"

# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1. Measured
# 2026-09-24 against OSM relation 435514 (495.9 km²): every station of all
# three lines is inside the obec, Flora included, so commune scope costs the
# metro nothing - Paris's and Marseille's shape.
EXPECTED_INSIDE_PER_LINE = {"A": 17, "B": 24, "C": 20}

# GATE 3 - A 17 / B 24 / C 20, 58 distinct stations: English Wikipedia's
# Prague Metro article, read 2026-09-24 (a SECONDARY source). The feed gives
# 16 / 24 / 20 from its trips and 17 for A only with Flora added, and OSM's
# route relations give 16 / 24 / 20, omitting Flora too - so the operator's
# count is what shows Flora still belongs to line A.
OPERATOR_STATION_COUNTS = {"Metro A": 17, "Metro B": 24, "Metro C": 20,
                           "Metro (network)": 58}
OPERATOR_COUNTS_SOURCE = ("A 17 / B 24 / C 20, 58 stations: en.wikipedia Prague Metro "
                          "(secondary), read 2026-09-24")

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "czech_nace2025"
RAW_CLASSIFICATION_COLUMN = "nace2025_label"
CITY_KEEP = "PRAHA"   # kept for the scaffold's templates; OBEC filters

# The per-city catch-all verdict, which czech_nace2025.py declines to make.
# TAKEN 2026-09-24 on Prague's own numbers: NOTHING is excluded.
#
#     96990  Poskytování ostatních osobních služeb j. n.   3 rows
#
# The code that Oslo (96.990) and Copenhagen (969900) excluded is almost EMPTY
# here - CZ-NACE 2025 has already sent its contents to specific classes. The
# largest personal-services class after hairdressing is 96230, day spas,
# saunas and steam baths (1,638 rows, 80% natural persons): a SPECIFIC class,
# not residual wording, and mostly massage salons with a street door - kept.
# The retail catch-alls (47120, 47270, 47690, 47780, 47799) are kept, as in
# Oslo, Copenhagen and France: shops by product.
CATCH_ALL_EXCLUDE = ()

# Sanity bounds: the placed storefronts' measured extent (49.9488-50.1716 N,
# 14.2657-14.6867 E, 2026-09-24) plus ~0.02 deg. The join to RUIAN does the
# placing; this catches a CRS or axis error, which the castle control in
# czechia_register.py catches first.
PRAGUE_BBOX = {
    "lat_min": 49.93,
    "lat_max": 50.19,
    "lon_min": 14.24,
    "lon_max": 14.71,
}
