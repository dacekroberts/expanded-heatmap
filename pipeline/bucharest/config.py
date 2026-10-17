"""Bucharest-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/bucharest.md), Staging's measurements and London's
OSM-rail build.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "bucharest" / "raw"
DATA_PROCESSED = ROOT / "data" / "bucharest" / "processed"
OUTPUTS = ROOT / "outputs" / "bucharest"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- The register --------------------------------------------------------
#
# DSVSA București (the sanitary-veterinary and food safety directorate): one
# XLSX per unit category, each listing registered units "active and closed" -
# the rows below a row reading ANULATE are cancelled. No status column, no
# coordinates. The hosts sit behind a browser challenge, so THE OWNER FETCHES
# THE FILES in their own browser (the Band C memo's condition); nothing here
# downloads them, and a cookie is never replayed. Files dated 25.08.2026.
DSVSA_PAGE_ANIMAL = "https://bucuresti.dsvsa.ro/"
# file -> what it holds. The taxonomy buckets each file, and reads the
# category text for the exceptions (labs, kiosk carts, vending machines).
# The animal-origin list (in data/bucharest/raw/):
ANIMAL_FILES = {
    "01-CARMANGERIE.xlsx": "pork butcher",
    "02.-MACELARIE.xlsx": "butcher",
    "11-MAGAZIN-DE-DESFACERE-PESTE-PESCARIE.xlsx": "fishmonger",
    "16-MAGAZIN-DE-DESFACERE-A-MIERII-DE-ALBINE-SI-A-ALTOR-PRODUSE-APICOLE.xlsx": "honey shop",
    "19-UNITATE-DE-ALIMENTATIE-PUBLICA.xlsx": "restaurants, cafés, bars",
    "20-PIZZERIE.xlsx": "pizzeria",
    "23-COFETARIE-PATISERIE.xlsx": "confectioner and pastry shop",
    "25-MAGAZIN-ALIMENTAR.xlsx": "food shop",
    "26-HIPERMARKET-SUPERMARKET.xlsx": "supermarket and hypermarket",
}
# The non-animal-origin list (in data/bucharest/raw/non-animal/):
NON_ANIMAL_FILES = {
    "01.-FABRICAREA-PAINII.xlsx": "bakery",
    "02.-FABRICAREA-PRAJITURILOR-A-PRODUSELOR-PROASPETE-DE-PATISERIE.xlsx": "pastry shop",
    "03.-FABRICAREA-PAINII-FABRICAREA-PRAJITURILOR-A-PRODUSELOR-PROASPETE-DE-PATISERIE.xlsx":
        "bakery and pastry shop",
    "24.-FABRICAREA-INGHETATEI.xlsx": "ice-cream maker",
    "33.-COMERT-CU-AMANUNTUL-EXCLUSIV-SUPERMARKETURI-HIPERMARKETURI.xlsx": "retail (not supermarkets)",
    "34.-SUPERMARKET-HIPERMARKET.xlsx": "supermarket (empty)",
    "36.-BARURI.xlsx": "bars and cafés",
    "42.-UNITATI-DE-COMERCIALIZARE-A-PRODUSELOR-ALIMENTARE-DE-ORIGINE-NONANIMALA-CONGELATE-REFRIGERATE.xlsx":
        "frozen and chilled food counters",
}
# Left out by the owner (2026-09-28) and never fetched: canteens (21), pastry
# labs (22), catering (31), local producers (34), internet-only sales, mobile
# stalls, vending machines, warehouses, fairs, farm and processing units.
REGISTER_DATE = "2026-08-25"   # the date printed on every file

# --- Addresses -----------------------------------------------------------
#
# OSM address objects inside the municipality (relation 377733) with both
# addr:street and addr:housenumber - the JOIN target (address-join): ANCPI's
# national nomenclature has no reachable geospatial service. Fetched
# 2026-09-28 with the owner's OK (9,523,237 bytes); the query is recorded
# here so fetch_sources.py can reproduce it into a new dated file.
OSM_ADDRESSES_CSV = DATA_RAW / "osm_addresses_2026-09-28.csv"
OSM_ADDRESSES_QUERY = (
    '[out:csv(::type,::id,::lat,::lon,"addr:street","addr:housenumber","addr:postcode")][timeout:300];'
    'area(3600377733)->.a;nwr["addr:street"]["addr:housenumber"](area.a);out center;')

# The six sectors (admin_level 9), fetched to test each register row's own
# Sector against where its OSM address lies: Bucharest reuses street names
# across sectors, and Staging's sector-free key put 11.2% of its first-pass
# matches on an address with points more than 300 m apart (2026-09-29).
SECTORS_QUERY = ('[out:json][timeout:180];rel(377733);map_to_area->.a;'
                 'rel["boundary"="administrative"]["admin_level"="9"](area.a);out geom;')
SECTORS_OSM_CACHE = DATA_RAW / "osm_sectors.json"
SECTORS_GEOJSON = DATA_RAW / "sectors.geojson"
# One matched address is ONE place when its OSM points link hop to hop within
# ADDRESS_HOP_M and span no more than SITE_SPREAD_MAX_M (a shopping centre or
# an industrial site); otherwise it is two places and the row is left
# unplaced rather than guessed. Measured 2026-09-29: a plain 150 m spread
# test left 3,177 rows "ambiguous", of which 1,701 of the 2,655 read were one
# continuous site (Casa Presei, Bucur Obor).
ADDRESS_HOP_M = 150
SITE_SPREAD_MAX_M = 600
# An OSM address counts for a sector it lies in or within this distance of:
# boulevards are often the boundary, with numbers on both sides.
SECTOR_EDGE_M = 100

# --- Rail ----------------------------------------------------------------
#
# Metrorex M1-M5 from OpenStreetMap's route relations (osm-rail): no GTFS for
# the metro is published that this project can use.
OSM_BBOX = "44.33,25.95,44.55,26.25"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:180];("
    f'rel["type"="route"]["route"="subway"]({OSM_BBOX});'
    ");out geom;")
OSM_ROUTES_JSON = DATA_RAW / "osm_rail_routes.json"
# Stop AND named platform members (Stockholm's lesson), out center.
OSM_STOPS_QUERY = OSM_ROUTES_QUERY.replace(
    ");out geom;",
    ')->.r;(node(r.r:"stop");node(r.r:"stop_entry_only");node(r.r:"stop_exit_only");'
    'node(r.r:"platform");node(r.r:"platform_entry_only");node(r.r:"platform_exit_only");'
    'way(r.r:"platform");way(r.r:"platform_entry_only");way(r.r:"platform_exit_only");'
    'rel(r.r:"platform"););out center;')
OSM_STOPS_JSON = DATA_RAW / "osm_rail_stops.json"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
BRANCH_NEAR_M = 100
BRANCH_MIN_NEW_M = 300
# A kept station further than this from its own drawn line stops step 1.
STATION_OFF_LINE_MAX_M = 100
STATION_CLUSTER_M = 400
UNNAMED_PLATFORM = r"(?i)^(track|linia|peron|platform)\s*\d+$"
# OSM's one station name carrying its line; Metrorex signs it "Basarab 1".
# The numbered interchange pairs (Basarab 1/2, Dristor 1/2, Eroilor/Eroilor 2,
# Nicolae Grigorescu 1/2, Piața Unirii 1/2, Piața Victoriei 1/2, Gara de Nord
# 1/2) stay two stations each: Metrorex counts them so, which is how 64 is
# reached.
STATION_NAME_ALIASES = {"Basarab 1 - M1": "Basarab 1"}

CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# Municipiul București, OSM relation 377733, polygonised from its outer ways
# and gated on its area: 238.9 km2 in UTM 35N on 2026-09-29, exactly the six
# sectors' sum.
BOUNDARY_OSM_RELATION = 377733
BOUNDARY_OSM_NAME = "București"
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_bucuresti.json"
BOUNDARY_AREA_KM2 = (234, 244)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 35N: the longitude (~26.10) falls in the 24 to 30 band. Derived per
# city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32635"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

CITY_LABEL = "the Municipality of Bucharest"
# On-map label: Metrorex's line code; the legend adds the line's termini.
# Hues are OSM's route colours (Metrorex's own); the drawn colour is
# scripts/line_colour_search.py's nearest feasible one.
LINES = {"M1": {"hue": "#FFFF00"}, "M2": {"hue": "#003399"}, "M3": {"hue": "#BC1725"},
         "M4": {"hue": "#347C11"}, "M5": {"hue": "#FF8040"}}
LINE_ORDER = list(LINES)
LINE_NAMES = {k: k for k in LINES}
# The legend row reads "<label> <this>" (build_legend).
LEGEND_NAMES = {"M1": "Dristor – Pantelimon", "M2": "Pipera – Tudor Arghezi",
                "M3": "Preciziei – Anghel Saligny", "M4": "Gara de Nord – Străulești",
                "M5": "Eroilor – Valea Ialomiței / Râul Doamnei"}
# `python scripts/line_colour_search.py bucharest`, run 2026-09-29: every line
# >= 45.0 from the pins of that run, closest pair within 500 m 20.1 (M1's
# olive-yellow against M4's green, which meet only at Basarab), five distinct
# dark-mode labels. M1's yellow darkens to read on the light page; M2's blue
# takes a violet beside the Food shops pins (Stockholm's Blue line precedent).
#
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search, and two
# lines sat under the owner's floor of 20 from it (2026-10-07): M4 #608000 at
# 11.6 and M1 #989800 at 15.7. Each moved to the colour nearest its OSM hue
# that reads 3:1 on both pages, clears 20 from both pins and 18 from every
# other line, taking a wider margin where it cost little: M4 #247810 (olive
# 30.0), M1 #B48C00, a dark gold held to a yellow hue (olive 25.8). Both sit
# between 20 and 45 from olive, an accepted trade (owner, 2026-10-07); closest
# pair now 26.0 (M3, M5), five distinct dark-mode labels. DECISIONS, "Lines
# within 20 of the olive and violet pins recoloured".
LINE_COLOURS = {"M1": "#B48C00", "M2": "#7840D0", "M3": "#C02008", "M4": "#247810", "M5": "#E87030"}
# Five lines, one key each; M5's two branches (to Valea Ialomiței and Râul
# Doamnei) are one line, as Metrorex presents it.
LINE_OSM_REFS = {r: (r,) for r in ("M1", "M2", "M3", "M4", "M5")}
RELATIONS_SKIPPED = {}
STATION_ADDITIONS = {}
OSM_ADDITIONS_JSON = DATA_RAW / "osm_station_additions.json"
# GATE 3 - the network against English Wikipedia's Bucharest Metro infobox
# (64 stations), read 2026-09-29, a SECONDARY source (Prague's precedent). No
# per-line count is published there, so the gate is network-level (Oslo's).
OPERATOR_STATION_COUNTS = {"Metrorex (network)": 64}
OPERATOR_COUNTS_SOURCE = "en.wikipedia: Bucharest Metro infobox, 64 stations - secondary, read 2026-09-29"
# The naming layer for stations outside the municipality (none expected).
NAMING_GEOJSON = DATA_RAW / "naming_layer.geojson"

# --- Business filtering ------------------------------------------------

CITY_KEEP = "București"
TAXONOMY_SYSTEM = "romania_dsvsa"
RAW_CLASSIFICATION_COLUMN = "Categorie"

# The municipality's polygon extent (44.3342-44.5414 N, 25.9667-26.2256 E,
# measured 2026-09-29) plus ~0.02 deg. Placement is by OSM address and the
# polygon does the filtering; this records the frame.
BUCHAREST_BBOX = {
    "lat_min": 44.31,
    "lat_max": 44.56,
    "lon_min": 25.94,
    "lon_max": 26.25,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600377733)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ro",)
PLACE_FOLD = None
# Rows a reader held that the owner ruled to keep (2026-10-13;
# docs/decisions_drafts/search-final.md). A record only: no code reads it.
# A street is listed by name, a place by OSM id with its name. Not in
# PLACE_REVIEWED, which check E holds to names carrying a leak word.
PLACE_RULED_KEPT = {
    "Prelugirea Ghencea": "a misspelled street is still that street (owner, 2026-10-13)",
    # Held rows kept by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    # A home, family or person row is listed by id alone.
    "way/242092560": "'The International School of Bucharest', An article of the object's own outweighs a private operator or a business reading (owner 2026-10-13, keep beats drop; dealer galleries go only without an article)",
    "node/13645220824": "'Stâlpul Electric Verzișori', A place name plus a type word is a name; the bare-type rule takes only a name that is all type (BARE_TYPE_NAMES, matched as the whole name)",
    "way/646051432": "'Eroilor militari Romani', Statues, busts and public memorials stay, and monuments are not held to the notable rule (owner 2026-10-13, personal names 2; 2026-10-11 answer 5, measured and put back)",
    "way/77940084": "'Biserica Sfinții Trei Ierarhi - Coltea Colțea', A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "way/338192471": "'Dumitru Teodoru - Viilor', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/641716026": "'La Militari', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/1459493780": "'La Rond', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "node/13766598373": "'Decebal', Rows of one name beyond the merge distance stay unless shown to be one object (ROW_MERGE_M, 300 m)",
    "relation/3166516": "A historic building or palace with an article of its own stays (owner 2026-10-13, fifteen answers 12)",
    "way/144932693": "A place of worship under a name of its own needs no article (NOTABLE_ONLY 2026-10-07; Anyang 2026-10-13: where the tags show worship or cannot tell, it stays)",
    "Aleea Iacob Andrei D": "A real lane name with a number or letter stays (owner 2026-10-13, six answers 2)",
    "Rondul Poarta 4": "The description, code and ramp-name rules read minor or ramp-class ways only; another street keeps such a name (owner 2026-10-13: The Avenue stays; German answers 3: Weg A and Weg B)",
    "Pasarela pietonală Popești-Leordeni": "Named bridges and tunnels stay as street rows (owner 2026-10-13, fourteen answers 1; fifteen answers 11)",
    "Strada Palatul Cotroceni": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Strada Sala Palatului": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Strada Institutul Medico-Militar": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "DN6D": "Numbered roads on larger ways stay (owner 2026-10-13, fifteen answers 10)",
}
PLACE_REVIEWED = {}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "way/309366769": "'Biserica Adventistă de Ziua a Șaptea - Conferința Muntenia': Biserica Adventistă de Ziua a Șaptea - Conferința Muntenia, the denomination's name with its regional conference, an administrative seat (lane 4 borderline read; owner, 2026-10-16)",
    "way/186600911": "'Sediul FSPUB': Sediul FSPUB (the seat of FSPUB), an office label with an organisation's initials on a building tagged historic=building, no wikidata (lane 4 borderline read; owner, 2026-10-16)",
    # Bare type words and type phrases (the flag read of 2026-10-13, applied on the owner's word;
    # docs/decisions_drafts/search-final.md).
    "way/68336726": "a bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; owner 2026-10-13, the flag read's verdicts, all approved)",
    # Places of worship named by a body, left for the rules and still rows (the flag read of 2026-10-13, applied on the owner's word;
    # docs/decisions_drafts/search-final.md).
    "node/8574653317": "a place of worship named only by its denomination, body or hall type is dropped (four rulings 1; sixteen rulings 2; left for the rules and still a row, owner 2026-10-13)",
    "node/10562338619": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/225644835": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "node/9048997742": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "node/899633232": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/452907275": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/308764455": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/582491064": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/227702630": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/241827568": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "node/8693785589": "a freight yard, depot or operating point, not a passenger station (owner, 2026-10-13)",
    "node/12733150278": "a freight yard, depot or operating point, not a passenger station (owner, 2026-10-13)",
    "node/2126282888": "a freight yard, depot or operating point, not a passenger station (owner, 2026-10-13)",
    "node/6536576824": "a freight yard, depot or operating point, not a passenger station (owner, 2026-10-13)",
    "node/3480025393": "a bus station in as a station, no rail tag",
    "way/242467499": "a developer's estate tagged a neighbourhood, the plural of the home word",
    "node/8864235867": "a duplicate row, the same suburb is way/240575327 317 m away",
    "node/13340068854": "a museum exhibit carrying its model's wikidata, not its own",
    "node/13340068830": "a museum exhibit carrying its model's wikidata, not its own",
    "way/1469721743": "a museum exhibit carrying its model's wikidata, not its own",
    "way/1471899535": "a museum exhibit carrying its model's wikidata, not its own",
    "node/13340068855": "a museum exhibit carrying its model's wikidata, not its own",
    "way/85130630": "museum contents, an exhibit with no services by its own tag",
    "node/14180087101": "a description standing in for a name, no article",
    "way/552452874": "a web address standing in for a name",
    "node/987457581": "a grave with no Wikipedia article of its own",
    "way/13460652": "a name that says the thing is abandoned",
    "node/509347116": "a convent tagged a place of worship, no article",
    "node/1211865828": "a religious house tagged a place of worship, no article",
    "node/5336508694": "a duplicate row, the same church is way/242104494 11 m away",
    "way/150539862": "a service way named by an address, not a street",
    "way/1547016258": "a service way named by an address, not a street",
    "way/1122545151": "a service way named by an address, not a street",
    "way/740314410": "a description (the metro's pedestrian underpass), not a street name",
    "way/1520124749": "a description (the metro's pedestrian underpass), not a street name",
    "way/23679712": "a description (the passage at the Grivița halt), not a street name",
    "way/357222296": "a description (the passage at the Grivița halt), not a street name",
    "way/1211546964": "a description (the passage at the Grivița halt), not a street name",
    "way/1211546965": "a description (the passage at the Grivița halt), not a street name",
    "way/226600474": "a road code standing in for a name",
    "way/893631354": "a glitched name (double space, variant of another street)",
    "way/661214156": "an address number as a name",
    "way/546300765": "an address number as a name",
    "way/23671202": "an address number as a name",
    "way/198994299": "an address number as a name",
    "way/151065621": "an address number as a name",
    "way/202802925": "an address range as a name",
    "way/202802930": "an address range as a name",
    "way/877985328": "an address range as a name",
    "way/877985329": "an address range as a name",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "way/1366689705": "A business with nothing else is dropped (2026-10-07); only an article of its own outweighs it (owner 2026-10-13); held rows settled 2026-10-13",
    "way/694299391": "An office, library, society or hall named for an organisation, tagged a place of worship or a historic building, goes by id (owner 2026-10-13, seven rulings 7; the reads' settled class); held rows settled 2026-10-13",
    "way/860001496": "a named hall or stand of a larger venue (owner, 2026-10-13)",
    "node/11259913598": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "node/1725768052": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/1229553616": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/678037221": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/297945586": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/210642313": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/430820893": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/423683662": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/545859282": "A description standing in for a name goes by id (owner 2026-10-11; skill: a description longer than a type word); held rows settled 2026-10-13",
    "way/395016793": "A description standing in for a name goes by id (owner 2026-10-11; skill: a description longer than a type word); held rows settled 2026-10-13",
    "way/239429322": "A housing development mapped as a neighbourhood is dropped by id (owner 2026-10-13, four rulings 2; estate rule 2026-10-08, 2026-10-11); held rows settled 2026-10-13",
    "way/238310820": "A housing development mapped as a neighbourhood is dropped by id (owner 2026-10-13, four rulings 2; estate rule 2026-10-08, 2026-10-11); held rows settled 2026-10-13",
    "node/12137771371": "A housing development mapped as a neighbourhood is dropped by id (owner 2026-10-13, four rulings 2; estate rule 2026-10-08, 2026-10-11); held rows settled 2026-10-13",
    "node/6053541823": "A wrong object's name is a glitch and goes by id (owner 2026-10-11); held rows settled 2026-10-13",
    "node/8399467017": "A grave or a plaque needs a Wikipedia article of its own (owner 2026-10-13, personal names 2); held rows settled 2026-10-13",
    "node/7040539622": "An object admitted only by another object's or its subject's entry gets no row (fourth pass 38; own_item); held rows settled 2026-10-13",
    "way/78442442": "A home with no sign of visiting is no row; an article or a heritage listing is not enough (home rule 2026-10-08; fifteen answers 2); held rows settled 2026-10-13",
    "node/8865171993": "Duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M 2026-10-08 and 2026-10-13; six answers 6: second nodes of one district dropped); held rows settled 2026-10-13",
    "node/672149975": "Duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M 2026-10-08 and 2026-10-13; six answers 6: second nodes of one district dropped); held rows settled 2026-10-13",
    "way/88337000": "One object drawn in parts is one row (fourth pass 40, 2026-10-13); held rows settled 2026-10-13",
    "way/91797290": "One object drawn in parts is one row (fourth pass 40, 2026-10-13); held rows settled 2026-10-13",
    "way/416444682": "A route description standing in for a street name goes by id (the reads' settled class 2026-10-13: Daugavpils' two); held rows settled 2026-10-13",
    "way/13858856": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/13858857": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746224": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746228": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746229": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746232": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746233": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746235": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746237": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746239": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746240": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746243": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746248": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746255": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746257": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746259": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746264": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746269": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746272": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746278": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746279": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436746281": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/1436781557": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "node/11259913599": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); the same-named twin of node/11259913598, a row once that id was dropped; held rows settled 2026-10-13",
    "node/1725768053": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); the same-named twin of node/1725768052, a row once that id was dropped; held rows settled 2026-10-13",
    "node/1725768054": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); the same-named twin of node/1725768052, a row once that id was dropped; held rows settled 2026-10-13",
}
