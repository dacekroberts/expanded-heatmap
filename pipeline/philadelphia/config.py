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
# The last two columns come from the City's property register, joined
# server-side on the licence's parcel id (94% of licences match). They exist to
# answer one question the address text cannot: is this "business" someone's
# home? The unit-indicator test in scripts/check_personal_exposure.py only
# fires on an APT/FL/RM/# and so cannot see a detached house, which is why this
# city first measured 0.00% residential.
#
# `homestead_exemption` is the sharp one: Philadelphia grants it only on an
# owner's PRIMARY RESIDENCE, so it is a claim the owner made to the City rather
# than an inference. It comes back as a boolean; the exemption amount is not
# downloaded because only its presence matters.
#
# Neither column is ever published - the rendered map emits only name,
# category, station and ring - and no mailing address is downloaded at all
# (tested 2026-09-21: matching it against the premises flagged 41.9% of pins
# and has no discriminating power).
BUSINESSES_SELECT = (
    "b.licensenum, b.licensetype, b.business_name, b.legalentitytype, "
    "b.address, b.unit_type, b.unit_num, b.zip, b.council_district, "
    "ST_X(b.the_geom) AS longitude, ST_Y(b.the_geom) AS latitude, "
    "p.category_code_description AS parcel_landuse, "
    "(COALESCE(p.homestead_exemption, 0) > 0) AS parcel_owner_occupied"
)
BUSINESSES_FROM = (
    "business_licenses b "
    "LEFT JOIN opa_properties_public p ON b.opa_account_num = p.parcel_number"
)

# Land-use categories that are purely residential, so a licensed business at
# one is probably operating from a home.
#
# MIXED USE IS DELIBERATELY NOT HERE, and neither is APARTMENTS > 4 UNITS.
# Mixed use is Philadelphia's signature storefront - a rowhouse with a shop
# below and a flat above, 3,378 mapped pins, whose owner routinely claims the
# homestead exemption on it (162 of them). And "residential" parcels carry
# ground-floor commercial in quantity: 147 thirty-plus-seat restaurants sit on
# APARTMENTS > 4 UNITS parcels and 92 on MULTI FAMILY. Treating land use alone
# as a privacy signal would delete hundreds of real storefronts to remove a few
# dozen homes, which is why the filter in step 2 pairs it with a name and
# entity-type test rather than acting on it alone.
PARCEL_RESIDENTIAL = frozenset({
    "SINGLE FAMILY",
    "GARAGE - RESIDENTIAL",
    "VACANT LAND - RESIDENTIAL",
})

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
#   G  319735 is the G1 Richmond-Westmoreland - 63rd-Girard; 319733 is its
#      short branch from the Frankford-Delaware loop, the same direction, which
#      joins Girard Av at Frankford Av (see BRANCH_SHAPES).
LINE_SHAPES = {
    "L": "319893",
    "B": ("319850", "319877"),
    "T": ("319740", "319746", "319768", "319779", "319804"),
    "G": ("319735", "319733"),
}

# A route's branch that its most-used shape does not run, read by step 1 as a
# second shape in the SAME direction as that most-used shape. Only the stops
# the main shape lacks are taken from it, plus the junction they leave from,
# so the shared trunk is thinned once, not twice.
#   G1  319733: Frankford-Delaware loop - Girard Av, westbound, 125 of the
#       feed's 840 G1 trips (2026-10-01). Its own stops are Frankford Av &
#       Delaware Av Loop and Frankford Av & Richmond St (Frankford-Delaware and
#       Richmond-Frankford in SEPTA's and Wikipedia's stop lists); it joins the
#       main line at Girard Av & Frankford Av.
BRANCH_SHAPES = {
    "G1": ("319733",),
}

# --- Stations closed for works (docs/category_rules.md, "Station scope") ----
# Drawn as the timetable runs (owner, 2026-09-29; Berlin's U6, Sacramento's
# Township 9): a station the feed does not serve is not drawn and gets no ring;
# step 1 lists it in excluded_stations.csv as closed for works with its
# reopening date, and STOPS once the feed serves it again.
#
# 11th St (L): SEPTA closed it on 5 September 2026 for its accessibility
# rebuild (two elevators, ADA compliance) and expects it back on 30 August
# 2027; L trains run through without stopping. SEPTA, "SEPTA to Break Ground
# on Accessibility Project at 11th Street Station", 2026-08-06 (septa.org/news/
# 11th-st-station-accessibility-project/): "closed to the public from September
# 5, 2026 through August 30, 2027". The feed of 2026-09-21 has no stop for it.
# Its position is OpenStreetMap's station node (ODbL, already credited on the
# map), since the feed no longer carries one.
CLOSED_FOR_WORKS = {
    "11th St": {
        "line": "L1",
        "reason": ("Market-Frankford Line, closed for works (accessibility "
                   "rebuild) from 5 September 2026, reopening 30 August 2027 "
                   "(SEPTA)"),
        "latitude": 39.9517977,
        "longitude": -75.1583456,
        "position_source": ("OpenStreetMap node 5372090220 (railway=station, "
                            "'11th Street', SEPTA), read 2026-10-01"),
    },
}
# A feed L stop this close to a closed station means SEPTA serves it again.
CLOSED_REOPEN_METRES = 100.0

# Only the trolley groups are street-running and need thinning; L and B are
# grade-separated with 681-711 m median spacing and are kept whole.
THINNED_GROUPS = frozenset({"T", "G"})

# --- Gate 3: the operator's own per-line station counts ----------------------
# Whole lines, BEFORE the city-limits cut (the L's Millbourne and 69th St count
# here) and BEFORE the T and G thinning: step 1's per-group union of the stops
# on each route's representative trip, which is one direction. An interchange
# counts once on each line it serves. Keyed as step 1 keys its line groups.
OPERATOR_STATION_COUNTS = {
    # 28 stations, less 11th St, closed by SEPTA from 2026-09-05 to 2027-08-30
    # for its accessibility rebuild (L trains run through). Not in this feed;
    # recorded as closed for works (CLOSED_FOR_WORKS).
    "L": 27,
    # 22 on the B1 Fern Rock - NRG, plus the B3 Ridge Spur's own Chinatown and
    # 8th-Market (its Fairmount and Girard are the B1's; Spring Garden on the
    # spur has been closed since 1989).
    "B": 24,
    # The T's Center City tunnel only - the part of the line that is never
    # thinned: 8 underground stations plus the 36th St and 40th St portals is
    # 10; less the 36th St portal, a T1-only surface stop that is not in
    # SUBWAY_STATION_NAMES and is thinned with the T1's street stops. Counted
    # as the T stops that are in SUBWAY_STATION_NAMES. The branches: see
    # OPERATOR_COUNTS_GAP.
    "T (Center City tunnel)": 9,
    # 64 stop rows, less the 5 served eastbound only (62nd-Girard, 61st-Girard,
    # Lancaster-Girard, Poplar-26th, Stillman-Poplar), since step 1 reads one
    # direction: 59. That includes Richmond-Frankford and Frankford-Delaware,
    # the short branch to the Frankford-Delaware loop, which step 1 reads from
    # BRANCH_SHAPES (matched 2026-10-01; it read 57 before the branch was added).
    "G": 59,
}
OPERATOR_COUNTS_SOURCE = (
    "Secondary, all en.wikipedia.org, read 2026-10-01: L (SEPTA Metro) infobox "
    "'28 (1 temporarily closed)', with SEPTA's own 11th St closure dates "
    "(septa.org news, 2026-08-06); Broad Street Line infobox 24; "
    "T (SEPTA Metro) infobox '8 underground stations 2 surface level "
    "stations'; G (SEPTA Metro) infobox '64 stops' and its stops table, read "
    "row by row (EB/WB marks). SEPTA's own route pages render their stop lists "
    "only in a browser."
)
OPERATOR_COUNTS_GAP = (
    "The T's five street-running branches (T1-T5): no per-branch stop count "
    "is published that is independent of SEPTA's GTFS, which this build reads. "
    "Looked for on 2026-10-01 in en.wikipedia.org/wiki/T_(SEPTA_Metro) (route "
    "table gives lengths, not stops) and SEPTA's route pages (stop lists drawn "
    "from the same feed, browser-only). The tunnel the branches share is "
    "checked above."
)

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
#
# The third is the G's own junction with its Frankford-Delaware branch: the
# branch's westbound stop "Frankford Av & Girard Av" (stop 481) is 13 m from
# the main line's "Girard Av & Frankford Av" (stop 20991) - one stop, counted
# once in the operator's stop list, at the corner both directions share.
STATION_NAME_ALIASES = {
    "Girard Av & Front St": "Front-Girard",
    "Girard Av & Broad St": "Broad-Girard",
    "Frankford Av & Girard Av": "Girard Av & Frankford Av",
}

# --- Business filtering ------------------------------------------------

# No city filter: this is the City of Philadelphia's own licence register, so
# every row is by definition a Philadelphia licence. Step 2 cross-checks the
# coordinates against the boundary polygon instead.
CITY_KEEP = None

# Encoding of this city's RAW source files, declared rather than inferred.
# pandas defaults to UTF-8 and raises on anything else - safe, but it leaves
# the next person to guess, and reaching for latin-1 to silence a
# UnicodeDecodeError corrupts accented names without ever failing. Declaring it
# makes the choice reviewable and part of the provenance. See the encoding rule
# in docs/data_sources.md; non-US cities are where this bites.
SOURCE_ENCODING = "utf-8"

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

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3600188022)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {
    "Lantern Theater Company": "a working theatre with its own article, named for its company",
    "Suzanne Roberts Theatre": "a theatre with its own article; only its alternative name carries the company",
    "The Library Company": "a historic library and museum with its own article",
}
PLACE_DROPPED = {
    "relation/10425740": "'Allen Lane', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/74661366": "'Artillery Shed', a description standing in for a name (owner, 2026-10-13)",
    "way/344417364": "'Autism Rec', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "node/9625262199": "'Barn Site', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/6157775445": "'Bear Country', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/707835658": "'Building 1', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/498593282": "'Building 10', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835659": "'Building 122', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707489046": "'Building 14', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/498593285": "'Building 15', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707489043": "'Building 17', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/498593278": "'Building 18', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707497022": "'Building 20', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707489045": "'Building 21', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707497027": "'Building 23', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835678": "'Building 26', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835615": "'Building 40', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707504506": "'Building 44', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/74661382": "'Building 542', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707504488": "'Building 545', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835620": "'Building 56', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/428152406": "'Building 567', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707490255": "'Building 571', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707504484": "'Building 6', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707497026": "'Building 602', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/607473252": "'Building 611', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707504511": "'Building 615', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/607473251": "'Building 624', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835617": "'Building 626', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707504508": "'Building 633', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707489054": "'Building 634', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835654": "'Building 640', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707504497": "'Building 643', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707490257": "'Building 646', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707504501": "'Building 662', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835664": "'Building 679', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/74661384": "'Building 694', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/498593283": "'Building 7', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/428152407": "'Building 712', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707504499": "'Building 745', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "relation/5484652": "'Building 75', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707497032": "'Building 754', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835641": "'Building 76', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/74661385": "'Building 763', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707490230": "'Building 772', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835636": "'Building 80', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/607473253": "'Building 83', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835680": "'Building 87', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707497028": "'Building 93', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "relation/10426060": "'Chestnut Hill East', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "relation/10425746": "'Chestnut Hill West', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/360777744": "'Columns and Capital from Amman Jordan', an exhibit inside a venue, which keeps its own row (owner, 2026-10-13)",
    "way/865756674": "'Esplanade', a bare type word for a name (owner, 2026-10-13)",
    "way/1147935165": "'Ferry Slip', a description standing in for a name (owner, 2026-10-13)",
    "way/239250013": "'Hospital', a description standing in for a name (owner, 2026-10-13)",
    "relation/9214361": "'Ivy Ridge', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/797191481": "'LandI North District Office', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/6169638906": "'Lock 70', abandoned by its own tags (owner, 2026-10-13)",
    "way/773890746": "'Log Cabin', a bare type word for a name (owner, 2026-10-13)",
    "way/1144344049": "'Main Magazines', a description standing in for a name (owner, 2026-10-13)",
    "way/1148991647": "'Marine Railway', a placeholder standing in for a name",
    "node/7124949158": "'Monastery Our Lady Mercy', a religious residence",
    "way/250892607": "'Mural Lofts', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "way/74661359": "'Officer's Quarters', a description standing in for a name (owner, 2026-10-13)",
    "way/787208677": "'Orthodox Street Parcel', a description standing in for a name (owner, 2026-10-13)",
    "node/6157776190": "'Outback Outpost', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/707489053": "'Pier 1', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707489049": "'Pier 2', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707489056": "'Pier 4', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707489050": "'Pier 5', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707489058": "'Pier 6', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707489064": "'Pier 6A', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835657": "'Quarters B', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835622": "'Quarters C', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835663": "'Quarters K', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835633": "'Quarters L', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835681": "'Quarters M', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835685": "'Quarters M1', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835624": "'Quarters M2', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835649": "'Quarters M3', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835613": "'Quarters M4', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835619": "'Quarters M5 & M6', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835638": "'Quarters M7', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835662": "'Quarters N', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835666": "'Quarters O', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/707835674": "'Quarters P', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/963721321": "'Richmond-Westmoreland Streets Loop', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/32121517": "'Rose Garden', a bare type word for a name (owner, 2026-10-13)",
    "relation/10425739": "'Saint Martins', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/1148986182": "'Seaplane Ramp', a description standing in for a name (owner, 2026-10-13)",
    "node/6944055387": "'Sisters of IHM', a religious residence",
    "way/74661358": "'Soldier's Barracks', a description standing in for a name (owner, 2026-10-13)",
    "node/9625262200": "'Spring House Site', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "way/60944305": "'St. Bridget Rectory', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/1144344051": "'Torpgioo Casemate', a description standing in for a name (owner, 2026-10-13)",
    "relation/10426058": "'Wyndmoor', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/67689754": "'Arrivals Road', a description standing in for a name (owner, 2026-10-13)",
    "way/387213403": "'Arrivals Road', a description standing in for a name (owner, 2026-10-13)",
    "way/492428624": "'Arrivals Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465250": "'Arrivals Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465252": "'Arrivals Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465255": "'Arrivals Road', a description standing in for a name (owner, 2026-10-13)",
    "way/900272531": "'Arrivals Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1098808302": "'Arrivals Road', a description standing in for a name (owner, 2026-10-13)",
    "way/39224274": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/387213404": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/491678815": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/492440340": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/492471875": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/492471876": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465235": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465236": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465237": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465238": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465239": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465240": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465243": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465246": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465260": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568465262": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/925236538": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/925236539": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1096251516": "'Departures Road', a description standing in for a name (owner, 2026-10-13)",
    "way/145467657": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/925215765": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/925221358": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/988030889": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1034136403": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1034136404": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1034136405": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1034136406": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1034136407": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1096325409": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1096325410": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1096489393": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1096489394": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1096489395": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1098756527": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1098756528": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1098756529": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1228478065": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1531460089": "'Garage Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/137469165": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/492471873": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520146": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520149": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520159": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520160": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520161": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520162": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520163": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520164": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520165": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520166": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520167": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520168": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/568520169": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/925232802": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/925232803": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1227510068": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1227510069": "'South Commercial Vehicles Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1226649939": "'Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1226649940": "'Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/552651222": "'Septa Driveway', a driveway described, not a street's name",
    "way/1180057778": "'Ramp', a bare type word for a name (owner, 2026-10-13)",
    "way/1180065746": "'Ramp', a bare type word for a name (owner, 2026-10-13)",
    "way/12167499": "'Krewstown Road Ramp', a description standing in for a name (owner, 2026-10-13)",
    "way/728199398": "'Vine Street Ramp', a description standing in for a name (owner, 2026-10-13)",
    "way/728199399": "'Vine Street Ramp', a description standing in for a name (owner, 2026-10-13)",
    "way/12115532": "'North Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1424715277": "'North Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1424718866": "'North Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1101822585": "'Traffic Circle', a description standing in for a name (owner, 2026-10-13)",
    "way/1268526118": "'Traffic Circle', a description standing in for a name (owner, 2026-10-13)",
    "way/1268526119": "'Traffic Circle', a description standing in for a name (owner, 2026-10-13)",
    "way/1268526120": "'Traffic Circle', a description standing in for a name (owner, 2026-10-13)",
    "way/479621019": "'columbus square park path', a description standing in for a name (owner, 2026-10-13)",
    "way/12110478": "'West Streetella Street', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/39228052": "'West Oregon Vare Avenue', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/626575006": "'West Oregon Vare Avenue', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/464797841": "'3000 Hedley Street', a type or model word standing in for a name (owner, 2026-10-13)",
    "way/293292962": "'Connector Trail', a description standing in for a name (owner, 2026-10-13)",
    "way/50108116": "'Grays Ferry Avenue Approach', a description standing in for a name (owner, 2026-10-13)",
    "way/12115279": "'Market Street', not yet open: highway=construction",
    "way/262962068": "'Market Street', not yet open: highway=construction",
    "way/424080774": "'Market Street', not yet open: highway=construction",
    "way/43061458": "'Frankford Avenue', not yet open: highway=construction",
    "way/12133522": "'East Sergeant Street', not yet open: highway=construction",
    "way/442519328": "'East Huntingdon Street', not yet open: highway=construction",
    "way/12173437": "'Lindbergh Boulevard', not yet open: highway=construction",
    "way/1320671075": "'Lindbergh Boulevard', not yet open: highway=construction",
    "way/49887112": "'Mausoleum Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/49887111": "'Spring Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1133157117": "'Spring Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/49887117": "'Main Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/997748618": "'Main Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1126408952": "'Main Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60427886": "'Centre Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/352414107": "'Centre Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/352414095": "'Poplar Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/352414097": "'Cherry Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/352414099": "'Elder Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/352414102": "'Ellm Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/352414105": "'Oakland AVenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/736561024": "'Willow Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/741783906": "'Dogwood Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/741783908": "'Damon Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1132608532": "'Tacony Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1133617032": "'Fairview Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1133617034": "'Thorn Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60427681": "'Bristol Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/69200475": "'Bristol Street', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/69200476": "'Cayuga Street', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/12197587": "'Jamestown Alley', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1133021447": "'Saint Anne's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/174864407": "'Saint Joachim's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1133021448": "'Saint Joseph's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/32121297": "'Saint Luke's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1133021446": "'Saint Mary's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/32121317": "'Saint Paul's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/747176455": "'Saint Paul's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/32121295": "'Saint Peter's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/747176454": "'Saint Peter's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/769468352": "'Oaks Cloister', a home with no sign of visiting, whatever its article (owner, 2026-10-13)",
    "way/769761127": "'Wynnestay', a home with no sign of visiting, whatever its article (owner, 2026-10-13)",
    "way/658548246": "'The Lilacs Building', a home with no sign of visiting, whatever its article (owner, 2026-10-13)",
    "way/244428094": "'Glen Fern', a home with no sign of visiting, whatever its article (owner, 2026-10-13)",
    "way/770083797": "'Druim Moir', a home with no sign of visiting, whatever its article (owner, 2026-10-13)",
    "way/766332792": "'Abraham Rittenhouse Home', a home with no sign of visiting, whatever its article (owner, 2026-10-13)",
    "way/766332795": "'Rittenhouse Home', a home with no sign of visiting, whatever its article (owner, 2026-10-13)",
    "way/341790041": "'Ben Franklin House', a home with no sign of visiting, whatever its article (owner, 2026-10-13)",
}
