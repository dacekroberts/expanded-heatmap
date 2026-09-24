"""Rennes-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; every scaffolded placeholder has been
replaced with a measured value, so this module ships none.

FIFTH AND LAST FRENCH CITY. What it inherits from Paris, Marseille, Toulouse
and Lille is the country module, the national NAF taxonomy, the shared parquet
cache, the Milan-hybrid naming and the Lambert-93 grid. What it does NOT
inherit is the scope decision, and the brief got that half wrong: it said "the
métro is city-contained", and line b is not. See the station-scope section.
"""

from pathlib import Path

# The national facts, shared with the four French cities before this one.
# SIRENE is ONE register for the whole country - Mexico's shape, not Spain's -
# so the columns, the active value, the diffusion mask and the geolocation
# schema live in the country module. Re-exported with noqa so this city's step
# files import them from here.
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
DATA_RAW = ROOT / "data" / "rennes" / "raw"
DATA_PROCESSED = ROOT / "data" / "rennes" / "processed"
OUTPUTS = ROOT / "outputs" / "rennes"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the commune, with the commune each IS in - a citable scoping
# record. Four rows here, all on line b, and they include both of its termini.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all public. `fetch_sources.py` downloads them; no step may fetch
# (scripts/check_no_fetch_in_steps.py enforces it).
GTFS_ZIP = DATA_RAW / "gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
METRO_COMMUNES_GEOJSON = DATA_RAW / "metropole_communes.geojson"
# SIRENE_PARQUET and GEOLOC_PARQUET are NATIONAL and imported from the country
# module above - one 3 GB cache for all five French cities, not one each.

# STAR's feed (Keolis Rennes), on Opendatasoft's file host. Measured 2026-09-23
# at 13,119,510 bytes, no key and no account.
#
# ⚠ `EN_COURS`, NEVER `A_VENIR`. The portal publishes a sibling resource, "GTFS
# (version à venir)", which is the FORTHCOMING timetable: reading it would draw
# services that do not run yet. Pinned by a brief check.
#
# ⚠ THIS HOST IS NOT THE PORTAL'S API. data.explore.star.fr enforces a
# DOMAIN-WIDE quota of 150,000 calls a day shared by every anonymous caller,
# and it was exhausted when first probed on 2026-09-23 (HTTP 429, errorcode
# 10003, reset at 00:00 UTC). The file host below answered throughout, so the
# build's one mandatory download does not depend on that quota.
GTFS_URL = ("https://eu.ftp.opendatasoft.com/star/gtfs/"
            "GTFS_STAR_BUS_METRO_EN_COURS.zip")

# Commune 35238 - Rennes.
# ⚠ `geometry=contour`, NOT `fields=contour`: the latter answers HTTP 200 with
# a 120-byte POINT and would scope the build to one coordinate without erroring.
BOUNDARY_COMMUNE_CODE = "35238"
BOUNDARY_URL = ("https://geo.api.gouv.fr/communes/35238"
                "?geometry=contour&format=geojson")

# Every commune of Rennes Métropole (EPCI 243500139), used ONLY to name the
# commune an excluded station lies in - the Los Angeles rule that an excluded
# station's municipality is worth naming rather than leaving as "outside".
# It scopes nothing. Lille reads the same endpoint shape for its EPCI.
METROPOLE_EPCI_CODE = "243500139"
METROPOLE_COMMUNES_URL = ("https://geo.api.gouv.fr/epcis/243500139/communes"
                          "?fields=nom,code&geometry=contour&format=geojson")

# ✅ THE FEED SELF-ATTESTS - Marseille's case, not Paris's or Toulouse's.
# feed_info.txt declares publisher Keolis Rennes, 2026-09-22 to 2026-10-18.
# ⚠ THAT WINDOW IS SHORT - four weeks - so brief_check's feed-window check will
# flag it long before Marseille's. A stale-window failure means refetch, not
# alarm: STAR publishes a rolling current timetable, and the stations and
# alignments this map draws do not change with it.
GTFS_SELF_ATTESTS = True
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# LAMBERT-93, as every French city takes it, and for the reason that made it
# decisive rather than merely permitted: metropolitan France spans UTM zones
# 30N, 31N and 32N, so a per-city UTM rule would give the French cities three
# different projections while they all read ONE national file. Lambert-93 is a
# single grid defined for exactly this extent.
#
# ⚠ THE SCAFFOLD PROPOSED EPSG:32630 (UTM 30N) from the longitude - the FIRST
# French city to land in zone 30 rather than 31, which is the national-grid
# argument made concrete: without Lambert-93, Rennes and Toulouse would be
# measured on different projections. Overridden deliberately.
#
# The invariant is "derived per city, never copied"; deriving from France's own
# national grid satisfies it. Rennes is at -1.68 E, inside the metropolitan
# domain check_provenance.py's NATIONAL_GRIDS bounds this entry to (-5.5 to
# 10.0).
CRS_PROJECTED = "EPSG:2154"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# NEW YORK'S EDGES, as all four French cities before it take them, so a reader
# comparing Rennes with Paris, Marseille, Toulouse or Lille is comparing the
# cities and not the bucket boundaries.
#
# Measured 2026-09-23 across the 24 in-commune stations, in Lambert-93 metres
# (nearest-neighbour):
#
#     min 237    median 541    mean 581    max 1,119
#     under 200 m: 0
#
# Toulouse's shape almost exactly (525 m median), so Toulouse's fit argument
# transfers: a 483 m outer ring very nearly TILES at a 541 m median, each
# station's outer edge stopping just short of its neighbour's, where the
# default 966 m would reach two stations deep.
#
# ⚠ The spacing gate in pipeline/stations.py does NOT fire here (network-wide
# median 560 m, nothing under 200 m), so no `spacing_min` is passed. The
# closest pair, 237 m, is République (line a) and Saint-Germain (line b) in
# the centre - two lines' separate stations, not a collapse failure. Next
# are Charles de Gaulle-Gares (385) and Charles de Gaulle-Colombier (399).
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# WHAT COUNTS: métro lines a and b, and nothing else in the feed. Matched on the
# exact route_id - the feed carries 150 bus routes alongside them.
#
# STAR runs no tram and no commuter rail, so there is no mode decision to take
# here: `route_type 1` is the whole rail network. (The TER and the SNCF
# stations at Rennes are not in this feed and are not STAR's.)
ROUTE_TYPES_RAIL = ("1",)
ROUTE_IDS = ["7-1001", "7-1002"]

# ✅ COMMUNE-ONLY, owner's call 2026-09-23 - taken against a measurement that
# CORRECTED THE BRIEF. The brief said "the métro is city-contained", and it is
# half true. Measured against commune 35238's own contour:
#
#     a   15 inside /  0 outside
#     b   11 inside /  4 outside    Atalante, Cesson - Viasilva (Cesson-Sévigné)
#                                   La Courrouze, Saint-Jacques - Gaîté
#                                   (Saint-Jacques-de-la-Lande)
#
# Line b loses BOTH of its termini. 26 station-line pairs inside -> 24 unique
# stations after collapsing the two interchanges (Gares and Sainte-Anne, a+b,
# both inside).
#
# WHY COMMUNE-ONLY, when Lille went regional on the same question:
#
#   - the deciding measure in France is the WORST LINE'S SURVIVAL. Lille's was
#     a stub - the tram kept 3 of 36 stations, Métro 2 19 of 44 - and went
#     regional. Toulouse's worst was T1 at 13 of 25 (52%, a whole branch lost)
#     and stayed commune-only. Rennes' worst is line b at 11 of 15 (73%),
#     better than Toulouse's, so commune-only is the consistent answer;
#   - it keeps Paris, Marseille, Toulouse and Rennes on one comparable scope,
#     with Lille the one exception and the stub as its reason.
#
# NOT the reason, and worth saying because it was once mis-stated for Toulouse:
# data availability. SIRENE is one national file, so Cesson-Sévigné's and
# Saint-Jacques-de-la-Lande's businesses are already in the parquet this city
# reads. Regional was a wider filter away, put to the owner, and declined.

# GATE 3: the operator's own station count, from outside the feed.
#
# SOURCE: STAR's portal, `tco-metro-topologie-dessertes-td` ("Dessertes des
# parcours de métro du réseau STAR", 60 records) - the operator's own list of
# which stop each métro route serves, with the line on every row. A
# first-party layer, osm-rail's first choice. Its catalogue `modified` reads
# 2014, but it carries line b (opened 2022) in full and was re-processed the
# night it was read, so the date is the dataset's creation, not its content.
# Measured 2026-09-24 00:04 UTC:
#
#     a   STAR 15   OSM 15   feed 15
#     b   STAR 15   OSM 15   feed 15
#
# Its sibling `tco-metro-topologie-stations-td` holds 28 stations - the feed's
# network-wide count - each with `codeinseecommune`, and puts exactly 24 in
# 35238, 2 in Cesson-Sévigné and 2 in Saint-Jacques-de-la-Lande: the same four
# excluded stations step 1 finds geometrically. So the scope split is the
# operator's own attribute, not only a point-in-polygon result.
#
# ⚠ IT WAS NOT READABLE ON THE DAY OF THE BUILD. data.explore.star.fr refused
# every call on 2026-09-23 on a spent domain-wide quota (see GTFS_URL), so the
# build first took gate 3 from OpenStreetMap's route relations (network=
# FR:STAR, four relations, nodes-first) and confirmed it here after the 00:00
# UTC reset. OSM stays the cross-check.
OPERATOR_STATION_COUNTS = {"a": 15, "b": 15}
OPERATOR_COUNTS_SOURCE = (
    "data.explore.star.fr tco-metro-topologie-dessertes-td (STAR's own per-line "
    "stop list), read 2026-09-24 - per-line, both lines; OpenStreetMap's route "
    "relations agree")

# WHAT SURVIVES THE BOUNDARY, PER LINE. Asserted in step 1 so the scope
# decision is CHECKABLE rather than merely written down. If these numbers move,
# the scope decision is being re-taken and should be re-taken deliberately.
EXPECTED_INSIDE_PER_LINE = {"a": 15, "b": 11}

# route_short_name -> the name riders use. The feed's short names are bare
# lower-case letters; STAR itself writes "ligne a" and "ligne b" in lower case,
# and the lower case is the operator's own styling, so it is kept.
LINE_NAMES = {
    "a": "Métro a",
    "b": "Métro b",
}

# STAR's livery, from the feed's own route_color. OSM's `colour` tags differ
# by one step on line a (#ED1C24 against the feed's #EE1D23); the feed is the
# publisher's and wins.
LINE_COLOURS = {
    "a": "#EE1D23",
    "b": "#00893E",
}

# --- Business filtering ------------------------------------------------

# HOW IN-CITY ROWS ARE IDENTIFIED: the INSEE commune code, SIRENE's
# authoritative marker. Like Toulouse, an EXACT code rather than a prefix
# family - Rennes has no arrondissements. Kept as a prefix tuple so the shared
# step-2 signature is the same for every French city.
COMMUNE_PREFIXES = ("35238",)

# Kept because the scaffold's shared step templates reference it. Rennes does
# not filter on a name string; COMMUNE_PREFIXES is the real filter.
CITY_KEEP = "RENNES"

# The per-city catch-all verdict, which france_naf.py deliberately declines to
# make. TAKEN 2026-09-23 from this city's own measured shares, not inherited.
#
# The national argument is INSEE's own class labels - "autres ... n.c.a." is a
# residual bucket, and in France it is where home-based sole traders land.
# That transfers. The shares were measured rather than assumed:
#
#     96.09Z   Paris  9.6%   Marseille  9.8%   Toulouse 13.9%   RENNES 14.0%  (576)
#     56.29B   Paris  1.0%   Marseille  1.0%   Toulouse  1.6%   RENNES  1.7%  ( 70)
#
# And the discriminator, measured with NOTHING excluded (step 2 prints it
# after the exclusion, when the dropped codes are already gone): rows with NO
# employee band are 28.8% catch-all against 9.8% for rows that record one,
# and are the less-named ones (52.8% vs 63.2%). Toulouse measured 26.4% vs
# 8.8%. That is the signature of a registered individual with no premises -
# a data-quality problem (not a storefront) and a privacy one (a person at
# their home address on a public map) - so the verdict is the same on this
# city's own numbers, not by inheritance.
#
# The three retail catch-alls are KEPT, as in every French city: 47.19B
# (0.9%), 47.29Z (1.8%) and 47.78C (3.1%) are small, and INSEE's labels for
# them say "EN MAGASIN" - premises on their face.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "naf_label"
# This taxonomy also classifies by naf_code: keep those raw column(s) through step 2
# (they are passed to classify() by filter_to_storefront() and the map).

# Sanity bounds, TIGHTENED to the commune's own measured extent plus ~0.02 deg
# (about 2 km). The contour measures 48.0769-48.1550 N, 1.6244-1.7525 W -
# 50.3 km2, the smallest commune of the five French cities (Toulouse 118.1).
#
# The box catches a CORRUPT coordinate - a swapped lat/lon, a zero, a
# whole-degree placeholder - and does not do the scoping; the boundary polygon
# does that.
RENNES_BBOX = {
    "lat_min": 48.05,
    "lat_max": 48.18,
    "lon_min": -1.78,
    "lon_max": -1.60,
}
