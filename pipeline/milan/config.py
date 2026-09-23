"""Milan-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Step 0 evidence and its checks: docs/build_briefs/milan.md (13/13).

Milan is a SIX-SOURCE build - the most of any city here, ahead of New York's
four - and the six are measurably DISJOINT registers rather than overlapping
views of one. See SOURCES below for why that means no cross-source
deduplication, which runs opposite to New York's decision.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "milan" / "raw"
DATA_PROCESSED = ROOT / "data" / "milan" / "processed"
OUTPUTS = ROOT / "outputs" / "milan"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# One feature per drawn line, written by step 1 from ds539's 31
# alignment variants - which is the shape map_common's GeoJSON loader
# expects, and the reason step 1 rather than step 3 does the selecting.
LINES_GEOJSON = DATA_PROCESSED / "metro_lines.geojson"

# Raw inputs, all downloaded by fetch_sources.py - deliberately NOT named
# step*.py, so drift_check.py never runs it.
BUSINESSES_RAW_DIR = DATA_RAW
BOUNDARY_GEOJSON = DATA_RAW / "confine_comune.geojson"
METRO_STOPS_GEOJSON = DATA_RAW / "tpl_metrofermate.geojson"
METRO_LINES_GEOJSON = DATA_RAW / "tpl_metropercorsi.geojson"
METRO_SEQUENCE_GEOJSON = DATA_RAW / "tpl_metrosequenza.geojson"
GTFS_ZIP = DATA_RAW / "gtfs.zip"

CKAN = "https://dati.comune.milano.it/api/3/action"

# --- The six registers -------------------------------------------------

# THE SIX ARE SEPARATE REGISTERS OF DIFFERENT ACTIVITIES, NOT OVERLAPPING
# VIEWS OF ONE, AND THAT IS MEASURED: `Codice` is unique within every register
# and there are ZERO collisions between any pair - the prefixes are distinct
# (EV/C-EV, PA/C-PA, AE/C-AE, PE/C-PE, FP/C-FP).
#
# SO THERE IS NO CROSS-SOURCE DEDUPLICATION, which runs opposite to New York.
# multi-source-city says to merge on address AND a normalised name because one
# storefront can hold several licences. Neither half transfers here:
#   - Address cannot be a key at all. 15,613 of 28,131 `vicinato` rows already
#     share an address with another row in the SAME register, and vicinato x
#     pe_in_piano share 4,855 addresses. Milan's buildings hold many premises;
#     merging on address would delete real businesses wholesale.
#   - Name-based merging is unavailable: `insegna` is 17.6% populated and
#     absent entirely from three of the six.
# A shop and a bar at one Milan address are two premises. The residual risk is
# an over-count where one business holds two licences; under-merging is the
# safer error and the city page says so.
#
# `bucket` here IS the classification. `Area di Competenza` is a single clean
# value per dataset at 100%, where every in-dataset classification field is
# 26-64% blank or corrupted by concatenation - so membership is the
# classification, which is multi-source-city's rule in its purest form.
#
# `label_col`: the source's own best field for the tooltip's activity line.
# All of them are dirty, so step 2 normalises case and splits concatenations,
# and falls back to `label_fallback` when blank (26-64% of the food rows).
SOURCES = {
    "vicinato": dict(
        resource="95ef10f2-c825-451d-aa3d-6ff4ed7fd267",
        package="ds49-economia-esercizi-vicinato-sede-fissa",
        rows=28131, bucket="Retail",
        name_col="insegna", label_col="settore_merceologico",
        label_fallback="Neighbourhood shop"),
    "pe_in_piano": dict(
        resource="d70a4002-af24-42db-9ace-00d4a102ccb8",
        package="ds58_economia_pubblici_esercizi_in_piano",
        rows=9269, bucket="Food service",
        name_col="insegna", label_col="tipo_eser_storico_pe",
        label_fallback="Bar or restaurant"),
    "servizi_persona": dict(
        resource="1f7244e8-a6ae-4777-a09f-06a325338be8",
        package="ds62_economia_parrucchieri_estetisti_centri_abbronzatura",
        rows=5732, bucket="Personal services",
        name_col=None, label_col="tipo_eser_pa",
        label_fallback="Personal services"),
    "pe_fuori_piano": dict(
        resource="bdb64cee-0f60-4271-8e35-dcda7a07de33",
        package="ds59-economia-pubblici-esercizi-fuori-piano",
        rows=3799, bucket="Food service",
        name_col="insegna", label_col="settore_storico_pe",
        label_fallback="Bar or restaurant"),
    "artigianato_alim": dict(
        resource="31bedae7-6fc3-473d-bc0f-316d9db9114d",
        package="ds250-economia-artigianato-settore-alimentare",
        rows=1471, bucket="Food service",
        name_col=None, label_col="tipo_eser_ae",
        label_fallback="Artisan food"),
    "panificatori": dict(
        resource="59cb72c3-a810-4f10-afad-9d7d2fe597b9",
        package="ds251-economia-panificatori",
        rows=443, bucket="Retail",
        # A baker's shop is NAICS 445 retail, the same line Dublin's BAKERY
        # takes - not food service, which is consumption on the premises.
        name_col=None, label_col="prevalente",
        label_fallback="Bakery"),
}

# `fuori piano` licenses premises OUTSIDE Milan's commercial plan, and at least
# 15.9% of it is not a public storefront: 472 staff canteens, 132 private
# clubs, 53 parish clubs. Owner's call 2026-09-22: include the register and
# filter what is nameable.
#
# 15.9% IS A FLOOR, NOT THE FIGURE. The `fuori_piano` clause column is 62.4%
# blank, so premises exempted under `art.3 comma 6 lett.*` cannot be classified
# from it at all. The city page must say some non-public premises remain.
FUORI_PIANO_EXCLUDE = ("mensa", "club privato", "circol", "parrocch")

# --- Boundary --------------------------------------------------------------

BOUNDARY_RESOURCE = "f56cb432-83e6-48de-ae30-d39b4be61e85"
BOUNDARY_PACKAGE = "ds2841-confini-amministrativi-del-comune-di-milano"
# One Polygon, 181.8 km2. No multipart dissolve needed - unlike Dublin's
# 90-part layer - and not an async Hub download.
BOUNDARY_AREA_KM2 = (175.0, 190.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 32N: Milan's longitude (~9.19) falls in the 6-12 band. An ordinary
# per-city UTM, derived not copied. Italy's national grids (Monte Mario,
# EPSG:3003/3004) are NOT used, because - unlike Dublin's ITM - no source here
# publishes in them: every register and both rail layers are EPSG:4326.
CRS_PROJECTED = "EPSG:32632"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail ------------------------------------------------------------------

# RAIL IS THE AGENCY'S OWN, AND BOTH osm-rail STEPS WERE RUN. ATM publishes
# metro stations and alignments as SEPARATE layers, both CRS84, plus a GTFS
# whose route_color carries the five official line colours. OSM is not used.
METRO_STOPS_RESOURCE = "dd6a770a-b321-44f0-b58c-9725d84409bb"
METRO_LINES_RESOURCE = "df024fd8-9c4e-4e22-a39e-7e91295b7a7b"
METRO_SEQUENCE_RESOURCE = "2d868218-3a74-4850-ac1c-0a151214577e"
# A stable short URL documented in the dataset's own notes, byte-identical to
# the long resource URL (sha256 matched 2026-09-22).
GTFS_URL = "https://dati.comune.milano.it/gtfs.zip"

# METRO ONLY. The 17 tram routes are NOT drawn - Barcelona excluded its T1-T6
# and Toronto its streetcars, and Milan's trams are a dense street-running
# network whose stops sit one or two blocks apart: San Francisco's Muni Metro
# shape, which needs docs/sub_transit_line_filters.md rather than a line list.
# They would also need 17 invented colours, because `route_color` is populated
# ONLY for the metro. Recorded as a costed extension, not a discard - the
# geometry is in the GTFS `shapes.txt` and the decision is reversible.
#
# THE COLOURS ARE THE AGENCY'S OWN, read from the GTFS `route_color`, so the
# project's rule keeps them even if they score badly against the category pins.
# That is the opposite of Dublin, where `route_color` was empty and the palette
# was therefore this project's to choose.
#
# `route_short_name` IS "1".."5", NOT "M1".."M5" - the M lives only in
# `route_id` and `route_long_name`, so the label is BUILT here, not copied.
LINES = {
    "M1": ("M1", "#ff0000", "M1 (linea rossa)"),
    "M2": ("M2", "#73ff01", "M2 (linea verde)"),
    "M3": ("M3", "#fcff01", "M3 (linea gialla)"),
    "M4": ("M4", "#0000ee", "M4 (linea blu)"),
    "M5": ("M5", "#c876b1", "M5 (linea lilla)"),
}

# The longest alignment variant per line, of ds539's 31, measured 2026-09-22.
# Each is the full end-to-end run; the others are short workings.
LINE_PERCORSI = {
    "M1": "100035",   # 123 verts, 21.16 km, Sesto 1 Maggio FS - Rho Fieramilano
    "M2": "100053",   # 354 verts, 33.25 km, Assago Milanofiori - Gessate
    "M3": "100081",   # 349 verts, 15.63 km, Comasina - San Donato
    "M4": "100164",   # 110 verts, 14.16 km, San Cristoforo - Linate Aeroporto
    "M5": "100084",   # 129 verts, 12.18 km, Bignami - San Siro Stadio
}

# ds535's 130 FEATURES ARE NOT 130 PHYSICAL STATIONS. Interchanges are modelled
# two incompatible ways: four are ONE point carrying both lines (CENTRALE FS
# "2,3", GARIBALDI FS "2,5", ZARA "3,5", SAN BABILA "1,4"), and the rest are
# TWO points needing three different rules. Suffix-strip alone gives 127; the
# aliases below take it to ~125.
#
# A DISTANCE THRESHOLD IS WRONG IN BOTH DIRECTIONS and must not be used:
# WAGNER <-> BUONARROTI at 277 m and DUOMO <-> CORDUSIO at 259 m are genuinely
# different stations, while LORETO M2 <-> LORETO M1 at 231 m are one. This is
# the per-city collapse osm-rail says is never inheritable.
STATION_NAME_SUFFIX = r"\s+M[1-5]$"        # DUOMO M3 -> DUOMO
STATION_ALIASES = {
    "S.AMBROGIO": "SAN AMBROGIO",           # 22 m apart, spelling variant
    "LOTTO FIERAMILANOCITY": "LOTTO",       # 71 m apart, name alias
    "CADORNA FN M1": "CADORNA FN",
    "CADORNA FN M2": "CADORNA FN",
}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "milan_source"
RAW_CLASSIFICATION_COLUMN = "attivita"

# NO REGISTER CARRIES A PERSONAL NAME - no titolare, ragione_sociale or
# nominativo in any of the six, confirmed against live headers. This is the
# France/Edmonton pattern: the publisher already did the stripping, so the
# residence-filter work San Diego, Los Angeles and Philadelphia each needed
# does not arise.
#
# `insegna` is a TRADE NAME and is used where present (17.6% / 23.8% / 9.1% on
# the three registers that have it); `Ubicazione` is the fallback and is 100%
# on every source. Because the fallback is an ADDRESS rather than an owner,
# Los Angeles' failure mode cannot occur - there is no person to fall back to.
NAME_FALLBACK_COLUMN = "Ubicazione"

MILAN_BBOX = {
    "lat_min": 45.35,
    "lat_max": 45.56,
    "lon_min": 9.02,
    "lon_max": 9.30,
}
