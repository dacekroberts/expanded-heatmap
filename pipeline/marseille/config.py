"""Marseille-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; every scaffolded placeholder has been
replaced with a measured value, so this module ships none.

SECOND FRENCH CITY. What it inherits from Paris is the country module, the
national NAF taxonomy, the parquet streaming, the Milan-hybrid naming and the
Lambert-93 grid. What it does NOT inherit is the scope decision, which the
brief was explicit about and which was re-measured here.
"""

from pathlib import Path

# The national facts, shared with Paris and the three French cities after this
# one. SIRENE is ONE register for the whole country - Mexico's shape, not
# Spain's - so the columns, the active value, the diffusion mask and the
# geolocation schema live in the country module. Re-exported with noqa so this
# city's step files import them from here.
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
    GEOLOC_PARQUET,
    GEOLOC_RESOURCE_TITLE_CONTAINS,
    JOIN_KEY,
    METROPOLITAN_EPSG,
    NAF_COLUMN,
    SIRENE_DATASET_SLUG,
    SIRENE_PARQUET,
    SIRENE_RESOURCE_TITLE_PREFIX,
    STATE_ACTIVE_VALUE,
    STATE_COLUMN,
    USUAL_NAME_COLUMN,
)

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "marseille" / "raw"
DATA_PROCESSED = ROOT / "data" / "marseille" / "processed"
OUTPUTS = ROOT / "outputs" / "marseille"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs. Record the exact download command for each (all public):
# Raw inputs, all four public. `fetch_sources.py` downloads them; no step may
# fetch (scripts/check_no_fetch_in_steps.py enforces it).
GTFS_ZIP = DATA_RAW / "gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# SIRENE_PARQUET and GEOLOC_PARQUET are NATIONAL and imported from the country
# module above - one 3 GB cache for all five French cities, not one each.

# THE FEED IS THE WHOLE METROPOLE AIX-MARSEILLE-PROVENCE, not Marseille's
# network - "Référentiel complet (tous les réseaux)". Measured 2026-09-23:
# 737 bus routes, 17 TER, 6 ferry, 4 tram, 2 metro. One of the four trams is
# **Aubagne's** (`AUB-T`, Le Charrel - Gare) and the TER routes reach Nice and
# Geneva, so "draw everything rail in the feed" would put another city's tram
# and half the national network on a Marseille map.
#
# ⚠ THE API KEY IS NOT A SECRET. It is published by the operator through
# France's National Access Point as part of the feed's own URL, and is recorded
# in `docs/build_briefs/marseille.md` and `docs/data_sources.md` for that
# reason. If a French city ever needs a key that IS private, it belongs in the
# environment and not in a committed file.
GTFS_URL = ("https://app.mecatran.com/utw/ws/gtfsfeed/static/mamp"
            "?apiKey=60327e505a214c77303f52206f11483069257343")

# Commune 13055 - Marseille, 238.1 km2 measured, 2.3x Paris's 105.4.
# ⚠ `geometry=contour`, NOT `fields=contour`: the latter answers HTTP 200 with
# a 120-byte POINT and would scope the build to one coordinate without erroring.
BOUNDARY_COMMUNE_CODE = "13055"
BOUNDARY_URL = ("https://geo.api.gouv.fr/communes/13055"
                "?geometry=contour&format=geojson")

# UNLIKE PARIS, this feed SELF-ATTESTS: feed_info.txt gives publisher Mecatran
# and 20260922-20261231, so staleness is readable from the artifact and there is
# no need for Paris's NAP-metadata capture. The fetch date is still recorded,
# because a licence may require the snapshot date to be DISPLAYED even when the
# file can be checked for freshness.
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# LAMBERT-93, as Paris takes it, and for the reason that made it decisive
# there rather than merely permitted: metropolitan France spans UTM zones 30N,
# 31N and 32N, so a per-city UTM rule would give the French cities three
# different projections while they all read ONE national file. Lambert-93 is a
# single grid defined for exactly this extent.
#
# This is the SECOND city on it, which is the point: the invariant is "derived
# per city, never copied", and deriving from France's own national grid
# satisfies that, where copying Paris's UTM zone to a city 660 km away would
# not. Marseille is at 5.37 E, inside the metropolitan domain that
# check_provenance.py's NATIONAL_GRIDS bounds this entry to (-5.5 to 10.0) -
# the DOM use 2975 / 5490 / 2972 and must not inherit it.
CRS_PROJECTED = "EPSG:2154"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
# THIRD CITY ON NEW YORK'S EDGES, and the measurement is the surprise: at a
# 341 m median nearest-neighbour distance Marseille is packed TIGHTER than
# Paris's 399 m, despite a commune 2.3x the size and a twentieth of the
# stations. The tram runs past the metro through the centre, so the two
# networks interleave along the Canebiere.
#
# `add-city` Step 3 says to reuse the shared edges "unless station spacing is
# meaningfully different". At a 0.6 mi (966 m) outer ring, a 341 m median means
# essentially every station reaches past its neighbours and the rings merge
# into one mass - New York's stated ground, at a tighter spacing than either
# New York (~0.30 mi) or Paris.
#
# Taking the same set rather than inventing a third keeps "dense city" one
# category with three members, so a reader comparing Marseille, Paris and New
# York gets identical bands.
#
# ⚠ Overlap is reduced, not removed: the halved outer ring is 483 m against a
# 341 m median, so neighbouring rings still touch. `map_common` assigns every
# business to its NEAREST station regardless, so no count depends on this.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# WHAT COUNTS: RTM's two métro lines and three tram lines. route_type 0 and 1,
# matched on the exact route_id, because the feed carries a sixth rail route
# that belongs to another city.
#
# ✅ COMMUNE-ONLY, SETTLED BY MEASUREMENT 2026-09-23 - the brief says Paris's
# answer does not transfer, and it was right to. Measured against commune
# 13055's own contour:
#
#     M1  18 inside / 0 outside      T2  15 / 0
#     M2  13 inside / 0 outside      T3  22 / 0
#     T1  14 inside / 0 outside      AUB-T  0 inside / 7 outside
#
# **All five of Marseille's own lines are 100% inside the commune** - 82
# station-line pairs, none lost, where Paris lost 76 of 321 to its boundary.
# Marseille's commune is 238.1 km2 against Paris's 105.4 and its network is
# compact, so the boundary costs it nothing.
#
# ⚠ AND IT DISPOSES OF AUBAGNE WITHOUT A SPECIAL RULE. `AUB-T` has ZERO
# stations inside, so the same spatial filter that scopes the city excludes
# another operator's tram as a side effect. That is worth more than a
# hard-coded exclusion, which would have to be remembered by the next French
# city reading a multi-network feed.
#
# ALSO EXCLUDED: 17 `route_type 2` TER routes, by the standing commuter-rail
# rule that drops Boston's CR-*, Chicago's Metra and Madrid's Cercanias - these
# reach Nice and Geneva. And 6 `route_type 4` FERRY routes (Vieux-Port
# shuttles, the Frioul islands service): owner's decision 2026-09-23 to drop
# them, RECORDED FOR POSSIBLE REVISITING. They are genuine urban transit here,
# which no other city's excluded mode is, so this is a judgment call rather
# than an automatic drop - the project measures density around RAIL stations
# and no built city draws a ferry.
ROUTE_TYPES_RAIL = ("0", "1")
ROUTE_IDS = ["RTM-116", "RTM-125", "RTM-2", "RTM-47", "RTM-48"]
EXCLUDED_RAIL_ROUTE_IDS = {"AUB-T": "Aubagne's tram, not Marseille's"}

# route_short_name -> the name riders use. RTM writes them exactly this way on
# its own maps and signage, so unlike Paris there is nothing to translate.
LINE_NAMES = {
    "M1": "Métro 1", "M2": "Métro 2",
    "T1": "Tramway 1", "T2": "Tramway 2", "T3": "Tramway 3",
}

# RTM's official livery, from the feed's own route_color. No overrides needed:
# all five are distinct from each other, unlike Paris where the feed gave the
# bis lines their parent's colour.
LINE_COLOURS = {
    "M1": "#009FE3", "M2": "#E30613",
    "T1": "#F28C00", "T2": "#F4E718", "T3": "#95C11F",
}

# --- Business filtering ------------------------------------------------

# HOW IN-CITY ROWS ARE IDENTIFIED. Not a city-name field - SIRENE is national
# and has none that is trustworthy. The authoritative marker is the INSEE
# commune code, and Marseille is subdivided into 16 arrondissements each with
# its own code (13201-13216), so it is a PREFIX match rather than one value.
#
# ⚠ `13055` is Marseille's code for the BOUNDARY API and is NOT what appears in
# this column - two code systems for one city, and mixing them returns zero
# rows silently, the same shape as the "Actif" bug. Validated 2026-09-22 across
# 14 row groups with Paris as the control; every prefix returned non-zero.
COMMUNE_PREFIXES = ("132",)

# Kept because the scaffold's shared step templates reference it. Marseille
# does not filter on a name string; COMMUNE_PREFIXES is the real filter.
CITY_KEEP = "MARSEILLE"

# The per-city catch-all verdict, which france_naf.py deliberately declines to
# make. NOT YET TAKEN for this city: Paris's two exclusions (96.09Z, 56.29B)
# were chosen on INSEE's own class labels, which is a national argument and so
# transfers - but the SHARES are a fact about each city and Marseille's have
# not been counted. Step 2 prints them; set this from those numbers and record
# the verdict in DECISIONS.md, exactly as Paris did.
#
# The brief already shows the two cities differ: distance selling is 16.4% of
# Marseille's bucket rows against Paris's 22.8%, so assuming Paris's profile
# would be assuming the thing to be measured.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "naf_label"
# This taxonomy also classifies by naf_code: keep those raw column(s) through step 2
# (they are passed to classify() by filter_to_storefront() and the map).

# Sanity bounds, TIGHTENED to the commune's own measured extent plus ~0.02 deg
# (about 2 km). The contour measures 43.1696-43.3911 N, 5.2288-5.5325 E.
#
# The box catches a CORRUPT coordinate - a swapped lat/lon, a zero, a
# whole-degree placeholder - and does not do the scoping; the boundary polygon
# does that. The scaffold's starting box spanned 0.8 deg of latitude and would
# have passed a point in Avignon.
MARSEILLE_BBOX = {
    "lat_min": 43.15,
    "lat_max": 43.41,
    "lon_min": 5.21,
    "lon_max": 5.55,
}
