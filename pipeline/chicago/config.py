"""Chicago-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Deliberately NOT yet folded into a shared data/registry.yaml loader: the
scaffold is planned for after this city (see PLAN.md), so the shared fields
can be chosen with a local-taxonomy city in hand.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "chicago" / "raw"
DATA_PROCESSED = ROOT / "data" / "chicago" / "processed"
OUTPUTS = ROOT / "outputs" / "chicago"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# CTA stations outside the City of Chicago (suburban stops on the Blue, Green,
# Pink, Purple and Red lines), recorded as a scoping decision, like the other
# cities' excluded_stations.csv.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs. Download commands (all public):
#   gtfs.zip  curl -sL https://www.transitchicago.com/downloads/sch_data/google_transit.zip
#   city_boundary.geojson  Socrata "Boundaries - City" (dataset qqq8-j68g;
#     the "- Map" asset ewy2-6yfk has null geometry):
#       curl -sL 'https://data.cityofchicago.org/resource/qqq8-j68g.geojson?$limit=10'
#   business_licenses_active.csv  Socrata "Business Licenses" (r5kz-chrr),
#     server-filtered to issued, unexpired licenses (the full table is every
#     license term since 2002, 1.2M rows). Snapshot taken 2026-09-20:
#       curl -sG https://data.cityofchicago.org/resource/r5kz-chrr.csv
#         --data-urlencode "$where=license_status='AAI' AND expiration_date >= '2026-09-20T00:00:00'"
#         --data-urlencode '$limit=200000' --data-urlencode '$order=id'
GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "business_licenses_active.csv"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"

# The date the raw licenses were downloaded (and the expiry cut-off applied):
# licenses expiring before it are not active. Step 2 re-applies it, so a
# re-run against the same file is deterministic.
AS_OF_DATE = "2026-09-20"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 16N. Chicago's longitude (~-87.65) falls in the -90 to -84 band.
# Derived per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32616"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# CTA 'L' only; Metra is deliberately out of scope for this build (one
# agency's rail system per city, as in the other cities; see DECISIONS.md).
# route_type 1 in the CTA feed; route_ids are the feed's own. Yellow ("Y") is
# NOT included: it has 3 stations and only Howard (also served by Red and
# Purple) lies in the city, so there is nothing of it to draw (the chopping-
# block rule agreed before the build). The other seven lines all have at
# least 15 in-city stations.
#
# Station spacing inside the city is uniformly sparse (median nearest-
# neighbour distance ~740 m, no street-running offshoots), so every in-city
# station is kept and the sub-transit-line filters are not needed. The
# exception is the Loop and Loop subway area, where stations are 140-250 m
# apart (Jackson and Monroe each have separate Blue and Red stations ~140 m
# apart): their rings overlap, which is a conscious choice - each business is
# assigned to its nearest station, so nothing is double-counted.
CTA_RAIL_ROUTE_IDS = ["Red", "P", "Blue", "Pink", "G", "Org", "Brn"]

# Real public names (CTA's own route_long_name, checked against the feed).
CTA_LINE_NAMES = {
    "Red": "Red Line",
    "P": "Purple Line",
    "Blue": "Blue Line",
    "Pink": "Pink Line",
    "G": "Green Line",
    "Org": "Orange Line",
    "Brn": "Brown Line",
}

# Gate 3: CTA's own station list on each line's page, keyed as
# CTA_RAIL_ROUTE_IDS and counted over every station the line's trips serve,
# before the city-limits cut. The five lines round the Loop each list
# State/Lake, which CTA marks "closed for reconstruction into 2029" and the
# feed no longer serves, so each figure is CTA's less State/Lake. Purple counts
# its Loop and North Side express stops, as CTA's page lists them.
OPERATOR_STATION_COUNTS = {
    "Red": 33,
    "P": 25,     # 26 less State/Lake (closed)
    "Blue": 33,
    "Pink": 21,  # 22 less State/Lake (closed)
    "G": 30,     # 31 less State/Lake (closed)
    "Org": 15,   # 16 less State/Lake (closed)
    "Brn": 26,   # 27 less State/Lake (closed)
}
OPERATOR_COUNTS_SOURCE = ("CTA line pages' station lists, "
                          "https://www.transitchicago.com/<line>line/ for red, "
                          "purple, blue, pink, green, orange and brown (read "
                          "2026-10-01)")

# --- Business filtering ------------------------------------------------

# The dataset's `city` field, exact match. Checked 2026-09-20: 49,066 of the
# 53,039 active rows say CHICAGO; the rest are suburbs (Cicero, Des Plaines,
# Melrose Park, Naperville, ...). Step 2 also cross-checks against the
# boundary polygon.
CITY_KEEP = "CHICAGO"

# Encoding of this city's RAW source files, declared rather than inferred.
# pandas defaults to UTF-8 and raises on anything else - safe, but it leaves
# the next person to guess, and reaching for latin-1 to silence a
# UnicodeDecodeError corrupts accented names without ever failing. Declaring it
# makes the choice reviewable and part of the provenance. See the encoding rule
# in docs/data_sources.md; non-US cities are where this bites.
SOURCE_ENCODING = "utf-8"

TAXONOMY_SYSTEM = "chicago_license"
# The raw export's own classification column (already the taxonomy's
# VALUE_COLUMN, so step 2's rename is a no-op).
RAW_CLASSIFICATION_COLUMN = "license_description"

# One storefront can hold several licenses (a restaurant's Retail Food
# Establishment plus adjunct Consumption on Premises, Outdoor Patio and Tobacco
# licenses); the site is (account_number, site_number). Step 2 keeps one row
# per site, taking the license earliest in this list, so the primary license
# decides the bucket and an adjunct counts only where a site has no primary.
LICENSE_PRIORITY = [
    "Retail Food Establishment",
    "Tavern",
    "Limited Business License",
    "Regulated Business License",
    "Package Goods",
    "Filling Station",
    "Secondhand Dealer",
    "Tobacco",
]

# Sanity bounds for the supplied lat/lng (Chicago spans roughly 41.64-42.02 N,
# -87.94 to -87.52 W). All 48,614 active in-city rows with coordinates fell
# inside this box on 2026-09-20: unlike Los Angeles, no corrupt coordinates.
CHICAGO_BBOX = {
    "lat_min": 41.60,
    "lat_max": 42.05,
    "lon_min": -87.95,
    "lon_max": -87.50,
}

# --- Place search (sample, 2026-10-08) ----------------------------------------

# OSM's places inside the city line, one Overpass query by
# pipeline/place_index_fetch.py, indexed by step2b_place_index.py (the Kyoto
# pilot, DECISIONS.md "Four ideas assessed", item 3). The area is the city's
# OSM boundary relation 122604 (admin_level 8, one match, looked up
# 2026-10-08); an area id is 3600000000 plus the relation's.
PLACE_AREA = "(id:3600122604)"
# A NEW file name: data/ is shared by every worktree.
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-08.json"
# place_index_fetch.EXTRA_QUERY's classes (stadiums, artworks, civic
# buildings, airports, beaches, bays, places as areas), a second query since
# 2026-10-08.
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-08.json"
# The local language(s) of OSM's `name` here (place_index.py, LANGUAGES); no
# long-vowel fold (place_index.FOLDS).
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
PLACE_REVIEWED = {
    "Schulze Baking Company": "an NRHP-listed former bakery building (Wikipedia), building=manufacture",
}
# OSM objects a reading by eye found to be a business or a home that no rule
# in place_index.py catches, each with why (place_index.build, `dropped`).
PLACE_DROPPED = {
    "node/8968057698": "'Waller Apartments', homes, kept by a lone tourism=attraction on a node",
    "way/807330592": "'Lawrence House Patio', a leisure=park named for an apartment building: its grounds",
    "way/1175801225": "'Northern Trust open space', a plaza named for the bank that owns it",
}

# Visitable former homes (owner, 2026-10-08: "visitable only hard line. Must
# make sure info is up-to-date"): homes the home rule holds out that the public
# can visit today, by OSM id, each checked at its source on the date given
# (place_index, VISITABLE FORMER HOMES). scripts/check_place_search.py G fails
# once an entry is a year old: check it again at its source and renew
# "checked", or remove it.
PLACE_VISITABLE = {
    "way/163325251": {"name": "Noble-Seymour Crippen House", "access": "OPEN_REGULAR",
        "source": "https://norwoodparkhistoricalsociety.org/about-us/",
        "checked": "2026-10-08",
        "why": "the Norwood Park Historical Society's museum, open Saturdays noon to 4 pm"},
}

# Public art kept by the owner's word against the article rule (place_index,
# PLACE_KEPT; owner, 2026-10-13). Each is a known work the Wikidata lookup
# cannot admit; DECISIONS.md of that date lists the works left out.
PLACE_KEPT = {
    "node/10780734457": "'Sue the Dinosaur', its own article, on an entry the map also gives as its subject's (owner, 2026-10-13)",
    "node/3554700407": "'Sir Georg Solti Bust', its own article, on an entry the map also gives as its subject's (owner, 2026-10-13)",
    "node/7022676547": "'Jack Brickhouse', its own article, on an entry the map also gives as its subject's (owner, 2026-10-13)",
    "node/667225235": "'A Signal of Peace', its own article, on an entry the map also gives as its subject's (owner, 2026-10-13)",
    "node/3554716802": "'The Alarm', its own article, on an entry the map also gives as its subject's (owner, 2026-10-13)",
    "way/210671752": "'Lion in an attitude of defiance', its own article, on an entry the map also gives as its subject's (owner, 2026-10-13)",
    "way/210671756": "'Lion on the prowl', its own article, on an entry the map also gives as its subject's (owner, 2026-10-13)",
    "way/1433718651": "'Richard Oglesby Monument', its own article, on an entry the map also gives as its subject's (owner, 2026-10-13)",
    "way/1433718663": "'Alexander Hamilton Monument', its own article, on an entry the map also gives as its subject's (owner, 2026-10-13)",
    "way/1433718665": "'John Peter Altgeld Momument', its own article, on an entry the map also gives as its subject's (owner, 2026-10-13)",
}
