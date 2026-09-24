"""Rotterdam-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

The Netherlands' second city, and Amsterdam's shape with the FOOD LAYER
REBUILT rather than read: Rotterdam publishes no hospitality register, but
every exploitation-permit decision is published in its Gemeenteblad, with a
point, through KOOP's official-publications API. A permit runs five years, so
the grants inside a five-year window approximate the permits in force - the
method recovers 97% of Amsterdam's live register and overcounts about 1.15x
(docs/build_briefs/rotterdam.md). Shops and services are the BAG's shop-class
units, from PDOK, exactly as Amsterdam's are from the city's own copy.
"""

from pathlib import Path

SLUG = "rotterdam"
NAME = "Rotterdam"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "rotterdam" / "raw"
DATA_PROCESSED = ROOT / "data" / "rotterdam" / "processed"
OUTPUTS = ROOT / "outputs" / "rotterdam"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs - every one written by pipeline/rotterdam/fetch_sources.py.
NOTICES_JSON = DATA_RAW / "koop_notices.json"          # the harvest, one list, every year
BAG_UNITS_JSON = DATA_RAW / "bag_verblijfsobjecten_winkelfunctie.json"
GTFS_ZIP = DATA_RAW / "gtfs-openov-nl.zip"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
OSM_NEIGHBOURS_JSON = DATA_RAW / "osm_neighbour_gemeenten.json"

# --- Endpoints ---------------------------------------------------------------

# KOOP's SRU 2.0 over the official publications. Keyless; its fair-use policy
# was not found in writing, so the harvest is paged politely (a pause per
# page). A query stops at 10,000 records, so it runs YEAR BY YEAR (the busiest,
# 2025, is 1,522). One TLS failure on 2026-09-24 cleared within the hour:
# retry, and a single failure is not a dead source.
SRU_URL = "https://repository.overheid.nl/sru"
SRU_PAGE = 500
SRU_FIRST_YEAR = 2021
# The UNION of the exploitation-permit rubric and the permit words in a title:
# neither alone is the set. On 2026-09-24 the rubric held 3,354 notices, while
# 424 provisional permits and 270 exploitation-titled notices sat outside it.
# Step 2 sorts each notice by its own title.
SRU_QUERY = ('c.product-area==officielepublicaties AND dt.creator=="Rotterdam" AND '
             '(dt.type=="exploitatievergunning" OR dt.title any "exploitatievergunning '
             'voorlopige alcoholwetvergunning terrasvlonder aanwezigheidsvergunning horeca")')

# PDOK's BAG WFS: shop-class units in use in gemeente 0599, served with their
# address (street, number, letter, addition, postcode) and a WGS84 point.
BAG_WFS_URL = "https://service.pdok.nl/lv/bag/wfs/v2_0"
BAG_WFS_PAGE = 1000
BAG_WFS_FILTER = (
    '<fes:Filter xmlns:fes="http://www.opengis.net/fes/2.0"><fes:And>'
    '<fes:PropertyIsLike wildCard="*" singleChar="." escapeChar="!"><fes:ValueReference>'
    'identificatie</fes:ValueReference><fes:Literal>0599*</fes:Literal></fes:PropertyIsLike>'
    '<fes:PropertyIsLike wildCard="*" singleChar="." escapeChar="!"><fes:ValueReference>'
    'gebruiksdoel</fes:ValueReference><fes:Literal>*winkelfunctie*</fes:Literal></fes:PropertyIsLike>'
    '<fes:PropertyIsEqualTo><fes:ValueReference>status</fes:ValueReference><fes:Literal>'
    'Verblijfsobject in gebruik</fes:Literal></fes:PropertyIsEqualTo></fes:And></fes:Filter>')

# National GTFS - the file Amsterdam's build downloaded and read (its licence
# read is in docs/data_sources.md: CC0 under the producer's LICENSE.TXT). RET
# publishes no standalone feed; RET is agency_id "RET" in this one. The file is
# COPIED from Amsterdam's cache by fetch_sources, not downloaded again.
GTFS_URL = "https://gtfs.openov.nl/gtfs-rt/gtfs-openov-nl.zip"
GTFS_SHARED_CACHE = ROOT / "data" / "amsterdam" / "raw" / "gtfs-openov-nl.zip"
GTFS_AGENCY_ID = "RET"

# --- Scope -------------------------------------------------------------------

# Gemeente Rotterdam, CBS code 0599, found by a BOUNDED tag search (osm-rail:
# an unbounded one is global) and required to be exactly one relation. It
# reaches from the Maasvlakte to Nesselande and takes in Hoek van Holland and
# Rozenburg, so the metro leaves it and re-enters it on line B.
GEMEENTE_CODE = "0599"
BOUNDARY_BBOX = (51.80, 3.90, 52.05, 4.65)          # s, w, n, e
NEIGHBOURS_BBOX = (51.75, 3.85, 52.12, 4.70)
BOUNDARY_AREA_KM2 = (300, 340)                      # CBS: ~325 km² including water

ROTTERDAM_BBOX = {"lat_min": 51.80, "lat_max": 52.05, "lon_min": 3.90, "lon_max": 4.65}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_SOURCE = "EPSG:28992"          # the notices' own RD New points
# UTM zone 31N: longitude ~4.48 falls in the 0-6 E band. Derived per city.
CRS_PROJECTED = "EPSG:32631"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope -----------------------------------------------------------

# RET's metro A-E and its trams, from the national feed. RECOMMENDED, for the
# owner's review: metro AND tram, Amsterdam's call of 2026-09-24 - Rotterdam's
# trams reach Noord, Blijdorp, Delfshaven, Kralingen and Charlois, where no
# metro runs, so they are not an overlay on the metro the way Milan's are.
# Line 12 is left out: it runs on 7 of the window's 82 days (the stadium
# event service). Lines 14 and 18 run on 62 of 82 (Monday to Saturday).
ROUTE_TYPES_RAIL = ("0", "1")        # basic GTFS: tram, metro
METRO_ROUTE_TYPE = "1"
NOT_DRAWN = {"12": "event service to Stadion Feijenoord - 7 of 82 days in the feed"}
LINE_ORDER = ("A", "B", "C", "D", "E",
              "1", "2", "3", "4", "5", "6", "7", "8", "11", "14", "18")
LINE_NAMES = {ln: (f"Metro {ln}" if ln.isalpha() else f"Tram {ln}") for ln in LINE_ORDER}

# A line's REGULAR ROUTE is the stops it serves on most days of the window -
# Amsterdam's rule (GVB runs up to 30 shapes per line); the same test here.
REGULAR_ROUTE_MIN_DAY_SHARE = 0.5
THIN_SPACING_MILES = 0.5
SPACING_MIN_M = 200.0
PLACE_LINK_M = 300
COLLAPSE_MAX_SPREAD_M = 400

# Stop names carry their town: "Rotterdam, Beurs", "Hoogvliet Rotterdam,
# Tussenwater", "Hoek van Holland, Hoek van Holland Strand" - all three places
# inside the gemeente, so all three prefixes are dropped for the label.
STRIP_PREFIXES = ("Rotterdam, ", "Hoogvliet Rotterdam, ", "Hoek van Holland, ")

# RET NAMES A PLATFORM, NOT A STOP, in the national feed - measured 2026-09-24:
# "Spartastraat spoor 1" and "spoor 2" 1 m apart, "Rotterdam Centraal perron A,
# B, E, F" for one tram stop, "Burgemeester Oudlaan 2" and "3" beside plain
# "Burgemeester Oudlaan", and "Burg. Van" beside "Burg. van Kempensingel". Each
# became its own station a few metres from its twin. These rewrite the name
# (after the town prefix) BEFORE platforms are grouped into places, so a
# platform's suffix can never split one stop; the 400 m spread gate still
# stops the build if a rewrite joined two real places.
STOP_NAME_PATTERNS = ((r"\s+spoor\s+\d+$", ""), (r"\s+[Pp]erron\s+[A-Z]$", ""),
                      (r"^(Burgemeester Oudlaan)\s+\d$", r"\1"),
                      (r"^Burg\. Van Kempensingel$", "Burg. van Kempensingel"),
                      (r"^Kleiweg RET$", "Kleiweg"),
                      # the tram stop at Blaak station is the metro's, 52 m away
                      (r"^Station Blaak$", "Blaak"))
# A turning siding a line lays over at is not a stop, whatever the feed's
# pickup flags say ("Opstelspoor Beverwaard", "Opstelspoor Carnisselande").
NON_REVENUE_PREFIX = "Opstelspoor"

# Gate 3: Wikipedia's line tables (read 2026-09-24, SECONDARY - RET publishes
# no per-line count). B 32, C 26, D 17, E 23 and the network's 71 match the
# nl article exactly. LINE A IS A RECORDED CORRECTION, not a relaxed gate:
# both articles give 24 - en.wikipedia with the terminus Vlaardingen West, and
# nl.wikipedia's table with Schiedam Centrum, which contradicts its own 24 -
# while the feed, valid to 2026-12-12, runs A from Binnenhof to Schiedam
# Centrum: 20 stations. The four in between are Vlaardingen's, outside the
# gemeente, so no ring here depends on which is current. en.wikipedia's line D
# (23, to Pijnacker Zuid) is the same extended network; the nl table's 17 is
# today's.
OPERATOR_STATION_COUNTS = {"Metro A": 20, "Metro B": 32, "Metro C": 26, "Metro D": 17,
                           "Metro E": 23, "Metro (network)": 71}
OPERATOR_COUNTS_SOURCE = ("nl.wikipedia.org/wiki/Rotterdamse_metro, read 2026-09-24 - "
                          "secondary; B 32, C 26, D 17, E 23, network 71 exact; A 24 there, "
                          "20 in the feed to 2026-12-12 (the extension to Vlaardingen West, "
                          "outside the gemeente) - a recorded correction")

# Metro colours are RET's own `route_color` in the feed, checked at step 1 so a
# change in the feed stops the build. Tram colours: the feed's own where it has
# one.
METRO_FEED_COLOURS = {"A": "#00983d", "B": "#ffdc00", "C": "#e52711", "D": "#00acd9",
                      "E": "#0f3f94"}
TRAM_FEED_COLOURS = {"1": "#3651a3", "2": "#f47b20", "3": "#f3aacb", "4": "#165d2f",
                     "5": "#ed1944", "6": "#55b948", "7": "#00aeef", "8": "#a1238f",
                     "11": "#3651a3"}
# RET gives trams 1 and 11 ONE colour (#3651a3), 8.6 from Metro E's #0f3f94,
# and this project refuses two lines under Delta-E 10. Oslo's and Amsterdam's
# rules: the metro keeps its colour and the tram moves, in HSL lightness only,
# by the smallest step that clears 13 from every other line - tram 1 lighter to
# #3f5ebe (L +0.07; 13.9 from its nearest line, 13.1 from the Retail pins),
# then tram 11 darker to #293e7d (L -0.10; 13.8).
#
# PROVISIONAL, FOR THE OWNER: trams 14 and 18 carry no route_color in the
# feed, and they serve seven stations no other line does (Euromast,
# Museumpark, Heemraadsplein...), so they are drawn. Until the owner picks a
# source - RET's own map (a download), OpenStreetMap's tags (a download), or
# this palette - they take the two candidates furthest from every other line
# and every pin: 14 brown #704214 (50.9 / 57.3), 18 grey #7f7f7f (40.2 / 53.1).
LINE_COLOURS = {**METRO_FEED_COLOURS, **TRAM_FEED_COLOURS,
                "1": "#3f5ebe", "11": "#293e7d", "14": "#704214", "18": "#7f7f7f"}

RET_SHAPES_ZIP = DATA_PROCESSED / "ret_rail_shapes.zip"
LINE_SHAPES_JSON = DATA_PROCESSED / "line_shapes.json"

# --- Business filtering ------------------------------------------------------

TAXONOMY_SYSTEM = "rotterdam_source"
RAW_CLASSIFICATION_COLUMN = "activity"

# A permit runs FIVE years (48 sampled notices, 2017-2026); coffeeshop
# permits one year. A premises is kept when an exploitation or provisional
# permit for it was published inside this window before the build date.
PERMIT_YEARS = 5
COFFEESHOP_YEARS = 1
# Points of one premises: notices for the same place land within a few metres
# (a renewal, a provisional-then-final pair). 3 m, from the brief's
# sensitivity (2,063 exact, 1,937 at 3 m, 1,904 at 5 m).
MERGE_M = 3.0
# A BAG shop unit this close to a kept permit premises is the same premises;
# the permit, which says what trades there, is kept. The notices carry no
# address, so this is the spatial form of Amsterdam's address rule - measured
# in step 2 before it is trusted.
DEDUP_M = 3.0

# BAG status is filtered at the WFS. A shop-class unit ALSO registered as a
# dwelling is left off - Amsterdam's owner call of 2026-09-24 (the likeliest to
# be a home, with nothing in open data to tell which), applied here the same.
BAG_EXCLUDE_IF_ALSO = ("woonfunctie",)
