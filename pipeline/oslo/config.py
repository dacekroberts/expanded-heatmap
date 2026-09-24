"""Oslo-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; every scaffolded placeholder has been
replaced with a measured value, so this module ships none.

FIRST NORWEGIAN CITY. The national facts - the register, its columns, the
contact columns never to load, the sole-trader guard - live in
`pipeline/countries/norway.py`; the shared step 2 in `norway_register.py`.
What is Oslo's own is below: the kommune, the address file, the scope, the
rail, the palette and the catch-all verdict.
"""

from pathlib import Path

from pipeline.countries.norway import (  # noqa: F401
    ADDRESS_URL_TEMPLATE,
    KOMMUNE_BOUNDARY_URL_TEMPLATE,
)

SLUG = "oslo"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "oslo" / "raw"
DATA_PROCESSED = ROOT / "data" / "oslo" / "processed"
OUTPUTS = ROOT / "outputs" / "oslo"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the kommune, with the kommune each IS in - a citable
# scoping record. Twelve rows, every one on the T-bane's two western branches
# into Bærum.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all public and keyless. `fetch_sources.py` downloads them; no
# step may fetch. The two register files are NATIONAL and cached once for the
# country (`norway.SHARED_RAW`), as France's SIRENE parquets are.
GTFS_ZIP = DATA_RAW / "gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
ADDRESS_ZIP = DATA_RAW / "adresser_0301.zip"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# Ruter's aggregated GTFS through Entur, Norway's national access point.
# ⚠ A HEAD REQUEST IS NOT A PROBE HERE: Google Storage answers 200 with size 0
# and an empty content-type, which reads exactly like an empty file. A ranged
# GET returns 206 and `PK\x03\x04`. Measured 2026-09-24 at 50,999,897 bytes.
#
# ⚠ `feed_info.txt` EXISTS BUT DECLARES NO WINDOW - publisher Entur, language
# `no`, and no feed_start_date / feed_end_date. So, like Toulouse, the fetch
# date is what pins the snapshot, and fetch_sources records it.
GTFS_URL = ("https://storage.googleapis.com/marduk-production/outbound/gtfs/"
            "rb_rut-aggregated-gtfs.zip")
GTFS_SELF_ATTESTS = False

# Kommune 0301 - Oslo. Kartverket's own boundary, 480.5 km² as measured
# (the land area usually quoted is ~454 km²; the polygon includes the inner
# fjord). ⚠ Not the business filter - that is the sub-unit's own
# `beliggenhetsadresse.kommunenummer`.
KOMMUNE_NUMBER = "0301"
KOMMUNE_NAME = "Oslo"
BOUNDARY_URL = KOMMUNE_BOUNDARY_URL_TEMPLATE.format(code=KOMMUNE_NUMBER)
ADDRESS_URL = ADDRESS_URL_TEMPLATE.format(code=KOMMUNE_NUMBER, name=KOMMUNE_NAME)

# The kommunes that hold an EXCLUDED station, fetched so step 1 can NAME each
# one's municipality offline - the Los Angeles rule. Only Bærum: all 12
# outside stations are on the T-bane's Kolsås and Østerås branches. Step 1
# exits if a station falls outside Oslo AND outside every kommune listed here.
NEIGHBOUR_KOMMUNER = {"3201": "Bærum"}
NEIGHBOURS_GEOJSON = DATA_RAW / "neighbour_kommuner.geojson"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# ETRS89 / UTM 32N. Oslo's longitude (~10.75 E) falls in UTM zone 32 (6-12 E),
# derived per city as the invariant asks. Kartverket publishes Oslo's address
# file in 25832 among others, so this is also the zone its own data uses here.
# (Norway's national mapping grid is UTM 33, EPSG:25833 - that is a
# country-wide convenience, not Oslo's zone, and France's national-grid
# argument does not carry: Norway spans 32-35, and there is one city so far.)
CRS_PROJECTED = "EPSG:25832"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# NEW YORK'S TIGHT EDGES, on Toulouse's measured ground rather than inherited.
# Measured 2026-09-24 across the 155 in-kommune stations (nearest neighbour,
# ETRS89 / UTM 32N metres, after the name collapse and alias):
#
#     min 138    median 465    mean 500    max 1,707
#
# At a 465 m median the 483 m outer ring very nearly TILES - each station's
# edge stops just short of its neighbour's - where the default 966 m ring
# would reach two stations deep. That is the fit argument Toulouse's 525 m
# was taken on, and Lille's 501 m and Rennes' 541 m after it; applied on that
# measurement rather than re-asked. (Madrid, Barcelona, Dublin and Milan keep
# the default edges; their networks are sparser, so the argument differs.)
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# WHAT COUNTS - owner's calls, 2026-09-24:
#
#   * T-bane lines 1-5 (`route_type 401`) AND tram lines 12, 13, 15, 17, 18, 19
#     (`902`). Oslo's trams serve corridors the T-bane does not - Grünerløkka,
#     Frogner, Torshov, Sagene - which is Marseille's and Toulouse's shape
#     rather than Paris's or Prague's dense overlay, and all six are inside
#     the kommune.
#   * NOT the 6 ferry routes (`1008`, B1-B21), on Marseille's call: dropped
#     and disclosed, revisitable.
#
# ⚠ EVERY ROUTE TYPE HERE IS EXTENDED. Not one of the feed's 386 routes uses
# the basic 0-12 set; a basic-only reader sees zero rail in Oslo - the trap
# add-country records for Berlin, Hamburg, Stockholm and Oslo itself.
ROUTE_TYPES_RAIL = ("401", "902")
ROUTE_IDS = [f"RUT:Line:{n}" for n in (1, 2, 3, 4, 5, 12, 13, 15, 17, 18, 19)]

# ✅ OSLO KOMMUNE ONLY, owner's call 2026-09-24, on the rule the French cities
# settled: the deciding measure is the WORST line's station survival.
#
#     T-bane 1  37/37   T-bane 2  38/47   T-bane 3  29/38 (76%)
#     T-bane 4  37/37   T-bane 5  45/51   every tram line 100%
#
# Line 3's 76% is better than Toulouse's T1 (52%) and Rennes' Métro b (73%),
# both commune-only; Lille went regional because its tram was a stub. The 12
# stations outside are ALL in Bærum (3201), on the Kolsås and Østerås branches.
# SIRENE's lesson applies: the register is national, so regional was a wider
# filter away, and declined.

# GATE 3 - NETWORK-LEVEL, and a SECONDARY source, recorded as such.
#
# The T-bane has 101 stations: the feed's 101 distinct parent stations for
# `route_type 401` match the figure Norwegian Wikipedia gives, and an OBOS
# article gives the same count for Sporveien's tracks (seen through a search
# summary, not read verbatim), 2026-09-24. Sporveien's own "Om Sporveien" page
# states no count. OSM could NOT be used, unlike Lille and Rennes: its line-2
# relation lists 25 stations against the feed's 47, so its relations are
# partial here. No per-line or tram figure from outside the feed was found,
# and none is invented.
OPERATOR_STATION_COUNTS = {"T-bane (network)": 101}
OPERATOR_COUNTS_SOURCE = (
    "101 T-bane stations: Norwegian Wikipedia and OBOS (citing Sporveien), "
    "read 2026-09-24 - a secondary source; no tram figure outside the feed")

# ONE STATION UNDER TWO NAMES - the alias list, explicit rather than a rule.
# The spacing gate flagged ten stations within 200 m; read by name 2026-09-24,
# exactly one pair is one place: the tram stop "Forskningsparken T" sits 12 m
# from the T-bane station "Forskningsparken" (Ruter's " T" suffix marks a stop
# serving the T-bane). The other four pairs under 200 m are real, distinct
# stops - Kjelsås / Kjelsåsalléen 138 m, Stortinget / Stortorvet 142 m,
# Heimdalsgata / Nybrua 152 m, Frydenlund / Welhavens gate 187 m. A blanket
# "strip the T suffix" rule was rejected: it would merge by spelling, and an
# alias merges only what was looked at.
STATION_NAME_ALIASES = {"Forskningsparken T": "Forskningsparken"}

# The shared spacing gate's floor on the collapsed stations' median spacing.
# The shared 400 m floor PASSES on its own terms (network-wide collapsed
# median 475 m), so no override is passed - unlike Paris and Marseille,
# which needed 200. Kept as a named setting so a future change is visible.
SPACING_MIN_M = 400.0

# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope
# decision is CHECKABLE rather than merely written down. Counted after step
# 1's name collapse, so tram figures sit a stop or two below a count of stop
# places (Trikk 12 is 32 names across 33 places). If these move, the scope
# decision is being re-taken and should be re-taken deliberately.
EXPECTED_INSIDE_PER_LINE = {
    "1": 37, "2": 38, "3": 29, "4": 37, "5": 45,
    "12": 32, "13": 23, "15": 34, "17": 28, "18": 27, "19": 22,
}

# route_short_name -> the name riders use. Ruter numbers its lines; the mode
# word distinguishes T-bane 1 from a bus 1.
LINE_NAMES = {
    "1": "T-bane 1", "2": "T-bane 2", "3": "T-bane 3", "4": "T-bane 4",
    "5": "T-bane 5",
    "12": "Trikk 12", "13": "Trikk 13", "15": "Trikk 15", "17": "Trikk 17",
    "18": "Trikk 18", "19": "Trikk 19",
}

# ⚠ THE FEED CANNOT COLOUR THESE LINES APART: every T-bane line is `EC700C`
# and every tram line `0B91EF`. Ruter's own network maps give each line its
# own colour, and OSM carries them on the route relations (operator Sporveien
# T-banen / Sporveien Trikken, network Ruter), read 2026-09-24.
#
# Nine of the eleven are Ruter's exact colours. Two were REFUSED by the shared
# check (pipeline/linecolour.py, Delta-E floor 10) and shifted in HSL
# LIGHTNESS ONLY, hue and saturation kept - Paris's bis-line and Lille's tram
# precedent:
#
#   T-bane 1  Ruter #0073db was 6.5 from the Retail pins (#2a78d6) - it would
#             vanish under its own pins. -> #0083fa (L .43 -> .49): worst pair
#             now 14.2, still vs Retail; 9.7 from Ruter's own shade. Darker
#             was rejected: it runs into T-bane 4's navy (#004a98).
#   Trikk 12  Ruter #a066aa was 5.7 from T-bane 3's #a85fa5 - Ruter's own two
#             purples are all but identical. T-bane 3 keeps Ruter's colour as
#             the primary line; Trikk 12 -> #ae7cb6 (L .53 -> .60): worst pair
#             13.5, vs T-bane 3; 9.8 from Ruter's shade.
#
# LIGHTER, not darker, for both: the maps open on a dark basemap, which the
# check does not score, and Lille's lesson is that a dark shade the check
# approves can vanish there - so both are confirmed in the browser too.
#
# Trikk 15 has NO Ruter colour recorded anywhere read: it is not in OSM, whose
# tram relations carry line 11 instead. The feed's 15 shares 32 of its 34
# stops with line 12 - line 11's Kjelsås service rerouted while the Briskeby
# line is closed (Sporveien: reopening autumn 2027). #00a3a8, a teal no other
# line or pin is near, is this project's choice, Dublin's precedent for a
# line with no published colour, and cleared the check first time.
LINE_COLOURS = {
    "1": "#0083fa", "2": "#ec700c", "3": "#a85fa5", "4": "#004a98",
    "5": "#32aa35",
    "12": "#ae7cb6", "13": "#00b26b", "15": "#00a3a8", "17": "#ed1b2f",
    "18": "#fdb913", "19": "#f7942a",
}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "norway_sn2025"
RAW_CLASSIFICATION_COLUMN = "sn2025_label"
CITY_KEEP = "OSLO"   # kept for the scaffold's templates; KOMMUNE_NUMBER filters

# The per-city catch-all verdict, which norway_sn2025.py declines to make.
# TAKEN 2026-09-24 from Oslo's own measured profile:
#
#     96.990  Andre personlige tjenester ikke nevnt annet sted
#             813 rows (6.0%) - employees registered on 5%, ENK parent on 87%
#
# The strongest home-based signature measured in any city here: nearly nine in
# ten are sole traders and almost none employ anyone. France's 96.09Z, on
# Oslo's own numbers. The five RETAIL catch-alls (47.120, 47.270, 47.559,
# 47.690, 47.780) are kept, as in every French city - they are shops by
# product, and SN2025's labels carry no in-store/out-of-store distinction to
# argue from either way.
CATCH_ALL_EXCLUDE = ("96.990",)

# Sanity bounds: the kommune's measured extent (59.8093-60.1351 N,
# 10.4892-10.9514 E) plus ~0.02 deg. Catches a corrupt coordinate; the join
# to Kartverket's own address file does the placing.
OSLO_BBOX = {
    "lat_min": 59.79,
    "lat_max": 60.16,
    "lon_min": 10.47,
    "lon_max": 10.97,
}
