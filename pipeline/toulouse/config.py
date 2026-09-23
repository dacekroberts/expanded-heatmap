"""Toulouse-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; every scaffolded placeholder has been
replaced with a measured value, so this module ships none.

THIRD FRENCH CITY. What it inherits from Paris and Marseille is the country
module, the national NAF taxonomy, the shared parquet cache, the Milan-hybrid
naming and the Lambert-93 grid. What it does NOT inherit is the scope
decision, the ring edges, the gate-3 source or the rail scope - and this is
the city that proves the rule, because the scope answer came out DIFFERENT
from Marseille's on the same measurement.

⚠ FIRST NON-RAIL MODE IN THE PROJECT. Téléo is an aerial cable car
(`route_type 6`). See the station-scope section; the decision is the owner's,
taken 2026-09-23, and it is the first time any built city draws something that
is not on rails.
"""

from pathlib import Path

# The national facts, shared with Paris, Marseille and the two French cities
# after this one. SIRENE is ONE register for the whole country - Mexico's
# shape, not Spain's - so the columns, the active value, the diffusion mask and
# the geolocation schema live in the country module. Re-exported with noqa so
# this city's step files import them from here.
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
DATA_RAW = ROOT / "data" / "toulouse" / "raw"
DATA_PROCESSED = ROOT / "data" / "toulouse" / "processed"
OUTPUTS = ROOT / "outputs" / "toulouse"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities). It carries 14 rows here and they are not a footnote:
# see the scope section.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all public. `fetch_sources.py` downloads them; no step may fetch
# (scripts/check_no_fetch_in_steps.py enforces it).
GTFS_ZIP = DATA_RAW / "gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# SIRENE_PARQUET and GEOLOC_PARQUET are NATIONAL and imported from the country
# module above - one 3 GB cache for all five French cities, not one each.

# Tisséo's feed, from Toulouse Métropole's Opendatasoft portal. Measured
# 2026-09-23 at 11,962,958 bytes, 11 files, no key and no account.
#
# ⚠ THE FILE ID IS LOAD-BEARING AND LONG. A truncated copy returns HTTP 404
# "Unknown image" naming the id you sent, rather than refusing you - so a
# typo reads as a dead dataset rather than as a typo. Pinned by a brief check.
GTFS_URL = ("https://data.toulouse-metropole.fr/explore/dataset/tisseo-gtfs"
            "/files/fc1dda89077cf37e4f7521760e0ef4e9/download/")

# Commune 31555 - Toulouse, 118.1 km2 measured, between Paris's 105.4 and
# Marseille's 238.1.
# ⚠ `geometry=contour`, NOT `fields=contour`: the latter answers HTTP 200 with
# a 120-byte POINT and would scope the build to one coordinate without erroring.
BOUNDARY_COMMUNE_CODE = "31555"
BOUNDARY_URL = ("https://geo.api.gouv.fr/communes/31555"
                "?geometry=contour&format=geojson")

# ⚠ NO feed_info.txt - PARIS'S GAP, NOT MARSEILLE'S SELF-ATTESTATION.
# Measured 2026-09-23: the zip carries agency, calendar, calendar_dates,
# fare_attributes, fare_rules, routes, shapes, stop_times, stops, transfers and
# trips, and NO feed_info.txt. So staleness is not readable from the artifact
# and the download date must be captured at fetch time or it is unknowable.
# Unlike Paris there IS a second attestation available - the Opendatasoft
# catalogue's own `modified` field, which read 2026-09-23 - so fetch_sources.py
# records both.
GTFS_SELF_ATTESTS = False
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# LAMBERT-93, as Paris and Marseille take it, and for the reason that made it
# decisive there rather than merely permitted: metropolitan France spans UTM
# zones 30N, 31N and 32N, so a per-city UTM rule would give the French cities
# three different projections while they all read ONE national file.
# Lambert-93 is a single grid defined for exactly this extent.
#
# ⚠ THE SCAFFOLD PROPOSED EPSG:32631 (UTM 31N) from the longitude, and that is
# the generic rule doing its job - it does not know this city reads a national
# file. Overridden deliberately, not by oversight.
#
# The invariant is "derived per city, never copied"; deriving from France's own
# national grid satisfies it, where copying a sibling city's UTM zone would
# not. Toulouse is at 1.44 E, inside the metropolitan domain that
# check_provenance.py's NATIONAL_GRIDS bounds this entry to (-5.5 to 10.0) -
# the DOM use 2975 / 5490 / 2972 and must not inherit it.
CRS_PROJECTED = "EPSG:2154"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# FOURTH CITY ON NEW YORK'S EDGES - AND THE FIRST TO TAKE THEM FOR A DIFFERENT
# REASON, which is why this comment does not simply point at Marseille's.
#
# Measured 2026-09-23 across the 48 in-commune stations, in Lambert-93 metres:
#
#     min 296    median 525    mean 583    max 2,017
#     under 200 m: 0           under 100 m: 0
#
# Paris (399 m) and Marseille (341 m) took these edges because the default
# 0.6 mi / 966 m outer ring swamped a tight network and merged every ring into
# one mass. Toulouse is LOOSER than both. The argument here is a fit argument
# instead: at a 525 m median, a 483 m outer ring very nearly TILES - each
# station's outer edge stops just short of its neighbour's - which is a better
# match than either sibling gets, while 966 m would still reach almost two
# stations deep.
#
# Taking the same set rather than tuning a fourth keeps the three French cities
# on identical bands, so a reader comparing Toulouse with Paris and Marseille
# is comparing the cities and not the bucket boundaries. Owner's call
# 2026-09-23, with the fit measurement above as the ground.
#
# ⚠ The spacing gate in pipeline/stations.py does NOT fire here (nothing under
# 200 m), unlike Paris and Marseille where it did and had to be passed a
# `spacing_min`. Nothing is being suppressed.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# WHAT COUNTS: métro A and B, tram T1, and the Téléo cable car. Matched on the
# exact route_id - the feed carries 120 bus routes alongside them.
#
# ⚠ `route_type` 6 IS INCLUDED, AND IT IS A FIRST. Téléo is an aerial lift, so
# this is the first time any built city draws a mode that is not on rails.
# Owner's decision 2026-09-23, on these grounds:
#
#   - it is ticketed on the Tisséo network exactly as the métro is;
#   - 3 stations, all inside the commune, so it costs the scope nothing;
#   - it crosses the Garonne where no other Tisséo line does, so its catchments
#     cover ground the rest of the map leaves blank;
#   - one of its three stops, Université Paul Sabatier, is a MÉTRO B
#     INTERCHANGE, so it is wired into the network rather than standing apart;
#   - dd4ced8's test for a mode is functional - is this the service, or an
#     overlay on one - not a question of vehicle technology.
#
# ⚠ THE BRIEF'S ARGUMENT FOR THIS WAS FALSE AND WAS CORRECTED DURING THE BUILD.
# It read "It does draw a funicular (Paris), so 'not a train' is not itself a
# reason to exclude." Paris draws no such thing: pipeline/paris/config.py says
# "the Metro, and only the Metro", and lists "1 funicular, 1 cable" among what
# it EXCLUDED. There was no precedent in either direction, and Paris's
# exclusion is not one - the Montmartre funicular is a 108 m two-station lift
# inside one arrondissement. Generalising from it would have repeated exactly
# the error dd4ced8 corrected.
#
# TRAMS ARE DRAWN, as in Marseille. dd4ced8's rule asks whether a tram is the
# rapid-transit system or a dense overlay on one; T1 is a single line on its
# own corridor to Blagnac, not an overlay on the métro.
#
# LEFT OUT: 120 `route_type 3` bus routes. There is no commuter rail in this
# feed to exclude - Tisséo runs none - so the standing rule that drops Boston's
# CR-*, Chicago's Metra and Madrid's Cercanías has nothing to act on here.
ROUTE_TYPES_RAIL = ("0", "1", "6")
ROUTE_IDS = ["line:61", "line:69", "line:68", "line:204"]

# ✅ COMMUNE-ONLY, SETTLED BY MEASUREMENT 2026-09-23 - and this is the city
# where Marseille's answer did NOT transfer cleanly. Measured against commune
# 31555's own contour:
#
#     A      17 inside /  1 outside     (Balma-Gramont)
#     B      19 inside /  1 outside     (Ramonville)
#     T1     13 inside / 12 outside     (the whole Blagnac/Beauzelle branch)
#     TELEO   3 inside /  0 outside
#
# 52 station-line pairs inside, 14 lost -> 48 unique stations after collapsing
# 4 interchanges (Arènes A+T1, Jean Jaurès A+B, Palais de Justice B+T1,
# Université Paul Sabatier B+TELEO).
#
# ⚠ MARSEILLE'S TEST PASSES HERE ONLY ON A TECHNICALITY. There the rule was
# "all five lines are 100% inside, so commune-only costs nothing". Here every
# line survives, but T1 survives at HALF STRENGTH - it loses Aéroconstellation,
# Servanty Airbus, MEETT, Pasteur-Mairie de Blagnac and eight more. So this is
# a real cost accepted deliberately, not a free choice:
#
#   - it matches Paris (751xx) and Marseille (132xx), keeping the three French
#     cities on one comparable scope;
#   - the standing rule is that stations in another city are a NEW PROJECT, not
#     a config change - drawing Blagnac's stations would need Blagnac's
#     business data, sourced and licence-checked separately;
#   - widening to Toulouse Métropole would mean filtering SIRENE on 37 commune
#     codes and would set a precedent the remaining French cities would inherit.
#
# Owner's call 2026-09-23, with the alternatives (métropole; commune plus the
# Blagnac/Beauzelle pair) both put and both declined.
#
# The 14 excluded stations are written to EXCLUDED_STATIONS_CSV with the
# commune each lies in - and the commune is AUTHORITATIVE rather than inferred,
# because Toulouse Métropole's own tram-station layer carries a `commune`
# column. See the gate-3 note.

# GATE 3: the operator's own station count, from outside the feed.
#
# SOURCE: Toulouse Métropole's Opendatasoft portal - `arrets-itineraire`
# ("TISSÉO - Arrêts par itinéraire", 8,527 rows), which joins stops to
# itineraries and carries the line code on every row. A first-party GIS layer,
# not the feed, which is what osm-rail says to look for first. Refreshed
# 2026-09-23, the same day it was read.
#
# Measured 2026-09-23 - FOUR LINES, FOUR EXACT MATCHES, the cleanest gate 3 of
# any city so far:
#
#     A      operator 18   build 18   EXACT
#     B      operator 20   build 20   EXACT
#     T1     operator 25   build 25   EXACT
#     TELEO  operator  3   build  3   EXACT
#
# ⚠ AND THE OBVIOUS LAYER WOULD HAVE FAILED IT. `stations-de-tramway`
# ("Stations de tramway - Toulouse Métropole") looks like the right source and
# holds 29 records against T1's 25. The 4 extra are AÉROPORT, NADOT, DAURAT and
# JEAN MAGA, every one of them tagged `en_service: 2027` - a line that has not
# opened, sitting in the same layer as the 2010 and 2013 stations and separated
# from them only by that column. Counting the layer's rows would have reported
# a 4-station hole in the feed that does not exist.
#
# That is osm-rail's "proposed infrastructure is mixed in with built" trap,
# found in a first-party agency layer rather than in OSM - so the whitelist
# rule it states is not an OSM rule. It applies wherever a layer is read.
#
# ⚠ IT ALSO DISPOSED OF THE T2 QUESTION. Tisséo has historically branded a T2,
# and the feed carries only one tram route, which looked like a gap. The
# operator's own `ligne` register settles it: 152 lines, of which
# `metro: 2, tram: 1, telepherique: 1`. There is no T2 to be missing.
OPERATOR_STATION_COUNTS = {"A": 18, "B": 20, "T1": 25, "TELEO": 3}
OPERATOR_COUNTS_SOURCE = (
    "data.toulouse-metropole.fr arrets-itineraire (TISSÉO - Arrêts par "
    "itinéraire), refreshed 2026-09-23 - per-line, all four lines checked")

# WHAT SURVIVES THE BOUNDARY, PER LINE. Asserted in step 1 so the scope
# decision is CHECKABLE rather than merely written down - the same reason
# ROUTE_IDS is compared against the feed rather than trusted.
#
# It matters more here than it would in Marseille, where the answer was "all
# lines, 100%, nothing lost". Here T1 keeps 13 of 25, so a silent drift in the
# boundary or the feed could halve a line again without anything looking wrong.
# If these numbers move, the scope decision is being re-taken and should be
# re-taken deliberately.
EXPECTED_INSIDE_PER_LINE = {"A": 17, "B": 19, "T1": 13, "TELEO": 3}

# route_short_name -> the name riders use, as Tisséo writes it on its own maps
# and signage. The feed's short names are bare letters, so unlike Marseille
# there is something to translate: "A" alone is not what anyone calls the line.
LINE_NAMES = {
    "A": "Métro A",
    "B": "Métro B",
    "T1": "Tramway T1",
    "TELEO": "Téléo",
}

# Tisséo's official livery, from the feed's own route_color. All four are
# distinct from each other.
#
# ⚠ B IS YELLOW (#ffdd00) and yellow is the one livery colour that can vanish
# against a light basemap. Checked against the business-category palette when
# the map was rendered rather than assumed.
LINE_COLOURS = {
    "A": "#db001b",
    "B": "#ffdd00",
    "T1": "#004687",
    "TELEO": "#dc006b",
}

# --- Business filtering ------------------------------------------------

# HOW IN-CITY ROWS ARE IDENTIFIED. Not a city-name field - SIRENE is national
# and has none that is trustworthy. The authoritative marker is the INSEE
# commune code.
#
# ⚠ UNLIKE PARIS AND MARSEILLE THIS IS AN EXACT CODE, NOT A PREFIX FAMILY.
# Both of those cities are subdivided into arrondissements with their own codes
# (751xx, 132xx), so their filter is a prefix. Toulouse has no such
# subdivision: `31555` is the whole commune and the prefix tuple holds one
# complete code. Kept as a prefix tuple so the shared step-2 signature is the
# same for every French city.
#
# ⚠ `31555` is ALSO the boundary API's code here, which is a coincidence rather
# than a rule - Marseille's are 13055 (boundary) and 132xx (SIRENE), two code
# systems for one city. Do not read this city as evidence that they agree.
COMMUNE_PREFIXES = ("31555",)

# Kept because the scaffold's shared step templates reference it. Toulouse does
# not filter on a name string; COMMUNE_PREFIXES is the real filter.
CITY_KEEP = "TOULOUSE"

# The per-city catch-all verdict, which france_naf.py deliberately declines to
# make. TAKEN 2026-09-23 from this city's own measured shares, not inherited.
#
# The national argument is INSEE's own class labels - "autres ... n.c.a." is a
# residual bucket, and in France it is where home-based sole traders land. That
# transfers. THE SHARES DO NOT, and Toulouse is the city that proves it:
#
#     96.09Z   Paris  9.6%   Marseille  9.8%   TOULOUSE 13.9%  (1,429 rows)
#     56.29B   Paris  1.0%   Marseille  1.0%   TOULOUSE  1.6%  (  162 rows)
#
# Toulouse's personal-services catch-all is roughly 40% LARGER than either
# sibling's. Step 2's own discriminator says why it matters rather than merely
# being bigger: rows with NO employee band are 26.4% catch-all against 8.8% for
# rows that record one, and the unbanded rows are also the less-named ones
# (47.0% vs 57.4%). That is the signature of a registered individual with no
# premises, which is both a data-quality problem (not a storefront) and a
# privacy one (a person at their home address on a public map).
#
# The three retail catch-alls are KEPT, as in both siblings: 47.19B (0.8%),
# 47.29Z (1.5%) and 47.78C (2.6%) are small, and INSEE's labels for them
# describe shops - "autres commerces de détail EN MAGASIN" says premises on its
# face, which is the distinction the exclusion turns on.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "naf_label"
# This taxonomy also classifies by naf_code: keep those raw column(s) through step 2
# (they are passed to classify() by filter_to_storefront() and the map).

# Sanity bounds, TIGHTENED to the commune's own measured extent plus ~0.02 deg
# (about 2 km). The contour measures 43.5327-43.6687 N, 1.3503-1.5154 E.
#
# The box catches a CORRUPT coordinate - a swapped lat/lon, a zero, a
# whole-degree placeholder - and does not do the scoping; the boundary polygon
# does that. The scaffold's starting box spanned 0.8 deg of latitude and would
# have passed a point in Montauban.
TOULOUSE_BBOX = {
    "lat_min": 43.51,
    "lat_max": 43.69,
    "lon_min": 1.33,
    "lon_max": 1.54,
}
