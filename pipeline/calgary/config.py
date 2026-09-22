"""Calgary settings. One municipality, one licence, one notice.

WHAT MAKES THIS CITY DIFFERENT
------------------------------
**Its licence taxonomy names premises explicitly, and no other city's does.**
Calgary suffixes its own categories with `- PREMISES`, `- NO PREMISES`,
`(MOBILE)`, `(HOME BASED)`, `(MAIL ORDER)` and `(DIRECT SALES)`. So the
question every other city answers by inference - is this a storefront? - is
answered here by the City itself, in the category string. That is why Calgary's
published ranking figure was inflated only 1.4x where Vancouver's was 4.2x: its
register was already premises-oriented before this project filtered anything.

**It has no home-business signal at all, and that is now confirmed rather than
suspected.** `homeoccind` is `N` on all 23,203 rows - constant, not merely
unreliable. Vancouver is the other city in that position, and its parcel-based
substitute turned out to remove nothing, so none is built here either. What
Calgary has instead is the `(HOME BASED)` suffix on individual categories,
which is a per-licence statement and is handled in the taxonomy.

**Two traps found by measurement, both recorded 2026-09-21.**

  1. `route_id` EMBEDS A FEED VERSION. The Mobility Database mirror gives
     `201-20780`; the agency feed gives `201-20786`. A config pinning the id
     silently matches nothing after the next release, so routes are matched on
     `route_short_name`. No other city here has versioned route ids.
  2. THE CITY BOUNDARY HAS TWO SOCRATA VIEWS AND ONE IS EMPTY. `7t9h-2z9s`
     is a `map` view and exports 53 bytes of unreadable GeoJSON; `erra-cqp9`
     is the `dataset` view and carries the real MultiPolygon. The rule
     generalises on this portal: take the `dataset` view, never the `map` one.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "calgary" / "raw"
DATA_PROCESSED = ROOT / "data" / "calgary" / "processed"
OUTPUTS = ROOT / "outputs" / "calgary"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (see pipeline/calgary/fetch_sources.py) -------------------

GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "business_licences.csv"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"

# --- Endpoints --------------------------------------------------------------

# Socrata. `$limit` is required: the default page is 1,000 rows.
BUSINESS_URL = "https://data.calgary.ca/resource/vdjc-pybd.csv"
BUSINESS_LIMIT = 60000

# Calgary Transit's OWN feed, not the Mobility Database mirror. Verified
# 2026-09-21 to reproduce the mirror's rail half exactly (2 route_type 0
# routes, 83 served stops, 83 distinct names).
GTFS_URL = ("https://data.calgary.ca/download/npk7-z3bj/"
            "application%2Fx-zip-compressed")

# THE `dataset` VIEW, NOT THE `map` VIEW - see this file's docstring. Measured:
# 1 MultiPolygon, EPSG:4326, 852.9 km2 dissolved.
CITY_BOUNDARY_URL = ("https://data.calgary.ca/api/geospatial/erra-cqp9"
                     "?method=export&format=GeoJSON")

# --- Transit feed -----------------------------------------------------------

# NEITHER Calgary feed carries feed_info.txt - not the mirror and not the
# agency's own - so unlike D.C., Montréal and Vancouver there is NO validity
# window to check and the expiry guard cannot be written. Staleness has to be
# judged from the Socrata resource's own `updatedAt` instead. Recorded because
# the absence looks like an oversight in this file otherwise.
GTFS_CHECK_FEED_WINDOW = False

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 11N: Calgary's longitude (~-114.07) falls in the -120 to -114 band.
# Derived per city, never copied - Vancouver 32610, Montréal 32618,
# Edmonton would be 32612.
CRS_PROJECTED = "EPSG:32611"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# MATCHED ON route_short_name, NOT route_id - see the docstring. The CTrain is
# the only rail in this feed; the other 258 routes are buses.
ROUTE_SHORT_NAMES = ["201", "202"]
LINE_NAMES = {
    "201": "Red Line",
    "202": "Blue Line",
}

# Calgary Transit's own colours for the two CTrain lines. MEASURE CONTRAST IN
# BOTH MODES, dark first, against the burnt-orange heat ramp - see
# pipeline/map_common.HEAT_GRADIENT, and D.C.'s Silver Line for the case where
# measuring only the light basemap gave a backwards answer.
LINE_COLOURS = {
    "201": "#CC0000",   # Red Line
    "202": "#0072CE",   # Blue Line
}

# ONE shape per line, the most-used trip shape, as most cities here use.
#
# Calgary needs no tuple, unlike Vancouver's Canada and Expo Lines. The reason
# is worth stating because the shape counts LOOK like branching - 12 shapes on
# the Red Line, 13 on the Blue - and a coverage test reports each direction
# covering only ~51% of platforms. That is the PLATFORM artefact again: each
# direction serves its own directional platform, so one direction's shape
# covers one platform per station. It still traces the whole route, terminus to
# terminus, which is what drawing needs.
#
# The one real simplification: along the downtown 7 Avenue ONE-WAY COUPLET the
# two directions run on DIFFERENT STREETS, so a single shape follows only one
# of them. That is a one-to-two-block difference over ~1 km of a 25 km line,
# and drawing both directions would overlap the entire suburban trunk with an
# identical second polyline to fix it. Left as one shape; recorded so the
# downtown offset is not later mistaken for an error.
LINE_SHAPES = {
    "201": "2010682",   # Red Line,  927 trips, 653 points
    "202": "2020431",   # Blue Line, 678 trips, 455 points
}
LINE_LABEL_ENDS = {}

# The CTrain is grade-separated except for the downtown 7 Avenue transit mall,
# which is street-running but has stations at normal spacing rather than the
# every-block spacing that forced San Francisco's thinning. Spacing is MEASURED
# and printed in step 1 rather than asserted here.
THINNED_GROUPS = frozenset()

# THE FEED PUBLISHES 83 PLATFORMS, NOT 83 STATIONS - and the whole Canada
# ranking recorded the platform count. Every stop name carries a direction
# prefix (`NB Banff Trail CTrain Station` / `SB Banff Trail ...`) and there is
# NO `parent_station` column, so nothing collapses them automatically and each
# name is unique. They collapse to **45**, which is the CTrain's real published
# station count - that agreement is what turns the regex below into evidence.
#
# What caught it was the SPACING, not a name check: the uncollapsed
# nearest-neighbour median was 17 m with a minimum of 8 m, physically
# impossible for rail stations. Collapsed it is 1,023 m. Recorded in the
# `add-city` skill as the standard diagnostic.
#
# Consequence for the ranking: Calgary's published 75 per station was 75 per
# PLATFORM, i.e. ~138 per station, which moves it from fifth of six to third.
IN_CITY_STATIONS_EXPECTED = 45
PLATFORMS_EXPECTED = 83

# Collapsing the direction prefix and the suffix variants. All of these are
# real and a naive strip gets 47 or 49 rather than 45:
#   - a TYPO in the feed: `CTrain Staion` alongside `CTrain Station`
#   - three suffixes for one system: `CTrain Station`, `CTrain Stn`,
#     `Station (Free Fare Zone)`, and bare `Station`
#   - the hyphen MOVES between the two directions of one station:
#     `EB Downtown West-Kerby Station` against `WB Downtown-West Kerby Station`
STATION_DIRECTION_PREFIX = r"^(NB|SB|EB|WB)\s+"
STATION_SUFFIX_PATTERNS = (
    r"\s*\(Free Fare Zone\)\s*$",
    r"\s*CTrain\s+(?:Station|Staion|Stn)\s*$",
    r"\s+Station\s*$",
)

# SEVEN of the 45 stations legitimately have ONE platform, and they must not be
# merged with a neighbour: 7 Avenue downtown is a ONE-WAY COUPLET, so
# `EB 3 Street SW` and `WB 4 Street SW` are different places on different
# streets. Collapsing by normalised NAME handles this correctly; collapsing by
# proximity would fuse them.
SINGLE_PLATFORM_STATIONS_EXPECTED = 7

# --- Business filtering ------------------------------------------------

SOURCE_ENCODING = "utf-8"

TAXONOMY_SYSTEM = "calgary_licencetype"
# The RAW column is plural and holds SEVERAL categories per row. Step 2 splits
# it and resolves to one winning category, which it writes to the taxonomy's
# VALUE_COLUMN (`licencetype`, singular).
RAW_CLASSIFICATION_COLUMN = "licencetypes"

# `licencetypes` is `",\n"`-DELIMITED - a comma AND a newline. Splitting on a
# bare "\n" is what produced the "173 categories" recorded in the Canada
# profile: it shreds each value and counts the fragments. The real count is 96,
# with 9,136 of 23,203 rows carrying more than one category.
CATEGORY_DELIMITER = ",\n"

# WHICH LICENCES COUNT AS ACTIVE. Measured 2026-09-21, all seven values:
#   Renewal Licensed          15,962   keep
#   Pending Renewal            2,889   keep - operating, renewal not yet done
#   Licensed                   2,542   keep
#   Renewal Invoiced           1,614   keep - invoiced, still trading
#   Renewal Notification Sent      2   keep
#   Move in Progress             168   DROP - relocating, so its recorded
#                                      address is the one thing this map
#                                      depends on and the one thing in doubt
#   Close in Progress             26   DROP - closing
# Dropping 194 rows of 23,203. `homeoccind` is not used at all (constant).
STATUS_COLUMN = "jobstatusdesc"
STATUS_KEEP = frozenset({
    "Renewal Licensed", "Pending Renewal", "Licensed", "Renewal Invoiced",
    "Renewal Notification Sent",
})

# `point` is a WKT POINT string ("POINT (-114.07 51.04)"), populated on 100% of
# rows, so there is no geocoding step. `tradename` is blank on ZERO rows, so
# there is no name fallback and no personal-name exposure from one - the
# strongest position available short of a register with no name column at all.
POINT_COLUMN = "point"
NAME_COLUMN = "tradename"

# This register publishes no owner, agent or contact column, so unlike New
# York, Miami, Boston, Surrey and Toronto there is nothing to omit at the
# download boundary. Step 2 asserts the absence anyway, so the claim stays true
# if the register ever gains one.
FORBIDDEN_COLUMNS = ("ownername", "owner_name", "applicant", "phone",
                     "telephone", "email", "licenseholder", "clientname")

# --- Coordinate sanity ------------------------------------------------------

# Calgary's real extent, a little wider than the boundary so a genuine edge
# premises is not clipped by the sanity check itself.
CALGARY_BBOX = {
    "lat_min": 50.80,
    "lat_max": 51.25,
    "lon_min": -114.35,
    "lon_max": -113.85,
}
