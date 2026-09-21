"""New York-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

New York is the first city whose businesses come from more than one registry.
It has no general business licence, so coverage is assembled from four public
sources (see SOURCES below and pipeline/taxonomies/new_york.py for why). Step 2
loads each, normalises it to the shared columns, and keeps one row per site.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "new_york" / "raw"
DATA_PROCESSED = ROOT / "data" / "new_york" / "processed"
OUTPUTS = ROOT / "outputs" / "new_york"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Step 3 writes this: step 2's output with DCA's missing coordinates recovered.
BUSINESSES_GEOCODED_CSV = DATA_PROCESSED / "businesses_geocoded.csv"

GTFS_ZIP = DATA_RAW / "gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"

# Raw inputs, all public. Verified live 2026-09-21 (add-city Step 0); the exact
# retrieval command for each is in docs/data_sources.md.
#
#   gtfs.zip
#     curl -sL https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip -o gtfs.zip
#     5.6 MB, 29 routes, 496 parent stations, shapes.txt present. NOTE: this
#     S3 feed is the live one; the old web.mta.info/developers path is dead.
#
#   city_boundary.geojson  (the five borough polygons = the city)
#     curl -sL 'https://data.cityofnewyork.us/resource/gthc-hcne.geojson?$limit=10'
#     NOTE: tqmj-j8zm, the borough-boundary id in circulation, now 404s.
GTFS_URL = "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip"
CITY_BOUNDARY_URL = "https://data.cityofnewyork.us/resource/gthc-hcne.geojson?$limit=10"

# Census bulk-geocoder batch cache (step 3). Keyed by batch content hash, so a
# re-run stays offline and the drift check is deterministic.
GEOCODE_CACHE_DIR = DATA_RAW / "geocode_cache"

# Borough -> the postal city name the Census geocoder expects. Manhattan
# addresses are "New York"; the other boroughs are their own postal cities.
# A row whose borough is blank (the statewide NYS registries never set one)
# falls back to "New York" and relies on its ZIP.
BOROUGH_TO_POSTAL_CITY = {
    "MANHATTAN": "New York",
    "BROOKLYN": "Brooklyn",
    "BRONX": "Bronx",
    "QUEENS": "Queens",
    "STATEN ISLAND": "Staten Island",
}
GEOCODE_DEFAULT_CITY = "New York"
GEOCODE_STATE = "NY"

# --- Business sources -------------------------------------------------------
# Each entry: the raw file step 2 reads, the endpoint it came from, the
# server-side filter applied at download, and which columns carry the name,
# category and address. `source` is written into every row and is what
# pipeline/taxonomies/new_york.py dispatches on.
#
# `name_column` is always a registered TRADE name. No source's registrant /
# licence-holder name column is listed here, and step 2 never loads one: see
# the personal-information note in the taxonomy module.
SOURCES = {
    "dohmh": {
        "file": DATA_RAW / "dohmh_restaurants.csv",
        "endpoint": "https://data.cityofnewyork.us/resource/43nn-pn8j.csv",
        # One row per inspection violation, so the download is unfiltered and
        # step 2 collapses it to one row per establishment (camis).
        "filter": "$select=camis,dba,boro,building,street,zipcode,"
                  "cuisine_description,inspection_date,action,latitude,longitude,"
                  "bin,bbl&$limit=500000",
        "key_column": "camis",
        "name_column": "dba",
        "category_column": "cuisine_description",
    },
    "nys_store": {
        "file": DATA_RAW / "nys_retail_food_stores.csv",
        "endpoint": "https://data.ny.gov/resource/9a8c-vfzj.csv",
        "filter": "$where=county in('KINGS','QUEENS','BRONX','NEW YORK','RICHMOND')"
                  "&$limit=50000",
        "key_column": "license_number",
        "name_column": "dba_name",
        "category_column": "estab_type",
    },
    "nys_salon": {
        "file": DATA_RAW / "nys_appearance_enhancement.csv",
        "endpoint": "https://data.ny.gov/resource/y3u4-jbgh.csv",
        # Statewide file with no county column: the NYC subset is taken by
        # point-in-boundary in step 2, not by city name (postal city names in
        # NYC are unreliable - Ridgewood, Corona, Astoria are all Queens).
        # license_holder_name is deliberately NOT selected.
        "filter": "$select=license_number,license_type,business_name,"
                  "business_address_1,business_address_2,business_city,"
                  "business_zip,georeference&$limit=50000",
        "key_column": "license_number",
        "name_column": "business_name",
        "category_column": "license_type",
    },
    "dca": {
        "file": DATA_RAW / "dca_licenses.csv",
        "endpoint": "https://data.cityofnewyork.us/resource/w7w3-xahh.csv",
        # license_type='Premises' drops the 8,854 active Individual licences
        # (licences held by a person, at frequently residential addresses).
        "filter": "$where=license_status='Active' AND license_type='Premises'"
                  "&$limit=100000",
        "key_column": "license_nbr",
        "name_column": "business_name",
        "category_column": "business_category",
    },
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 18N: the longitude (~-74.01) falls in the -78 to -72 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32618"

# --- Ring geometry ---------------------------------------------------------
# NEW YORK IS THE ONE CITY THAT DOES NOT USE THE SHARED EDGES.
# Every other city uses [0, 0.1, 0.2, 0.3, 0.6] miles. New York has 496
# stations and Manhattan station spacing of roughly 0.3 mi, so a 0.6 mi outer
# ring reaches past the next two stations in every direction: the rings merge
# into one solid mass over Manhattan and downtown Brooklyn, which says nothing
# about any individual station. The add-city skill's instruction is to reuse
# the shared edges "unless station spacing is meaningfully different" - this is
# that case. Halving them keeps each ring inside its own station's catchment.
# Decided 2026-09-21; see DECISIONS.md.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------
# Every station of the MTA's own rail network inside the five boroughs, which
# is the whole subway plus the Staten Island Railway. Nothing is thinned: every
# NYC subway station is a full station (unlike San Francisco's street-running
# Muni stops), so the sub-transit-line filters do not apply here.
#
# LINES, not services. The feed carries 29 routes, which are service patterns
# (the 4, 5, 6 and 6X all run on the Lexington Avenue line). Drawing 29 would
# also break the map: the label layout treats the legend as an obstacle
# 178 + 19*n_lines px tall in a 650 px map, so 29 lines leaves no clear space
# and every label collides. The MTA's own route_color groups the 29 into the
# trunk lines it signs and prints on its map, which is both the fix and the
# more honest geography. 11 entries -> a 387 px obstacle.
#
# Each entry: trunk key -> (shape_ids, colour, public name, label end).
# shape_ids is every member service's most-used trip shape (the mode of
# trips.txt per route_id), so a trunk is drawn with its real branches.
# Colours are the MTA's own from routes.txt. Label end None = automatic.
ROUTE_IDS = [
    "1", "2", "3", "4", "5", "6", "6X", "7", "7X",
    "A", "B", "C", "D", "E", "F", "FX", "G", "H", "J", "L", "M",
    "N", "Q", "R", "W", "Z", "GS", "FS", "SI",
]

# route_id -> the trunk it belongs to. Derived from route_color in routes.txt,
# with two deliberate departures, both recorded in DECISIONS.md:
#   - L is separated from the shuttles. MTA paints the L and all three shuttles
#     the same grey, but the 14 St-Canarsie line is a full line and the
#     shuttles are not; merging them would label a Brooklyn trunk "Shuttles".
#   - The three shuttles are grouped as one "Shuttles" entry rather than three
#     legend rows for 2, 4 and 5 stations.
ROUTE_TO_TRUNK = {
    "A": "8av", "C": "8av", "E": "8av",
    "B": "6av", "D": "6av", "F": "6av", "FX": "6av", "M": "6av",
    "1": "7av", "2": "7av", "3": "7av",
    "4": "lex", "5": "lex", "6": "lex", "6X": "lex",
    "N": "bway", "Q": "bway", "R": "bway", "W": "bway",
    "J": "nassau", "Z": "nassau",
    "7": "flushing", "7X": "flushing",
    "G": "crosstown",
    "L": "canarsie",
    "GS": "shuttles", "FS": "shuttles", "H": "shuttles",
    "SI": "sir",
}

# Trunk -> (public name, MTA colour). The name is what the MTA and riders call
# the line, with the services on it in brackets so it is unambiguous on the
# map; verified against route_long_name in the feed, which carries these same
# trunk names ("8 Avenue Express", "Lexington Avenue Local", and so on).
LINE_NAMES = {
    "8av":       ("8 Av (A/C/E)", "#0062CF"),
    "6av":       ("6 Av (B/D/F/M)", "#EB6800"),
    "7av":       ("7 Av (1/2/3)", "#D82233"),
    "lex":       ("Lexington Av (4/5/6)", "#009952"),
    "bway":      ("Broadway (N/Q/R/W)", "#F6BC26"),
    "nassau":    ("Nassau St (J/Z)", "#8E5C33"),
    "flushing":  ("Flushing (7)", "#9A38A1"),
    "crosstown": ("Crosstown (G)", "#799534"),
    "canarsie":  ("14 St-Canarsie (L)", "#7C858C"),
    "shuttles":  ("Shuttles (S)", "#A7ADB2"),
    # SIR is the one line NOT using the MTA's own colour. Theirs is #08179C, a
    # navy so dark (L* ~17) that the on-map label - which takes the line's
    # colour - is hard to read on the light basemap and nearly invisible in
    # dark mode. Lightened within the same navy family so it still reads as
    # SIR, and kept violet enough not to be confused with 8 Av's azure
    # (#0062CF); the two never appear near each other anyway, Staten Island
    # being its own separate system.
    "sir":       ("Staten Island Railway", "#4358D4"),
}

# Which end of each trunk carries its label; None = automatic (the end farthest
# from the other lines). Set only where a rendered map showed a bad landing.
LINE_LABEL_ENDS = {}

# Routes whose geometry is NOT drawn, because it duplicates another route on
# the same trunk. They stay in ROUTE_TO_TRUNK, so their stations still count -
# this only avoids drawing the same track twice.
#   6X, 7X, FX  express variants running on their local's own track
#   Z           skip-stop service on the J's track
#   W           runs the N's Broadway alignment (its most-used shape in the
#               feed is literally an "N.." shape)
DRAW_EXCLUDE_ROUTES = frozenset({"6X", "7X", "FX", "Z", "W"})

# --- Business filtering ------------------------------------------------

# The DOHMH file is an inspection history, not a list of open restaurants: an
# establishment that shut in 2019 still has its old rows. Fixed rather than
# "today" so a re-run and a drift check stay deterministic (Chicago's
# AS_OF_DATE is the same idea).
AS_OF_DATE = "2026-09-21"
# An establishment counts as trading if its most recent inspection is within
# this window. Two years covers DOHMH's inspection cycle with room for
# establishments inspected less often; see DECISIONS.md for the measured
# distribution behind the number.
DOHMH_ACTIVE_WITHIN_DAYS = 730
# DOHMH writes 1900-01-01 for an establishment that is permitted but has never
# been inspected. Those are kept: a brand-new restaurant is trading.
DOHMH_NEVER_INSPECTED = "1900-01-01"

# Actions on the most recent inspection that mean the establishment was shut.
DOHMH_CLOSED_ACTIONS = ("ESTABLISHMENT CLOSED BY DOHMH", "ESTABLISHMENT RE-CLOSED BY DOHMH")

# In-city rows are identified by point-in-boundary against the five borough
# polygons, not by a city-name field. DCA's own address_borough is used as a
# cross-check (it holds 'Outside NYC' on 2,597 active rows and is blank on
# 3,075), and the NYS files have no NYC marker at all.
CITY_KEEP = None

TAXONOMY_SYSTEM = "new_york"
# Step 2 writes each source's own category column into this name.
RAW_CLASSIFICATION_COLUMN = "business_category"

# Sanity bounds for supplied and geocoded coordinates: the real extent of the
# five boroughs, from Tottenville (40.50, -74.26) to the north Bronx (40.92)
# and eastern Queens (-73.70), padded slightly.
NEW_YORK_BBOX = {
    "lat_min": 40.47,
    "lat_max": 40.93,
    "lon_min": -74.27,
    "lon_max": -73.68,
}

# New York State's envelope, used to tell two very different kinds of
# out-of-city coordinate apart (step 2). Measured 2026-09-21: 16,692 source
# coordinates fall outside NEW_YORK_BBOX, and they are not one problem but two.
#
#   Valid point, inside the state, outside the city (16,073 rows, 15,392 of
#   them salons in Watertown, Buffalo, Utica, Poughkeepsie...). The two NYS
#   registries are statewide and carry no NYC marker, so these are simply not
#   New York City businesses. They are DROPPED as out of scope. Geocoding them
#   would waste ~16k geocoder calls and could pull an upstate business back
#   inside the city on a same-named street.
#
#   Not in the state at all (619 rows, 411 of them exactly (0,0)). These ARE
#   New York businesses whose coordinates are broken - HASAKI at 210 E 9th St,
#   White Castle, Tal Bagels. Their coordinates are BLANKED and recovered by
#   address in step 3, the same treatment Los Angeles' ~9% corrupt coordinates
#   got. Recovery is expected to be partial: some of these rows also have
#   mangled addresses ("975979 FIRST AVENUE") or none at all ("4 - JFK
#   AIRPORT"), and step 3 reports what it could not recover.
NY_STATE_BBOX = {
    "lat_min": 40.40,
    "lat_max": 45.10,
    "lon_min": -79.80,
    "lon_max": -71.80,
}
