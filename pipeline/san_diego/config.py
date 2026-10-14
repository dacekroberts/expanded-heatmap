"""San Diego-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Deliberately NOT yet folded into a shared data/registry.yaml loader: wait
until more cities show the real common shape before generalizing (see
PLAN.md).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "san_diego" / "raw"
DATA_PROCESSED = ROOT / "data" / "san_diego" / "processed"
OUTPUTS = ROOT / "outputs" / "san_diego"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Step 2's output BEFORE its home-business filter. fetch_parcels.py reads THIS,
# never businesses_clean.csv. Reading the filtered file leaves the already
# removed rows out of the cache, and without a cache row they are not flagged,
# so they return on the next run. Removed once on the mistaken reasoning that
# "the filter only removes rows, so the candidate set can only shrink" - true,
# but the shrinkage is exactly the rows that must stay removed.
BUSINESSES_PREFILTER_CSV = DATA_PROCESSED / "businesses_clean_prefilter.csv"

GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "sd_businesses_active_datasd.csv"
MUNICIPAL_BOUNDARIES_GEOJSON = DATA_RAW / "municipal_boundaries.geojson"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 11N. San Diego's longitude (~-117) falls in the -120 to -114
# band. Derived per city, not copied - see docs/project_context.md's CRS
# lesson.
CRS_PROJECTED = "EPSG:32611"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city. This is a category-definition
# choice (how far from a station counts as "walkshed"), not a city-specific
# measurement, so there's no reason to vary it yet. Revisit if a city's
# station spacing is meaningfully different.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# MTS Trolley route_ids with route_type "0" (tram/light rail) in the GTFS
# feed, i.e. Blue/Orange/Green/Copper/Silver - excludes the "MTG Event
# Line" (route_id 540), a one-off special-event shuttle, not regular
# trolley service.
TROLLEY_ROUTE_SHORT_NAMES = ["Blue", "Orange", "Green", "Copper", "Silver"]

# GTFS station names that are the same physical station split by a
# disambiguating suffix - collapse before city-boundary filtering so it
# isn't treated as two separate stations. Found by inspection of the raw
# stop_name list (2026-09-18).
GTFS_NAME_ALIASES = {
    "12th & Imperial Station (Bayside)": "12th & Imperial Station",
}

# --- Gate 3: the operator's own per-line station counts ----------------------
# Whole lines, BEFORE the city-limits cut (Santee, El Cajon, La Mesa, Lemon
# Grove, National City and Chula Vista stations count here). An interchange
# counts once on each line it serves. Keyed as step 1 keys its lines: the
# feed's route_short_name (TROLLEY_ROUTE_SHORT_NAMES).
OPERATOR_STATION_COUNTS = {
    # UTC - San Ysidro is 32. This feed also has 2 of its 1,898 Blue trips
    # (12th & Imperial-bound, one each on two weekday service_ids) running via
    # the Bayside - Seaport Village, Convention Center, Gaslamp Quarter - so
    # the feed's Blue Line calls at 35. All three are Green Line stations,
    # drawn anyway; no station changes. 32 + 3 = 35.
    "Blue": 35,
    "Orange": 19,
    # 12th & Imperial - El Cajon. Wikipedia's network table still says 27,
    # from before 2024-09-29, when the Green Line was cut back to El Cajon and
    # the Copper Line took over Arnele Avenue, Gillespie Field and Santee; the
    # Green Line article's own infobox and station table say 24.
    "Green": 24,
    "Copper": 4,
    "Silver": 9,
}
OPERATOR_COUNTS_SOURCE = (
    "en.wikipedia.org/wiki/San_Diego_Trolley, table of lines (Blue 32, Orange "
    "19, Copper 4, Silver 9), and en.wikipedia.org/wiki/Green_Line_(San_Diego_"
    "Trolley), infobox and station table (24), read 2026-10-01 - secondary. "
    "MTS's own line pages (sdmts.com) give termini, not station lists."
)

# City boundary name to filter Municipal_Boundaries.geojson (SanGIS's
# municipal boundaries, hosted by SANDAG; covers all San Diego County
# municipalities) down to.
CITY_BOUNDARY_NAME = "SAN DIEGO"

# --- Business filtering ------------------------------------------------

# Kept for the scaffold's templates; NOT the filter. Step 2 decides "in San
# Diego" by testing each business point against the city's polygon in
# MUNICIPAL_BOUNDARIES_GEOJSON (CITY_BOUNDARY_NAME), the file step 1 already
# uses for stations (owner, 2026-10-04). The exact match on address_city that
# this string drove dropped storefronts inside the city whose address names
# the neighborhood instead: La Jolla 477, San Ysidro 194, Del Mar 43 and stray
# spellings, 724 in all; it also kept 55 rows that lie outside the city
# (both measured 2026-10-04, before the booth-rental codes left).
CITY_KEEP = "SAN DIEGO"

# Encoding of this city's RAW source files, declared rather than inferred.
# pandas defaults to UTF-8 and raises on anything else - safe, but it leaves
# the next person to guess, and reaching for latin-1 to silence a
# UnicodeDecodeError corrupts accented names without ever failing. Declaring it
# makes the choice reviewable and part of the provenance. See the encoding rule
# in docs/data_sources.md; non-US cities are where this bites.
SOURCE_ENCODING = "utf-8"

TAXONOMY_SYSTEM = "naics"
# The raw export's own classification column. Step 2 renames it to the
# taxonomy's VALUE_COLUMN, then filters via pipeline.taxonomies.
RAW_CLASSIFICATION_COLUMN = "naics_code"

# NAICS codes excluded for THIS city only, EXACT match (owner, 2026-09-29) -
# Los Angeles' and San Francisco's NAICS_EXCLUDE_CODES idiom, applied as its
# own printed filter in step 2. San Diego's registry files codes at variable
# length, and these three are its own:
#   8129    "OTHER PERSONAL SERVICES" at the bare industry-group level (569
#           pins). A sample reads calibration labs, marine services, waste
#           collection, remodelling, photographers: the catch-all under
#           another number. EXACT, because the prefix would take 81291 pet
#           care and 81292 photofinishing, which stay.
#   72234   "COTTAGE FOOD OPERATOR" (192): California's licence for a home
#           kitchen (bakers, sweets) - food with no counter of its own.
#   81295 / 812959  "KIOSK/ATM BUSINESSES" / "OTHER KIOSK RELATED BUSINESS"
#           (23 + 3): ecoATM phone-recycling machines and two carrier kiosks
#           - a machine, not a storefront. ecoATM files under both codes.
#   812114 / 812115  "BARBER SHOPS - BOOTH RENTAL" / "BEAUTY SHOPS - BOOTH
#           RENTAL" (owner, 2026-10-04): a chair rented inside someone else's
#           shop, the renter's own licence, so out under docs/category_rules.md
#           "A person's own license to work inside someone else's premises".
#           The precedent is D.C.'s "Beauty Booth" (DECISIONS 2026-10-03,
#           "Washington D.C. drops "Beauty Booth" under the person-licence
#           rule"). The shop's own 812111/812112 licence keeps the shop on the
#           map. Measured before the change: 67 pins (58 + 9), 347 rows.
#   452999  "SWAP MEET VENDOR" (owner, 2026-10-04): a stall at a weekend
#           swap meet is not a storefront, as Mexico City keeps fixed premises
#           only and R1 drops food stalls. 176 rows city-wide, 55 pins at the
#           largest swap meet; accounts there filed as ordinary retail stay.
NAICS_EXCLUDE_CODES = {"8129", "72234", "81295", "812959", "812114", "812115", "452999"}

# The near misses: exact matching must leave 81291 pet care and 81292
# photofinishing classified and on the map.
from pipeline.taxonomies.naics import naics_group as _ng  # noqa: E402
assert _ng("81291") == "Personal services" and "81291" not in NAICS_EXCLUDE_CODES
assert _ng("81292") == "Personal services" and "81292" not in NAICS_EXCLUDE_CODES
assert all(_ng(_c) is not None for _c in NAICS_EXCLUDE_CODES), \
    "a per-city exclusion must name a code the taxonomy would otherwise map"

# Sanity bounds for the business dataset's own lat/lng. San Diego's data
# ships pre-geocoded (see step2), so this is a data-quality check on the
# supplied coordinates, not a post-geocode validation.
SAN_DIEGO_BBOX = {
    "lat_min": 32.53,
    "lat_max": 33.15,
    "lon_min": -117.32,
    "lon_max": -116.75,
}

# --- Assessor parcels, for the home-business filter ------------------------
# San Diego was the city with NO residence signal at all: its address_suite
# holds bare values ("A", "101") with no APT/STE token, so address text cannot
# flag a residence, and 903 of its mapped pins display a name identical to the
# registered owner's. Its 0.03% reading was a MEASUREMENT GAP, not a clean
# result. Step 0 on 2026-09-21 found it is in fact the best-equipped of the
# three cities that needed this.
#
# SanGIS publishes ONE countywide parcel layer, hosted by SANDAG (1,089,758 polygons), so
# the geographically split Parcels_South/_North/_East siblings are not needed.
PARCEL_SERVICE_URL = (
    "https://geo.sandag.org/server/rest/services/Hosted/Parcels/"
    "FeatureServer/0/query"
)
# `ownerocc` is 'Y' on 472,498 parcels and null otherwise - a genuine
# owner-occupancy flag, the signal this city was thought to lack.
#
# `asr_landuse` is numeric with NO coded-value domain published, so the codes
# were verified empirically rather than guessed (2026-09-21):
#   11  571,236 parcels, nucleus_use_cd 110/111, unitqty 1, mostly ownerocc='Y'
#       -> single-family detached. THIS is the residential signal.
#   17  199,972 parcels, nucleus_use_cd 171 -> condominium. EXCLUDED, for the
#       same reason as San Francisco's Multi-Family and New York's
#       multi-family lots: a unit in a shared building may be ground-floor
#       retail, and filtering it would delete real storefronts.
PARCEL_RESIDENTIAL_CODES = (11,)
# WHY THIS CITY NEEDS A NEAREST JOIN RATHER THAN A POINT-IN-PARCEL TEST.
# San Diego's business coordinates sit SYSTEMATICALLY 5-15 m from their own
# parcel: measured on 30 sampled pins, an exact point-in-parcel test matched
# 1/30, a 5 m buffer 9/30, 10 m 21/30 and 25 m 30/30. Not a precision problem -
# these carry 8 decimal places against Los Angeles' 4 - but a placement one:
# they sit at the street frontage, and SanGIS parcels exclude road
# right-of-way. So "which parcel contains this point?" has almost no answers
# here, and the question to ask is "which parcel is nearest?".
#
# REPLACED the per-point lookup on 2026-09-21. Per-point queries were the
# wrong tool for this city twice over: they answered the unanimity question
# rather than the nearest-parcel one (because these coordinates sit 5-15 m
# outside their own parcel), and ~5,000 of them got the service to block us.
# A single bulk download plus a local nearest join is both correct and politer,
# and it is what San Francisco already does.
PARCELS_CENTROIDS_CSV = DATA_RAW / "parcels_centroids.csv"
# The layer returns 2,000 features per page and supports centroid-only
# responses (supportsReturningGeometryCentroid), so no polygon geometry is
# transferred. Paging needs a stable sort - `apn` is the layer's own key.
PARCEL_PAGE_SIZE = 2000
# Covers every mapped business point plus ~400 m, measured from the data
# rather than reusing SAN_DIEGO_BBOX, which is a deliberately loose sanity
# box reaching far into the back country (861k parcels against 665k here).
PARCEL_QUERY_BBOX = {
    "lon_min": -117.280,
    "lon_max": -116.914,
    "lat_min": 32.540,
    "lat_max": 33.134,
}
# Nearest-parcel tolerance for the local join. Chosen from the measured
# offset: on 30 sampled pins an exact point-in-parcel test matched 1, a 5 m
# buffer 9, 10 m 21 and 25 m 30. 25 m accepts the frontage parcel without
# reaching across a street.
PARCEL_TOLERANCE_M = 25.0
# The registry's own structural signal, the same kind as Philadelphia's
# legalentitytype: 24,974 rows are sole proprietorships. Requiring this as
# well as a person-like name, a single-family parcel and owner occupancy makes
# this the most conservative of the three filters.
SOLE_OWNERSHIP_TYPE = "SOLE"

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3600253832)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {
    "Pharmacy Lane": "a public street of that name in a medical district, not a pharmacy's drive",
}
PLACE_DROPPED = {
    "way/148910128": "'Balboa Park Miniature Railroad Station', a tourist or heritage ride indexed as a station: not transit (owner, 2026-10-13)",
    "node/3844511892": "'Northern Frontier', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/289336107": "'Shipwreck Isle', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/275049180": "'Bayside Amphitheater', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/80664580": "'Nautilus Amphitheater', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/499843853": "'Orca Stadium', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/275056223": "'Sea Lion and Otter Stadium', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/174506301": "'Reviewing Stands', a description standing in for a name (owner, 2026-10-13)",
    "way/621633429": "'Bench area', a description standing in for a name (owner, 2026-10-13)",
    "way/481134990": "'BMX course', a description standing in for a name (owner, 2026-10-13)",
    "node/5474499377": "'Public Gazebo', a description standing in for a name (owner, 2026-10-13)",
    "way/773892434": "'Faculty Staff Club outside patio.', a business's own way, named for the business",
    "way/1219435263": "'Cyanide Vat', abandoned by its own tags (owner, 2026-10-13)",
    "way/1219435264": "'Cyanide Vat', abandoned by its own tags (owner, 2026-10-13)",
    "way/1219435266": "'Cyanide Vat', abandoned by its own tags (owner, 2026-10-13)",
    "node/5872436694": "'Del Mar Airport (historic)', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "way/978812546": "'Pasatiempo Neighborhood Park (Undeveloped)', not yet open by its own tags or name (owner, 2026-10-13)",
    "way/567949743": "'b-rice Purk', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "node/358846048": "'Second Church', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/358845417": "'Seventh Church', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/1414334909": "'Carmelite Monastery', a religious residence",
    "node/358860205": "'Dominican Fathers', a religious residence",
    "way/960932873": "'Marriot Marquis Square', a business's own way, named for the business",
    "node/6858400911": "'Chaplain's Office - Naval Base San Diego Chapel', an office under a description, not a place",
    "node/351916273": "'La Jolla Presbyterian', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/358860547": "'Saint Gregory the Great Catholic Parish', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/597141288": "'Allied Gardens Park', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/358787116": "'La Jolla Park', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/358792013": "'San Carlos Park', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/368171193": "'Christian Center', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "relation/4729047": "'Silver Line', a route relation indexed as a landmark: not a place",
    "way/6051495": "'Emergency Access', a bare type word for a name (owner, 2026-10-13)",
    "way/652999978": "'Emergency Access', a bare type word for a name (owner, 2026-10-13)",
    "way/246182889": "'Business Access Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1341594433": "'Business Access Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1430130644": "'Business Access Road', a bare type word for a name (owner, 2026-10-13)",
    "way/234729692": "'Community Garden access road', a bare type word for a name (owner, 2026-10-13)",
    "way/234729696": "'Community Garden access road', a bare type word for a name (owner, 2026-10-13)",
    "way/234729698": "'Community Garden access road', a bare type word for a name (owner, 2026-10-13)",
    "way/234729699": "'Community Garden access road', a bare type word for a name (owner, 2026-10-13)",
    "way/234729704": "'Community Garden access road', a bare type word for a name (owner, 2026-10-13)",
    "way/621632732": "'Powerline access road', a bare type word for a name (owner, 2026-10-13)",
    "way/477238606": "'Old Transmitter Site Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/638809246": "'KM Gasoline Pipeline Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/5940421": "'Kinder-Morgan Petrol Access Road', a bare type word for a name (owner, 2026-10-13)",
    "way/6038175": "'Kinder-Morgan Petrol Access Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1368694534": "'Kinder-Morgan Petrol Access Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1554299872": "'Kinder-Morgan Petrol Access Road', a bare type word for a name (owner, 2026-10-13)",
    "way/754719083": "'Lake Murray Reservoir Maintenance Road', a bare type word for a name (owner, 2026-10-13)",
    "way/385800467": "'SD Aqueduct Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/400527034": "'SD Aqueduct Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/814360761": "'SD Aqueduct Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/814398699": "'SD Aqueduct Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/819666294": "'SD Aqueduct Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/85620754": "'SD Aqueduct service road', a bare type word for a name (owner, 2026-10-13)",
    "way/674876814": "'SD Aqueduct service road', a bare type word for a name (owner, 2026-10-13)",
    "way/828365993": "'SD Aqueduct service road', a bare type word for a name (owner, 2026-10-13)",
    "way/829552217": "'SD Aqueduct service road', a bare type word for a name (owner, 2026-10-13)",
    "way/1088984689": "'SD Aqueduct service road', a bare type word for a name (owner, 2026-10-13)",
    "way/385774762": "'SD Aqueduct service road.', a bare type word for a name (owner, 2026-10-13)",
    "way/401669458": "'SDCWD Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/401671809": "'SDCWD Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/401699369": "'SDCWD Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/401699588": "'SDCWD Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/101918396": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/103761838": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/103761839": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/103761840": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/203029952": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/203029984": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/204063628": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/216891722": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/250913684": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/253283501": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/254979121": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/256533988": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/256533989": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/273638088": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/295316074": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/368471069": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/368595511": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/452793871": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/477238607": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/477238611": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/523146658": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/523146660": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/523146662": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/523146673": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/523146675": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/523146677": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/523146680": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/523146686": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/523146688": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/523146691": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/523146693": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/523146695": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/536168599": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/536168601": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/536168602": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/536194807": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/536194808": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/536221416": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/537539732": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/537564871": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/537564879": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/583836966": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/617771599": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/617771602": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/617771606": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/617771629": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/617771630": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/619049825": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/619049834": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/619049842": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620194328": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620194329": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620198949": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620198951": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620198952": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620198954": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620198955": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620199177": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620199178": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620199179": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620200727": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620200728": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620200729": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620200730": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620200731": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620200732": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620200733": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620728901": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/620728902": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/638679297": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/673003953": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/674876765": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/691889307": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/813560528": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/813560529": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/814440615": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/814440616": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/819653940": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/819653941": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/819653943": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/819653947": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/819653949": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/819653950": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/857930507": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/863703249": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/863706992": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/865243340": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/881766874": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/892927194": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/892932247": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/892932248": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/892932249": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/892932250": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/892934753": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1003841170": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1018429823": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1018429824": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1085506182": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1323970589": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1370470927": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1389057949": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1493332311": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/1493332317": "'SDG&E Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/85620753": "'SDG&E Service Road - North Fortuna Perimeter Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/863706986": "'SDG&E Service Road - North Fortuna Perimeter Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/863706987": "'SDG&E Service Road - North Fortuna Perimeter Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/863706991": "'SDG&E Service Road - North Fortuna Perimeter Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/863706993": "'SDG&E Service Road - North Fortuna Perimeter Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/863706994": "'SDG&E Service Road - North Fortuna Perimeter Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/863706995": "'SDG&E Service Road - North Fortuna Perimeter Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/256672309": "'SDG&E Service Road / Fire Emergency Road', a bare type word for a name (owner, 2026-10-13)",
    "way/134865504": "'SDGE / SDMWD Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/417914313": "'SDGE / SDMWD Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/674876816": "'SDMWD Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/389460873": "'Cowles Service Road', a bare type word for a name (owner, 2026-10-13)",
    "way/828264828": "'fire road / footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/19155372": "'mountain bike trail', a description standing in for a name (owner, 2026-10-13)",
    "way/1081311865": "'mountain bike trail', a description standing in for a name (owner, 2026-10-13)",
    "way/1551883796": "'mountain bike trail', a description standing in for a name (owner, 2026-10-13)",
    "way/658291324": "'military road (Patrolled - penalty for access)', a description standing in for a name (owner, 2026-10-13)",
    "way/658291326": "'military road (Patrolled - penalty for access)', a description standing in for a name (owner, 2026-10-13)",
    "way/813559270": "'military road (Patrolled - penalty for access)', a description standing in for a name (owner, 2026-10-13)",
    "way/814360762": "'military road (Patrolled - penalty for access)', a description standing in for a name (owner, 2026-10-13)",
    "way/814398700": "'military road (Patrolled - penalty for access)', a description standing in for a name (owner, 2026-10-13)",
    "way/860237064": "'utility path', a description standing in for a name (owner, 2026-10-13)",
    "way/451472170": "'Stairs (steep)', a description standing in for a name (owner, 2026-10-13)",
    "way/451472169": "'Ramp and Footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/259245135": "'PQ to RB path', a description standing in for a name (owner, 2026-10-13)",
    "way/108049940": "'PV Footpath Network', a description standing in for a name (owner, 2026-10-13)",
    "way/674876807": "'Path to SD River Crossing Trail', a description standing in for a name (owner, 2026-10-13)",
    "way/912641289": "'Let's Go (Trail 28 as posted on Scripps Ranch Blvd)', a description standing in for a name (owner, 2026-10-13)",
    "way/109938666": "'Cabaret - Rancho Mission Park path', a description standing in for a name (owner, 2026-10-13)",
    "way/1254512157": "'Cabaret - Rancho Mission Park path', a description standing in for a name (owner, 2026-10-13)",
    "way/1317649005": "'Cabaret - Rancho Mission Park path', a description standing in for a name (owner, 2026-10-13)",
    "way/1317649006": "'Cabaret - Rancho Mission Park path', a description standing in for a name (owner, 2026-10-13)",
    "way/431586776": "'Hemingway - Rancho Mission Footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/431586970": "'Hemingway - Rancho Mission Footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/1006634572": "'Hemingway - Rancho Mission Footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/401701418": "'Navajo - Rancho Mission Path', a description standing in for a name (owner, 2026-10-13)",
    "way/115152003": "'\"Tunnel\" Trail 4', a description standing in for a name (owner, 2026-10-13)",
    "way/115166259": "'Deer Creek Trail (\"Tunnel\" 1)', a description standing in for a name (owner, 2026-10-13)",
    "way/369536116": "'Fishhead Creek (10N) Trail', a description standing in for a name (owner, 2026-10-13)",
    "way/709302310": "'City Heights Cherokee Point Playground Footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/994550059": "'City Heights Cherokee Point Playground Footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/287209454": "'First Aid Path', a description standing in for a name (owner, 2026-10-13)",
    "way/324922170": "'Sundevil Road Hilltop Park connector', a description standing in for a name (owner, 2026-10-13)",
    "way/5945458": "'Camp Elliott Road / Green Farm Road', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/948529446": "'Camp Elliott Road / Green Farm Road', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1513886018": "'Corridor Section (Empty Trucks Only)', a notice or code as a street's name: a description (owner, 2026-10-13)",
    "way/33407712": "'Corridor Section (Loaded Trucks Only)', a notice or code as a street's name: a description (owner, 2026-10-13)",
    "way/123698524": "'Corridor Section (Loaded Trucks Only)', a notice or code as a street's name: a description (owner, 2026-10-13)",
    "way/129602107": "'Tierrasanta Boulevard (Proposed)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/683943070": "'Tierrasanta Boulevard (Proposed)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/5962316": "'Old el C R Road', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/101476504": "'Vista San Pedro Mart', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/101476518": "'Vista Santa Margarit', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/432254988": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/438083307": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/438083309": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334877": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334878": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334880": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334881": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334900": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334902": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334912": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334914": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334916": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334920": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334922": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334929": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334948": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334949": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/468334950": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/527295353": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/527295355": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/527295359": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/527298939": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/1014945696": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/1062388017": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/1062388018": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/1062388019": "'Ready Lane', not a street: another kind of object indexed as one",
    "way/114198558": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/220571803": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318908": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318944": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318948": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318950": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318952": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318953": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318954": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318955": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318956": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318957": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318958": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318959": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318964": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318965": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318966": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318967": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/468318969": "'Ready Lane (Línea)', not a street: another kind of object indexed as one",
    "way/297678229": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/438083306": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/438083312": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/438083313": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468318909": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468318911": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468318913": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468318914": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468318938": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468334870": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468334871": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468334874": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468334875": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468334904": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468334906": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468334908": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/468334910": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/527295354": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/527295356": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/527295357": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/527295358": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/879914182": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/1014945620": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/1021256925": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/1021258605": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/1022151738": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/1062388015": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/1230208580": "'Global Entry SENTRI Lane', not a street: another kind of object indexed as one",
    "way/1014945649": "'Carril SENTRI de entrada global', not a street: another kind of object indexed as one",
    "way/1021256923": "'I-94 Permit Lane', not a street: another kind of object indexed as one",
    "way/1062388014": "'Bus Passengers Lane', not a street: another kind of object indexed as one",
    "way/265138741": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/284556683": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/438083308": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/438083311": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/468334883": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/468334887": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/468334889": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/468334891": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/468334893": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/468334895": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/468334896": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/468334898": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/527302477": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/527302478": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/527302479": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/527302480": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/527304745": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/527304746": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/527323470": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503563": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503564": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503565": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503566": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503568": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503569": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503570": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503571": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503573": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503574": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503575": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503576": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503577": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/879503579": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/1014945618": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/1014945741": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/1062388016": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/1087655262": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/1087741464": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/1087765168": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/1230208579": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/1230208582": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/1425847178": "'All Travelers Lane', not a street: another kind of object indexed as one",
    "way/5987693": "'Chabad Center Driveway', a driveway described, not a street's name",
    "way/1052571560": "'Chabad Center Driveway', a driveway described, not a street's name",
    "way/1527343837": "'Chabad Center Driveway', a driveway described, not a street's name",
    "way/1530693764": "'Chabad Center Driveway', a driveway described, not a street's name",
    "way/1530693765": "'Chabad Center Driveway', a driveway described, not a street's name",
    "way/1530693766": "'Chabad Center Driveway', a driveway described, not a street's name",
    "way/1530693767": "'Chabad Center Driveway', a driveway described, not a street's name",
    "way/5961165": "'De Portola School Driveway', a driveway described, not a street's name",
    "way/369450250": "'De Portola School Driveway', a driveway described, not a street's name",
    "way/1079928081": "'De Portola School Driveway', a driveway described, not a street's name",
    "way/367918161": "'Casey Driveway', a driveway described, not a street's name",
    "way/367918162": "'Casey Driveway', a driveway described, not a street's name",
    "way/754416717": "'Casey Driveway', a driveway described, not a street's name",
    "way/1064493688": "'Casey Driveway', a driveway described, not a street's name",
    "way/1065165641": "'Casey Driveway', a driveway described, not a street's name",
    "way/1065165643": "'Casey Driveway', a driveway described, not a street's name",
    "way/1072561226": "'Casey Driveway', a driveway described, not a street's name",
    "way/1072561229": "'Casey Driveway', a driveway described, not a street's name",
    "way/66983391": "'Donahue Driveway', a driveway described, not a street's name",
    "way/66983400": "'Donahue Driveway', a driveway described, not a street's name",
    "way/1072677337": "'Donahue Driveway', a driveway described, not a street's name",
    "way/531747916": "'Graduate Driveway', a driveway described, not a street's name",
    "way/1293625403": "'Graduate Driveway', a driveway described, not a street's name",
    "way/66644665": "'Kilroy Driveway', a driveway described, not a street's name",
    "way/414034761": "'Kilroy Driveway', a driveway described, not a street's name",
    "way/414034762": "'Kilroy Driveway', a driveway described, not a street's name",
    "way/414034763": "'Kilroy Driveway', a driveway described, not a street's name",
    "way/1238698006": "'Kilroy Driveway', a driveway described, not a street's name",
    "way/1449283741": "'Kilroy Driveway', a driveway described, not a street's name",
    "way/1454796076": "'Kilroy Driveway', a driveway described, not a street's name",
    "way/101148480": "'Industrial Park Driveway', a driveway described, not a street's name",
    "way/101888881": "'Industrial Park Driveway', a driveway described, not a street's name",
    "way/1077773210": "'Industrial Park Driveway', a driveway described, not a street's name",
    "way/272205773": "'Pacific Plaza Driveway', a driveway described, not a street's name",
    "way/272205774": "'Pacific Plaza Driveway', a driveway described, not a street's name",
    "way/1062920588": "'Pacific Plaza Driveway', a driveway described, not a street's name",
    "way/1062920590": "'Pacific Plaza Driveway', a driveway described, not a street's name",
    "way/65067040": "'Fenton Marketplace Driveway', a driveway described, not a street's name",
    "way/227452618": "'Fenton Marketplace Driveway', a driveway described, not a street's name",
    "way/227452619": "'Fenton Marketplace Driveway', a driveway described, not a street's name",
    "way/227452620": "'Fenton Marketplace Driveway', a driveway described, not a street's name",
    "way/229951456": "'Fenton Marketplace Driveway', a driveway described, not a street's name",
    "way/229951459": "'Fenton Marketplace Driveway', a driveway described, not a street's name",
    "way/398286345": "'Fenton Marketplace Driveway', a driveway described, not a street's name",
    "way/926448183": "'Fenton Marketplace Driveway', a driveway described, not a street's name",
    "way/926448184": "'Fenton Marketplace Driveway', a driveway described, not a street's name",
    "way/1307864786": "'Fenton Marketplace Driveway', a driveway described, not a street's name",
    "way/1533124101": "'Fenton Marketplace Driveway', a driveway described, not a street's name",
    "way/1533124102": "'Fenton Marketplace Driveway', a driveway described, not a street's name",
    "way/25499281": "'La Jolla Village Square Driveway', a driveway described, not a street's name",
    "way/25499293": "'La Jolla Village Square Driveway', a driveway described, not a street's name",
    "way/38064361": "'La Jolla Village Square Driveway', a driveway described, not a street's name",
    "way/103762849": "'La Jolla Village Square Driveway', a driveway described, not a street's name",
    "way/103762853": "'La Jolla Village Square Driveway', a driveway described, not a street's name",
    "way/227971799": "'La Jolla Village Square Driveway', a driveway described, not a street's name",
    "way/227971800": "'La Jolla Village Square Driveway', a driveway described, not a street's name",
    "way/227971876": "'La Jolla Village Square Driveway', a driveway described, not a street's name",
    "way/1057092761": "'La Jolla Village Square Driveway', a driveway described, not a street's name",
    "way/1112436872": "'La Jolla Village Square Driveway', a driveway described, not a street's name",
    "way/849529604": "'Lilly Driveway Entrance', a driveway described, not a street's name",
    "way/52735397": "'Pottery Park Driveway', a driveway described, not a street's name",
    "way/1315455741": "'Pottery Park Driveway', a driveway described, not a street's name",
    "way/1556617321": "'Pottery Park Driveway', a driveway described, not a street's name",
    "way/5964248": "'Sorrento South Driveway', a driveway described, not a street's name",
    "way/622955147": "'Thrive Driveway', a driveway described, not a street's name",
    "way/624681712": "'Thrive Driveway', a driveway described, not a street's name",
    "way/1320785511": "'Thrive Driveway', a driveway described, not a street's name",
    "way/1320785513": "'Thrive Driveway', a driveway described, not a street's name",
    "way/5952400": "'Villa La Jolla Driveway', a driveway described, not a street's name",
    "way/25499291": "'Villa La Jolla Driveway', a driveway described, not a street's name",
    "way/69707463": "'Villa La Jolla Driveway', a driveway described, not a street's name",
    "way/1205866832": "'Villa La Jolla Driveway', a driveway described, not a street's name",
    "way/1341999811": "'Villa La Jolla Driveway', a driveway described, not a street's name",
    "way/325114409": "'Arena Concourse', a business's own feature under its own name",
    "way/325114419": "'Arena Concourse', a business's own feature under its own name",
    "way/325114421": "'Arena Concourse', a business's own feature under its own name",
    "way/325114423": "'Arena Concourse', a business's own feature under its own name",
    "way/325114424": "'Arena Concourse', a business's own feature under its own name",
    "way/1076037187": "'Arena Concourse', a business's own feature under its own name",
    "way/323120430": "'Aztec Bowl', a business's own feature under its own name",
    "way/325114420": "'Aztec Bowl', a business's own feature under its own name",
    "way/468014228": "'Aztec Bowl', a business's own feature under its own name",
    "way/68506441": "'Aztec Center', a business's own feature under its own name",
    "way/68506442": "'Aztec Center', a business's own feature under its own name",
    "way/323076733": "'Aztec Center', a business's own feature under its own name",
    "way/323084757": "'Aztec Center', a business's own feature under its own name",
    "way/323084767": "'Aztec Center', a business's own feature under its own name",
    "way/324408439": "'Aztec Center', a business's own feature under its own name",
    "way/325116985": "'Aztec Center', a business's own feature under its own name",
    "way/325117008": "'Aztec Center', a business's own feature under its own name",
    "way/336890691": "'Aztec Center', a business's own feature under its own name",
    "way/336890692": "'Aztec Center', a business's own feature under its own name",
    "way/336890693": "'Aztec Center', a business's own feature under its own name",
    "way/336890694": "'Aztec Center', a business's own feature under its own name",
    "way/336890695": "'Aztec Center', a business's own feature under its own name",
    "way/336890696": "'Aztec Center', a business's own feature under its own name",
    "way/336890697": "'Aztec Center', a business's own feature under its own name",
    "way/692276215": "'Aztec Center', a business's own feature under its own name",
    "way/1049256856": "'Aztec Center', a business's own feature under its own name",
    "way/1447322956": "'Aztec Center', a business's own feature under its own name",
    "way/1447322957": "'Aztec Center', a business's own feature under its own name",
    "way/1447322960": "'Aztec Center', a business's own feature under its own name",
    "way/1447322961": "'Aztec Center', a business's own feature under its own name",
    "way/5959144": "'Aztec Walk', a business's own feature under its own name",
    "way/27056627": "'Aztec Walk', a business's own feature under its own name",
    "way/68471403": "'Aztec Walk', a business's own feature under its own name",
    "way/68474612": "'Aztec Walk', a business's own feature under its own name",
    "way/68482864": "'Aztec Walk', a business's own feature under its own name",
    "way/323084766": "'Aztec Walk', a business's own feature under its own name",
    "way/324408437": "'Aztec Walk', a business's own feature under its own name",
    "way/327171995": "'Aztec Walk', a business's own feature under its own name",
    "way/806795151": "'Aztec Walk', a business's own feature under its own name",
    "way/1103937178": "'Aztec Walk', a business's own feature under its own name",
    "way/1447322958": "'Aztec Walk', a business's own feature under its own name",
    "way/1447322962": "'Aztec Walk', a business's own feature under its own name",
    "way/5940362": "'Aztec Walk East', a business's own feature under its own name",
    "way/27056626": "'Aztec Walk East', a business's own feature under its own name",
    "way/839125222": "'Aztec Walk East', a business's own feature under its own name",
    "way/839125224": "'Aztec Walk East', a business's own feature under its own name",
    "way/990664817": "'Aztec Walk East', a business's own feature under its own name",
    "way/1477021348": "'Aztec Walk East', a business's own feature under its own name",
    "way/1049165440": "'Geisel Library', a business's own feature under its own name",
    "way/331164852": "'Peterson Gym', a business's own feature under its own name",
    "way/331164855": "'Peterson Gym', a business's own feature under its own name",
    "way/248983059": "'Caltrans Plaza', a business's own feature under its own name",
    "way/966167450": "'Pacific Bell Plaza', a business's own feature under its own name",
    "way/51868658": "'Towne Center Plaza', a business's own feature under its own name",
    "way/51868663": "'Towne Center Plaza', a business's own feature under its own name",
    "way/52835931": "'Towne Center Plaza', a business's own feature under its own name",
    "way/52835932": "'Towne Center Plaza', a business's own feature under its own name",
    "way/120905482": "'Towne Center Plaza', a business's own feature under its own name",
    "way/120905483": "'Towne Center Plaza', a business's own feature under its own name",
    "way/253925687": "'Towne Center Plaza', a business's own feature under its own name",
    "way/332227061": "'Towne Center Plaza', a business's own feature under its own name",
    "way/674609836": "'Towne Center Plaza', a business's own feature under its own name",
    "way/1289703011": "'Towne Center Plaza', a business's own feature under its own name",
    "way/185140649": "'Uptown Center', a business's own feature under its own name",
    "way/1346823386": "'Uptown Center', a business's own feature under its own name",
    "way/1421418467": "'Uptown Center', a business's own feature under its own name",
    "way/530271571": "'Village Hillcrest', a business's own feature under its own name",
    "way/556603988": "'Village Walk', a business's own feature under its own name",
    "way/830832356": "'Warren Mall', a business's own feature under its own name",
    "way/1052753773": "'Warren Mall', a business's own feature under its own name",
    "way/1052815384": "'Warren Mall', a business's own feature under its own name",
    "way/5967190": "'Autoport Mall', a business's own feature under its own name",
    "way/1300721922": "'Reptile Walk', a business's own feature under its own name",
    "way/1465512148": "'Admiral Boland Way', not a street: another kind of object indexed as one",
    "way/297126574": "'Plaza de Panama', not a street: another kind of object indexed as one",
    "way/849762593": "'Aztec Bowl seats', description: a part of a structure described: 'seats' of the Aztec Bowl, two ways (also way/966617024), by id (flag check, 2026-10-13)",
    "way/966617024": "'Aztec Bowl seats', description: a part of a structure described: 'seats' of the Aztec Bowl, two ways (also way/966617024), by id (flag check, 2026-10-13)",
    "way/388782057": "'Case Study House #23A', home: houses with an entry and no home tag: a private house; HOME_NAME misses a name that ends in a number (flag check, 2026-10-13)",
    "way/388782145": "'Case Study House #23C', home: houses with an entry and no home tag: a private house; HOME_NAME misses a name that ends in a number (flag check, 2026-10-13)",
    "node/358860095": "'Catholic Diocese of San Diego', organisation office: a church body's name on a GNIS place-of-worship node: a diocese is a governing body; decided by the name, not a tag (flag check, 2026-10-13)",
    "way/816411968": "'Electric Eel', ride inside a paid venue: the config already drops this venue's interior sections by id (owner, 2026-10-13) (flag check, 2026-10-13)",
    "way/287211122": "'Manta', ride inside a paid venue: the config already drops this venue's interior sections by id (flag check, 2026-10-13)",
    "node/358860499": "'Presbytery of San Diego', organisation office: a church body's name on a GNIS place-of-worship node: a presbytery is a governing body; decided by the name, not a tag (flag check, 2026-10-13)",
    "way/34188302": "'The Lot', business: a tenant's trade name on a registered building: the entry is the building's; the name is a cinema chain's, by id (flag check, 2026-10-13)",
    "way/1454307773": "'អគារ ទេវ សុវណ្ណគីរី វត្តសុវណ្ណគីរី', duplicate: a second building of one temple: its name is 'building' plus the temple's name; the temple has its own row (flag check, 2026-10-13)",
    "way/1163124118": "'Biology Field Station', description: a campus facility tagged a neighbourhood: place=neighbourhood; way; no other tag (flag check, 2026-10-13)",
    "way/459455885": "'Campus Services Complex', description: a campus facility tagged a neighbourhood: place=neighbourhood; way; no other tag (flag check, 2026-10-13)",
    "node/13064469244": "'Fairbanks Ranch Country Club', private club tagged a place: a members' country club, by id (flag check, 2026-10-13)",
    "way/1219401550": "'The Landing at Ocean View Hills', a housing development mapped as a place (owner, 2026-10-13)",
    "node/14138092788": "'The Preserve at Del Mar Mesa', a housing development mapped as a place (owner, 2026-10-13)",
    "node/14151240229": "'Villa Antigua', a condominium complex tagged a neighbourhood, one of 11 'Villa' nodes in one district (owner, 2026-10-13)",
    "node/14151205285": "'Villa Barbados', a condominium complex tagged a neighbourhood, one of 11 'Villa' nodes in one district (owner, 2026-10-13)",
    "node/14151205281": "'Villa Dominique', a condominium complex tagged a neighbourhood, one of 11 'Villa' nodes in one district (owner, 2026-10-13)",
    "node/14151240231": "'Villa Granada', a condominium complex tagged a neighbourhood, one of 11 'Villa' nodes in one district (owner, 2026-10-13)",
    "node/14151240230": "'Villa Majorca', a condominium complex tagged a neighbourhood, one of 11 'Villa' nodes in one district (owner, 2026-10-13)",
    "node/14151205286": "'Villa Martinique', a condominium complex tagged a neighbourhood, one of 11 'Villa' nodes in one district (owner, 2026-10-13)",
    "node/14151205283": "'Villa Monserate', a condominium complex tagged a neighbourhood, one of 11 'Villa' nodes in one district (owner, 2026-10-13)",
    "node/14151205284": "'Villa Monterey', a condominium complex tagged a neighbourhood, one of 11 'Villa' nodes in one district (owner, 2026-10-13)",
    "node/14151205282": "'Villa Portofino', a condominium complex tagged a neighbourhood, one of 11 'Villa' nodes in one district (owner, 2026-10-13)",
    "node/14151240227": "'Villa Trinidad', a condominium complex tagged a neighbourhood, one of 11 'Villa' nodes in one district (owner, 2026-10-13)",
    "node/14151240226": "'Villa Vista', a condominium complex tagged a neighbourhood, one of 11 'Villa' nodes in one district (owner, 2026-10-13)",
    "node/14192362004": "'Otay International Center', a business park or centre mapped as a quarter, one of 11 community-plan sub-areas by one mapper, no Wikidata entry (owner, 2026-10-13)",
    "node/14130228535": "'Plaza Sorrento', a business park or centre mapped as a quarter, one of 11 community-plan sub-areas by one mapper, no Wikidata entry (owner, 2026-10-13)",
    "node/14138853976": "'Rancho Bernardo Business Park', a business park or centre mapped as a quarter, one of 11 community-plan sub-areas by one mapper, no Wikidata entry (owner, 2026-10-13)",
    "node/14120160782": "'Rancho Peñasquitos Town Center', a business park or centre mapped as a quarter, one of 11 community-plan sub-areas by one mapper, no Wikidata entry (owner, 2026-10-13)",
    "node/14127383433": "'Sabre Springs Town Center', a business park or centre mapped as a quarter, one of 11 community-plan sub-areas by one mapper, no Wikidata entry (owner, 2026-10-13)",
    "way/370126095": "'Science Research Park', a business park or centre mapped as a neighbourhood, one of 11 community-plan sub-areas by one mapper, no Wikidata entry (owner, 2026-10-13)",
    "node/14131530332": "'Scripps Ranch Business Park', a business park or centre mapped as a neighbourhood, one of 11 community-plan sub-areas by one mapper, no Wikidata entry (owner, 2026-10-13)",
    "node/14131530331": "'Scripps Ranch Technology Park', a business park or centre mapped as a neighbourhood, one of 11 community-plan sub-areas by one mapper, no Wikidata entry (owner, 2026-10-13)",
    "node/14095801948": "'Spectrum Center', a business park or centre mapped as a quarter, one of 11 community-plan sub-areas by one mapper, no Wikidata entry (owner, 2026-10-13)",
    "node/14130466440": "'University Towne Center', a business park or centre mapped as a quarter, one of 11 community-plan sub-areas by one mapper, no Wikidata entry (owner, 2026-10-13)",
    "node/13513291492": "'Uptown Medical Complex', a business park or centre mapped as a quarter, one of 11 community-plan sub-areas by one mapper, no Wikidata entry (owner, 2026-10-13)",
}
