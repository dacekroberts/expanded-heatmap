"""Stockholm-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/stockholm.md) and London's OSM-rail build.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "stockholm" / "raw"
DATA_PROCESSED = ROOT / "data" / "stockholm" / "processed"
OUTPUTS = ROOT / "outputs" / "stockholm"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# Raw inputs, all keyless, downloaded by fetch_sources.py (never by a step).
#
# The register: Stockholms stad's food inspection layer (miljöförvaltningen,
# from Ecos 2), an ArcGIS FeatureServer. ONE ROW PER INSPECTION, not per
# premises: 289,742 rows for 8,146 premises (ObjektId). FROZEN: no inspection
# after 2025-10-21, layer last edited 2025-10-22; built on as it stands
# (owner, 2026-09-28). Every field is fetched (owner, 2026-09-28); none names
# a person (the register names premises, AnlaggningsNamn).
REGISTER_LAYER_URL = ("https://services-eu1.arcgis.com/81H0sgjoIWj6WxIM/arcgis/rest/services/"
                      "Livsmedelstillsyn/FeatureServer/41")
REGISTER_PAGE_SIZE = 2000   # the layer's maxRecordCount
REGISTER_CSV = DATA_RAW / "livsmedelstillsyn.csv"
# The fields the fetch expects, in the layer's order; a field added or dropped
# upstream stops the fetch rather than changing what is stored.
REGISTER_FIELDS = ("OBJECTID", "ObjektId", "AnlaggningsNamn", "Fastighet", "Adress",
                   "AnlaggningsTyp", "GeoPositionNorr", "GeoPositionOst", "Riskklass",
                   "VerksamhetsTyp", "Kontrollorsak", "Typ", "Kontrollomrade", "Nr",
                   "Beskrivning", "Anmarkning", "TillsynsDatum", "TillsynsDatumTid", "GlobalID")
# GeoPositionNorr / GeoPositionOst are SWEREF 99 18 00, the register's own
# position; step 2 checks them against the served point geometry.
REGISTER_POSITION_CRS = "EPSG:3011"
# The licence position rests on the publisher's own Hub feed (SILENT, with
# the pages named): docs/data_sources/sweden.md.
PUBLISHER_DCAT_URL = "https://open-data-sthlm-miljo.hub.arcgis.com/api/feed/dcat-us/1.1.json"

# Rail (owner, 2026-09-28): the Tunnelbana only - seven routes, 10-19.
# Pendeltåg, Roslagsbanan, Saltsjöbanan and the trams are left out. SL
# publishes GTFS only behind a Trafiklab key, so track and stations are
# OpenStreetMap's route relations (osm-rail), all subway relations in the bbox;
# step 1 assigns each by ref and stops on a ref no line claims.
OSM_BBOX = "59.22,17.75,59.45,18.20"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:180];("
    f'rel["type"="route"]["route"="subway"]({OSM_BBOX});'
    ");out geom;")
OSM_ROUTES_JSON = DATA_RAW / "osm_rail_routes.json"
# The relations' STOP members of every role (Glasgow's Govan lesson) AND their
# PLATFORM members, with a centre: some stations are carried only as a
# platform (line 14's Västertorp, 2026-09-29). Step 1 stops if any member is
# missing - the first fetch came from a mirror older than the relations and
# lacked eleven stations' stop nodes.
OSM_STOPS_QUERY = OSM_ROUTES_QUERY.replace(
    ");out geom;",
    ')->.r;(node(r.r:"stop");node(r.r:"stop_entry_only");node(r.r:"stop_exit_only");'
    'node(r.r:"platform");node(r.r:"platform_entry_only");node(r.r:"platform_exit_only");'
    'way(r.r:"platform");way(r.r:"platform_entry_only");way(r.r:"platform_exit_only");'
    'rel(r.r:"platform"););out center;')
OSM_STOPS_JSON = DATA_RAW / "osm_rail_stops.json"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
# "Gul linje till Älvsjö" (relation 21104772, no ref, #f5c700): the Yellow
# line, under construction, not in service. Skipped by id; step 1 says so if
# it disappears.
RELATIONS_SKIPPED = {21104772: "Gul linje - under construction, not in service"}
BRANCH_NEAR_M = 300
BRANCH_MIN_NEW_M = 1000
STATION_CLUSTER_M = 400

CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# Stockholms kommun, OSM relation 398021 - NOT name=Stockholm, which matches
# nothing at admin_level 7 and two US townships when widened (the brief).
# Polygonised from its outer ways and gated on its area.
BOUNDARY_OSM_RELATION = 398021
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_stockholms_kommun.json"
# 215.8 km2 in UTM 34N on 2026-09-29 (water included).
BOUNDARY_AREA_KM2 = (210, 222)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 34N: the longitude (~18.07) falls in the 18 to 24 band - just east
# of 18, so not 33N. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32634"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# Three lines, seven routes (SL's own shape): each line is drawn and labelled
# once, its routes named in the legend - Melbourne's treatment, since a
# line's routes share one track and one colour through the centre. OSM
# colours the relations by line, as words (blue, red, green).
LINE_OSM_REFS = {"Gröna linjen": ("17", "18", "19"),
                 "Röda linjen": ("13", "14"),
                 "Blå linjen": ("10", "11")}
# On-map label: the line's Swedish name, as SL signs it; the legend names its
# routes. Hues: OSM tags the relations with colour WORDS, taken as the CSS
# colours of those names; the drawn colour is scripts/line_colour_search.py's
# nearest feasible one (LINE_COLOURS).
LINES = {"Gröna linjen": {"hue": "#008000"}, "Röda linjen": {"hue": "#FF0000"},
         "Blå linjen": {"hue": "#0000FF"}}
LINE_ORDER = list(LINES)
LINE_NAMES = {k: k for k in LINES}
# The legend row reads "<label> <this>" (build_legend), so only the routes.
LEGEND_NAMES = {"Gröna linjen": "(T17, T18, T19)",
                "Röda linjen": "(T13, T14)",
                "Blå linjen": "(T10, T11)"}
# `python scripts/line_colour_search.py stockholm`, run 2026-09-29: every line
# >= 45.4 from every pin, the closest pair 133.3, three distinct dark-mode
# labels. The Food shops pins' blue takes the Blue line's, which reads violet
# here (London's Piccadilly precedent).
LINE_COLOURS = {"Gröna linjen": "#40A800", "Röda linjen": "#F80000", "Blå linjen": "#8018F8"}
STATION_NAME_ALIASES = {}
# A station OSM's relations do not carry, found by gate 3 (2026-09-29):
# Hallonbergen on route 11, in Sundbyberg - outside the kommun, so it is
# recorded as excluded, never drawn. Placed at its OSM station node; step 1
# STOPS once a relation carries it.
STATION_ADDITIONS = {"Hallonbergen": "11"}
OSM_ADDITIONS_QUERY = (
    '[out:json][timeout:90];node["railway"="station"]["name"~"^('
    + "|".join(STATION_ADDITIONS) + f')$"]({OSM_BBOX});out body;')
OSM_ADDITIONS_JSON = DATA_RAW / "osm_station_additions.json"
# A platform member named only by its track ("track 3") names no station.
UNNAMED_PLATFORM = r"(?i)^(track|spår|plattform|platform)\s*\d+$"
# GATE 3 - per ROUTE and the whole network, against English Wikipedia's
# Stockholm Metro table of lines, read 2026-09-29 (a SECONDARY source,
# Prague's precedent). Routes 17 and 18 are left out of the per-route gate:
# the table gives their daytime runs (to Åkeshov, 24; to Alvik, 23) while
# OSM's relations run on to Hässelby strand, route 19's stations; the network
# count covers them.
OPERATOR_STATION_COUNTS = {"10": 14, "11": 12, "13": 25, "14": 19, "19": 35,
                           "Tunnelbana (network)": 100}
OPERATOR_COUNTS_SOURCE = ("en.wikipedia: Stockholm Metro, table of lines (10: 14, 11: 12, 13: 25, "
                          "14: 19, 17: 24, 18: 23, 19: 35; network 100) - secondary, read 2026-09-29")
# The NAMING layer (not the scoping one): the kommuner around Stockholm, so
# each excluded station is recorded with the kommun it lies in (Oslo's Bærum
# layer, Paris's communes). Every admin_level 7 relation touching the rail
# bbox, polygonised by fetch_sources.py.
KOMMUNER_QUERY = (f'[out:json][timeout:180];rel["boundary"="administrative"]["admin_level"="7"]'
                  f'({OSM_BBOX});out geom;')
KOMMUNER_OSM_CACHE = DATA_RAW / "osm_kommuner.json"
KOMMUNER_GEOJSON = DATA_RAW / "kommuner.geojson"

# --- Business filtering ------------------------------------------------

# In-city rows: the register is Stockholms stad's own; the polygon then drops
# any point outside the kommun.
CITY_KEEP = "Stockholms kommun"

TAXONOMY_SYSTEM = "sweden_livsmedel"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "VerksamhetsTyp"

# Untyped premises classified from their name go on only if last inspected in
# these years (owner, 2026-09-28): older ones are likely closed.
NAME_CLASSIFIED_YEARS = ("2022", "2023")

# Sanity bounds: Stockholms kommun's polygon extent (59.2273-59.4403 N,
# 17.7607-18.2001 E, measured 2026-09-29) plus ~0.02 deg. The polygon does
# the filtering; this catches a CRS or axis error.
STOCKHOLM_BBOX = {
    "lat_min": 59.21,
    "lat_max": 59.46,
    "lon_min": 17.74,
    "lon_max": 18.22,
}
