"""Philadelphia-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Every value here was live-verified on 2026-09-21 (add-city Step 0); the
endpoints, filters and licences are recorded in docs/data_sources.md.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "philadelphia" / "raw"
DATA_PROCESSED = ROOT / "data" / "philadelphia" / "processed"
OUTPUTS = ROOT / "outputs" / "philadelphia"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stops cut by the trolley spacing filter, with what each was nearest to
# instead (a citable scoping record, as in San Francisco).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "business_licenses_active.csv"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"

# --- Raw inputs: endpoints and the filter applied at download --------------
# Fetched by pipeline/philadelphia/fetch_sources.py.

# SEPTA publishes one zip containing two nested feeds, google_bus.zip and
# google_rail.zip. The rail one is Regional Rail; the SEPTA Metro lines this
# map draws are in the BUS feed (SEPTA's City Transit Division), which is not
# guessable from the names - verified by reading both route tables.
# fetch_sources.py extracts the inner feed to GTFS_ZIP so step 1 reads an
# ordinary GTFS zip like every other city.
GTFS_URL = "https://github.com/septadev/GTFS/releases/latest/download/gtfs_public.zip"
GTFS_INNER_ZIP = "google_bus.zip"

# OpenDataPhilly "City Limits" (Department of Planning and Development).
# One polygon, 2,957 vertices.
CITY_BOUNDARY_URL = (
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/"
    "City_Limits/FeatureServer/0/query"
)
CITY_BOUNDARY_PARAMS = {
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "true",
    "outSR": "4326",
    "f": "geojson",
}

# L&I Business Licenses, via the Carto SQL API. PostGIS is evaluated
# server-side, so ST_X/ST_Y return plain coordinates and no WKB parsing is
# needed. `the_geom` is populated on 100% of the kept rows.
BUSINESSES_ENDPOINT = "https://phl.carto.com/api/v2/sql"

# Columns deliberately NOT selected, all of them individuals' names:
# legalfirstname, legallastname, legalname, opa_owner, ownercontact1name,
# ownercontact2name. `business_name` is the trade name and is never blank
# (0 of 118,535 active rows), so this city needs no name fallback at all -
# which is why no pin here CAN be a registrant's own name. step 2 asserts
# none of those columns ever arrives, the same structural guarantee New
# York's salon registry needed.
# `legalentitytype` is kept: it is Individual/Company, a structured privacy
# signal rather than a name, and a better one than any name heuristic.
BUSINESSES_SELECT = (
    "licensenum, licensetype, business_name, legalentitytype, address, "
    "unit_type, unit_num, zip, council_district, "
    "ST_X(the_geom) AS longitude, ST_Y(the_geom) AS latitude"
)

# The licence types the taxonomy maps to a bucket. Filtering at download keeps
# the raw file to the ~9k rows this project uses instead of 435k, and means the
# excluded residential registrations are never fetched at all.
KEPT_LICENSETYPES = [
    "Food Preparing and Serving",
    "Food Preparing and Serving (30+ SEATS)",
    "Food Caterer",
    "Sidewalk Cafe",
    "Streetery License",
    "Food Establishment, Outdoor",
    "Food Establishment, Retail Permanent Location",
    "Food Establishment, Retail Perm Location (Large)",
    "Curb Market",
    "Vendor - Newsstand",
    "Tire Dealer",
    "Precious Metal Dealer",
    "Pawn Shop",
]

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 18N: floor((-75.16 + 180) / 6) + 1 = 18, so EPSG:32618. Derived
# from Philadelphia's own longitude, not copied from another city (it happens
# to share New York's zone) - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32618"

# --- Ring geometry ---------------------------------------------------------
# The shared edges, unlike New York's. Philadelphia's kept stations sit a
# median 711 m apart on the subway/el and are thinned to roughly 0.5 mi on the
# trolleys, so the 0.6 mi outer ring still reads as a gradient rather than a
# wash.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# SEPTA Metro, the agency's own branding for its rapid-transit and trolley
# network. Four line groups are drawn, keyed by SEPTA's own letters:
#
#   L  Market-Frankford Line   grade-separated, 25 in-city stations
#   B  Broad Street Line       grade-separated, 24 in-city (incl. Ridge Spur)
#   T  subway-surface trolleys  5 branches sharing a Center City tunnel
#   G  Girard Avenue trolley    street-running end to end
#
# Deliberately NOT drawn:
#   M1 (Norristown High Speed Line) and D1/D2 (routes 101/102) have ZERO
#     in-city stops - 44 and 99 respectively, all outside Philadelphia, since
#     both start at 69th Street in Upper Darby. The boundary filter removes
#     them; they are listed here so their absence is a recorded fact rather
#     than an oversight.
#   Regional Rail (the separate google_rail.zip feed, 52 in-city stations) is
#     commuter rail, excluded to match Chicago leaving out Metra and New York
#     leaving out the LIRR and Metro-North. SEPTA's own branding separates it
#     from SEPTA Metro. It is the obvious later addition if that call changes.
#   Routes 59, 66 and 75 are route_type 11 (trackless trolley) - electric
#     buses, not rail.
ROUTE_GROUPS = {
    "L": ["L1"],
    "B": ["B1", "B2", "B3"],
    "T": ["T1", "T2", "T3", "T4", "T5"],
    "G": ["G1"],
}
ROUTE_IDS = [r for rs in ROUTE_GROUPS.values() for r in rs]

# Real public names, and SEPTA's own route_color from routes.txt.
LINE_NAMES = {
    "L": ("Market-Frankford Line", "#0097D6"),
    "B": ("Broad Street Line", "#F26100"),
    "T": ("Subway-Surface Trolleys", "#5A960A"),
    "G": ("Girard Avenue Trolley", "#FFD700"),
}

# The shape_id(s) whose geometry each line group is drawn from: each route's
# single most-used trip shape, found by counting trips per shape_id per route
# and taking the mode (2026-09-21). Re-derive if the feed is re-downloaded.
# A tuple draws several shapes as one legend entry, which is how a trunk with
# branches is handled (see load_line_shapes in map_common.py).
#   B  319850 is B1 Fern Rock-NRG; 319877 is the B3 Ridge Spur branch. B2 is
#      the express over B1's own tracks, so it adds no geometry.
#   T  one shape per branch: T1 63rd-Malvern, T2 61st-Baltimore, T3 Yeadon,
#      T4 Darby, T5 80th-Eastwick - all sharing the Center City tunnel.
LINE_SHAPES = {
    "L": "319893",
    "B": ("319850", "319877"),
    "T": ("319740", "319746", "319768", "319779", "319804"),
    "G": "319735",
}

# Only the trolley groups are street-running and need thinning; L and B are
# grade-separated with 681-711 m median spacing and are kept whole.
THINNED_GROUPS = frozenset({"T", "G"})

# Target spacing for the thinning filter, measured along each line's real
# stop-to-stop path (see docs/sub_transit_line_filters.md). San Francisco's
# value, which suits the same shape of problem: 190 in-city T stops and 71 G
# stops at a 134-137 m median.
STATION_SPACING_MILES = 0.5

# Filter 1 of the sub-transit-line pattern: central-corridor stations are
# always kept, never thinned. For the T that is the Center City subway-surface
# tunnel its five branches share, from 13th St west to the 40th Street portal;
# the G has no tunnel, so the filter never fires on it.
#
# EXACT canonical names, not substrings, and deliberately so: the tunnel stops
# are named "36th-Sansom", "37th-Spruce" and "40th St Portal" in the real feed,
# which a "36th St"-style keyword list would miss, while "33rd St" as a
# substring would wrongly match surface stops like "Girard Av & 33rd St".
SUBWAY_STATION_NAMES = frozenset({
    "13th St",
    "15th St/City Hall",
    "19th St",
    "22nd St",
    "Drexel Station at 30th St",
    "33rd St",
    "36th-Sansom",
    "37th-Spruce",
    "40th St Portal",
})

# SEPTA suffixes a stop name with the route that serves it where platforms
# differ ("Olney Transit Center - B1" vs "- B2 & B3", "15th St/City Hall - B1"
# vs the plain name on the L), and with a stop-position code on surface track
# ("- FS" far side, "- MBFS" mid-block far side). Both are platform detail, not
# distinct stations, so they are stripped before any station logic runs.
# `parent_station` is populated on only 695 of 14,054 stops, so it cannot do
# this job alone.
STATION_SUFFIX_PATTERN = r"\s+-\s+[A-Z0-9][A-Z0-9 &]*$"

# Hand-curated after the physical-distance check step 1 runs across the final
# list, per docs/sub_transit_line_filters.md's implementation note. Both of
# these are a Girard trolley stop sitting on top of the rapid-transit station
# it interchanges with - 6.7 m and 18.4 m apart respectively, far too close to
# be two stations - under names that share no suffix pattern to detect. The
# rapid-transit name wins because that is what riders call the place.
STATION_NAME_ALIASES = {
    "Girard Av & Front St": "Front-Girard",
    "Girard Av & Broad St": "Broad-Girard",
}

# --- Business filtering ------------------------------------------------

# No city filter: this is the City of Philadelphia's own licence register, so
# every row is by definition a Philadelphia licence. Step 2 cross-checks the
# coordinates against the boundary polygon instead.
CITY_KEEP = None

TAXONOMY_SYSTEM = "phl_licensetype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "licensetype"

# One storefront can hold several licences (a restaurant with a sidewalk cafe
# holds both), so step 2 keeps one row per site with the most specific licence
# deciding. Adjunct permissions rank last - see ADJUNCT_LICENSETYPES in the
# taxonomy - so the restaurant, not its pavement seating, is what the pin says.
LICENSE_PRIORITY = [
    "Food Preparing and Serving (30+ SEATS)",
    "Food Preparing and Serving",
    "Food Establishment, Retail Perm Location (Large)",
    "Food Establishment, Retail Permanent Location",
    "Food Caterer",
    "Curb Market",
    "Vendor - Newsstand",
    "Tire Dealer",
    "Precious Metal Dealer",
    "Pawn Shop",
    # Adjunct, ranked last on purpose.
    "Sidewalk Cafe",
    "Streetery License",
    "Food Establishment, Outdoor",
]

# Sanity bounds for the supplied coordinates. The real extent of the kept rows
# measured -75.274..-74.959, 39.880..40.134; this box is that, rounded out.
PHILADELPHIA_BBOX = {
    "lat_min": 39.86,
    "lat_max": 40.15,
    "lon_min": -75.29,
    "lon_max": -74.94,
}
