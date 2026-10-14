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

# Gate 3, keyed by TRUNK (LINE_NAMES), as step 1 draws and labels its lines.
# The MTA publishes no count per trunk, so each figure is counted from the
# MTA's own station register: every station whose `daytime_routes` names any
# of the trunk's services (route bullets: A/C/E for 8av; "S" for all three
# shuttles; "SIR"). 496 stations, the same 496 parent stations the feed has.
#
# The build counts every station any trip of the trunk serves, nights and
# odd-hour patterns included, and the register lists DAYTIME routes only.
# Where they differ, each extra station was identified by stop id and its
# serving trips' times read from the feed (2026-10-01); the figure here is the
# register's plus those stations:
#   8av  80 + 14: E trips to Jamaica-179 St (F01-F04: 179 St, 169 St, Parsons
#        Blvd, Sutphin Blvd) and the late-night E local on Queens Blvd (G09-G20:
#        67 Av, 63 Dr, Woodhaven, Grand Av, Elmhurst Av, 65 St, Northern Blvd,
#        46 St, Steinway St, 36 St), daytime R/M stations.
#   6av  119 + 4: the late-night D local on 4 Av, Brooklyn (R32-R35: Union St,
#        4 Av-9 St, Prospect Av, 25 St; trips 21:00-07:00).
#   lex  91 + 12: the late-night and early 4 to New Lots Av and two weekday
#        early-morning 5 trips (236-238, 248-257: Bergen St to New Lots Av),
#        daytime 2/3 stations.
#   bway 85 + 3: one weekday R and two weekday W trips over the West End line
#        (B12 9 Av, B16 62 St, B21 Bay Pkwy), daytime D stations.
#   shuttles 11 + 4: the summer-weekend Rockaway Park Shuttle extension to
#        Rockaway Blvd (A61, H01-H03: Rockaway Blvd, Aqueduct Racetrack,
#        Aqueduct-N Conduit Av, Howard Beach-JFK), service ids
#        Saturday/Sunday-H-20260526-20260907 - ended 2026-09-07, still in the
#        cached feed.
# The other six trunks match the register exactly.
OPERATOR_STATION_COUNTS = {
    "8av": 94,        # register 80 + 14 (above)
    "6av": 123,       # register 119 + 4
    "7av": 93,
    "lex": 103,       # register 91 + 12
    "bway": 88,       # register 85 + 3
    "nassau": 30,
    "flushing": 22,
    "crosstown": 21,
    "canarsie": 24,
    "shuttles": 15,   # register 11 + 4
    "sir": 21,
}
OPERATOR_COUNTS_SOURCE = ("MTA, 'MTA Subway Stations' register (data.ny.gov "
                          "dataset 39hk-dx4f), stations per trunk by "
                          "daytime_routes, https://data.ny.gov/resource/"
                          "39hk-dx4f.json (read 2026-10-01)")

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

# Encoding of this city's RAW source files, declared rather than inferred.
# pandas defaults to UTF-8 and raises on anything else - safe, but it leaves
# the next person to guess, and reaching for latin-1 to silence a
# UnicodeDecodeError corrupts accented names without ever failing. Declaring it
# makes the choice reviewable and part of the provenance. See the encoding rule
# in docs/data_sources.md; non-US cities are where this bites.
SOURCE_ENCODING = "utf-8"

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

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3608398124,3609691750,3609691819,3609691916,3609691948)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
# Read and kept, 2026-10-13 (the flag check of wave 1; the owner's ruling
# to settle unsure rows by the existing rules). None carries a leak word,
# so check E takes no PLACE_REVIEWED entry for it; the reason is kept here.
#   way/241857932 'Biddle House': historic=manor with access=yes: a house the tags mark open to the public
#   way/249742821 'Historic Wyckoff-Bennett-Mont Residence': tourism=attraction and an article of its own: a home tagged an attraction is kept
#   node/368043220 'Pellman Cottage': historic=ruins: the ruin of a cottage, no home
#   node/4451144258 'Temple of Dendur': a museum exhibit with an article of its own, a landmark people look for (owner, 2026-10-13)
#   relation/1341944 'The Dakota': tourism=attraction and an article of its own, a landmark people look for (owner, 2026-10-13)
#   way/266170658 'The Penn Club': a historic building with an article of its own (30 West 44th Street), under its club's name
PLACE_REVIEWED = {
    "Classic Stage Company": "a theatre with its own article, named for its company",
    "Coney Island Yard Electric Motor Repair Shop": "a registered historic building with its own article",
    "Eagle Warehouse & Storage Company": "a historic building with its own article",
    "Mount Vernon Hotel Museum": "a museum with its own article; \"Hotel\" is the historic building's name",
}
PLACE_DROPPED = {
    "relation/11171793": "'Grand Central Terminal', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/812714851": "'Pennsylvania Station', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/3039737083": "'16th Street', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3039737086": "'20th Street', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3039737089": "'25th Street', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3026462198": "'Court Street - Myrtle Avenue', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/5977004658": "'DeKalb Avenue Station', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3026462201": "'Franklin Avenue', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/5977004660": "'Franklin Avenue Station', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3039734880": "'Fulton Street', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3026462207": "'Grand Avenue', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/5977004659": "'Greene Avenue Station', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/357609892": "'Croton Reservoir', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "way/531480623": "'Green Grass', a description standing in for a name (owner, 2026-10-13)",
    "way/461448945": "'courtyard', a bare type word for a name (owner, 2026-10-13)",
    "node/5735397809": "'Iglesia', a bare type word for a name (owner, 2026-10-13)",
    "node/4148050758": "'Cannon', a bare type word for a name (owner, 2026-10-13)",
    "way/355814424": "'Beach/Kayak launch ramp', a description standing in for a name (owner, 2026-10-13)",
    "node/7184912473": "'18th Century Cistern', a description standing in for a name (owner, 2026-10-13)",
    "node/10536259275": "'Historic Stone Chimney', a description standing in for a name (owner, 2026-10-13)",
    "way/405885395": "'Aquatheater', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "node/14240441071": "'Historic Cold Frames', an exhibit inside a venue, which keeps its own row (owner, 2026-10-13)",
    "node/14240435247": "'Horse-drawn potato digger', an exhibit inside a venue, which keeps its own row (owner, 2026-10-13)",
    "way/1113769510": "'Barger Privy', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/1113769511": "'Barn Foundation', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/1113769518": "'Carriage Manufactory', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/1113769514": "'First County Jail', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/1113769517": "'Journeay Privy', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "relation/3745714": "'Corpus Christi Monastery', a religious residence",
    "node/357612293": "'Franciscan Missionaries of Mary', a religious residence",
    "way/276410380": "'Franciscan Sisters of the Renewal', a religious residence",
    "way/247835145": "'Little Sisters of the Poor Convent', a religious residence",
    "way/266930863": "'Building at 133 East 80th Street', a home: an apartment complex's own feature",
    "relation/3582905": "'Building at 45 East 66th Street', a home: an apartment complex's own feature",
    "way/1077518596": "'Hester Street Park', a housing estate's own way, named for the estate",
    "node/14144337556": "'Citizens of Italy', a business's own feature under its own name",
    "way/1004601095": "'The Corporate Park of Staten Island', a business's own feature under its own name",
    "way/277075652": "'Chabad Lube\\avitch of Riverdale', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "node/357624055": "'Congregation Ahawath', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "node/357624470": "'Congregation Krasna Ohel Brch', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1466653479": "'Congregation Boyaner Kloiz Tifereth', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/281894279": "'Church of the Atonement Food Pantry', another object's name on this one: not the thing its name says",
    "way/702073753": "'Goethe', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/369042126": "'Floyd Bennett Field', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/12550057961": "'James B. Warden', named for private persons: a personal name, not a place (owner, 2026-10-13)",
    "way/279772394": "'Order of Saint Dominic Convent', a religious residence",
    "way/276336696": "'Our Lady of Angels Rectory', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/357612429": "'Saint Francis Xavier Convent', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/357611900": "'Saint Johns Convent', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/276412864": "'Saint Patrick's Convent', a religious residence",
    "node/357612443": "'Saint Raymonds Convent', a religious residence",
    "node/357612568": "'Saint Theresa Convent', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/5977004657": "'Myrtle Avenue Station', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/5977004664": "'Reid Avenue Station', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/5977004663": "'Sumner Avenue Station', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/5977004662": "'Tompkins Avenue Station', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3026462210": "'Navy Street', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3026462213": "'Nostrand Avenue', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3026462216": "'Sands Street', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3026462225": "'Sumner Avenue', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3026462228": "'Tompkins Avenue', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3026462231": "'Vanderbilt Avenue', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3026465034": "'Washington Avenue', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3039734887": "'Ninth Street', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3039734893": "'Third Street', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/3039734896": "'Union Street', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/597694825": "'Penny Bridge', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/5889613634": "'Whitestone LIRR (historical site)', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "way/1113769522": "'Site of 1st County Courthouse', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/1810241472": "'Rubin Museum of Art', closed for a year or more by its own tags (owner, 2026-10-13)",
    "way/247499678": "'Pathology Laboratory', abandoned by its own tags (owner, 2026-10-13)",
    "node/357609017": "'Trinity Chapel School', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/7142951490": "'Meditation Area', a description standing in for a name (owner, 2026-10-13)",
    "node/5528646940": "'Parish Center', a bare type word for a name (owner, 2026-10-13)",
    "node/5891693971": "'Majid', a bare type word for a name (owner, 2026-10-13)",
    "way/1554877867": "'Stadium 1', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/1554877868": "'Stadium 2', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/277447830": "'Stadium 17', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "node/9681109101": "'Rooftop Farm', a description standing in for a name (owner, 2026-10-13)",
    "node/4312078590": "'Wodworth Building', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/4315047478": "'PortSide New York', an organisation's name on another object",
    "node/14197015414": "'St. Nicholas National Shrine Donor Wall', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/368061644": "'Museum of the Moving Image', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/357635065": "'United We Stand Garden', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/2810116541": "'Saint Stephen's Methodist Episcopal Church', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/994049384": "'Memorial Field Park', a home",
    "way/578280392": "'PATH - 33rd Street entrance (closed)', not a street: another kind of object indexed as one",
    "way/578280393": "'PATH - 33rd Street entrance (closed)', not a street: another kind of object indexed as one",
    "way/578280394": "'PATH - 33rd Street entrance (closed)', not a street: another kind of object indexed as one",
    "way/578280395": "'PATH - 33rd Street entrance (closed)', not a street: another kind of object indexed as one",
    "way/578280396": "'PATH - 33rd Street entrance (closed)', not a street: another kind of object indexed as one",
    "way/812938418": "'PATH - 33rd Street entrance (closed)', not a street: another kind of object indexed as one",
    "way/812938419": "'PATH - 33rd Street entrance (closed)', not a street: another kind of object indexed as one",
    "way/554696791": "'14th Street (PATH) underground passage', not a street: another kind of object indexed as one",
    "way/554696793": "'14th Street (PATH) underground passage', not a street: another kind of object indexed as one",
    "way/591434575": "'Christopher Street (PATH) underground passage', not a street: another kind of object indexed as one",
    "way/813541251": "'Christopher Street (PATH) underground passage', not a street: another kind of object indexed as one",
    "way/554402298": "'14th Street IRT Seventh Avenue Line-BMT Sixth Avenue Line Subway transfer', not a street: another kind of object indexed as one",
    "way/554402303": "'14th Street/6th Avenue-7th Subway transfer', not a street: another kind of object indexed as one",
    "way/731890792": "'Metropolitan Avenue Marked Crosswalk', not a street: another kind of object indexed as one",
    "way/833386640": "'Broadway Sidewalk (west side)', not a street: another kind of object indexed as one",
    "way/833386641": "'Broadway Sidewalk (west side)', not a street: another kind of object indexed as one",
    "way/833386642": "'Broadway Sidewalk (west side)', not a street: another kind of object indexed as one",
    "way/982319751": "'Broadway Sidewalk (west side)', not a street: another kind of object indexed as one",
    "way/982319752": "'Broadway Sidewalk (west side)', not a street: another kind of object indexed as one",
    "way/5671626": "'West 134th Street (upper)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/537122095": "'West 155th Street (surface)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1434926674": "'West 155th Street (surface)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1452454291": "'West 155th Street (surface)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1453922322": "'West 155th Street (surface)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/317731925": "'Sharansky Steps (East 43rd Street)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/633060696": "'West 238th Street, Manhattan College', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/46189288": "'Canal Street (lower level)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/46189291": "'Canal Street (lower level)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/166038501": "'Canal Street (lower level)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/492441172": "'Canal Street (lower level)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1555188774": "'Canal Street (lower level)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/46189305": "'Flatbush Avenue Extension (lower level)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/357279521": "'Flatbush Avenue Extension (lower level)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1262001667": "'Flatbush Avenue Extension (lower level)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1262001668": "'Flatbush Avenue Extension (lower level)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1262001669": "'Flatbush Avenue Extension (lower level)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/5703750": "'Boulevard', a bare type word for a name (owner, 2026-10-13)",
    "way/1316984161": "'Boulevard', a bare type word for a name (owner, 2026-10-13)",
    "way/1316984163": "'Boulevard', a bare type word for a name (owner, 2026-10-13)",
    "way/1316985163": "'Boulevard', a bare type word for a name (owner, 2026-10-13)",
    "way/815950309": "'116th Street Entrance to Riverside Park', a description standing in for a name (owner, 2026-10-13)",
    "way/1098028445": "'116th Street Entrance to Riverside Park', a description standing in for a name (owner, 2026-10-13)",
    "way/1098028446": "'116th Street Entrance to Riverside Park', a description standing in for a name (owner, 2026-10-13)",
    "way/31311315": "'Former Drive', a description standing in for a name (owner, 2026-10-13)",
    "way/113049822": "'Former Drive', a description standing in for a name (owner, 2026-10-13)",
    "way/936978385": "'Unmarked Trail', a description standing in for a name (owner, 2026-10-13)",
    "way/1070109028": "'Trail C2', a description standing in for a name (owner, 2026-10-13)",
    "way/1231608736": "'Trail C2', a description standing in for a name (owner, 2026-10-13)",
    "way/1231608737": "'Trail C2', a description standing in for a name (owner, 2026-10-13)",
    "way/1070109027": "'Trail W2', a description standing in for a name (owner, 2026-10-13)",
    "way/587942466": "'Trail W3', a description standing in for a name (owner, 2026-10-13)",
    "way/1230895066": "'RFK North Side Path', a description standing in for a name (owner, 2026-10-13)",
    "way/524630433": "'RFK south side walkway', a description standing in for a name (owner, 2026-10-13)",
    "way/685461548": "'RFK south side walkway', a description standing in for a name (owner, 2026-10-13)",
    "way/798923811": "'RFK south side walkway', a description standing in for a name (owner, 2026-10-13)",
    "way/801411755": "'RFK south side walkway', a description standing in for a name (owner, 2026-10-13)",
    "way/808614658": "'RFK south side walkway', a description standing in for a name (owner, 2026-10-13)",
    "way/849465511": "'RFK south side walkway', a description standing in for a name (owner, 2026-10-13)",
    "way/1233024340": "'RFK south side walkway', a description standing in for a name (owner, 2026-10-13)",
    "way/330958300": "'Walton Highschool Footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/222266004": "'VA Hospital Entrance Road', a description standing in for a name (owner, 2026-10-13)",
    "way/540295561": "'VA Hospital Entrance Road', a description standing in for a name (owner, 2026-10-13)",
    "way/540295563": "'VA Hospital Entrance Road', a description standing in for a name (owner, 2026-10-13)",
    "way/540295573": "'VA Hospital Entrance Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1357699935": "'VA Hospital Entrance Road', a description standing in for a name (owner, 2026-10-13)",
    "way/5671562": "'Riverbank Park Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/46568279": "'Riverbank Park Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/46568285": "'Riverbank Park Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/118524657": "'Riverbank Park Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/910522621": "'Riverbank Park Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1443589781": "'Riverbank Park Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/570980349": "'Ferry Point Park Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/570980351": "'Ferry Point Park Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/570980353": "'Ferry Point Park Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/570980366": "'Ferry Point Park Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/570980367": "'Ferry Point Park Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/570980369": "'Ferry Point Park Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1017252756": "'Ferry Point Park Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/225868289": "'Gravel Road Esplanade', a description standing in for a name (owner, 2026-10-13)",
    "way/1128345763": "'Gravel Road Esplanade', a description standing in for a name (owner, 2026-10-13)",
    "way/39332455": "'Bronx River Parkway Entrance', a description standing in for a name (owner, 2026-10-13)",
    "way/944979805": "'Major Deegan Entrance Northbound', a description standing in for a name (owner, 2026-10-13)",
    "way/32947291": "'Queensboro Bridge Approach', a description standing in for a name (owner, 2026-10-13)",
    "way/46419222": "'Queensboro Bridge Approach', a description standing in for a name (owner, 2026-10-13)",
    "way/32947297": "'Queensboro Bridge Exit', a description standing in for a name (owner, 2026-10-13)",
    "way/46419221": "'Queensboro Bridge Exit', a description standing in for a name (owner, 2026-10-13)",
    "way/46420287": "'Queensboro Bridge Exit', a description standing in for a name (owner, 2026-10-13)",
    "way/1458857123": "'Queensboro Bridge Exit', a description standing in for a name (owner, 2026-10-13)",
    "way/842448272": "'Federal Circle Pickup', a description standing in for a name (owner, 2026-10-13)",
    "way/842448270": "'Federal Circle Pickup Area', a description standing in for a name (owner, 2026-10-13)",
    "way/842448271": "'Federal Circle Pickup Area', a description standing in for a name (owner, 2026-10-13)",
    "way/842448269": "'Rental Car North', a description standing in for a name (owner, 2026-10-13)",
    "way/1421993295": "'Rental Car North', a description standing in for a name (owner, 2026-10-13)",
    "way/1473969372": "'Rental Car North', a description standing in for a name (owner, 2026-10-13)",
    "way/1473969373": "'Rental Car North', a description standing in for a name (owner, 2026-10-13)",
    "way/5700101": "'Rental Car South', a description standing in for a name (owner, 2026-10-13)",
    "way/130008710": "'Rental Car South', a description standing in for a name (owner, 2026-10-13)",
    "way/666925142": "'Rental Car South', a description standing in for a name (owner, 2026-10-13)",
    "way/666925143": "'Rental Car South', a description standing in for a name (owner, 2026-10-13)",
    "way/1556624915": "'Rental Car South', a description standing in for a name (owner, 2026-10-13)",
    "way/46930223": "'Terminal 1 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/46930231": "'Terminal 1 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/46930229": "'Terminal 1 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/46930792": "'Terminal 1 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1271205816": "'Terminal 1 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1271205817": "'Terminal 1 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/46932161": "'Terminal 4 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/998413801": "'Terminal 4 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/998413802": "'Terminal 4 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1133932818": "'Terminal 4 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1133932819": "'Terminal 4 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1508698638": "'Terminal 4 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1508698646": "'Terminal 4 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1508698647": "'Terminal 4 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/403555736": "'Terminal 5 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/997344098": "'Terminal 5 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/997344099": "'Terminal 5 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/997344100": "'Terminal 5 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1133972449": "'Terminal 5 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1133972450": "'Terminal 5 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1208018749": "'Terminal 5 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/46933399": "'Terminal 5 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/46933400": "'Terminal 5 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/46933418": "'Terminal 5 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/997344096": "'Terminal 5 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/997344097": "'Terminal 5 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1133972458": "'Terminal 5 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1208213360": "'Terminal 5 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1530514734": "'Terminal 5 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/46931917": "'Terminal 7 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/46931930": "'Terminal 7 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/46932201": "'Terminal 7 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/46932568": "'Terminal 7 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1435860445": "'Terminal 7 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1435860446": "'Terminal 7 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/46931914": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/46931923": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/46931925": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/46944041": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/997394208": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/997394211": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/997394212": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/997394213": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/997394214": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1133981737": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1415604711": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1415604712": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1423336170": "'Terminal 7 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/46931238": "'Terminal 8 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/997361435": "'Terminal 8 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/997397406": "'Terminal 8 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1134072082": "'Terminal 8 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1134072083": "'Terminal 8 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1134072087": "'Terminal 8 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1134072088": "'Terminal 8 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1134072089": "'Terminal 8 Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/46930780": "'Terminal 8 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/46931915": "'Terminal 8 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/997397411": "'Terminal 8 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/997397412": "'Terminal 8 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/997397413": "'Terminal 8 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1011547736": "'Terminal 8 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1134072094": "'Terminal 8 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1134072095": "'Terminal 8 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1434590129": "'Terminal 8 Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/677649595": "'Terminal B Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/730270540": "'Terminal B Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/818527302": "'Terminal B Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/656821460": "'Terminal B Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/818527303": "'Terminal B Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1086564978": "'Terminal C Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1134684413": "'Terminal C Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/647439389": "'Terminal C Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/657014234": "'Terminal C Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1134684412": "'Terminal C Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/695816991": "'Terminal C Inner Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/695816992": "'Terminal C Inner Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1069843813": "'Terminal C Inner Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1086564977": "'Terminal C Inner Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1134684418": "'Terminal C Inner Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1134684421": "'Terminal C Inner Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/650689142": "'Terminal C Inner Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/731142642": "'Terminal C Inner Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/834733833": "'Terminal C Inner Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1134684419": "'Terminal C Inner Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/646590591": "'Terminal C Outer Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/719957193": "'Terminal C Outer Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1069843812": "'Terminal C Outer Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1134581657": "'Terminal C Outer Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1134684423": "'Terminal C Outer Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/1208232681": "'Terminal C Outer Arrivals', a description standing in for a name (owner, 2026-10-13)",
    "way/653176169": "'Terminal C Outer Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1134684417": "'Terminal C Outer Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/1134684420": "'Terminal C Outer Departures', a description standing in for a name (owner, 2026-10-13)",
    "way/463925180": "'Hunts Point Co-Op Market', a housing estate's own way, named for the estate",
    "way/1082200167": "'Hunts Point Co-Op Market', a housing estate's own way, named for the estate",
    "way/1082200168": "'Hunts Point Co-Op Market', a housing estate's own way, named for the estate",
    "way/1082200169": "'Hunts Point Co-Op Market', a housing estate's own way, named for the estate",
    "way/1420131626": "'Hunts Point Co-Op Market', a housing estate's own way, named for the estate",
    "way/27518032": "'Hudson View Gardens', a housing estate's own way, named for the estate",
    "way/38834613": "'Rentar Plaza', a housing estate's own way, named for the estate",
    "way/38834614": "'Rentar Plaza', a housing estate's own way, named for the estate",
    "way/157168829": "'Rentar Plaza', a housing estate's own way, named for the estate",
    "way/157168830": "'Rentar Plaza', a housing estate's own way, named for the estate",
    "way/157168833": "'Rentar Plaza', a housing estate's own way, named for the estate",
    "way/570279275": "'Rentar Plaza', a housing estate's own way, named for the estate",
    "way/570279278": "'Rentar Plaza', a housing estate's own way, named for the estate",
    "way/1495601426": "'Rentar Plaza', a housing estate's own way, named for the estate",
    "way/5697353": "'Riverdale Yacht Club', a housing estate's own way, named for the estate",
    "way/362875966": "'Whole Foods Promenade', a housing estate's own way, named for the estate",
    "way/226998567": "'IKEA Greenway', a housing estate's own way, named for the estate",
    "way/226998571": "'IKEA Greenway', a housing estate's own way, named for the estate",
    "way/5695880": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/5696234": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/223939820": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/223939824": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/552581428": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/552581429": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/552581430": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/552581431": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/586133540": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/586133541": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/1416501146": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/1418624242": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/1418624243": "'Bronx State Hospital', a housing estate's own way, named for the estate",
    "way/420900450": "'Edward L. Grant Highway', not a street: another kind of object indexed as one",
    "way/421842668": "'Edward L. Grant Highway', not a street: another kind of object indexed as one",
    "way/984188814": "'Edward L. Grant Highway', not a street: another kind of object indexed as one",
    "way/1160271928": "'Edward L. Grant Highway', not a street: another kind of object indexed as one",
    "way/1160271931": "'Edward L. Grant Highway', not a street: another kind of object indexed as one",
    "way/1160271933": "'Edward L. Grant Highway', not a street: another kind of object indexed as one",
    "way/60836965": "'Saint Aloysius Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1078676065": "'Saint Anne Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60836971": "'Saint Boniface Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60837023": "'Saint Bridget Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/336930600": "'Saint Calixtus Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1078676060": "'Saint Cecilia Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1078676049": "'Saint Jerome Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60840033": "'Saint John's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1102469825": "'Saint John's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1078676069": "'Saint Mark Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60840010": "'Saint Mary's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1102469824": "'Saint Mary's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60836952": "'Saint Matthew Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1102412392": "'Saint Matthew Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1102412393": "'Saint Matthew Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60837111": "'Saint Michael Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60837074": "'Saint Patrick Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60839993": "'Saint Peter Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1102469830": "'Saint Peter Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60840046": "'Saint Rose Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60840000": "'Saint Stephen's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1102469822": "'Saint Stephen's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1102469823": "'Saint Stephen's Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/1078676046": "'Saint Thomas Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/724428590": "'Saint Veronica Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60836994": "'Saint Vincent de Paul Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/60837033": "'Saint William Avenue', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/705304809": "'30 Lincoln Plaza', home: an apartment tower's plaza under the tower's address (leisure=park); precedent: an apartment complex's own feature (flag check, 2026-10-13)",
    "way/1466260659": "'Aqueduct Walk (Morten to West Burnside)', description: one of eight segment rows 'Aqueduct Walk (X to Y)' beside the park's own 'Aqueduct Walk' row; the other seven were not flagged (flag check, 2026-10-13)",
    "node/2547006642": "'Bungalow 45', home: amenity=place_of_worship with religion=none at an apartment unit's address; a code and a type word for a name (flag check, 2026-10-13)",
    "way/247867461": "'Capitale', business: an events venue under its trade name (amenity=events_venue); the landmark bank is only its old_name (flag check, 2026-10-13)",
    "way/796271669": "'Italian American Organizations of Queens Soccer', glitch: name cut short (ends 'Soccer'); leisure=park (flag check, 2026-10-13)",
    "way/265345877": "'Knickerbocker Clubhouse', a members' club's building with no article: a private club (flag check, settled by the existing rules, 2026-10-13)",
    "way/1157217875": "'Loujane', not a place: a derelict ship, access=no, historic=ship with no tourism tag and no article (flag check, 2026-10-13)",
    "way/296322565": "'Lowe's Esplanade', business: an esplanade named for the store beside it: a brand as the name (flag check, 2026-10-13)",
    "node/357607736": "'Lower Forecourt', description: a position word and a type word (precedent: Boston's 'Upper Plaza') (flag check, 2026-10-13)",
    "node/4798493527": "'Michael Altman Fine Art', business: an art dealer's firm under the dealer's name: tourism=gallery, wikidata only, no article (flag check, 2026-10-13)",
    "way/36870581": "'Park Village's', glitch: a residents' association's park (its note tag) under a cut-short possessive name (flag check, 2026-10-13)",
    "node/5995383978": "'Roseland Ballroom', gone: historic=theatre node whose own article says the building was demolished; no lifecycle tag, so by id (flag check, 2026-10-13)",
    "way/1053727138": "'Royal Ranch Pool Club', private facility: a members' pool club tagged leisure=park (flag check, 2026-10-13)",
    "way/697722180": "'South Bronze Names Parapets', description: a component of a memorial (barrier=wall) named by a description (flag check, 2026-10-13)",
    "way/1025959315": "'The Square', description: an article and a type word (precedent: Boston's 'The Green') (flag check, 2026-10-13)",
    "node/357607739": "'Upper Forecourt', description: a position word and a type word (precedent: Boston's 'Upper Plaza') (flag check, 2026-10-13)",
    "way/1263525980": "'Urban Plaza', description: 'urban plaza' is the zoning type of the space; operator a property company (flag check, 2026-10-13)",
    "way/218327131": "'Verizon Plaza', business: a privately run plaza named for its corporate tenant (operator a property company) (flag check, 2026-10-13)",
    "node/4148060867": "'World War I', description: a monument named only by its subject (flag check, 2026-10-13)",
    "node/11013387510": "'World War I/II victims', description: a monument named only by its subject (flag check, 2026-10-13)",
    "node/158807303": "'Cedar Manor Houses', a housing development mapped as a place (owner, 2026-10-13)",
    "node/158813854": "'Lambert Houses', a housing development mapped as a place (owner, 2026-10-13)",
    "node/158843513": "'Richmond Terrace Houses', a housing development mapped as a place (owner, 2026-10-13)",
    "way/1134632481": "'Terminal B Bus/Taxi Lane', description: an airport bus and taxi lane (flag check, 2026-10-13)",
    "way/785917467": "'Terminal B Bus/Taxi Lane', description: an airport bus and taxi lane (flag check, 2026-10-13)",
    "way/882869690": "'Terminal B Bus/Taxi Lane', description: an airport bus and taxi lane (flag check, 2026-10-13)",
    "way/1110193733": "'Zoo Center Path', description: a path inside a paid zoo (flag check, 2026-10-13)",
    "way/1110193734": "'Zoo Center Path', description: a path inside a paid zoo (flag check, 2026-10-13)",
    "way/221286927": "'Zoo Center Path', description: a path inside a paid zoo (flag check, 2026-10-13)",
    "way/266940034": "'George F. Baker Jr. and Sr. Houses', houses with an article of their own and no tourism tag: a home is kept only when open to visit or tagged an attraction (wave 1's unsure rows, settled on the Wikidata lookup and the existing rules, 2026-10-13)",
    "node/5171173318": "'La Sinagoga', a place of worship named only by a denomination, a body or a chain, in a form the shared rule's lists do not hold; no wikipedia tag of its own (owner's rulings, 2026-10-13)",
    # The pattern screen of 2026-10-13: rows that fall squarely in one of the owner's
    # class rulings of that date, each with its ruling.
    "way/225190636": "'Playground 103', a park named only by a category and an inventory number (owner, 2026-10-13, ruling 1 of the class rulings; pattern screen)",
    "way/765274333": "'Playground 11', a park named only by a category and an inventory number (owner, 2026-10-13, ruling 1 of the class rulings; pattern screen)",
    "way/389592778": "'Playground 115', a park named only by a category and an inventory number (owner, 2026-10-13, ruling 1 of the class rulings; pattern screen)",
    "way/185148215": "'Playground 286', a park named only by a category and an inventory number (owner, 2026-10-13, ruling 1 of the class rulings; pattern screen)",
    "way/1539568479": "'Playground 80', a park named only by a category and an inventory number (owner, 2026-10-13, ruling 1 of the class rulings; pattern screen)",
    "way/1013201642": "'Plaza 67', a park named only by a category and an inventory number (owner, 2026-10-13, ruling 1 of the class rulings; pattern screen)",
    "way/280354485": "'Queens Assembly Hall of Jehovahs Witnesses', a religious body's reading room, assembly hall or institute tagged a place of worship, not a congregation (owner, 2026-10-13, ruling 2; pattern screen)",
    "way/249973243": "'Saint Thomas Parish House', a part of one church as its own row, the church's own row within 300 m (owner, 2026-10-13, ruling 4; pattern screen)",
    "node/8265113845": "'Campus Plaza', a stock plaza or square name with no place in it (owner, 2026-10-13, ruling 5 and its follow-up: every plaza name with no place in it; pattern screen)",
    "way/556607149": "'Alumni Plaza', a stock plaza or square name with no place in it (owner, 2026-10-13, ruling 5 and its follow-up: every plaza name with no place in it; pattern screen)",
    "way/453456965": "'Tribeca Tower Courtyard', the grounds of an office or apartment building, or of a housing estate by its operator, tagged a park or square (owner, 2026-10-13, the estate-facility ruling as applied to Toronto; pattern screen)",
    "way/1205355316": "'Evans Tower Plaza', the grounds of an office or apartment building, or of a housing estate by its operator, tagged a park or square (owner, 2026-10-13, the estate-facility ruling as applied to Toronto; pattern screen)",
    "way/998966824": "'Barbadoes Basin', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
    "way/998966847": "'Bergen Basin', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
    "way/998966837": "'Grassy Bay', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
    "way/998966815": "'Little Bay', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
    "way/998966814": "'Norton Basin', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
    "way/998966839": "'Paerdegat Basin', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
    "way/998966845": "'Shellbank Basin', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
    "way/998966816": "'Sommerville Basin', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
    "way/998966821": "'Thurston Basin', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
    "way/998966825": "'Vernam Basin', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
    "node/369038512": "'Little Neck Bay', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
    "way/999755798": "'Little Neck Bay', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
    "node/6030126915": "'Joseph Sanford Jr. Channel', one bay or channel labelled more than once; the row with the Wikidata entry or article stays (owner, 2026-10-13, ruling 9; pattern screen)",
}

# Public art kept by the owner's word against the article rule (place_index,
# PLACE_KEPT; owner, 2026-10-13). Each is a known work the Wikidata lookup
# cannot admit; DECISIONS.md of that date lists the works left out.
PLACE_KEPT = {
    "way/958999496": "'John Lennon's Imagine', a known work the article rule drops for want of an article of its own (owner, 2026-10-13)",
    "node/2727025839": "'Balto', a known work the article rule drops for want of an article of its own (owner, 2026-10-13)",
    "node/7826843768": "'Patience', a known work the article rule drops for want of an article of its own (owner, 2026-10-13)",
    "node/7826843767": "'Fortitude', a known work the article rule drops for want of an article of its own (owner, 2026-10-13)",
}
