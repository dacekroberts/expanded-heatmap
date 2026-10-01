"""Daugavpils-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py. The brief is docs/build_briefs/daugavpils.md.

THIRD LATVIAN CITY, Liepāja's shape: Riga's two layers through the shared
`pipeline/countries/latvia_register.py` -

  * FOOD SERVICE from VID's excise-licence register (Riga's national cache),
    placed on VZD's national address file `aw_eka.csv`;
  * SHOPS AND SERVICES from VZD's cadastre premise groups of use class 1230
    in ATVK 0002000, placed at the building's footprint.

The classification is Riga's, imported from `pipeline/riga/config.py`.

Rail: Daugavpils Satiksme's trams, routes 1-5, from OpenStreetMap through the
shared `pipeline/osm_tram.py` (the city's GTFS declares no licence; brief).
ALL FIVE ROUTES ARE DRAWN (owner, 2026-09-30, overruling call 28), with each
route's wait stated on the page.
"""

from pathlib import Path

from pipeline.riga.config import (  # noqa: F401 - the country's rules, decided in Riga
    CADASTRE_NS,
    CRS_SOURCE_LV,
    EXCISE_COLUMNS,
    EXCISE_CURRENT,
    EXCISE_NEVER,
    FOOD_RE,
    NAME_KEEP,
    NAME_KIND,
    NAME_RULES,
    TRADE_USE_KIND,
    UNIT_SUFFIX_RE,
)

SLUG = "daugavpils"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "daugavpils" / "raw"
DATA_PROCESSED = ROOT / "data" / "daugavpils" / "processed"
OUTPUTS = ROOT / "outputs" / "daugavpils"
# The national excise register and premise groups, as Riga fetched them.
NATIONAL_RAW = ROOT / "data" / "riga" / "raw"
NATIONAL_PROVENANCE = ROOT / "outputs" / "riga" / "provenance.json"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_CITY_JSON = DATA_RAW / "osm_city.json"
EXCISE_CSV = NATIONAL_RAW / "pdb_akclicences_odata.csv"
PREMISEGROUP_ZIP = NATIONAL_RAW / "premisegroup.zip"
ATVK = "0002000"
KK_ZIP = DATA_RAW / f"{ATVK}_kk_shp.zip"
AW_EKA_CSV = DATA_RAW / "aw_eka.csv"

CKAN_API = "https://data.gov.lv/dati/api/3/action/"
CADASTRAL_MAP_DATASET = "b28f0eed-73b0-4e44-94e7-b04b11bf0b69"
ADDRESS_REGISTER_DATASET = "varis-atvertie-dati"

# --- Scope: the city of Daugavpils ---------------------------------------------
# ATVK 0002000; OSM relation 13048683, 72 km2 (brief).
CITY_NAME_LV = "Daugavpils"
OSM_CITY_RELATION = 13048683
CITY_AREA_KM2 = (66.0, 78.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 35N: Daugavpils's longitude (~26.5) falls in the 24 to 30 band, as
# Riga's does. Derived per city.
CRS_PROJECTED = "EPSG:32635"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the brief's 298 m median gap over all 38 stops (approved with the
# tram kit's calls, 2026-09-30). Step 1 prints the median again.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (240.0, 360.0)
# 38. The brief's 38 counted "Lokomotīvju demo", one direction's misspelling of
# Lokomotīvju depo, as a stop of its own (aliased below; read 2026-09-30), which
# left 37; Užvaldes iela, a stop OSM does not map, is placed on OSM's track
# (TRACK_STOPS below, 2026-10-01), which makes 38.
EXPECTED_STATIONS = 38

# --- Station scope: EVERY STOP OF ROUTES 1-5 -----------------------------------
# Nine route=tram relations, refs 1-4, all kept (read 2026-09-30):
#   1  1708349, 1708350           Butļerova iela - Stacija
#   2  1707560, 1707561           Butļerova iela - Maizes kombināts
#   3  1707562, 1707563           Cietoksnis - Stropu ezers (route 3)
#   3  17096731                   the loop Cietoksnis - Stropu ezers - Ķīmija -
#                                 Cietoksnis, which the operator's own page
#                                 linked from it calls route 5; OSM tags it 3
#   4  15057095, 15057096         Stacija - Maizes kombināts
# Ref 3's stops are the union of its three relations (route 3 adds Balvu iela
# and Stropu ciemats); its track lies almost wholly on the loop (0.07-0.09 km
# off it), so drawing the loop - the relation with the most geometry - draws
# both routes.
ROUTE = "tram"
# NO operator whitelist: the relations say "Daugavpils Satiksme AS" and, on
# route 2, "Daugavpils Satiksme SIA" - one operator, two spellings - and every
# tram relation in the box is one of these nine.
OPERATOR = None
LINE_REFS = ("1", "2", "3", "4")
NOT_DRAWN = {}
STATION_ADD = {}
# Stropu ciemats is a stop member of both route-3 relations, tagged only
# highway=bus_stop + public_transport=platform + tram=yes - accepted by node.
ACCEPT_MEMBERS = {10293447147: "Stropu ciemats"}
# One stop spelled two ways: route 2 and route 4 each have one direction's
# member named "Lokomotīvju demo" (sic).
STATION_NAME_ALIASES = {"Lokomotīvju demo": "Lokomotīvju depo"}
# A STOP OSM DOES NOT MAP: Užvaldes iela, which Daugavpils satiksme SIA's
# published tram timetable lists on routes 2 and 4, both directions, between
# A. Pumpura iela and Lokomotīvju depo (the name and the line membership are
# the operator's published facts). OSM has no stop or platform there under any
# name (live probe 2026-10-01). The position is OSM's own: the vertex of the
# single-track way 38785621 (on all four route-2 and route-4 relations) that is
# node 1307786297, the railway=tram_level_crossing where OSM's Užvaldes iela
# (ways 107423184, 1014388819) crosses the track - one point for both
# directions, on the drawn track. New Orleans's South Carrollton at Sycamore
# precedent (2026-10-01). The operator's GTFS (data/daugavpils/raw/GTFS.zip)
# declares no licence and has no licence row, so it is NOT used for anything
# here - not the position, not the name. {name: (lines, ((way, lat, lon), ...),
# source)}. Step 1 stops if the vertex leaves that way or the way leaves a
# listed line's relations, or if OSM maps a stop within 60 m (then it becomes a
# STATION_ADD and this entry goes).
TRACK_STOPS = {
    "Užvaldes iela": (("2", "4"), ((38785621, 55.8890735, 26.5339858),),
                      "operator's published timetable (name, routes 2 and 4); "
                      "OSM track vertex, node 1307786297 (position)"),
}

# Gate 3 (tram-city skill, section 2): the operator's own stops per route, read
# for the count only, distinct stops over both directions of each regular
# pattern. Ref 3 is routes 3 and 5, one loop run each way: 29 stops each, the
# same 29. The operator names two stops differently from OSM - "Latvijas
# maiznieks" (OSM's Maizes kombināts, the terminus) and "Kultūras pils" (OSM's
# Kultūras un sporta pils) - which changes no count.
OPERATOR_STATION_COUNTS = {
    "1": 19,
    # 17 with Užvaldes iela (TRACK_STOPS); OSM's relations alone give 16.
    # Re-probed live 2026-10-01 (Overpass, every public_transport, railway and
    # highway=bus_stop node within 250 m, and anything named like "vald" within
    # 400 m; the kumi mirror, data to 2026-07-24, as overpass-api.de 504'd): OSM
    # has NO stop or platform there - only node 1307786297, the
    # railway=tram_level_crossing where Užvaldes iela crosses the track, which
    # TRACK_STOPS uses as the position.
    "2": 17,
    "3": 29,
    "4": 17,   # as route 2: 17 with Užvaldes iela, 16 from OSM's relations alone
}
OPERATOR_COUNTS_SOURCE = (
    "Daugavpils satiksme SIA's published tram timetable "
    "(satiksme.daugavpils.lv/transports/tramvaju-saraksts), as the GTFS it publishes "
    "lists it (feed_publisher 'Daugavpilssatiksme SIA', feed_version 01.09.2026, "
    "valid 2026-04-30 to 2027-04-30; the cached data/daugavpils/raw/GTFS.zip, which "
    "the build does not use): route 1 19 stops each way; route 2 17; route 4 17; "
    "routes 3 and 5 29 each, one set. Read 2026-10-01; primary.")

SPACING_MIN_M = 200.0

DRAWN_LINES = ("1", "2", "3", "4")
# Ref 3 is one loop, Cietoksnis - Stropu ezers - Ķīmija, which Daugavpils
# Satiksme runs as route 3 one way and route 5 the other; OSM tags both 3.
LINE_NAMES = {"1": "Tram 1", "2": "Tram 2", "3": "Trams 3 and 5", "4": "Tram 4"}
# OSM records no colour on any relation (brief): this project's own palette.
# Three from Riga's; trams 3 and 5 take deep purple, since Riga's cyan scored
# 40.9 against Personal services, under the preferred 45. CIE76 nearest pin
# (2026-09-30): 1 72.2, 2 45.2, 3 47.1, 4 84.4; the closest pair of lines is
# 2 and 4 at 50+.
LINE_COLOURS = {"1": "#ff7f0e", "2": "#8c564b", "3": "#4a148c", "4": "#e6ac00"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "riga_source"
RAW_CLASSIFICATION_COLUMN = "activity"

DAUGAVPILS_BBOX = {"lat_min": 55.80, "lat_max": 55.98, "lon_min": 26.40, "lon_max": 26.66}
