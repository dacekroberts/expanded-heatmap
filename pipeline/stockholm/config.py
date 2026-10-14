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

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600398021)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("sv",)
PLACE_FOLD = None
# Rows a reader held that the owner ruled to keep (2026-10-13;
# docs/decisions_drafts/search-final.md). A record only: no code reads it.
# A street is listed by name, a place by OSM id with its name. Not in
# PLACE_REVIEWED, which check E holds to names carrying a leak word.
PLACE_RULED_KEPT = {
    # Held rows kept by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    # A home, family or person row is listed by id alone.
    "way/420005727": "'Koloniträdgård', kept on an article of the object's own (keep beats drop, owner 2026-10-13 #1); Skansen's contents stay only with a Wikipedia article: the 8 kept (15 answers #4)",
    "node/3200805766": "'Avrättningsplats', kept on an article of the object's own (keep beats drop, owner 2026-10-13 #1)",
    "way/154616186": "'Fontändamm', kept on an article of the object's own (keep beats drop, owner 2026-10-13 #1)",
    "way/208187273": "'Blåklockan', a park named for a city block is kept (owner, 2026-10-13)",
    "way/304275102": "'Blåkråkan', a park named for a city block is kept (owner, 2026-10-13)",
    "way/480894598": "'Dellen', a park named for a city block is kept (owner, 2026-10-13)",
    "way/409283552": "'Hagelbössan', a park named for a city block is kept (owner, 2026-10-13)",
    "way/41985612": "'Solvändan', a park named for a city block is kept (owner, 2026-10-13)",
    "way/255446767": "'Träsket', a park named for a city block is kept (owner, 2026-10-13)",
    "way/116418157": "'Häradsdomaren', a park named for a city block is kept (owner, 2026-10-13)",
    "way/116631981": "'Aspvirket', a park named for a city block is kept (owner, 2026-10-13)",
    "way/322112164": "'Murlindan', a park named for a city block is kept (owner, 2026-10-13)",
    "way/983874377": "'Repslagargården', a named square is a landmark row; Swedish -garden is a ruled ending (language call 2)",
    "way/741743697": "'Bredsätra lekplats- och parkområde', parks need no article; a place name beside a type phrase is the park's name",
    "way/54237497": "'Chapmansgården', a park tied to a housing complex only by its name stays (second batch question g); only an estate operator tag drops one (third list rule 3)",
    "way/54237501": "'Jaktvarvsgården', a park tied to a housing complex only by its name stays (second batch question g); only an estate operator tag drops one (third list rule 3)",
    "way/54237498": "'Pontonjärgården', a park tied to a housing complex only by its name stays (second batch question g); only an estate operator tag drops one (third list rule 3)",
    "way/54237496": "'Rinmansgården', a park tied to a housing complex only by its name stays (second batch question g); only an estate operator tag drops one (third list rule 3)",
    "way/28976758": "'Fågelbärsgården', a park tied to a housing complex only by its name stays (second batch question g); only an estate operator tag drops one (third list rule 3)",
    "node/4868147701": "'Frihamspiren', a misspelled or glitched name is still that place (seven rulings #1; typo line, 2026-10-13)",
    "node/936059771": "'Astrid Lindgrens Berg', statues, monuments and public memorials stay without an article (personal names ruling #2, 2026-10-13; monuments not held to the notable rule)",
    "node/2242928761": "'Frihetens Port', kept on an article of the object's own (keep beats drop, owner 2026-10-13 #1); statues, monuments and public memorials stay without an article (personal names ruling #2, 2026-10-13; monuments not held to the notable rule)",
    "node/29835352": "'Mäster Palm', statues, monuments and public memorials stay without an article (personal names ruling #2, 2026-10-13; monuments not held to the notable rule)",
    "node/4318365079": "'Pontonjärbataljonen', statues, monuments and public memorials stay without an article (personal names ruling #2, 2026-10-13; monuments not held to the notable rule)",
    "node/5482219701": "'Svea Livgardesstenen', statues, monuments and public memorials stay without an article (personal names ruling #2, 2026-10-13; monuments not held to the notable rule)",
    "node/13625140161": "'The Frescati obelisk', statues, monuments and public memorials stay without an article (personal names ruling #2, 2026-10-13; monuments not held to the notable rule)",
    "node/783800851": "'Vegamonumentet', statues, monuments and public memorials stay without an article (personal names ruling #2, 2026-10-13; monuments not held to the notable rule)",
    "node/4786195249": "'fd Snösätra torp', a 'former' or 'site of' word in a name is not read as gone; lifecycle is read from tags, narrowly (third list 11, narrow version); kept on an article of the object's own (keep beats drop, owner 2026-10-13 #1)",
    "way/542372697": "'Skarpnäcks Skatepark', parks need no article; candidate 15 names pools, clubs and offices only",
    "way/492642127": "'Järva discgolfpark', parks need no article; candidate 15 names pools, clubs and offices only",
    "node/1547924149": "'Delsbogården', Skansen's contents stay only with a Wikipedia article: the 8 kept (15 answers #4)",
    "node/1548045603": "'Finngården', Skansen's contents stay only with a Wikipedia article: the 8 kept (15 answers #4)",
    "way/141433538": "'Mekaniska Verkstaden', Skansen's contents stay only with a Wikipedia article: the 8 kept (15 answers #4)",
    "node/1547924215": "'Moragården', Skansen's contents stay only with a Wikipedia article: the 8 kept (15 answers #4)",
    "node/1548045731": "'Oktorpsgården', Skansen's contents stay only with a Wikipedia article: the 8 kept (15 answers #4)",
    "way/33407223": "'Seglora kyrka', Skansen's contents stay only with a Wikipedia article: the 8 kept (15 answers #4)",
    "node/1588253628": "'Älvrosgården', Skansen's contents stay only with a Wikipedia article: the 8 kept (15 answers #4)",
    "way/23620152": "'Ölands-Kvarnar', Skansen's contents stay only with a Wikipedia article: the 8 kept (15 answers #4)",
    "node/465490000": "'Solbergaskogen', peaks need no article (NOTABLE_ONLY comment); no rule reads who uses a name",
    "way/721248066": "'Fornborg Spånga 58:1', a registered code is a name where the object carries wikidata, wikipedia, heritage or ref:nrhp (owner 2026-10-12)",
    "Norra brobänken": "a minor way keeps its row on an article of its own (2026-10-07); kept on an article of the object's own (keep beats drop, owner 2026-10-13 #1)",
    "Västra brobänken": "a minor way keeps its row on an article of its own (2026-10-07); kept on an article of the object's own (keep beats drop, owner 2026-10-13 #1)",
    "Östra brobänken": "a minor way keeps its row on an article of its own (2026-10-07); kept on an article of the object's own (keep beats drop, owner 2026-10-13 #1)",
    "Kungsholms Strandstig": "a misspelled or glitched name is still that place (seven rulings #1; typo line, 2026-10-13)",
    "Karl XII:s Torg": "a misspelled or glitched name is still that place (seven rulings #1; typo line, 2026-10-13)",
    "G.a Hagsätravägen": "a misspelled or glitched name is still that place (seven rulings #1; typo line, 2026-10-13)",
    "Akutvägen": "a site's or utility's road with a street word is kept (15 answers #9; six answers #4)",
    "Patientvägen": "a site's or utility's road with a street word is kept (15 answers #9; six answers #4)",
    "Vårdvägen": "a site's or utility's road with a street word is kept (15 answers #9; six answers #4)",
    "Vårdstigen": "a site's or utility's road with a street word is kept (15 answers #9; six answers #4)",
    "Friskvårdsvägen": "a site's or utility's road with a street word is kept (15 answers #9; six answers #4)",
    "Sopvägen": "a site's or utility's road with a street word is kept (15 answers #9; six answers #4)",
    "Kioskvägen": "a site's or utility's road with a street word is kept (15 answers #9; six answers #4)",
    "Parkeringsbacken": "a site's or utility's road with a street word is kept (15 answers #9; six answers #4)",
    "Terminalslingan": "a site's or utility's road with a street word is kept (15 answers #9; six answers #4)",
    "Inre Bassängkajen": "a site's or utility's road with a street word is kept (15 answers #9; six answers #4)",
    "Norra Bassängkajen": "a site's or utility's road with a street word is kept (15 answers #9; six answers #4)",
    "Albanotunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Bagartunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Björktunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Bronstunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Galaxtunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Guldtunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Karolinertunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Komettunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Koppartunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Murartunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Målartunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Måntunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Planettunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Roslagstunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Silvertunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Skeppartunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Skräddartunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Soltunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Sotartunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Stallmästartunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Stjärntunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Sågtunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Talltunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Tranebergsslingan": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a); Zurich's five named city ramps stay (six answers #5, 2026-10-13)",
    "Tångtunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Yxtunneln": "named tunnels stay as street rows, as bridges (15 answers #11, Stockholm 27; second batch question a)",
    "Vardagslivets gång": "Swedish -gang is a ruled way ending (language call 6); a path under a name of its own stays",
}
PLACE_REVIEWED = {}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    # Rows the owner's later rulings of 2026-10-13 decide, and the twin checks' drops (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "way/181153125": "a place of worship named only by a denomination, a body or a chain, with no place or dedication in the name and no branch tag, is dropped (four rulings 1; ruling 2; owner 2026-10-13, relayed by Cleanup)",
    "way/42067241": "a place of worship named only by a denomination, a body or a chain, with no place or dedication in the name and no branch tag, is dropped (four rulings 1; ruling 2; owner 2026-10-13, relayed by Cleanup)",
    "node/459389822": "duplicate: a place node on the Wikidata entry of the island's own landmark row, which stays (owner 2026-10-13, relayed by Cleanup)",
    "node/470618034": "duplicate: a place node on the Wikidata entry of the island's own landmark row, which stays (owner 2026-10-13, relayed by Cleanup)",
    "node/470618434": "duplicate: a place node on the Wikidata entry of the island's own landmark row, which stays (owner 2026-10-13, relayed by Cleanup)",
    "node/443304029": "duplicate: a place node on the Wikidata entry of the island's own landmark row, which stays (owner 2026-10-13, relayed by Cleanup)",
    "node/1551361779": "a same-named object beside a row dropped by id, which that drop made the row: dropped with it under the same ruling (finding 53; the twin check; owner 2026-10-13, relayed by Cleanup)",
    # Rows the read-only screen helper gave a drop verdict (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "node/6940314211": "religious body's meeting hall: ruling 2 (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/749348757": "bare type-word park: bare type-word parks (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    # A second row for one object within 300 m (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "relation/2705872": "duplicates of one object are one row: a place row on the landmark of its name (owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "node/2988661746": "a ride inside an amusement park (owner, 2026-10-13)",
    "node/2988582415": "a ride inside an amusement park (owner, 2026-10-13)",
    "node/2988582414": "a ride inside an amusement park (owner, 2026-10-13)",
    "node/2988661755": "a ride inside an amusement park (owner, 2026-10-13)",
    "node/1588236196": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "node/1588236198": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "node/6191623912": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "node/1548045769": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "node/6192023568": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "node/1548045560": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "node/1547974379": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "node/6192314773": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "node/1548045556": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "way/33485731": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "way/141433537": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "way/33487812": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "node/1548045722": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "node/1548045577": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "node/6192303779": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "way/145404334": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "way/666416577": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "way/141433541": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "way/48399121": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "way/151113215": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "way/662370988": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "node/6191512981": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "way/34344428": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/34344429": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/28263429": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24324795": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/6108470": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/624109356": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24324793": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/291464554": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27349059": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/41987868": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23997020": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/422189275": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/73306211": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/76447375": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27252384": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/804442617": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23575686": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/262515032": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/262515041": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/28600746": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/300183418": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/31105185": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/31097193": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/31097195": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/31097196": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/31097197": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/4215416": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/4969059": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/4812454": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/4880205": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23271381": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/457660003": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/978179556": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/191470085": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/42258786": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/262515033": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/8117109": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23523475": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1525239732": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1525239735": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24396104": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24396114": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/619556620": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/681394650": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23841487": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/4726607": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/5200669": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/888976672": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/193811129": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/616114961": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/623906434": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/623906435": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1126757834": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/4695823": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/155580372": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/279476970": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/315196051": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/624726396": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/5200666": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/816615788": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/913690544": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/195027210": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/624726381": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/624726382": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/659397817": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/269884254": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/269884256": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/269884265": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/616096876": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/624726399": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/772226592": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/917202178": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/252863766": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/88293606": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/88293603": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/10560808": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/10560848": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/87481572": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/87481576": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/137842944": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/224502630": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/224502631": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/977568969": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/977568970": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/977568971": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/137842943": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/224502627": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/14872645": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24991054": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/451565960": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/451565961": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/458916882": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/458916883": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/458916884": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27591123": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/28082635": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/28082636": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24017942": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1158774738": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/116771484": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1339082214": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/116771485": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/186602025": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/262515034": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/40009150": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/114388558": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/204505200": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/38780854": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/40469213": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23125190": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/146655058": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/195956261": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/636606926": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/636606927": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/195956262": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/195987306": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/258838601": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/636606928": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/34353713": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/127674501": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/20278907": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/777573843": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/8021591": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/269310411": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/269310429": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/312736021": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/436900044": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/664546473": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/688039069": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/269310418": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/369017966": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/11922042": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/37290707": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/119679931": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/119679932": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/121494944": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1339601555": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24394075": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24394081": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/56065985": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/681394648": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/8021521": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/299985137": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/299985142": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/31099178": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/31105171": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/123457682": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/380104542": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23841496": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/146651475": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/304503854": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/977427735": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/267212330": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1127370511": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27343726": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27423365": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/5173754": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23317358": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/25200456": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/304783229": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/304503131": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/40560404": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/636586768": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/636586769": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/239176543": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1374228749": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1389906760": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1389906765": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1389906767": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1389906768": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1389906771": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1390075437": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/158573182": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/806177115": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/244924026": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/279545763": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/806177120": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/136608803": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/205884052": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/237156616": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/39068318": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/39068320": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/39068322": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/52090430": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/538599719": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/87407843": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/87407845": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/111657493": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/52089318": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/14878847": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/14878879": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1271392980": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1271392981": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23161297": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23161298": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/88774566": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1126759016": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/139548961": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23161283": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23161284": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/610512321": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/6107578": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1409723342": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24324810": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/6107629": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/636606918": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1359674748": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23427038": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/254115696": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/4876161": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/816615792": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/34964420": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/34964424": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/151885006": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/34964160": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/82483335": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23710091": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/4802622": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1341785421": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1080361225": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/115374419": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23304829": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23781926": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/262515038": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/262515039": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/115374418": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/136135918": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23304805": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23571329": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23594563": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/262515040": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/58107573": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/92840546": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/367618421": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/444657795": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/658141142": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/684962399": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/805544002": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/805544003": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/290877192": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/19877844": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/369017964": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/369017967": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/688039071": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/31115010": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/447867492": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27252449": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/37835153": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/446728692": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27252477": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/37835154": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/10371335": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/123457680": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/123457689": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/623904456": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/803873932": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/803873933": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/803873934": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23807800": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/35473144": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/10595116": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/306545409": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/146651484": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/267229252": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/146651457": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/109219492": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/121547391": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/46100890": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23317355": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/37080810": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/610512331": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/238899925": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/254297493": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/254297495": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/304503132": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/239176544": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/255977264": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/255977265": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1080535036": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/137842945": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/8021537": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/803873924": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/135379356": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/234169241": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/636586814": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/140154595": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/636586815": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/5173679": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/20278946": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/34231303": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23841890": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23841894": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/146651458": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/109566080": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/154324247": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/10595107": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/258937466": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/49772360": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/803873942": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/803873943": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/22822468": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/450081187": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/22823490": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23984989": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23984993": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24395193": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/681394649": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/14878298": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/14878357": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/87481571": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/87481575": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/22822707": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/22822698": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/77238733": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/135379350": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/385121142": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/636586811": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/135379357": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/135379359": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/140154600": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/636586812": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/191918675": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/192085246": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/20278421": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/34387764": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23841789": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23841884": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/146651482": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/636586773": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/977427739": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1178443052": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1178443053": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1178443054": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/186257294": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/8116874": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1178443060": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1178443061": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/8116889": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/979328278": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/23125140": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/458964191": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/458964192": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/795989414": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/22822549": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/475702094": "a description standing in for a name: a yard with a playground",
    "way/557788484": "a description standing in for a name, in English",
    "way/749348756": "a description standing in for a name: a stand of cherry trees",
    "node/13927039922": "a glitched name (typo) on a dog exercise yard tagged a park",
    "way/24396033": "a name that says the thing is gone: a former ice rink",
    "way/222138753": "a name that says the thing is gone: a former school hall",
    "node/2351153347": "a vanished station site; its own description says it is gone",
    "node/10311221771": "a description standing in for a name: a Bronze Age cairn",
    "node/5875531808": "a description standing in for a name, in English",
    "node/6237921405": "a description with a typo standing in for a name: a moved milestone, museum contents",
    "node/13423826196": "a description with English glued on: a telephone booth",
    "node/8238115542": "a plaque with no Wikipedia article of its own",
    "node/12136207934": "a description standing in for a name: a displayed spire, no article",
    "node/4706569034": "a farmhouse ruin with no article",
    "way/38692398": "a farmhouse ruin with no article",
    "way/663093965": "a description standing in for a name: a planting bed inside an open-air museum",
    "node/6207729492": "a description standing in for a name: a planting bed inside an open-air museum",
    "node/4581111990": "a duplicate row of the gallery 80 m away, with a wikidata tag that is not its own",
    "node/377903470": "a duplicate row: a second label node of the same bay",
    "node/1072754846": "a duplicate row: a label node of a waterway that has its own row",
    "node/1262177568": "a duplicate row: a label node of a waterway that has its own row",
    "relation/9193109": "a duplicate row: the district's boundary beside its place node",
    "node/9050718625": "a duplicate row: a second stop position of the same tram stop",
    "way/284898675": "a glitched name (typo) on a motorway interchange description",
    "way/1296951722": "an inner courtyard under its type word",
    "way/439570805": "footpaths inside a garden; the garden's own landmark row stays",
    "way/47361938": "footpaths inside a garden; the garden's own landmark row stays",
    "way/145296861": "a description: bridle path",
    "way/145296867": "a description: bridle path",
    "way/99093308": "a description: small path",
    "way/34003388": "a description: footbridge",
    "way/957525119": "a description: footbridge",
    "way/206418941": "an indoor shopping arcade",
    "way/1328596403": "walkways inside a shopping center; already dropped by the leak word",
    "way/41679286": "walkways inside a shopping center; already dropped by the leak word",
    "way/43327380": "walkways inside a shopping center; already dropped by the leak word",
    "way/748874120": "a station ticket hall, not a street",
    "way/825671668": "a description standing in for a name",
    "way/182668070": "a glitched name (underscore)",
    "way/182668071": "a glitched name (underscore)",
    "way/656252728": "a glitched name (underscore)",
    "way/656252729": "a glitched name (underscore)",
    "way/656252734": "a glitched name (underscore)",
    "way/345766023": "a glitched name (stray letters glued on)",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "way/733417530": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "way/20679943": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); campus lawns and courts go, by id (wave 1 lettered list, owner 2026-10-13; Goteborg campus yards, 15 answers #1); held rows settled 2026-10-13",
    "way/815832450": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/141425975": "museum contents with no Wikipedia article are dropped (15 answers #4); also a bare type word; held rows settled 2026-10-13",
    "way/141416382": "museum contents with no Wikipedia article are dropped (15 answers #4); also a bare type word; held rows settled 2026-10-13",
    "way/705991789": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/583885700": "campus lawns and courts go, by id (wave 1 lettered list, owner 2026-10-13; Goteborg campus yards, 15 answers #1); held rows settled 2026-10-13",
    "relation/16004116": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); a description standing in for a name is dropped (settled call of the reads; seven rulings #4; Ostia finds named by location, 15 answers #8); held rows settled 2026-10-13",
    "way/643215342": "a park tag on a pool, club, office or other non-park is a by-id drop (third list candidate 15, narrow version); held rows settled 2026-10-13",
    "way/205780045": "a housing or commercial development mapped as a place is dropped (four rulings #2, 2026-10-13); held rows settled 2026-10-13",
    "way/137825915": "a home is kept only when open to visit or with an article of its own (home rule, 2026-10-08, 2026-10-13); bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/137825911": "a home is kept only when open to visit or with an article of its own (home rule, 2026-10-08, 2026-10-13); bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/4837314321": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); a street's object is no landmark row where a street row bears its name (second batch rule 7); duplicates are one row; held rows settled 2026-10-13",
    "way/1245453269": "a park tag on a pool, club, office or other non-park is a by-id drop (third list candidate 15, narrow version); a business with nothing else is dropped; a place named for a business (LEAK rule, 2026-10-08); held rows settled 2026-10-13",
    "way/559464978": "a park tag on a pool, club, office or other non-park is a by-id drop (third list candidate 15, narrow version); held rows settled 2026-10-13",
    "way/981647942": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/468028209": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/468040078": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); an object admitted only by another object's entry or name is dropped (Gwangju read, settled call; SUBJECT_ENTRY_KEYS); held rows settled 2026-10-13",
    "node/492883288": "a code beside a type word is no name (CODED_TYPE, owner 2026-10-12; Ostia plot codes, 15 answers #8); held rows settled 2026-10-13",
    "node/9056228543": "the search must not land where the thing is not (owner 2026-10-13 #1); held rows settled 2026-10-13",
    "way/813423971": "a city block is no neighborhood (place values that are no neighborhood are skipped, 2026-10-08); held rows settled 2026-10-13",
    "way/8021611": "motorway ramps and interchange labels are dropped (14 answers #2; street_never); held rows settled 2026-10-13",
    "way/35312123": "motorway ramps and interchange labels are dropped (14 answers #2; street_never); held rows settled 2026-10-13",
}
