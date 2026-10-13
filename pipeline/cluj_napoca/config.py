"""Cluj-Napoca-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/cluj_napoca.md. Romania's second city and the first DSVSA
county after Bucharest's (owner, calls 215a and 222): food only.

Business leg: DSVSA Cluj's lists of registered retail food units, one file
per unit category, for the whole county, saved by the owner in their own
browser on 2026-10-07 (the county's hosts refuse scripts). Each file is read
by its ROLE, from its name (pipeline/taxonomies/romania_dsvsa.py), never by
its number: Cluj numbers its files differently from Bucharest. A row is in
the city where its address names Cluj-Napoca. Placed by JOINING its address
to OpenStreetMap's address objects inside the municipality (Bucharest's
join), with three repairs of this city's and, where the street is known but
not the number, the nearest listed number on the same side of the street
(Palma's tier, owner call 215a). The unplaced share is stated on the page.

Rail: CTP's tram lines 100, 101 and 102 from OpenStreetMap's route relations
(pipeline/osm_tram.py): CTP publishes no feed this project can use. Stations
are the two directions' stops paired (the brief's call 11).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "cluj_napoca" / "raw"
DATA_PROCESSED = ROOT / "data" / "cluj_napoca" / "processed"
OUTPUTS = ROOT / "outputs" / "cluj_napoca"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities). Header-only here: every stop is inside.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

NAME = "Cluj-Napoca"
SLUG = "cluj_napoca"

# --- The register ---------------------------------------------------------
#
# DSVSA Cluj's files as the owner's browser saved them (the animal-origin list
# in data/cluj_napoca/raw/, the non-animal-origin list in raw/non-animal/),
# each with the first 16 hex digits of its SHA-256 as the brief measured it
# on 2026-10-07 and the date the file itself states. fetch_sources.py stops
# on a file whose hash has changed: a changed file is a new fetch to
# re-measure, never a silent update. The role each file plays is read from
# its NAME by romania_dsvsa.role_for_file().
ANIMAL_FILES = {
    "01.inregistrate-carmangerie.xls": ("137d5b6ed5914d01", "2026-09-15"),
    "02.inregistrate-macelarie.xls": ("07d5496e889e40fd", "2026-09-15"),
    "15.inregistrate-magazin-desfacere-miere.xls": ("044d73fad049be25", "2026-09-25"),
    "17.inregistrate-restaurant-bistro.xls": ("3e6a8eb2a8b19454", "2026-06-29"),
    "18.inregistrate-pizzerie.xls": ("eb44ad444be9462e", "2026-09-25"),
    "21.inregistrate-cofetarie_patiserie.xls": ("cd08919fc1e38a05", "2026-09-25"),
    "23.inregistrate-magazin-alimentar.xls": ("da52efeccf6512fb", "2026-09-25"),
    "24INREGISTRARE-SUPERMARKET.xls": ("f3ac53f85b0fe751", "2026-09-28"),
    # Listed with the animal-origin files; its own title says non-animal
    # origin. It and the non-animal list's bars file (27) share premises, and
    # both are read and merged (the brief's call 2).
    "36.inregistrate-Bar.xlsx": ("b9940846f7ce2db2", "2026-04-30"),
}
NON_ANIMAL_FILES = {
    "01.-FABRICARE-PAINE.xls": ("6cc35b7890a2fbdf", "2026-10-06"),
    "02.inregistrate-prajituri_proaspete-patiserie.xlsx": ("987eef23f4a4ba70", "2026-10-06"),
    "03.inregistrate-paine_prajituri_proaspete-patiserie-1-ok.xlsx": ("9da1a32b5d02cf96", "2026-10-06"),
    "19.inregistrate-fabricare-inghetata_25047ro.xlsx": ("efd5139501aee774", "2026-10-06"),
    "26.inregistrate-comercializ-cu-amanuntul-prod-nonanimala.xlsx": ("b203ce558a526971", "2026-10-06"),
    "27-.inregistrate-Bar_25092ro-1.xlsx": ("58fc0c88abd40a3e", "2026-10-06"),
    "29.inregistrate-cantine-catering_restaurant-vegan.xlsx": ("fde2868c8fa7fde6", "2026-10-06"),
    "33.inregistrate-comercializ-prod-nonanimala-congelate.xlsx": ("34568629f1a2ff14", "2026-10-06"),
}
# The files state five dates, not one: the bars file 30 April 2026, the
# restaurants file 29 June 2026, the rest 15 September to 6 October 2026. The
# page states the range (the brief's call 3).
REGISTER_DATE_FIRST = "2026-04-30"
REGISTER_DATE_LAST = "2026-10-06"
# The county's rows each file must hold (the brief's table, measured
# 2026-10-07); step 2 stops on a different count.
EXPECTED_ROWS = {"A01": 22, "A02": 4, "A15": 4, "A17": 3113, "A18": 405, "A21": 350, "A23": 4716, "A24": 234,
                 "A36": 1235, "N01": 19, "N02": 156, "N03": 95, "N19": 7, "N26": 490, "N27": 650, "N29": 63,
                 "N33": 24}

# --- Addresses -----------------------------------------------------------
#
# OSM address objects inside the municipality (relation 3277038) with both
# addr:street and addr:housenumber - the JOIN target, Bucharest's query on
# this relation. Cached under its fetch date; a re-fetch writes a NEW dated
# file and this name is then pointed at it on purpose.
OSM_ADDRESSES_CSV = DATA_RAW / "osm_addresses_2026-10-11.csv"
OSM_ADDRESSES_QUERY = (
    '[out:csv(::type,::id,::lat,::lon,"addr:street","addr:housenumber","addr:postcode")][timeout:300];'
    'area(3603277038)->.a;nwr["addr:street"]["addr:housenumber"](area.a);out center;')
# The fewest address objects a whole answer holds (the brief counted 22,217
# on 2026-10-07): a shorter file is a partial answer, not the city.
OSM_ADDRESSES_MIN = 20000
# One matched address is ONE place when its OSM points link hop to hop within
# ADDRESS_HOP_M and span no more than SITE_SPREAD_MAX_M: Bucharest's values,
# which its place() reads from its own config.
ADDRESS_HOP_M = 150
SITE_SPREAD_MAX_M = 600
# The nearest-number tier (owner, call 215a; Palma's rule): where OSM has the
# street but not the number, the nearest number OSM lists on the same side
# (odd or even), at most this many numbers away, a tie going to the lower
# number, and only where that number's points are one site.
NEAREST_NUMBER_MAX = 6
# The placed share the owner's call rests on (71.6% measured by staging,
# 2026-10-07, against the reduced-bucket bar of 70%): step 2 stops under the
# bar rather than publish a thinner map than the one approved.
PLACED_SHARE_MIN = 0.70

CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# Municipiul Cluj-Napoca, OSM relation 3277038 (admin_level 8), polygonised
# from its outer ways and gated on its area: 174.9 km2 in UTM 34N (the brief,
# 2026-10-07).
BOUNDARY_OSM_RELATION = 3277038
BOUNDARY_OSM_NAME = "Cluj-Napoca"
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_cluj_napoca.json"
BOUNDARY_AREA_KM2 = (170, 180)

# --- Rail ----------------------------------------------------------------
#
# CTP's trams from OpenStreetMap's route relations (osm-rail, tram-city): the
# relations `out geom`, their stop nodes `out body`. S, W, N, E.
RAIL_BBOX = (46.70, 23.45, 46.83, 23.72)
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
ROUTE = "tram"
OPERATOR = None          # select on ref; the relations' operator tag is printed
LINE_REFS = ("100", "101", "102")
# 102L: the depot runs between Disp. Bucium and the depot, with no stops.
NOT_DRAWN = {
    3793880: "102L, a depot run with no stops (the brief)",
    13922576: "102L, a depot run with no stops (the brief)",
}
# Three stop members OSM leaves unnamed (tagged only with the operator), named
# from CTP's own linear stop maps (ctpcj.ro/orare/png/img_<line>_lv_<direction>.png,
# read 2026-10-07; the brief's call 11). osm_tram stops if OSM names or tags
# one: remove the entry then.
NAME_MEMBERS = {
    11067242917: "Libertatea Est Tram",
    11259441754: "Primăria IRIS",
    11254713222: "Sala Sporturilor",
}
# STATIONS ARE DIRECTION PAIRS (the brief's call 11, its recommendation, on
# tram-city section 2's rule that a merge of differently named stops is
# stated): CTP names each direction's stop separately, so an exact-name
# collapse gives 41 points a median 67 m apart. Each stop is paired with the
# nearest stop of the opposite direction within PAIR_MAX_M; a pair whose two
# names differ is labeled with both, the westbound name first.
PAIR_MAX_M = 300
STATIONS_EXPECTED = 20
# Gate 3: CTP's linear stop maps, per direction (the brief): 100 10 / 10; 101
# 9 / 11 (CTP's map toward Bucium ends at Clăbucet, where OSM's relation runs
# on to Disp. Bucium, so OSM holds 10 / 11); 102 19 / 20. Stop members per
# OSM relation, as the brief read them:
STOP_MEMBERS_PER_RELATION = {5671140: 10, 5671141: 10, 5673690: 10, 5673691: 11, 5673735: 19, 5673736: 20}
# Stations per line once the directions are paired: line 100 ten pairs; line
# 101 nine pairs, G. Barițiu (no opposite stop) and Disp. Bucium; line 102
# all twenty.
OPERATOR_STATION_COUNTS = {"100": 10, "101": 11, "102": 20}
OPERATOR_COUNTS_SOURCE = ("CTP Cluj-Napoca's linear stop maps (ctpcj.ro/orare/png/), read 2026-10-07: 100 10 and "
                          "10 stops per direction, 101 9 and 11, 102 19 and 20; CTP's 101 map toward Bucium "
                          "ends at Clăbucet, one stop before OSM's relation")
# Gate 1's floor: Toyama's and Riga's 200 m for a tram network; the pairs'
# median gap is recomputed by step 1.
SPACING_MIN_M = 200.0
MEDIAN_GAP_BOUNDS_M = (350.0, 550.0)

DRAWN_LINES = LINE_REFS
LINE_NAMES = {"100": "Tram 100", "101": "Tram 101", "102": "Tram 102"}
# The project's own colours (no OSM relation carries a colour; 2026-10-11):
# each reads 3:1 on both map pages, clears CIE76 45 from every pin (blue
# 82.0, violet 69.4, orange 62.4) and stands 42.9 or more from the other
# two lines, which share track end to end.
LINE_COLOURS = {"100": "#0868B8", "101": "#7848C8", "102": "#E06000"}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 34N: the longitude (~23.59) falls in the 18 to 24 band. Derived
# per city, not copied (Bucharest is 35N) - see docs/project_context.md's CRS
# lesson.
CRS_PROJECTED = "EPSG:32634"

# --- Ring geometry ---------------------------------------------------------
# Halved rings by the spacing rule (a median gap of about 550 m or less,
# docs/ring_rules.md): the brief measured 475 m on the 20 pairs; step 1
# recomputes it on the stations drawn.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Business filtering ------------------------------------------------

CITY_LABEL = "the Municipality of Cluj-Napoca"
TAXONOMY_SYSTEM = "romania_dsvsa"
RAW_CLASSIFICATION_COLUMN = "Categorie"

# The municipality's frame; placement is by OSM address and the polygon does
# the filtering.
CLUJ_NAPOCA_BBOX = {
    "lat_min": 46.68,
    "lat_max": 46.85,
    "lon_min": 23.43,
    "lon_max": 23.76,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3603277038)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ro",)
PLACE_FOLD = None
PLACE_REVIEWED = {}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "way/278312772": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/276704844": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/275161895": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/207452268": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "node/11491274868": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/283161804": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/258878037": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "node/14270671517": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "node/8257918819": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "node/9346436677": "a freight yard, depot or operating point, not a passenger station (owner, 2026-10-13)",
    "way/669521911": "a duplicate place row, the node carries the same name",
    "way/669535695": "a duplicate place row, the node carries the same name",
    "node/4494264091": "a duplicate row, the same church as the way beside it",
    "way/304949094": "an open-air museum exhibit, a farmstead with no article",
    "way/278142636": "an open-air museum exhibit, a farmstead with no article",
    "relation/4062712": "an open-air museum exhibit, a farmstead with no article",
    "way/278142777": "an open-air museum exhibit, a description as its name",
    "way/1424822217": "a description standing in for a name",
    "way/278312124": "a description standing in for a name",
    "node/3586268027": "a description with a code glued on, inside a firm's premises",
    "way/1024562571": "dwellings with no article, a home",
    "way/1337279960": "a house with no article, and a typo in the name",
    "node/7848257077": "a religious residence with no article",
    "way/1462802583": "a religious residence with no article",
    "way/585206582": "a service way named by an address, not a street",
    "way/585204635": "a service way named by an address, not a street",
    "way/694262074": "a coded footway, no street name",
    "way/223357863": "a coded footway, no street name",
    "way/1549103365": "a name that says the bridge is temporary",
    "way/1550723831": "a name that says the bridge is temporary",
    "way/1550723832": "a name that says the bridge is temporary",
    "way/356779834": "a glitched name, street word glued to the name",
}
