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

# TRAM RESCOPE BRANCH ONLY: stations.csv is written under processed/tram/ so
# the shared data folder's built file stays as master reads it. At landing,
# drop "tram" here and in STREETCAR_SHAPES_JSON and re-run steps 1 and 4.
STATIONS_CSV = DATA_PROCESSED / "tram" / "stations.csv"
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

# --- Streetcars (tram rescope; owner, 2026-10-13) ---------------------------
#
# The owner's list: the day streetcar routes, one label and legend row each
# ("Streetcar 501" on the map, "Streetcar 501 Queen" in the legend). The night
# routes run their day routes' streets and are not drawn. A route joining or
# leaving either set is a scope decision: pipeline/toronto/streetcars.py
# stops if the feed's streetcar routes are not exactly these two sets.
# docs/decisions_drafts/tram-rescope.md has the overlap test that brought
# them in (305 of 558 stops beyond every rapid-transit station's outer ring).
STREETCAR_LINES = {
    "501": "Queen", "503": "Kingston Rd", "504": "King", "505": "Dundas",
    "506": "Carlton", "507": "Long Branch", "508": "Lake Shore",
    "509": "Harbourfront", "510": "Spadina", "511": "Bathurst",
    "512": "St Clair",
}
STREETCAR_NIGHT_NOT_DRAWN = ("301", "303", "304", "305", "306", "310", "312")
STREETCAR_LINE_NAMES = {k: f"Streetcar {k}" for k in STREETCAR_LINES}
STREETCAR_LEGEND_NAMES = {k: f"Streetcar {k} {v}" for k, v in STREETCAR_LINES.items()}

# THREE OF THE ELEVEN ARE NOT DRAWN (owner, 2026-10-13: "follow those rules
# (8 not 11) note the drops and reasoning"). Both rules are
# docs/category_rules.md, "Station scope":
#   503 Kingston Rd, 507 Long Branch: CLOSED FOR WORKS. Every trip in the
#     feed's window (to 2026-10-31) is a replacement bus, 1,098 of 1,098 and
#     1,603 of 1,603, so the lines are drawn as the timetable runs: not at
#     all (Berlin's U6 Tegel branch, Prague's Flora).
#   508 Lake Shore: THE 15-MINUTE TEST. 35 trips, weekday peaks only, none
#     between 09:00 and 15:00 (Aarhus's converted railways).
# 512 St Clair runs streetcars east of Lansdowne and a replacement bus west
# of it; 506 Carlton's "506B" bus runs beside a streetcar that covers the
# whole route. Read on the cached feed and a re-pull of 2026-10-13, which
# agree. streetcars.py compares all of this with the feed and stops when a
# line returns, closes or changes frequency. Each value: the street-name
# prefixes whose stops are recorded as that line's own.
STREETCAR_CLOSED_FOR_WORKS = {
    "503": ("Kingston Rd", "Bingham Loop"),
    "507": ("Lake Shore Blvd West", "Long Branch Loop", "Humber Loop"),
}
STREETCAR_PART_CLOSED = {"512": ("St Clair Ave West", "St. Clair Ave West", "Gunns Loop")}
STREETCAR_INFREQUENT = ("508",)
STREETCAR_NOT_DRAWN_NEAR_M = 100.0

# STREETCAR COLOURS: THE PROJECT PALETTE. The TTC gives every streetcar route
# one red (route_color ED1C24), so eight lines cannot be told apart by it.
# Chosen 2026-10-13 from the sRGB cube in steps of 8, Lines 1 to 6 held on
# their colours above: 3:1 on both map pages, CIE76 >= 45 from every pin,
# >= 18 from every line within 500 m; each line takes the colour farthest
# from every line already chosen, the most crowded line first. Measured:
#   501 #608000  pins 45.0  nearest line 37.7 (506)
#   504 #00A800  pins 46.1  nearest line 37.9 (501)
#   505 #0050F8  pins 49.7  nearest line 38.6 (511)
#   506 #886010  pins 68.7  nearest line 37.7 (501)
#   509 #C870C8  pins 45.3  nearest line 36.2 (Line 4)
#   510 #F80028  pins 47.0  nearest line 45.0 (Line 5)
#   511 #A000F8  pins 79.9  nearest line 37.7 (Line 4)
#   512 #00A0C0  pins 45.2  nearest line 35.9 (Line 6)
# Re-run the search if a line returns (503, 507, 508) or a rapid-transit
# colour moves. The three lines not drawn hold no colour.
STREETCAR_COLOURS = {
    "501": "#608000", "504": "#00A800", "505": "#0050F8", "506": "#886010",
    "509": "#C870C8", "510": "#F80028", "511": "#A000F8", "512": "#00A0C0",
}

# Trips with this in the headsign are buses filed under a streetcar route.
STREETCAR_BUS_HEADSIGN = "Bus"

# A line's REGULAR route: the stop patterns each run by at least this share of
# the line's trips. Short turns and diversions under it add no stops.
STREETCAR_REGULAR_TRIP_SHARE = 0.10

# The feed names a streetcar stop per direction ("... at Spadina Ave East
# Side"), `parent_station` is empty, and 280 of 469 names sit on one stop id,
# so stops are grouped into places by DISTANCE, measured 2026-10-13 on 662
# stop ids (nearest other stop: median 37 m, 95th percentile 131 m):
#   within PLACE_LINK_M of each other, or
#   within PLACE_CROSS_M and sharing no line-and-direction (the far-side stop
#   of the other direction, or the crossing line's stop at one intersection).
# No merge may stretch a place past PLACE_MAX_SPREAD_M (the widest real
# crossing measured, Queen at Spadina with its Richmond stop, is 183 m).
STREETCAR_PLACE_LINK_M = 60.0
STREETCAR_PLACE_CROSS_M = 120.0
STREETCAR_PLACE_MAX_SPREAD_M = 200.0

# A streetcar place at a drawn rapid-transit station IS that station: it adds
# no station and moves none, and it resets the spacing count. Within
# ATTACH_M (40 stop ids measured under 150 m; "Queen St West at University
# Ave - Osgoode Station" is 38 m), or named for the station and within
# ATTACH_NAMED_M ("Spadina Station" is 162 m from the subway's point).
STREETCAR_ATTACH_M = 150.0
STREETCAR_ATTACH_NAMED_M = 400.0

# Sub-transit-line filters (docs/sub_transit_line_filters.md), as Amsterdam's
# trams: rapid-transit stations and each line's terminals kept, the rest one
# per half mile along the line's own stop sequence.
STREETCAR_THIN_SPACING_MILES = 0.5

# The 15-minute test (docs/category_rules.md, "Station scope"): the weekday
# 09:00 to 15:00 headway each line must hold, one direction.
STREETCAR_MAX_HEADWAY_MIN = 15.0

# Step 1 writes the line shapes it chose here; step 4 reads them.
STREETCAR_SHAPES_JSON = DATA_PROCESSED / "tram" / "streetcar_shapes.json"

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
# WIRED 2026-09-22, and finding it unused is what exposed a real bug. Step 1's
# collapse check compared `len(stations)` - which is this number, 110, before
# the boundary filter - against IN_CITY_STATIONS_EXPECTED, which is 108. So it
# printed a NOTE on EVERY run while this constant sat unread. Both now guard
# the quantity they are named for. The per-line check in `pipeline/stations.py`
# remains the stronger test and cannot cover either: those counts sum to 117,
# because an interchange counts once on each of its lines.
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
