"""Copenhagen-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

FIRST DANISH CITY. The national facts - Datafordeler, CVR's four-file join,
DAR, the columns never to load, the sole-trader guard - live in
`pipeline/countries/denmark.py`. What is Copenhagen's own is below: the two
kommuner, the rail scope, the palette and the catch-all verdict.
"""

from pathlib import Path

SLUG = "copenhagen"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "copenhagen" / "raw"
DATA_PROCESSED = ROOT / "data" / "copenhagen" / "processed"
OUTPUTS = ROOT / "outputs" / "copenhagen"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the two kommuner, with the kommune each IS in - a citable
# scoping record. Most are S-tog stations on the lines' suburban reaches.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs. `fetch_sources.py` downloads them; no step may fetch. CVR and DAR
# are cached once for the country (`denmark.SHARED_RAW`); the two OSM files
# are Copenhagen's own.
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_KOMMUNER_JSON = DATA_RAW / "osm_kommuner.json"
# What was fetched, which generation, and when - committed, and never a URL
# with the key in it.
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Scope: TWO kommuner ------------------------------------------------------
#
# ✅ KOBENHAVN (0101) + FREDERIKSBERG (0147), owner's call 2026-09-24.
# Frederiksberg is a separate kommune ENTIRELY ENCLOSED by Kobenhavn and holds
# 7 Metro stations; scoped out, it is a hole in the middle of the map with
# three Metro lines drawn through it. By the worst-line rule the French cities
# and Oslo were scoped on:
#
#                 Kobenhavn only      + Frederiksberg
#     M1          10/15               15/15
#     M2           9/16 (56%)         14/16   (Kastrup, Lufthavnen: Taarnby)
#     M3          13/17               16/17   (to be re-measured at step 1)
#     M4          12/13               12/13
#
# Taarnby's two airport stations stay out and are named as excluded.
#
# ⚠ THE BUSINESS FILTER IS CVR's OWN `CVRAdresse_kommunekode` ON THE LOCATION
# ADDRESS, never a polygon - it is the register's authoritative field. The
# polygons below decide only which STATIONS are in scope.
KOMMUNER = {"101": "Kobenhavn", "147": "Frederiksberg"}   # CVR's unpadded codes
DAR_KOMMUNER = ("0101", "0147")                           # Datafordeler's padded

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# ETRS89 / UTM 33N. Copenhagen's longitude (~12.57 E) falls in UTM zone 33
# (12-18 E) - by 0.57 degrees, derived per city as the invariant asks. ⚠ DAR
# publishes its points in zone 32 (EPSG:25832) NATIONALLY, Copenhagen
# included; that is `denmark.DAR_CRS` and is converted on read, never used
# for this city's geometry.
CRS_PROJECTED = "EPSG:25833"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# THE SHARED EDGES, on Philadelphia's measured ground rather than by default.
# Measured 2026-09-24 across the 64 in-scope stations (nearest neighbour,
# ETRS89 / UTM 33N metres, after the name collapse):
#
#     min 358    median 708    mean 753    max 1,743
#
# Philadelphia's subway/el sits at a 711 m median and keeps these edges, "so
# the 0.6 mi outer ring still reads as a gradient rather than a wash". The
# halved edges were taken where the median was 341-541 m (Marseille, Oslo,
# Lille, Toulouse, Rennes); at 708 m their 483 m outer ring would stop well
# short of every neighbour. Settled on that measurement, not re-asked.
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# WHAT COUNTS - owner's calls, 2026-09-24:
#
#   * Metro M1-M4 (OSM `route=subway`).
#   * S-tog A, B, Bx, C, E, F, H (OSM `route=light_rail`, network S-tog) - on
#     the published spacing-and-frequency test, Dublin's DART precedent,
#     NOT as an exception to it. Inside the two kommuner S-tog's median
#     station spacing is 1,227 m (F: 892 m) against the Metro's 884 m, every
#     line runs every 10 minutes through the day, and 22 of its 31 stations in
#     scope have no Metro station within 400 m. Paris's RER was excluded as an
#     overlay on a Metro that already covers the city; S-tog is the network in
#     the districts the Metro does not reach.
#   * NOT regional or InterCity trains (`route=train`), Lokaltog 910, or
#     Hovedstadens Letbane - the last opened in full on 22 August 2026 and has
#     no stop in either kommune.
#
# RAIL FROM OSM, NOT REJSEPLANEN - owner's call 2026-09-24, and the ground
# the osm-rail skill asks for. Rejseplanen's national GTFS is keyless and
# current, but its Labs guidelines ask users not to change the data so that
# it differs from the original, and document access as by request with those
# guidelines accepted. Neither point was resolved in this project's favour,
# so the feed was not downloaded. OSM (ODbL) names and colours every line.
METRO_REFS = ("M1", "M2", "M3", "M4")
STOG_REFS = ("A", "B", "Bx", "C", "E", "F", "H")
# A WHITELIST ON THREE TAGS, never on `network`: every relation in the bbox,
# Lokaltog and Movia's Letbane included, carries network "Takst Sjaelland" -
# the fare zone, not the system. Metro is `route=subway` by ref; S-tog is
# `route=light_rail` by ref AND operator, which is what keeps out Lokaltog 910
# (Lokaltog A/S) and the Letbane's "L" (no operator), both also light_rail.
STOG_OPERATOR = "DSB"

# OSM ref -> the name riders use. The mode word distinguishes Metro M1 from
# a bus and S-tog A from anything else lettered A.
LINE_NAMES = {
    "M1": "Metro M1", "M2": "Metro M2", "M3": "Metro M3", "M4": "Metro M4",
    "A": "S-tog A", "B": "S-tog B", "Bx": "S-tog Bx", "C": "S-tog C",
    "E": "S-tog E", "F": "S-tog F", "H": "S-tog H",
}

# One station under two names, merged only where named here. Interchanges
# that share ONE name across the two modes (Norreport, Kobenhavn H, Osterport,
# Nordhavn, Kobenhavn Syd, Norrebro, Flintholm, Vanlose) collapse by name
# without an entry, and step 1 prints each one's spread before trusting it.
STATION_NAME_ALIASES = {}

SPACING_MIN_M = 400.0

# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope
# decision is CHECKABLE rather than merely written down. Measured 2026-09-24
# on OSM's kommune polygons (Kobenhavn 94.4 km2 with Frederiksberg's 8.7 km2
# as its inner ring). Every Metro line keeps all its stations but M2, whose
# two missing are Kastrup and Lufthavnen in Taarnby; Gammel Strand, which
# DAWA's polygon left in the harbour, is inside OSM's. S-tog F is 12 of 12
# because Hellerup's platforms sit just inside Kobenhavn on BOTH DAWA's and
# OSM's boundary - its ring counts only the Kobenhavn side, since businesses
# are filtered on CVR's own kommune code. If these move, the scope decision
# is being re-taken and should be re-taken deliberately.
EXPECTED_INSIDE_PER_LINE = {
    "M1": 15, "M2": 14, "M3": 17, "M4": 13,
    "A": 11, "B": 12, "Bx": 12, "C": 17, "E": 11, "F": 12, "H": 9,
}

# GATE 3, read 2026-09-24 - and neither figure is a clean first-party count.
#   * Metro: 15 / 16 / 17 / 13, network 44 - English Wikipedia's line table
#     (a secondary source; Metroselskabet's own pages were not read for it).
#   * S-tog: DSB's own S-tog page says BOTH "dækker 87 stationer" and, lower
#     down, "dækker 86 stationer og består af 7 linjer". 87 is used because it
#     is the page's first statement and Danish Wikipedia's figure; the other
#     is recorded rather than hidden. A one-station disagreement is a prompt
#     to look at the network list, not a pass.
OPERATOR_STATION_COUNTS = {
    "Metro M1": 15, "Metro M2": 16, "Metro M3": 17, "Metro M4": 13,
    "Metro (network)": 44, "S-tog (network)": 87,
}
OPERATOR_COUNTS_SOURCE = (
    "Metro per line and 44: en.wikipedia Copenhagen Metro (secondary); S-tog 87: "
    "dsb.dk/s-tog, which also says 86 on the same page - read 2026-09-24")

# The Overpass bbox: the whole S-tog network, Koge to Hillerod and
# Frederikssund, so step 1 can name the kommune of every station it drops.
RAIL_BBOX = (55.40, 12.00, 56.00, 12.70)       # south, west, north, east

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "denmark_db25"
RAW_CLASSIFICATION_COLUMN = "db25_label"
CITY_KEEP = "COPENHAGEN"   # kept for the scaffold's templates; KOMMUNER filters

# TODO: the per-city catch-all verdict (969900 first), from a hand sample and
# the sole-trader share, as Oslo's 96.990 was taken.
CATCH_ALL_EXCLUDE = ()

# Sanity bounds: the two kommuner's extent plus ~0.02 deg. Catches a corrupt
# coordinate; the join to DAR does the placing.
# TODO: tighten to the measured extent at step 2.
COPENHAGEN_BBOX = {
    "lat_min": 55.58,
    "lat_max": 55.76,
    "lon_min": 12.43,
    "lon_max": 12.75,
}
