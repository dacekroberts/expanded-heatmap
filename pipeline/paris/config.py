"""Paris-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py. Every TODO is a value only this city's
real data can supply (see the add-city skill); none should ship.
"""

from pathlib import Path

# The national facts. SIRENE is ONE register for all of France, so the columns,
# the active value, the diffusion mask, the geolocation schema and the licence
# live in the country module and five cities share them - Mexico's shape
# (`pipeline/countries/mexico.py`), not Spain's per-city one. Re-exported with
# noqa so this city's step files import them from here, unchanged.
from pipeline.countries.france import (  # noqa: F401
    COMMUNE_COLUMN,
    DIFFUSION_COLUMN,
    DIFFUSION_PUBLIC_VALUE,
    EMPLOYEE_BAND_COLUMN,
    ENSEIGNE_COLUMNS,
    GEO_EPSG_COLUMN,
    GEO_LAT_COLUMN,
    GEO_LON_COLUMN,
    GEO_QUALITY_COLUMN,
    GEOLOC_DATASET_SLUG,
    GEOLOC_RESOURCE_TITLE_CONTAINS,
    JOIN_KEY,
    METROPOLITAN_EPSG,
    NAF_COLUMN,
    PARIS_GTFS_URL,
    SIRENE_DATASET_SLUG,
    SIRENE_RESOURCE_TITLE_PREFIX,
    STATE_ACTIVE_VALUE,
    STATE_COLUMN,
    USUAL_NAME_COLUMN,
)

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "paris" / "raw"
DATA_PROCESSED = ROOT / "data" / "paris" / "processed"
OUTPUTS = ROOT / "outputs" / "paris"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all four public and keyless. `fetch_sources.py` downloads them;
# no step may fetch (scripts/check_no_fetch_in_steps.py enforces it).
#
#   gtfs.zip          IDFM's own feed, PARIS_GTFS_URL. NOT either of the two
#                     third-party copies the NAP lists beside it - Google's is
#                     stale since 2023-11-17 and ITO World's reports
#                     is_available false.
#   city_boundary     geo.api.gouv.fr commune 75056. ⚠ `geometry=contour`, NOT
#                     `fields=contour` - the latter returns HTTP 200 with a
#                     120-byte POINT (the commune centre) and would scope the
#                     whole build to one coordinate without erroring.
#   sirene parquet    StockEtablissement, ~2,210 MB. Resolved through the
#                     data.gouv API rather than hard-coded: the filename
#                     carries its own monthly release date.
#   geoloc parquet    INSEE's separate geolocation file, ~811 MB. The
#                     coordinate leg is a JOIN on siret, so there is no
#                     geocoder, no key and no rate limit in this build.
GTFS_ZIP = DATA_RAW / "gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
SIRENE_PARQUET = DATA_RAW / "sirene_etablissements.parquet"
GEOLOC_PARQUET = DATA_RAW / "sirene_geoloc.parquet"

BOUNDARY_URL = ("https://geo.api.gouv.fr/communes/75056"
                "?geometry=contour&format=geojson")

# Every Ile-de-France commune, with contours (~6.2 MB, 1,268 communes). Not for
# scoping - the single contour above does that - but to NAME the commune each
# EXCLUDED station sits in, which Los Angeles established as the standard for a
# system that crosses municipal borders: "54 of 110 stations, across 23 other
# places" is a readable record and a bare count is not.
#
# ⚠ THE PATH FORMS DO NOT EXIST. `/regions/11/communes` and a comma-separated
# `/departements/75,92,.../communes` both return 404; the region filter is a
# QUERY PARAMETER. Recorded because both were tried, and a 404 on a constructed
# URL is the cheap failure - the expensive one was `fields=contour`, which
# answers 200 with a Point.
IDF_COMMUNES_URL = ("https://geo.api.gouv.fr/communes?codeRegion=11"
                    "&format=geojson&geometry=contour&fields=nom,code,contour")
IDF_COMMUNES_GEOJSON = DATA_RAW / "idf_communes.geojson"

# WHAT NOTHING INSIDE THE ARTIFACTS CAN TELL US, so fetch_sources.py writes it.
# The GTFS carries NO feed_info.txt (14 files, measured), so the zip declares
# no validity window at all - and notice 24 (Licence Mobilites Art. 5.7)
# requires this project to DISPLAY the data's last-updated date and its update
# interval. Capture both at download time or they cannot be shown honestly.
#
# ⚠ IT LIVES IN outputs/, NOT data/raw/, and that is the whole point. `data/`
# is gitignored and the deployed app reads only `outputs/`, so a provenance
# file in the raw folder could never reach the page that is REQUIRED to display
# it. Writing it here makes the Art. 5.7 obligation durable - the page reads
# the date rather than carrying a hardcoded string that goes stale on the next
# fetch.
PROVENANCE_JSON = OUTPUTS / "provenance.json"
NAP_API = "https://transport.data.gouv.fr/api/datasets"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# LAMBERT-93, NOT THE UTM ZONE THE SCAFFOLD DERIVED (32631, zone 31N).
# Dublin set the precedent for a national grid (EPSG:2157); this is the second,
# and unlike Dublin's it is forced by the source rather than merely permitted:
#
#   1. INSEE's geolocation file publishes `x`/`y` NATIVELY in 2154 on 99.3% of
#      rows, so reading it in 2154 means the source coordinates are never
#      reprojected at all. UTM would add a transform in front of every pin.
#   2. `pipeline/countries/france.py` already names METROPOLITAN_EPSG = 2154,
#      so this keeps the config and the country module from disagreeing.
#   3. DECIDING: metropolitan France spans UTM zones 30N, 31N and 32N, so a
#      per-city UTM rule would give the five cities of france.py's
#      BUILD_SEQUENCE three different projections while they all read ONE
#      national file. Lambert-93 is a single grid for exactly this extent -
#      that is what it was defined for. The invariant is "projected metres,
#      derived per city, never copied"; deriving it from France's own grid
#      satisfies that, and copying a UTM zone between Paris and Lille would not.
#
# The DOM are a different grid per the brief (2975 Réunion, 5490 Antilles,
# 2972 Guyane), which is why check_provenance.py's NATIONAL_GRIDS entry bounds
# this to metropolitan longitudes - a Fort-de-France build must NOT inherit it.
CRS_PROJECTED = "EPSG:2154"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# WHAT COUNTS: the Metro, and only the Metro. `route_type == 1`, 16 routes.
#
# IDFM's feed is the WHOLE Ile-de-France network - measured 2026-09-23 at 1,966
# bus routes, 24 rail/RER, 17 tram, 16 metro, 1 funicular, 1 cable. So the
# filter here is doing real work rather than confirming a single-mode feed.
#
# WHAT IS LEFT OUT, AND WHY IT IS NOT A SCOPE DECISION. RER and Transilien are
# commuter rail, excluded by the standing rule in every built city (Boston's
# CR-*, Chicago's Metra, Madrid's Cercanias, Miami's Tri-Rail, Philadelphia's
# Regional Rail, Vancouver's West Coast Express). Trams are excluded in
# Barcelona, Milan and Toronto already. Both would be dropped at ANY scope, so
# commune-only is not what decides them - see docs/build_briefs/paris.md.
#
# Matched on route_type plus the exact short name, never a substring: "1" is a
# substring of "11", "12", "13" and "14".
ROUTE_TYPE_METRO = "1"
ROUTE_IDS = [
    "IDFM:C01371", "IDFM:C01372", "IDFM:C01373", "IDFM:C01374",
    "IDFM:C01375", "IDFM:C01376", "IDFM:C01377", "IDFM:C01378",
    "IDFM:C01379", "IDFM:C01380", "IDFM:C01381", "IDFM:C01382",
    "IDFM:C01383", "IDFM:C01384", "IDFM:C01386", "IDFM:C01387",
]

# route_short_name -> the name riders use. Madrid's convention (`Linea 1`):
# the operator's own public naming, not an English translation. The feed's
# route_long_name is just the number again, so it supplies nothing.
LINE_NAMES = {
    "1": "Ligne 1", "2": "Ligne 2", "3": "Ligne 3", "4": "Ligne 4",
    "5": "Ligne 5", "6": "Ligne 6", "7": "Ligne 7", "8": "Ligne 8",
    "9": "Ligne 9", "10": "Ligne 10", "11": "Ligne 11", "12": "Ligne 12",
    "13": "Ligne 13", "14": "Ligne 14",
    "3B": "Ligne 3bis", "7B": "Ligne 7bis",
}

# RATP's official livery from the feed's own route_color, with TWO OVERRIDES.
#
# **The feed gives the bis lines their parent's colour, and that collides.**
# Measured: M13 and M3bis are both 82C8E6, M6 and M7bis are both 82DC73. That
# is not a feed error - RATP really does colour them that way - but a 16-entry
# legend with two identical pairs cannot be read, which is the case add-city
# Step 6 names: "if the agency's official line colours are ambiguous or shared,
# use a palette of your own". The 14 main lines keep their official colour and
# only the two bis lines are shifted, so the deviation is as small as it can be
# and is visible here rather than inferred from the map.
LINE_COLOURS = {
    "1": "#FFBE00", "2": "#0055C8", "3": "#6E6E00", "4": "#A0006E",
    "5": "#FF5A00", "6": "#82DC73", "7": "#FF82B4", "8": "#D282BE",
    "9": "#D2D200", "10": "#DC9600", "11": "#6E491E", "12": "#00643C",
    "13": "#82C8E6", "14": "#640082",
    "3B": "#3D7A99",   # was 82C8E6, identical to Ligne 13
    "7B": "#2E8B57",   # was 82DC73, identical to Ligne 6
}

# --- Business filtering ------------------------------------------------

# HOW IN-CITY ROWS ARE IDENTIFIED. Not a city-name field: SIRENE has none that
# is trustworthy, and this register is national. The authoritative marker is the
# INSEE commune code, and Paris is subdivided into 20 arrondissements each with
# its own code (75101-75120), so it is a PREFIX match rather than one value.
#
# ⚠ `75056` is Paris's commune code for the BOUNDARY API and is NOT what
# appears in this column - the two are different code systems for the same
# city, and mixing them returns zero rows silently, the same shape as the
# "Actif" bug. Validated 2026-09-22 across 14 row groups with Paris as the
# control; every prefix returned non-zero.
COMMUNE_PREFIXES = ("751",)
BOUNDARY_COMMUNE_CODE = "75056"

# Kept because the scaffold's shared step templates reference it. Paris does
# not filter on a name string; COMMUNE_PREFIXES is the real filter.
CITY_KEEP = "PARIS"

# THE PER-CITY CATCH-ALL VERDICT, which france_naf.py deliberately declines to
# make because a catch-all's composition is a fact about a city. Los Angeles'
# NAICS_EXCLUDE_CODES is the worked example.
#
# **THE RULE IS THE PUBLISHER'S OWN HIERARCHY, NOT THE WORD "AUTRES".** Three
# of the five catch-alls sit under a NAF class whose official label asserts a
# shop, so INSEE is saying these premises exist:
#
#   47.19B  5,359 | class 47.19 "Autre commerce de detail EN MAGASIN non
#                 | specialise"                                      -> KEEP
#   47.29Z  1,413 | class 47.29 "... EN MAGASIN specialise"          -> KEEP
#   47.78C    903 | class 47.78 "Autre commerce de detail de biens
#                 | neufs EN MAGASIN specialise"                     -> KEEP
#   96.09Z  9,349 | class 96.09 "Autres services personnels n.c.a."
#                 | - asserts no premises at all                     -> DROP
#   56.29B    958 | class 56.29 "Autres services de restauration"
#                 | - catering, asserts no premises                  -> DROP
#
# This is Barcelona's finding in French: two calls the publisher's hierarchy
# made rather than a reading of the language. 96.09Z is also the direct
# analogue of the NAICS 812990 that Los Angeles excludes, and it is the single
# largest contributor to the bucket that diverges most from OSM (Personal
# services measured 4.40x OSM before this exclusion).
#
# ⚠ THIS DOES NOT CLOSE THE GAP, and it is not meant to. Measured 2026-09-23
# against OSM inside the same commune: 97,445 SIRENE against 48,973 OSM, 1.99x
# overall. Excluding these two takes it to about 1.78x. The residual is
# DISCLOSED on the city page rather than filtered away - SIRENE is a register
# of registered establishments and some have no customer-facing shopfront,
# which nothing in the data identifies. Tuning filters until the number
# matched OSM would be fitting to a number, which is what put the superseded
# 50,156 in the brief in the first place.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "naf_label"
# This taxonomy also classifies by naf_code: keep those raw column(s) through step 2
# (they are passed to classify() by filter_to_storefront() and the map).

# Sanity bounds for the supplied lat/lng. TODO: tighten to the city's real
# extent once the boundary is known (this box is a wide starting guess).
PARIS_BBOX = {
    "lat_min": 48.46,
    "lat_max": 49.26,
    "lon_min": 1.85,
    "lon_max": 2.85,
}
