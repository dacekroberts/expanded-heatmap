"""Vancouver settings. Scoped to the REGION - Vancouver AND Surrey - rather
than one municipality.

WHY REGIONAL, AND WHY IT IS HARDER HERE THAN IN MIAMI
-----------------------------------------------------
Surrey has no rail of its own. SkyTrain is TransLink's, so one transit licence
covers both cities, and Surrey contributes 4 in-city stations at 361
Commercial/Industrial sites each - second only to Vancouver's own density.
Decided 2026-09-21 (see DECISIONS.md, "Vancouver is built at REGIONAL scope").

Miami is the precedent for a deliberately regional city, but it is the EASY
version of this shape: Miami-Dade licenses all 34 of its municipalities in ONE
file, with one schema, one publisher and one set of terms. Vancouver and Surrey
are **two publishers, two schemas and two licences** - the `multi-source-city`
shape applied across municipalities instead of across buckets. So this config
carries a `SOURCES` table and the taxonomy dispatches on a `source` column,
exactly as New York's and Boston's do.

The one way it is easier than New York: the two registries cover DISJOINT
municipalities, so no premises can appear in both and there is no cross-source
dedup. Dedup is per-source only. That absence is recorded here because an
absent dedup step is otherwise indistinguishable from a forgotten one.

Consequences carried through the rest of this file: there is no single
`CITY_KEEP`, each source has its own boundary and its own in-city test, and
the page is labelled "Vancouver (Regional)" because a map spanning two
municipalities cannot honestly be called Vancouver.

RESCOPING BACK TO VANCOUVER ALONE means deleting the "surrey" entry from
SOURCES, its boundary, and the Surrey branch of pipeline/taxonomies/vancouver.py.
Nothing else in the pipeline knows Surrey exists.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "vancouver" / "raw"
DATA_PROCESSED = ROOT / "data" / "vancouver" / "processed"
OUTPUTS = ROOT / "outputs" / "vancouver"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside both cities, with the municipality each lies in - a citable
# scoping record, as in the other cities. Named from a real boundary layer
# (BC ABMS), never guessed from the station name.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
# The regional scoping record: every KEPT station with the city it sits in, so
# a reader can see the map deliberately spans two municipalities rather than
# silently leaking past Vancouver's edge. Miami's equivalent file.
STATION_MUNICIPALITIES_CSV = OUTPUTS / "station_municipalities.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (see pipeline/vancouver/fetch_sources.py) -----------------

GTFS_ZIP = DATA_RAW / "gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "vancouver_local_areas.geojson"
SURREY_BOUNDARY_GEOJSON = DATA_RAW / "surrey_city_boundaries.geojson"
MUNICIPALITIES_GEOJSON = DATA_RAW / "bc_municipalities.geojson"
# The residence filter's two hops (see RESIDENTIAL_ZONING_CLASSES below).
PARCELS_GEOJSON = DATA_RAW / "property_parcel_polygons.geojson"
TAX_REPORT_CSV = DATA_RAW / "property_tax_report.csv"

# --- Endpoints for everything that is not a business registry ---------------

_ODS = "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets"

# Vancouver's 22 local areas. See BOUNDARY_AREA_KM2_EXPECTED for why this is
# not `city-boundary`.
CITY_BOUNDARY_URL = f"{_ODS}/local-area-boundary/exports/geojson"

# Surrey's boundary, read from the SERVICE (f=geojson) rather than the Hub's
# file export, which is the one that mislabels its CRS.
SURREY_BOUNDARY_URL = (
    "https://services5.arcgis.com/YRpe0VKTJytZSSIB/arcgis/rest/services/"
    "Surrey City Boundaries/FeatureServer/0/query"
)

# BC ABMS municipalities, for NAMING excluded stations only. WFS 2.0 with a
# urn: CRS means the bbox is in the AUTHORITY's axis order - lat,lon, not
# lon,lat. Given lon,lat it returns zero features and no error.
MUNICIPALITIES_URL = ("https://openmaps.gov.bc.ca/geo/pub/"
                      "WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_MUNICIPALITIES_SP/ows")
MUNICIPALITIES_TYPENAME = ("pub:WHSE_LEGAL_ADMIN_BOUNDARIES."
                           "ABMS_MUNICIPALITIES_SP")
MUNICIPALITIES_BBOX = "49.0,-123.35,49.45,-122.55,urn:ogc:def:crs:EPSG::4326"

# The residence filter's two hops.
PARCELS_URL = f"{_ODS}/property-parcel-polygons/exports/geojson"
TAX_REPORT_URL = f"{_ODS}/property-tax-report/exports/csv"
# Only what the zoning join needs. The full file is 1,553,448 rows across seven
# report years; narrowed to one year and four columns it is ~229k rows.
TAX_REPORT_SELECT = ("land_coordinate,legal_type,zoning_classification,"
                     "zoning_district")

# --- Transit feed -----------------------------------------------------------

# TransLink's OWN host, not the Mobility Database mirror. The mirror is what
# told the Canada profile this feed has no feed_info.txt; the agency's copy has
# one. Toronto's stale-mirror lesson, in a new form - not staleness this time
# but a mirror missing a file the source publishes.
GTFS_URL = "https://gtfs-static.translink.ca/gtfs/google_transit.zip"
GTFS_FEED_INFO_MEMBER = "feed_info.txt"
# Measured 2026-09-21: feed_start_date 20260907, feed_end_date 20270103 - a
# 118-day window. Far longer than WMATA's ten days, but it EXISTS, so the same
# check applies: an expired feed still parses, still has 54 stations and still
# builds a map. fetch_sources.py re-reads this on every run.
GTFS_CHECK_FEED_WINDOW = True

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 10N: Vancouver's longitude (~-123.12) and Surrey's (~-122.8) both
# fall in the -126..-120 band, so one projected CRS serves the whole region.
# Derived per city, never copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32610"

# Surrey's business x/y are NOT degrees. They arrive only in the CSV export -
# the layer's own attribute schema has no coordinate fields at all - and they
# are in the service's native SR, NAD83 UTM zone 10N metres. Reading them as
# lon/lat puts Surrey in the Gulf of Guinea. The ~1 m datum difference from
# EPSG:32610 is immaterial at ring scale but the reprojection is still done
# properly rather than assumed away.
SURREY_SOURCE_XY_CRS = "EPSG:26910"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# SkyTrain's three lines. The West Coast Express (route_id 6770) is
# route_type 2, commuter rail, and is excluded as everywhere in this project;
# the SeaBus (route_type 4) is a passenger ferry, not rail.
#
# MATCH BY route_id, NOT route_short_name: `route_short_name` is EMPTY on all
# three rail routes in this feed. The public names are in `route_long_name`.
ROUTE_IDS = ["30053", "30052", "13686"]
LINE_NAMES = {
    "30053": "Expo Line",
    "30052": "Millennium Line",
    "13686": "Canada Line",
}

# Official TransLink colours, taken from the feed's own `route_color` rather
# than from a style guide, so they are the agency's current values.
#
# CONTRAST WAS MEASURED IN BOTH MODES, dark first, because dark is this site's
# default and measuring the light basemap alone produced a backwards
# recommendation for D.C.'s Silver Line. Minimum CIE76 Delta-E from OSM Carto's
# land (#f2efe9) and road (#ffffff) fills, with map_common's own filter chains
# applied - strokes brightness(1.55) saturate(0.9), tiles invert/hue-rotate/
# brightness/contrast/saturate:
#
#     | line                  | dark (default) | light (toggle) |
#     | Expo #0033a0          |      98.0      |      99.6      |
#     | Millennium #ffcd00    |     127.2      |      82.8      |
#     | Canada #007c9f        |      76.2      |      57.5      |
#     | for scale: D.C. Silver|        -       |      31.4      |
#
# The weakest is the Canada Line's teal in light mode at 57.5 - still 1.8x the
# project's known-weak case - so NO line here needs the disclosure D.C.'s
# Silver Line got. Official colours kept, per the branding decision of
# 2026-09-21, and the non-affiliation notice covers using them.
#
# Caveat recorded rather than hidden: this reproduces D.C.'s published LIGHT
# figures exactly (Silver 31.4 land, darkened 51.0 land) but NOT its dark ones,
# whose model was never written down. See DECISIONS.md.
LINE_COLOURS = {
    "30053": "#0033a0",   # Expo - deep blue
    "30052": "#ffcd00",   # Millennium - yellow
    "13686": "#007c9f",   # Canada - teal
}

# Which shape_ids draw each line. A TUPLE where the line branches: the bare
# mode shape would silently drop a whole branch - the Canada Line splits for
# YVR-Airport and Richmond-Brighouse, the Expo Line for King George and
# Production Way-University. One direction only, so an alignment is not drawn
# twice. Verified 2026-09-21 to cover every station on each line (Expo 24,
# Millennium 17, Canada 17).
LINE_SHAPES = {
    "30053": ("322353", "322354"),
    "30052": ("322339",),
    "13686": ("322331", "322332"),
}

# Which end of each line carries its label; None = automatic (map_common picks
# the tail farthest from the other lines). Filled in after looking at the
# rendered map, as in every other city.
LINE_LABEL_ENDS = {}

# TransLink names every rail stop "<Station> @ Platform N" (and a few
# "@ <Line>"), two to four rows per station. Stripped in step 1, then platform
# positions are averaged. Unlike San Francisco this needs no hand-curated alias
# dict - the pattern is perfectly regular, and step 1 ASSERTS that every
# "@"-bearing name matched, so a new suffix form fails loudly.
STATION_SUFFIX_PATTERN = r"\s*@\s*(Platform\s*\d+|Canada Line|Expo Line|Millennium Line)\s*$"
STATION_NAME_STRIP_SUFFIX = " Station"

# SkyTrain is fully grade-separated - elevated or in tunnel, with no
# street-running stops - so every in-city station is kept and no
# sub-transit-line filter applies (docs/sub_transit_line_filters.md). Same
# verdict as D.C., for the same structural reason.
#
# Downtown spacing IS tight: median nearest-neighbour 841 m, minimum 201 m
# (Granville to Vancouver City Centre, two different lines), and 17 of 20
# in-city stations have a neighbour inside the 965 m outer ring. Those rings
# overlap visibly. Each business is assigned to its NEAREST station, so nothing
# is double-counted; the overlap is a conscious choice, recorded here because
# it would matter directly if ring statistics were ever added.
THINNED_GROUPS = frozenset()

# --- Business sources -------------------------------------------------------

# Encoding of this city's RAW source files, declared rather than inferred -
# an add-city requirement that bites hardest outside the US. Both sources are
# UTF-8; Surrey's CSV carries a BOM.
SOURCE_ENCODING = "utf-8"

SOURCES = {
    "vancouver": {
        "file": DATA_RAW / "vancouver_business_licences.csv",
        # Opendatasoft Explore v2.1. CSV exports are SEMICOLON-delimited, not
        # comma - a portal-wide trap, not a Vancouver one.
        "endpoint": ("https://opendata.vancouver.ca/api/explore/v2.1/catalog/"
                     "datasets/business-licences/exports/csv"),
        "delimiter": ";",
        # folderyear is the licence vintage and it ROLLS. Verified 2026-09-21
        # that '26' is current: 73,075 rows against 69,889 for '25'. Re-check
        # before a rebuild rather than trusting this string.
        "filter": "folderyear='26' AND status='Issued'",
        # `geom` (the full parcel-ish geo_shape) is deliberately NOT selected:
        # only the point is needed, and the polygon would multiply the download
        # for nothing.
        "select": ("licencersn,licencenumber,businessname,businesstradename,"
                   "businesstype,businesssubtype,unit,unittype,house,street,"
                   "city,localarea,numberofemployees,geo_point_2d"),
        "key_column": "licencersn",
        "name_column": "businesstradename",
        # Sole proprietors register under their own name, so this fallback is
        # the person-name exposure. See NAME_FALLBACK_POLICY below.
        "name_fallback_column": "businessname",
        "category_column": "businesstype",
        "boundary": CITY_BOUNDARY_GEOJSON,
        "municipality": "Vancouver",
        "licence": "Open Government Licence - Vancouver",
    },
    "surrey": {
        "file": DATA_RAW / "surrey_business_licences.csv",
        # ArcGIS Hub async export. Returns the CSV as
        # application/octet-stream, NOT text/csv - a content-type check on
        # "csv" rejects a perfectly good download.
        "endpoint": ("https://hub.arcgis.com/api/download/v1/items/"
                     "468ff5ff67354da5be095a9bce006137/csv"),
        "delimiter": ",",
        # Surrey publishes one annual table with no status column: every row is
        # a current licence. The scope filter is LicenseType instead - see
        # SURREY_LICENSE_TYPE_KEEP.
        "filter": None,
        "select": None,       # the Hub export takes no field list
        "key_column": "OBJECTID",
        "name_column": "BusinessName",
        "name_fallback_column": None,   # Surrey publishes no second name field
        "category_column": "BusinessCategory",
        "boundary": SURREY_BOUNDARY_GEOJSON,
        "municipality": "Surrey",
        "licence": "Open Government License - City of Surrey",
    },
}

# Surrey's BusinessCategory holds SEVERAL categories per row, newline-
# separated: 628 naive distinct values against 210 real ones, with 4,837 rows
# carrying more than one. A value_counts() on the raw column returns
# COMBINATIONS. This is the Canadian trap that is not in the US playbook
# (Calgary uses ",\n", Edmonton ";"); Vancouver's own businesstype is
# single-valued and needs none of it.
SURREY_CATEGORY_DELIMITER = "\n"

# Surrey STATES on the licence whether a business is home-based, which is
# better evidence than any inference this project makes elsewhere - the city
# asserts it. Home Occupation is 14,015 of 27,082 rows (51.8%) and is dropped:
# a home business is not a storefront, which is a scope correction first and a
# privacy one second.
#
# A single row reads " home" (lowercase, leading space) rather than one of the
# two real values, so the comparison is normalised. Left in the data as found;
# fixing it here rather than pretending the column is clean.
SURREY_LICENSE_TYPE_KEEP = "commercial/industrial"
SURREY_LICENSE_TYPE_COLUMN = "LicenseType"

# --- Boundaries -------------------------------------------------------------

# Vancouver's 22 LOCAL AREAS, dissolved. NOT `city-boundary`, which returns a
# single MultiLineString that a point-in-polygon test silently matches nothing
# against. Verified 2026-09-21: the 22 polygons union to ONE Polygon of
# 118.8 km2 against the city's ~115, and the area check is the load-bearing
# part - a dissolve that dropped a local area would still return a valid
# Polygon, and only the km2 and the containment rate catch it.
BOUNDARY_AREA_KM2_EXPECTED = 118.8
BOUNDARY_AREA_TOLERANCE_KM2 = 3.0

# Surrey's boundary file has 10 features and only ONE is the city:
# BOUNDARY_TYPE 2 / NAME 'SURREY'. The other 9 are town centres (Newton,
# Whalley, Guildford...), so an unfiltered read would test containment against
# a neighbourhood.
SURREY_BOUNDARY_NAME_FIELD = "NAME"
SURREY_BOUNDARY_NAME_KEEP = "SURREY"

# Reading the FeatureServer with f=geojson returns real degrees, correctly
# reprojected from EPSG:26910. The "declares EPSG:4326 while containing UTM
# metres" trap recorded in the Canada profile belongs to the Hub's FILE export,
# not the service - so this build needs no set_crs(..., allow_override=True)
# anywhere. Step 1 asserts the boundary really is in degrees, so a switch back
# to the file export fails loudly instead of quietly matching nothing.

# Used only to NAME the municipality of each station, never to filter. The BC
# ABMS municipalities layer, via WFS.
MUNICIPALITIES_NAME_FIELD = "ADMIN_AREA_NAME"
# BOTH cities' stations are kept, so these are the two names that are in scope.
MUNICIPALITIES_KEEP = ("City of Vancouver", "City of Surrey")

# --- Classification ---------------------------------------------------------

TAXONOMY_SYSTEM = "vancouver"
# Each source's own category string, so a tooltip shows the registry's own
# words. Step 2 renames both sources' category columns to this.
RAW_CLASSIFICATION_COLUMN = "category"

# --- The name-fallback policy ----------------------------------------------

# Vancouver's `businesstradename` is blank on 49.6% of MAPPABLE rows (not the
# 63.0% measured on the whole current-year file - the difference is the rentals
# and contractors that carry no coordinates and are excluded anyway). The label
# therefore falls back to `businessname`, which for a sole proprietor IS a
# person's name.
#
# Los Angeles met this at 68% and answered by excluding the category driving
# it. D.C. answered with a structural ENTITYTYPE signal. Vancouver has neither,
# and `unittype` - which looked like NYC's APT/STE/FL signal - is 'Unit' on
# 12,803 of 29,660 rows against 'Apt' on TWO, so it cannot separate a dwelling
# from a commercial suite.
#
# So the answer is at the label: fall back to the legal name, but where that
# name matches residence.looks_personal, display the row's own business type
# instead. Every storefront stays on the map; no individual's name is
# published. Owner's call, 2026-09-21.
NAME_FALLBACK_POLICY = "suppress_personal"

# One structural help worth recording: this registry publishes NO registrant-
# name column. `businessname` and `businesstradename` are the only name fields,
# so unlike New York there is nothing to omit at the download boundary. Surrey
# publishes no owner name either - but it does publish PhoneNumber, which is
# omitted in step 2 and asserted absent, because a business phone number is not
# needed to draw a dot and a home-based licence's number is a personal one.
FORBIDDEN_COLUMNS = ("PhoneNumber",)

# --- The residence filter ---------------------------------------------------

# Vancouver is the only Canadian city of the six with NO licence-level
# home-business flag (Surrey states it, Edmonton and Calgary have their own
# fields), and no province publishes owner-occupancy - BC Assessment is not
# open data. So the US-style parcel inference is the ONLY residence signal
# available here, which is why it is built rather than skipped.
#
# Two hops, both in EPSG:32610:
#   business point -> property-parcel-polygons  (spatial)
#                 -> property-tax-report on tax_coord = land_coordinate
#                 -> zoning_classification
#
# The ADDRESS join is REJECTED - do not retry it. Tested 2026-09-21: 6.5%
# matched. Direction is prefixed in licences ("W 8TH AV") and suffixed in the
# tax roll ("8TH AVE W"), "AV" against "AVE", only 35% of street names appear
# verbatim, and civic numbers are stored as RANGES with nulls, so exact
# matching fails structurally.
TAX_REPORT_YEAR = "2026"
TAX_REPORT_KEY = "land_coordinate"
PARCEL_KEY = "tax_coord"

# THE BRIEF'S ZONING VALUES NO LONGER EXIST. It recorded One-Family Dwelling
# 202,740 / Two-Family Dwelling 48,300 / Multiple Dwelling 87,557 / Commercial
# 132,576. Those are Vancouver's PRE-2024 scheme, and the counts were taken
# across all seven years in the file at once - the D.C. denominator error in a
# new place. On report_year='2026' the classes are: Comprehensive Development
# 84,292, Residential Inclusive 65,706, Residential 51,152, Commercial 19,782,
# Industrial 5,122, Historical Area 2,621, Limited Agriculture 166,
# Residential Rental 22, None 6.
RESIDENTIAL_ZONING_CLASSES = frozenset({
    "Residential",
    "Residential Inclusive",   # the post-2024 low-density class (R1-1)
    "Residential Rental",
})

# The blind spot, stated rather than hidden: Comprehensive Development is
# MIXED-USE, so it never flags residential and a home business on CD land is
# invisible to this filter. CD covers exactly the dense central areas where a
# "home" is a condo.
#
# The obvious refinement was TESTED AND REJECTED - do not retry it. legal_type
# STRATA on CD land looks like it should isolate the condo home business: of
# 11,935 CD licences, LAND 9,648 / STRATA 2,271, and of the 1,183 with a
# person-like name, LAND 928 / STRATA 253. That is a STRATA share of 21.4%
# against a 19.0% baseline - 1.12x, i.e. no enrichment. A sample of 16
# candidates returned Tim Hortons, Taco Time, Kiku Sushi, Caffe Artigiano,
# Praxis Legal and CoastKids Pediatrics: not one a home business. STRATA on CD
# land means "a commercial unit in a mixed-use building", which is what CD
# zoning is designed to produce.
MIXED_USE_ZONING_CLASSES = frozenset({"Comprehensive Development"})

# --- Coordinate sanity ------------------------------------------------------

# Tightened to the two cities' real combined extent. Vancouver's boundary spans
# roughly -123.225..-123.023 / 49.198..49.317; Surrey's -122.957..-122.679 /
# 49.002..49.221. This box is deliberately a little wider than the union, so a
# genuine edge premises is not clipped by the sanity check itself.
VANCOUVER_BBOX = {
    "lat_min": 48.95,
    "lat_max": 49.35,
    "lon_min": -123.30,
    "lon_max": -122.62,
}
