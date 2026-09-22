"""Montréal settings. Scoped to the AGGLOMERATION (the island), decided
2026-09-21 before the build - see DECISIONS.md, "Montreal will be built at
AGGLOMERATION scope".

WHAT MAKES THIS CITY DIFFERENT FROM EVERY OTHER ONE HERE
--------------------------------------------------------
**Its source is a SURVEY, not a licence register.** `locaux-commerciaux` is
the Ville de Montréal's annual field survey of street-level commerce: someone
walks the commercial streets and records what is in each unit. Every other city
in this project infers commerce from licences, which is why every other city
spends most of its step 2 throwing away rentals, contractors and professional
offices. Here **69.4% of non-vacant rows are storefronts** against Vancouver's
28.2%, and the consequences run through this whole file:

  - **It needs no taxonomy module.** `SCIAN` IS NAICS, so
    `pipeline/taxonomies/naics.py` applies unchanged and this is the only
    Canadian city of the six where that is true.
  - **It has no name problem.** `NOM_ETAB` is the establishment's name,
    populated on 100% of rows, and there is NO registrant-name column at all -
    so no pin can display a person's name this pipeline substituted. That is a
    structural claim, like New York's and Miami's, not a measurement.
  - **It needs no geocoding step.** `LAT`/`LONG` are 100% populated.
  - **It records VACANT units**, which no licence register does, and they have
    to be excluded: an empty shopfront is not a business.

**And it is the first source in this project written in French.** Column names
and `USAGE1` labels are French; they stay that way. Bucketing goes through
`naics.py`, whose legend text is already English and already shared with five
other cities, so nothing has to be translated.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "montreal" / "raw"
DATA_PROCESSED = ROOT / "data" / "montreal" / "processed"
OUTPUTS = ROOT / "outputs" / "montreal"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (see pipeline/montreal/fetch_sources.py) ------------------

GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "occupation_commerciale.csv"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "agglomeration.geojson"

# --- Endpoints --------------------------------------------------------------

# CKAN. The 2025 vintage; the package holds 2021-2025 as separate resources and
# gains one a year, so re-check `package_show` rather than trusting this id.
BUSINESS_URL = (
    "https://donnees.montreal.ca/dataset/f8582c4d-a933-4306-bb27-d883e13dd207/"
    "resource/01ded48e-f982-4703-975e-4be0769ef3ee/download/"
    "occupation-commerciale-2025.csv"
)
BUSINESS_PACKAGE = "locaux-commerciaux"

# THE WGS 84 RESOURCE, not the `-nad83` one, which is MTM zone 8 and would need
# reprojecting from a CRS this project uses nowhere else.
CITY_BOUNDARY_URL = (
    "https://donnees.montreal.ca/dataset/9797a946-9da8-41ec-8815-f6b276dec7e9/"
    "resource/e18bfd07-edc8-4ce8-8a5a-3b617662a794/download/"
    "limites-administratives-agglomeration.geojson"
)

# `donnees.montreal.ca` answers a plain client with `RBAC: access denied`. A
# browser User-Agent is required, and this is portal-wide rather than specific
# to one dataset.
BUSINESS_NEEDS_BROWSER_HEADERS = True

# --- Transit feed -----------------------------------------------------------

# STM'S OWN HOST, and this city is the proof that it matters. Measured
# 2026-09-21: the agency feed was valid to 20261025 (+34 days) while the
# Mobility Database mirror (id 2126) was 29 days EXPIRED. Station counts
# happened to agree, but Toronto's mirror hid an entire mode, so a build never
# takes the mirror.
GTFS_URL = "https://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip"
GTFS_FEED_INFO_MEMBER = "feed_info.txt"
GTFS_CHECK_FEED_WINDOW = True

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 18N: Montréal's longitude (~-73.57) falls in the -78 to -72 band.
# Distinct from every other Canadian candidate (Vancouver 32610, Calgary 32611,
# Edmonton 32612) - the projected CRS is derived per city, never copied.
CRS_PROJECTED = "EPSG:32618"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# The four Métro lines, matched on exact route_id. There is no other rail in
# this feed: the STM operates the Métro and buses only, so unlike Vancouver
# there is no commuter-rail or ferry route to exclude.
ROUTE_IDS = ["1", "2", "4", "5"]
LINE_NAMES = {
    "1": "Ligne 1 - Verte",
    "2": "Ligne 2 - Orange",
    "4": "Ligne 4 - Jaune",
    "5": "Ligne 5 - Bleue",
}

# The agency's own colours, read from the feed's `route_color` rather than a
# style guide. MEASURE CONTRAST IN BOTH MODES, dark first - see
# pipeline/vancouver/config.py for the method and D.C.'s Silver Line for the
# case where measuring only the light basemap gave a backwards answer.
LINE_COLOURS = {
    "1": "#00B300",   # Verte
    "2": "#D95700",   # Orange
    "4": "#FFD900",   # Jaune
    "5": "#0095E6",   # Bleue
}

# ONE shape per line - verified 2026-09-21 to cover every stop on its line
# (27 / 31 / 3 / 12). No Métro line branches, so unlike Vancouver's Canada and
# Expo Lines none of these needs a tuple.
LINE_SHAPES = {
    "1": "1_1071",
    "2": "2_236",
    "4": "4_24",
    "5": "5_1763",
}

LINE_LABEL_ENDS = {}

# Platforms collapse via `parent_station`, which is populated on all 72 served
# stops, so there is no suffix regex and no alias dict - Vancouver needed both.
#
# The DISPLAY name comes from the CHILD stop, not the parent: children are
# mixed case ("Station Angrignon") and parents are upper case ("STATION
# ANGRIGNON"), and an all-caps label on a map reads as shouting.
#
# Only the LEADING "Station " is stripped. Do NOT strip a trailing word here:
# Boston's bug turned "North Station" into "North", and this feed has
# "Square-Victoria-OACI" and "Université-de-Montréal" where a trailing-token
# rule would do real damage.
STATION_NAME_STRIP_PREFIX = "Station "

# The Métro is fully underground and grade-separated, so every in-scope station
# is kept and no sub-transit-line filter applies
# (docs/sub_transit_line_filters.md) - D.C.'s and SkyTrain's shape.
#
# It is DENSER than Vancouver downtown, and that is measured rather than
# assumed: nearest-neighbour min 355 m (Place-des-Arts to Saint-Laurent),
# median 728 m, max 1874 m, with 57 of 64 stations inside the 966 m outer ring.
# Those rings overlap heavily; each business is assigned to its NEAREST station
# so nothing is double-counted.
THINNED_GROUPS = frozenset()

# --- Boundary and station scope ---------------------------------------------

# 34 features: 19 `Arrondissement` (Montréal proper) and 15 `Ville liée` (the
# related municipalities). AGGLOMERATION scope dissolves ALL of them, so this
# field is not used to filter - it is recorded because it is what makes the
# other scope one filter away, and because a reader of this file will ask.
BOUNDARY_TYPE_FIELD = "TYPE"
BOUNDARY_NAME_FIELD = "NOM"
BOUNDARY_FEATURES_EXPECTED = 34

# Area is NOT checked tightly here, unlike Vancouver's 118.8 km2 +-3. This
# boundary follows the river channel rather than the shoreline, so it measures
# 619.0 km2 against the agglomeration's ~499 km2 of land. Do not copy
# Vancouver's tolerance; a loose sanity floor is all this layer can support.
BOUNDARY_AREA_KM2_MIN = 450.0

# The Métro leaves the island: 3 stations in Laval (Cartier, De la Concorde,
# Montmorency) and 1 in Longueuil. They are dropped by the SPATIAL filter
# against the boundary, never by name - the project invariant.
#
# STM happens to mark them structurally too: each carries a " -Zone B" suffix,
# its fare zone, and Zone B is exactly the off-island network. Step 1 asserts
# the two agree, so a silent change in either is caught.
OFF_ISLAND_FARE_ZONE_SUFFIX = " -Zone B"
IN_CITY_STATIONS_EXPECTED = 64

# --- Business filtering ------------------------------------------------

SOURCE_ENCODING = "utf-8"
SOURCE_DELIMITER = ","

TAXONOMY_SYSTEM = "naics"
# The survey's own column name; step 2 renames it to the taxonomy's
# VALUE_COLUMN ("naics").
RAW_CLASSIFICATION_COLUMN = "SCIAN"

# VACANT UNITS ARE EXCLUDED, and nothing else in this project has needed this.
# `USAGE1 == 'VACANT'` on 3,500 of 28,621 rows (12.2%) - an empty shopfront is
# premises, not a business, and counting it would measure supply of retail
# space rather than commerce.
#
# `VACANT_A_LOUER` ("vacant and for rent", Oui on 712) is a SEPARATE and
# narrower flag. It is not a substitute for the USAGE1 value and does not
# identify the same rows.
USAGE_COLUMN = "USAGE1"
USAGE_VACANT = "VACANT"
VACANT_FOR_RENT_COLUMN = "VACANT_A_LOUER"

# `SCIAN` is a 1-CHARACTER PLACEHOLDER on some rows, so a length test is the
# filter rather than a null test. Measured: 6-digit codes on 24,827 of 25,121
# non-vacant rows (98.8%). The profile's "99.6%" was measured on the whole
# file including vacancies - the denominator error this project keeps meeting.
SCIAN_CODE_LENGTH = 6

# THE PREMISES KEY IS `ID`, AND ADDRESS DEDUP MUST NOT HAPPEN.
#
# `ID` is unique across all 28,621 rows: one row is one surveyed unit. 6,500
# rows share an ADRESSE with another, and that is CORRECT rather than
# duplication - 7275 rue Sherbrooke E holds 174 units and 7999 boulevard des
# Galeries-d'Anjou holds 152, each a distinct business with its own SUITE.
# Deduplicating on address, as Miami and Vancouver do, would delete a shopping
# centre down to one shop.
PREMISES_KEY = "ID"

# `T_COMMERCE` is the survey's own premises type, and it is why the address
# duplication is legible: Commerce rue 25,176 / Centre commercial 3,098 /
# Marché public 199 / Mégacentre 128 / Foire alimentaire 20.
#
# ALL of them are kept. Each is a fixed commercial unit a person can walk into,
# which is what this project measures; a mall unit near a station is commerce
# near a station. Recorded as a deliberate scope decision rather than an
# oversight, because it is the one lever here that would materially change the
# count (dropping the non-street types would remove 3,445 units, 12%).
PREMISES_TYPE_COLUMN = "T_COMMERCE"

# Flags examined and NOT used, so that a later reader does not assume they were
# missed: MULTIUSAGE (Oui 717), MULTIOCCUPANT (Oui 585) and ENFANT (Oui 541).
# They do not explain the shared addresses - of the 6,500 rows sharing one,
# only 141 are MULTIOCCUPANT and 92 ENFANT - so they are not a dedup signal.
# `ID` being unique makes them unnecessary.

# This registry publishes NO personal column, so unlike New York, Miami, Boston
# and Surrey there is nothing to omit at the download boundary. Step 2 asserts
# the absence anyway, so that the claim stays true if the survey ever gains a
# column.
FORBIDDEN_COLUMNS = ("NOM_PROPRIETAIRE", "PROPRIETAIRE", "NOM_LOCATAIRE",
                     "TELEPHONE", "COURRIEL")

# --- Coordinate sanity ------------------------------------------------------

# The island and its related municipalities, a little wider than the boundary
# so a genuine edge premises is not clipped by the sanity check itself.
MONTREAL_BBOX = {
    "lat_min": 45.35,
    "lat_max": 45.75,
    "lon_min": -74.05,
    "lon_max": -73.40,
}
