"""Amsterdam-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

The Netherlands' first city, and the first built from TWO LAYERS OF DIFFERENT
KINDS: a live register of hospitality permits (named businesses, points) and
the national building register's (BAG) shop-class units (points, no name, no
activity). Both come from the city's own API with coordinates already on them,
so there is no geocoder and no join for the point - only an address join to
de-duplicate the two layers and to place the few permits with no point.
Brief: docs/build_briefs/amsterdam.md.
"""

from pathlib import Path

SLUG = "amsterdam"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "amsterdam" / "raw"
DATA_PROCESSED = ROOT / "data" / "amsterdam" / "processed"
OUTPUTS = ROOT / "outputs" / "amsterdam"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs - every one written by pipeline/amsterdam/fetch_sources.py, which
# records URL, bytes, sha256 and retrieval time in PROVENANCE_JSON.
PERMITS_JSON = DATA_RAW / "horeca_exploitatievergunning.json"
BAG_UNITS_JSON = DATA_RAW / "bag_verblijfsobjecten_winkelfunctie.json"
BAG_ADDRESSES_JSON = DATA_RAW / "bag_nummeraanduidingen.json"
BAG_STREETS_JSON = DATA_RAW / "bag_openbareruimtes.json"
BAG_PERMIT_LOOKUP_JSON = DATA_RAW / "bag_permit_address_lookup.json"
GTFS_ZIP = DATA_RAW / "gtfs-openov-nl.zip"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
OSM_RAIL_JSON = DATA_RAW / "osm_rail.json"
OSM_NEIGHBOURS_JSON = DATA_RAW / "osm_neighbour_gemeenten.json"

# --- Endpoints ---------------------------------------------------------------

# The city's DSO API. HAL JSON, paged with _pageSize and _links.next. It
# refuses a request without an Accept header, and a 5,000-row page of the BAG
# ends mid-stream ("Response ended prematurely", 2026-09-24), so pages are
# 1,000 rows with retries. An API key is OPTIONAL today and will become
# mandatory on an unset date - registering is an owner's act
# (docs/build_briefs/amsterdam.md, "MUST DO, later").
API_BASE = "https://api.data.amsterdam.nl/v1"
API_PAGE_SIZE = 1000
PERMITS_URL = f"{API_BASE}/horeca/exploitatievergunning/"
BAG_UNITS_URL = f"{API_BASE}/bag/verblijfsobjecten/"
BAG_UNITS_FILTER = {"gebruiksdoel.omschrijving": "winkelfunctie"}
BAG_ADDRESSES_URL = f"{API_BASE}/bag/nummeraanduidingen/"
BAG_STREETS_URL = f"{API_BASE}/bag/openbareruimtes/"
BAG_IN_BATCH = 100

# National GTFS, built by OVapi / Bliksem Labs from the operators' NDOV data.
# GVB publishes no standalone feed (gtfs.ovapi.nl/gvb/... is a 404,
# 2026-09-24), so the national file is read for GVB's routes only.
#
# WHICH NATIONAL FILE, AND WHY THIS ONE. GVB's data is CC0 at every level
# upstream (the concession annex, both NDOV lokets). But the README beside the
# usual `gtfs.ovapi.nl/nl/gtfs-nl.zip` grants only "You are free to use this
# data" and never says CC0, while `gtfs-openov-nl.zip` sits in a directory
# under the producer's own `LICENSE.TXT` - "These works are available under
# CC0 1.0 Universal." It is the same feed minus AVV and Thalys, neither of
# which runs in Amsterdam. Fetching it AVOIDS the question of what the README
# grants rather than answering it in the project's favour. Read by
# `licence-read`, 2026-09-24; see docs/data_sources.md.
GTFS_URL = "https://gtfs.openov.nl/gtfs-rt/gtfs-openov-nl.zip"
GTFS_AGENCY_ID = "GVB"

# --- Scope -------------------------------------------------------------------

# OSM relation 47811, "Amsterdam", admin_level 8, ref:gemeentecode 0363 - found
# by a BOUNDED name search (osm-rail: an unbounded one is global), and the only
# candidate. Weesp has been part of the gemeente since 2022-03-24. CBS's
# figure for the gemeente is ~245 km² including water.
OSM_BOUNDARY_RELATION = 47811
BOUNDARY_AREA_KM2 = (230, 260)
GEMEENTE_CODE = "0363"

# The gemeente polygon's own extent (4.729-5.108 E, 52.278-52.431 N - Weesp is
# the eastern end), padded slightly.
AMSTERDAM_BBOX = {"lat_min": 52.27, "lat_max": 52.44, "lon_min": 4.72, "lon_max": 5.12}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# Both layers publish RD New points. Kept only to read them; all geometry is
# done in the city's own UTM zone.
CRS_SOURCE = "EPSG:28992"
# UTM zone 31N: longitude ~4.89 falls in the 0-6 E band. Derived per city.
CRS_PROJECTED = "EPSG:32631"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope -----------------------------------------------------------

# OWNER'S CALL 2026-09-24: METRO AND TRAM. GVB's metro 50-54 and its 16 tram
# lines. The standing test leaves out trams that run over a metro (Milan,
# Prague), but Amsterdam's metro barely enters the canal ring, and Oslo's
# trams were kept on the same ground. Tram 3 is on GVB's 31 August map but
# runs no trip in the feed's window (to 2026-12-12), so it is not drawn. The
# heritage museum tram (EMA, OSM's "20") is not GVB's. NS trains are commuter
# rail, out as everywhere; ferries are out.
ROUTE_TYPES_RAIL = ("0", "1")        # basic GTFS: tram, metro
METRO_ROUTE_TYPE = "1"
LINE_ORDER = ("50", "51", "52", "53", "54",
              "1", "2", "4", "5", "6", "7", "12", "13", "14", "17", "19",
              "24", "25", "26", "27", "29")
LINE_NAMES = {ln: (f"Metro {ln}" if len(ln) == 2 and ln.startswith("5") else f"Tram {ln}")
              for ln in LINE_ORDER}

# A LINE'S REGULAR ROUTE is the stops it serves on MOST days of the feed's
# window, not what any one trip or date does. GVB runs up to 30 shapes per line
# in this window - short workings, weekend closures (metro 50 and 51 on 26-27
# September) and diversions for works (tram 7 on 24 September, tram 1 from
# October to mid-November) - so the most-used shape covers 11 of metro 50's 20
# stations, and any single date can be the odd one. Measured 2026-09-24.
REGULAR_ROUTE_MIN_DAY_SHARE = 0.5

# Sub-transit-line filters (docs/sub_transit_line_filters.md), because the
# owner's metro-and-tram call brings in ~200 tram stops a few hundred metres
# apart. Metro stations are the central corridor - always kept; each line's
# own two in-gemeente terminals kept; a stop shared by 2+ lines kept; the rest
# thinned to one per half mile along the line's own path, as San Francisco.
THIN_SPACING_MILES = 0.5

# Gate 1's floor: Paris's and Marseille's 200 m, deliberately not a new
# number - a dense tram network is genuinely closer than 400 m and still clears
# a platform-spaced set by an order of magnitude.
SPACING_MIN_M = 200.0

# Gate 3: English Wikipedia's "Amsterdam Metro" (read 2026-09-24, a SECONDARY
# source - GVB publishes no station count per line). 39 network-wide. No
# comparable per-line figure exists for the trams.
OPERATOR_STATION_COUNTS = {"Metro 50": 20, "Metro 51": 19, "Metro 52": 8,
                           "Metro 53": 14, "Metro 54": 15, "Metro (network)": 39}
OPERATOR_COUNTS_SOURCE = ("en.wikipedia.org/wiki/Amsterdam_Metro, read 2026-09-24 - "
                          "secondary; 50: 20, 51: 19, 52: 8, 53: 14, 54: 15, network 39")

# A GVB stop name is a STREET, not a place (the metro's Jan van Galenstraat
# and the tram stop of that name are 1.6 km apart). Platforms of one name
# within PLACE_LINK_M of each other are one place; a place wider than
# COLLAPSE_MAX_SPREAD_M stops the build.
PLACE_LINK_M = 300
COLLAPSE_MAX_SPREAD_M = 400

# --- Line colours --------------------------------------------------------------
#
# METRO: GVB's own `route_color` in the feed. TRAM: the feed carries none, and
# OSM's are unusable (seven lines share one orange, five have none), so they
# are read from GVB'S OWN MAP - `GVB_railnetwerk_31aug_2026.pdf`, linked from
# gvb.nl/plattegronden - as the fill of each line-number badge, the text inside
# each badge decoded through the PDF's own font encoding (2026-09-24). Line 3
# is on the map and not in service; the metro badges are not drawn as text.
#
# GVB REUSES COLOURS on lines that barely meet - 6 and 25 are one red, 19 and
# 29 one orange - and this project's check refuses two lines under Delta-E 10.
# Five lines are therefore shifted in HSL LIGHTNESS ONLY, hue and saturation
# kept, by the smallest step that clears 13 from every other line: the METRO
# keeps GVB's colour and the tram moves (Oslo's rule), and between two trams
# the lower number keeps it.
#   Tram 6   #e30613 -> #b1050f (L -0.10): 6.1 from Metro 53's #d81118
#   Tram 25  #e30613 -> #f70715 (L +0.04): the same red as 6, and 6.1 from 53
#   Tram 24  #00853e -> #009948 (L +0.04): 6.0 from Metro 50's #187a36
#   Tram 26  #6859a2 -> #5b4e8e (L -0.06): 9.5 from Tram 5's #7c6eb0
#   Tram 29  #ed6942 -> #f5ac96 (L +0.18): the same orange as 19, and near 7
GVB_MAP_COLOURS = {"1": "#e94f2d", "2": "#3aaa35", "4": "#ed6ea7", "5": "#7c6eb0",
                   "6": "#e30613", "7": "#f39872", "12": "#a69dcd", "13": "#afca0b",
                   "14": "#e71a84", "17": "#86bc25", "19": "#ed6942", "24": "#00853e",
                   "25": "#e30613", "26": "#6859a2", "27": "#00a295", "29": "#ed6942"}
LINE_COLOURS = {**GVB_MAP_COLOURS,
                "6": "#b1050f", "25": "#f70715", "24": "#009948", "26": "#5b4e8e",
                "29": "#f5ac96"}
# Metro colours are filled from the feed's route_color at step 1/3 time and
# checked against these, so a change in the feed stops the build.
METRO_FEED_COLOURS = {"50": "#187a36", "51": "#ff6600", "52": "#00adef",
                      "53": "#d81118", "54": "#fff200"}
LINE_COLOURS.update(METRO_FEED_COLOURS)

# Step 1 writes GVB's slice of the national feed here so step 3 does not read
# a 275 MB shapes.txt to draw 21 lines.
GVB_SHAPES_ZIP = DATA_PROCESSED / "gvb_rail_shapes.zip"
LINE_SHAPES_JSON = DATA_PROCESSED / "line_shapes.json"

# --- Business filtering ------------------------------------------------------

TAXONOMY_SYSTEM = "amsterdam_source"
RAW_CLASSIFICATION_COLUMN = "activity"
CITY_KEEP = "AMSTERDAM"   # kept for the scaffold's templates; both layers are gemeente-only

# PERMITS PAST THEIR END DATE ARE KEPT - a measured call, 2026-09-24, flagged
# for the owner. 128 of 4,092 permits carry an `einddatum` before the
# retrieval date, ALL of them between July and September 2026, and all still
# `Verleend`. Nothing that ended earlier is in the register at all, so the
# city prunes lapsed permits itself with a lag of about three months, and the
# 128 read as renewals in progress (La Madonnina on Rembrandtplein, Café De
# Walvis). `einddatum` ends the permit's TERM, not the business - unlike
# Prague's DATUKON, which ends the establishment. False drops them.
KEEP_PERMITS_PAST_END_DATE = True

# BAG status: only units in use. `Verblijfsobject gevormd` (planned, 575) and
# `Verbouwing verblijfsobject` (being rebuilt, 134) are not premises yet.
BAG_STATUS_KEEP = "Verblijfsobject in gebruik"
# OWNER'S CALL 2026-09-24: a shop-class unit that is ALSO registered as a
# dwelling is left off (757 of 10,898) - the likeliest to be a home rather than
# a shop, with nothing in open data to tell which. Prague's sole traders at
# their own seat are the precedent. Other mixes (office, assembly, industry)
# stay.
BAG_EXCLUDE_IF_ALSO = ("woonfunctie",)
