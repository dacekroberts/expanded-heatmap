"""Toronto-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "toronto" / "raw"
DATA_PROCESSED = ROOT / "data" / "toronto" / "processed"
OUTPUTS = ROOT / "outputs" / "toronto"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
BUSINESSES_GEOCODED_CSV = DATA_PROCESSED / "businesses_geocoded.csv"

# Raw inputs, all public, all City of Toronto CKAN (OGL - Toronto).
#
#   Business: Municipal Licensing & Standards. `datastore_search_sql` 404s on
#   this portal, and `datastore_search` pages at 32k, so the CSV dump endpoint
#   is what this build uses:
#     curl -sL "https://ckan0.cf.opendata.inter.prod-toronto.ca/datastore/dump/169e90ba-3ae0-43dd-8b2f-919e87002f50?format=csv" -o business_licences.csv
#
#   Address points: the One Address Repository, 525,440 points, SAME licence.
#   This is Toronto's answer to having no coordinates at all - Canada has no
#   national bulk geocoder, and this city is the only one of six that needed
#   one. The 4326 CSV, ~183 MB:
#     curl -sL "<resource 64d4e54b-738f-4cd9-a9e7-8050fac8a52f>" -o address_points.csv
#
#   GTFS: the AGENCY feed via the City's own CKAN package
#   `ttc-routes-and-schedules`. **NOT the Mobility Database mirror**, which was
#   three months expired and contained NO SUBWAY AT ALL - the single worst
#   catalogue failure this project has found, and the reason
#   `scripts/screen_rail.py` prints feed expiry.
#
#   Boundary: `regional-municipal-boundary`, a zipped shapefile (geopandas
#   reads the zip directly). 1 feature, 641.4 km2 against Toronto's ~630 km2
#   of land.
GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "business_licences.csv"
ADDRESS_POINTS_CSV = DATA_RAW / "address_points.csv"
CITY_BOUNDARY_ZIP = DATA_RAW / "toronto_boundary_wgs84.zip"

CKAN_DOMAIN = "ckan0.cf.opendata.inter.prod-toronto.ca"
BUSINESS_RESOURCE_ID = "169e90ba-3ae0-43dd-8b2f-919e87002f50"
BUSINESS_URL = (f"https://{CKAN_DOMAIN}/datastore/dump/"
                f"{BUSINESS_RESOURCE_ID}?format=csv")
ADDRESS_POINTS_URL = (
    f"https://{CKAN_DOMAIN}/dataset/"
    "address-points-municipal-toronto-one-address-repository/resource/"
    "64d4e54b-738f-4cd9-a9e7-8050fac8a52f/download/"
    "Address%20Points%20-%204326.csv")
GTFS_URL = (f"https://{CKAN_DOMAIN}/dataset/"
            "7795b45e-e65a-4465-81fc-c36b9dfff169/resource/"
            "cfb6b2b8-6191-41e3-bda1-b175c51148cb/download/"
            "opendata_ttc_schedules.zip")
CITY_BOUNDARY_URL = (f"https://{CKAN_DOMAIN}/dataset/"
                     "841fb820-46d0-46ac-8dcb-d20f27e57bcc/resource/"
                     "41bf97f0-da1a-46a9-ac25-5ce0078d6760/download/"
                     "toronto-boundary-wgs84.zip")

SOURCE_ENCODING = "utf-8"

# THREE personal columns, not one, and the count is the point: the Canada
# profile recorded `Client Name` and missed `Business Phone` and `Business
# Phone Ext.` They are dropped the moment the file is read and asserted gone
# before anything else runs. `Operating Name` is blank on only 0.8% of rows, so
# there is no fallback pressure and no excuse for loading any of them.
FORBIDDEN_COLUMNS = ("Client Name", "Business Phone", "Business Phone Ext.")

NAME_COLUMN = "Operating Name"
ADDRESS_COLUMN = "Licence Address Line 1"
CATEGORY_COLUMN = "Category"
LICENCE_KEY = "Licence No."
WARD_COLUMN = "Ward"
CANCEL_DATE_COLUMN = "Cancel Date"

BOUNDARY_AREA_KM2_RANGE = (550.0, 750.0)   # measured 641.4

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 17N: the longitude (~-79.38) falls in the -84 to -78 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32617"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# FIVE routes: the three subway lines at `route_type 1`, plus the two LRT lines
# which the TTC codes as `route_type 0` ALONGSIDE 18 streetcar routes. The
# split is a regex, not a research problem: the LRT lines are named `Line 5
# Eglinton` and `Line 6 Finch West` while every streetcar carries a street name
# (Bathurst, Carlton, Dundas, King, Queen...). `^Line \d` separates them.
#
# Streetcars are EXCLUDED, and that is a scope decision rather than an
# oversight: adding all 18 takes the network to 913 platforms / 706 names and
# makes Toronto a street-running city like San Francisco, needing
# docs/sub_transit_line_filters.md. This map is the rapid-transit network.
SUBWAY_ROUTE_TYPE = "1"
LRT_ROUTE_TYPE = "0"
LRT_NAME_REGEX = r"^Line \d"
ROUTE_IDS_EXPECTED = 5
LINE_NAMES = {
    "1": "Line 1 Yonge-University",
    "2": "Line 2 Bloor-Danforth",
    "4": "Line 4 Sheppard",
    "5": "Line 5 Eglinton",
    "6": "Line 6 Finch West",
}

# LINE COLOURS: FOUR OF FIVE ARE THE TTC'S OWN, and only one needed changing.
#
# Measured against the three business-category pin colours this map spends,
# with this project's ~45 Delta-E working threshold (see the add-city skill):
#
#   Line 1  #D5C82B  yellow   min 69.2  KEPT, the TTC's own
#   Line 2  #008000  green    min 37.2  FAILS against Personal services
#   Line 4  #B300B3  purple   min 55.1  KEPT
#   Line 5  #FF8000  orange   min 74.3  KEPT
#   Line 6  #808080  grey     min 53.0  KEPT
#
# Only Line 2's green collides - the same `008000` that failed for Edmonton's
# Valley Line, against Personal services' `#1baf7a`. Darkened to a forest green
# that keeps the line readable as green: `#173F1B`, min Delta-E 48.2. Nothing
# else is touched, so Toronto looks like the TTC's own map almost everywhere.
#
# Worst line-vs-line separation is 42.2 (Line 2 against Line 6's grey, both
# muted); acceptable because every line carries an on-map label AND a legend
# entry. Separation is an INTRA-city constraint: Line 5's orange is near
# Miami's Metrorail orange and that costs nothing, because no map shows both.
LINE_COLOURS = {
    "1": "#D5C82B",   # Line 1 Yonge-University - TTC's own
    "2": "#173F1B",   # Line 2 Bloor-Danforth - TTC's 008000 darkened, see above
    "4": "#B300B3",   # Line 4 Sheppard - TTC's own
    "5": "#FF8000",   # Line 5 Eglinton - TTC's own
    "6": "#808080",   # Line 6 Finch West - TTC's own
}

# One shape per line, the most-used trip shape. **Checked against EXTENT as
# well as trip count**, because Edmonton's Metro Line mode drew only half that
# line and Miami's Metrorail needed a tuple. Here the two agree - each line's
# most-used shape is also its widest - so the plain mode is correct:
#
#   Line 1  1124986    254 of 1,900 trips  633 pts  Vaughan/Finch to Union
#   Line 2  1125629    293 of 2,206 trips  465 pts  Kipling to Kennedy
#   Line 4  1125751    882 of 1,761 trips   54 pts
#   Line 5  1125772    649 of 1,330 trips  302 pts
#   Line 6  1125786    542 of 1,118 trips  160 pts
#
# Lines 1 and 2 publish 62 and 80 shapes because the TTC ships short-turn and
# single-track working variants; the mode is still the full alignment.
LINE_SHAPES = {
    "1": "1124986",
    "2": "1125629",
    "4": "1125751",
    "5": "1125772",
    "6": "1125786",
}
LINE_LABEL_ENDS = {}

# PLATFORM-TO-STATION COLLAPSE, AND THIS CITY IS WHY THE PROJECT DISTRUSTS
# STATION COUNTS AT ALL.
#
# `parent_station` is NOT POPULATED - not on one stop - so the best of this
# project's four collapse mechanisms is unavailable and the names must be
# munged. Every Toronto figure before 2026-09-21 rested on 234 "stations" that
# were PLATFORMS, and the first correction of that error then made a smaller
# one of the same kind.
#
# **TWO NAMING CONVENTIONS LIVE IN THIS ONE FEED**, which is what the first
# correction missed:
#     subway HYPHENATES      "Finch Station - Southbound Platform"
#     LRT DOES NOT           "Aga Khan Park & Museum Station Eastbound Platform"
#     and one bare form      "Finch West Station LRT Platform"
# A pattern written for the subway leaves all 86 LRT platforms uncollapsed.
# Three stations also appear TWICE, once plain and once suffixed `- Subway`
# (`Kipling Station` against `Kipling Station - Subway`, 33 m apart).
#
# MEASURED 2026-09-21, and checked against the operator's own counts rather
# than trusted:
#     subway only   148 platforms -> 72 stations   (TTC: 38+31+5 less 3 = 71)
#     subway + LRT  234 platforms -> 111 stations  (TTC: ~110)
# Nearest-neighbour median 632 m at 111. The intermediate 160 that leaves the
# LRT uncollapsed sits at 70 m, which is platform spacing - so the spacing
# diagnostic catches the error the name check cannot.
# ORDER MATTERS: the "Towards" forms must be stripped BEFORE the plain
# "...bound Platform$" ones, because those anchor on end-of-string and so leave
# a directional terminus untouched.
STATION_STRIP_PATTERNS = (
    # Union Station's four platforms name the DESTINATION, not just the
    # direction: "Union Station - Northbound Platform Towards Finch" against
    # "... Towards Vaughan Metropolitan Centre". Found on the first real run of
    # this step - without it Union counts TWICE and Line 1 reads 39 stations
    # against the TTC's own 38.
    r"\s*-\s*\w+bound Platform Towards .*$",
    r"\s+\w+bound Platform Towards .*$",
    r"\s*-\s*\w+bound Platform\s*$",    # subway, hyphenated
    r"\s+\w+bound Platform\s*$",        # LRT, not hyphenated
    r"\s+LRT Platform\s*$",             # Finch West Station LRT Platform
    r"\s*-\s*Platform\s*\d*\s*$",
    r"\s+Platform\s*\d*\s*$",
    r"\s*-\s*Subway\s*$",               # the duplicate-name suffix
)
# MEASURED on the first real run, and every per-line count now agrees with the
# TTC's own published figures, which is the check that matters:
#     Line 1  38   Line 2  31   Line 4  5   Line 5  25   Line 6  18
# 234 platforms -> 110 stations -> 108 in-city. The two outside are on Line 1's
# extension into York Region: Highway 407 (876 m out) and Vaughan Metropolitan
# Centre (2,113 m) - San Diego's situation, and they are recorded in
# outputs/toronto/excluded_stations.csv rather than quietly dropped.
#
# 110 is one above a strict TTC station count because the feed names the
# Bloor-Yonge interchange as two stops, "Bloor Station" and "Yonge Station",
# 78 m apart, where the TTC signs and counts it once. Left unmerged: they are
# genuinely different platforms on different lines, the per-line counts are
# exact either way, and merging on proximity rather than on a naming rule is
# how a real adjacent pair gets destroyed.
PLATFORMS_EXPECTED = 234
# NOT ASSERTED ANYWHERE, unlike the three constants around it - noticed
# 2026-09-22 by `check_stale_claims.py` category D, which reports config
# constants no script reads. What DOES verify the collapse is
# `pipeline/stations.py`'s per-line check against the TTC's own published
# figures, and that is the stronger test. But it cannot cover this number:
# the per-line counts sum to 117, not 110, because an interchange counts once
# on each of its lines. So the total below is currently a record rather than a
# check. Wiring it is a one-line comparison in step 1 and belongs to whoever
# owns this city, not to a documentation sweep.
STATIONS_COLLAPSED_EXPECTED = 110
IN_CITY_STATIONS_EXPECTED = 108
SUBWAY_ONLY_STATIONS_EXPECTED = 71
STATION_SPACING_MEDIAN_M_MIN = 400.0
PLATFORM_SPACING_MEDIAN_M_MAX = 150.0

# GATE 3, and the only check here that is outside the data: what the TTC itself
# publishes. Toronto's earlier counts of 118 and 77 were internally consistent
# and agreed with nothing - this is what would have caught them on the first
# pass rather than the third. Line 1 has 38 stations, Line 2 31, Line 4 5,
# Line 5 25 and Line 6 18.
PUBLISHED_STATIONS_PER_LINE = {
    "Line 1 Yonge-University": 38,
    "Line 2 Bloor-Danforth": 31,
    "Line 4 Sheppard": 5,
    "Line 5 Eglinton": 25,
    "Line 6 Finch West": 18,
}

# Toronto has NO non-revenue rail stops - `pickup_type`/`drop_off_type` are
# boardable on every rail stop_time. Checked rather than assumed, because
# Edmonton's feed hid two garages and a tail track among its 33 stations.
NON_REVENUE_STOPS_EXPECTED = 0

# The agency feed carries no `feed_info.txt`, so there is no validity window to
# check - the same as Calgary's and unlike Edmonton's. The mirror's expiry is
# what mattered here, and this build does not use the mirror.
GTFS_CHECK_FEED_WINDOW = False

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "toronto_mlscategory"
RAW_CLASSIFICATION_COLUMN = "Category"

# IN-CITY IDENTIFICATION: THE BOUNDARY POLYGON, NOT `MUNICIPALITY_NAME`.
#
# The build brief says the address repository "returns `MUNICIPALITY_NAME`, so
# it doubles as the in-city filter". **It does not filter anything**, and
# reading it as a filter would have been the worst error available here.
# MEASURED 2026-09-21 - the field holds the SIX PRE-1998 municipalities that
# amalgamated into the City of Toronto:
#
#     former Toronto  156,172      Etobicoke   73,807
#     Scarborough     123,897      York        32,463
#     North York      114,963      East York   24,138
#
# So "Toronto" as a value is 30% of the repository, and matching it would have
# silently dropped Scarborough, North York and Etobicoke - about 70% of the
# city, including most of Line 2's eastern and western halves. This is Los
# Angeles' `CITY_KEEP` trap exactly (its field holds postal community names, so
# an exact match keeps about half the city), and the fix is the same: use the
# authoritative geometry.
#
# Every point in this repository is inside the City of Toronto, so the join
# needs no municipal filter at all; the boundary polygon is the check that a
# geocoded coordinate landed where it claims.
ADDRESS_MUNICIPALITY_COLUMN = "MUNICIPALITY_NAME"
MUNICIPALITY_VALUES_EXPECTED = frozenset({
    "former Toronto", "Scarborough", "North York", "Etobicoke", "York",
    "East York",
})

# --- Geocoding (step 3, which is why the map is step 4) --------------------
#
# Toronto is the ONLY city of the six Canadian candidates that genuinely needs
# a geocoding step: `Licence Address Line 1` is a street address and there is
# no coordinate field of any kind. There is no national Canadian geocoder, so
# the answer is a join against the City's own address points.
#
# **THE NORMALISATION THAT MATTERS IS ONE LINE, AND IT IS NOT STREET
# NORMALISATION.** The brief's stated obstacle was abbreviation handling. It is
# not: the register writes the UNIT into the address line (`280 SPADINA AVE,
# #308`, `1835 EGLINTON AVE W, 2ND FLR` - 20,091 such rows) and the address
# repository carries no units. Measured 2026-09-21:
#     raw case+whitespace join                48.1% of all rows
#     everything from the first comma dropped 73.1% of all rows
#                                             92.8% of STOREFRONT rows
# The 71.4% recorded in the brief was measured across all 159,872 licence rows,
# more than half of which are person-licences with no premises address (tow
# truck owners, master plumbers, taxicab owners). **Read it on the storefront
# subset, which is the only one this map uses: 92.8%.**
ADDRESS_UNIT_PATTERN = r",.*$"
ADDRESS_TRAILING_UNIT_PATTERN = (
    r"\s+(FL|FLR|FLOOR|BSMT|REAR|UNIT|STE|SUITE)\s*\d*\s*$")
GEOCODE_MATCH_RATE_MIN = 0.85   # storefront rows; measured 0.928

# --- Sanity bounds, from the boundary's real extent plus a margin ---------
TORONTO_BBOX = {
    "lat_min": 43.55,
    "lat_max": 43.88,
    "lon_min": -79.67,
    "lon_max": -79.09,
}
