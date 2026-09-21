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
