"""Florence-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

FIRENZE, on Milan's and Rome's template (the Comune's own activity layers, an
OSM comune boundary) and the shared `pipeline/osm_tram.py` (the tram-city
skill). The business leg is the Comune di Firenze's four GeoJSON layers
(CC BY 4.0): a point and a type on every row, no name and no address, so a dot
shows its type (`pipeline/taxonomies/florence_attivita.py`). Rail from
OpenStreetMap; GEST's GTFS is not used.
"""

from pathlib import Path

SLUG = "florence"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "florence" / "raw"
DATA_PROCESSED = ROOT / "data" / "florence" / "processed"
OUTPUTS = ROOT / "outputs" / "florence"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# T1's four stops in Scandicci, outside the comune: drawn, not ringed, listed
# here with the comune each lies in (call 17).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) ----------------

# The Comune's four layers (datigis.comune.fi.it/json/, CC BY 4.0; credit the
# Comune di Firenze, state the changes). EPSG:3003 (Monte Mario / Italy 1).
# Layer key -> file. The key is the taxonomy's `source`.
LAYERS = {
    "commercio": "commercio_sede_fissa_od.json",
    "pubblici_esercizi": "pubblici_esercizi_od.json",
    "estetiche": "attivita_estetiche_od.json",
    "tintolavanderie": "tintolavanderie_od.json",
}
LAYER_URL = "https://datigis.comune.fi.it/json/"     # + the file name
LAYER_CRS = "EPSG:3003"
LAYER_MIN_ROWS = {"commercio": 6000, "pubblici_esercizi": 2500, "estetiche": 1000,
                  "tintolavanderie": 100}

# OSM: every tram relation in the network's box, and the comuni around it.
RAIL_BBOX = (43.72, 11.15, 43.84, 11.34)          # south, west, north, east
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_COMUNI_JSON = DATA_RAW / "osm_comuni.json"
# Comune di Firenze, OSM relation 42602, ref:ISTAT 048017; the other comuni in
# the box only name where an outside stop lies.
ISTAT_FIRENZE = "048017"
COMUNE_AREA_KM2 = (95.0, 110.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 32N: the longitude (~11.25) falls in the 6-12 E band. Derived per
# city, not copied.
CRS_PROJECTED = "EPSG:32632"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the 39 in-comune stops' 322 m median gap (the brief, 2026-09-30;
# the owner's spacing rule). Step 1 prints the median again and stops outside
# 270-380 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (270.0, 380.0)

# --- Station scope: T1 and T2, every stop in the comune ------------------------
#
# Tramvia di Firenze: T1 Leonardo (Villa Costanza - Careggi) and T2 Vespucci
# (Aeroporto - Unità). T1 runs on into Scandicci, so its four stops there are
# drawn but not ringed (owner, call 17). The T3 and T4 relations are under
# construction with no stops (filled from the fetch).
ROUTE = "tram"
OPERATOR = None
LINE_REFS = ("T1", "T2")
# Under construction, with track and no stops in OSM (owner, call: T3 not drawn
# until it opens). T3.2.1 Libertà - Bagno a Ripoli is due to open about January
# 2027 (Comune di Firenze; read 2026-09-30). Re-check when it opens.
_BUILDING = "under construction, no stops in OSM; not drawn until it opens (owner)"
NOT_DRAWN = {
    18624687: "T3.2.1 Libertà - Bagno a Ripoli: " + _BUILDING,
    18624725: "T3.2.1 Bagno a Ripoli - Libertà: " + _BUILDING,
    18649601: "T3.2.2 Libertà - Rovezzano (no ref): " + _BUILDING,
    18649602: "T3.2.2 Rovezzano - Libertà (no ref): " + _BUILDING,
    18621862: "T4 Firenze - Le Piagge: " + _BUILDING,
    18622253: "T4 Le Piagge - Firenze: " + _BUILDING,
    18651301: "T2.2 Aeroporto - Sesto Fiorentino: " + _BUILDING,
    18651302: "T2.2 Sesto Fiorentino - Aeroporto: " + _BUILDING,
}
STATION_ADD = {}
EXPECTED_IN_COMUNE = 39
EXPECTED_OUTSIDE = 4

# Gate 3: GEST's own stop counts per line, the whole line before the comune
# split (T1's four Scandicci stops included). Step 1 stops on a mismatch.
#   T1 Villa Costanza - Careggi: 26 stops.
#   T2 Peretola Aeroporto - San Marco Università: 20 stops. GEST's diagram also
#      shows Unità, greyed out: the Comune closed it to regular service on
#      2 January 2025, first and last runs only. It is not drawn, so it is not
#      counted (secondary sources that say 21 include it).
OPERATOR_STATION_COUNTS = {"T1": 26, "T2": 20}
OPERATOR_COUNTS_SOURCE = (
    "GEST's stop diagram 'Sinottico fermate' on its Linee page, "
    "https://www.gestramvia.it/linee/ (image wp-content/uploads/2025/01/"
    "Sinottico-fermate-1.png), read 2026-10-01; Unità's closure from the Comune di "
    "Firenze, 'Linea 2 della tramvia, tratto Fortezza-San Marco' (16 Jan 2025). "
    "Cross-checked against it.wikipedia 'Rete tranviaria di Firenze' (secondary).")

SPACING_MIN_M = 100.0

DRAWN_LINES = ("T1", "T2")
LINE_NAMES = {"T1": "T1 Leonardo", "T2": "T2 Vespucci"}
# OSM's own colours (the brief).
LINE_COLOURS = {"T1": "#254395", "T2": "#5d3988"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "florence_attivita"
RAW_CLASSIFICATION_COLUMN = "tipologiaattivita"

# Sanity bounds for the placed points: the comune plus a margin.
FLORENCE_BBOX = {
    "lat_min": 43.70,
    "lat_max": 43.85,
    "lon_min": 11.13,
    "lon_max": 11.35,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600042602)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("it",)
PLACE_FOLD = None
# Rows a reader held that the owner ruled to keep (2026-10-13;
# docs/decisions_drafts/search-final.md). A record only: no code reads it.
# A street is listed by name, a place by OSM id with its name. Not in
# PLACE_REVIEWED, which check E holds to names carrying a leak word.
PLACE_RULED_KEPT = {
    # Held rows kept by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    # A home, family or person row is listed by id alone.
    "way/463513949": "'Ex cappella di villa il Casone', A landmark that stands, ruined, abandoned or under a former-use name, stays (owner 2026-10-13: keep all standing abandoned landmarks; third list 11: former in a name is not read as gone)",
    "way/480911018": "'Ex chiesa di Santa Maria di Orbatello', A landmark that stands, ruined, abandoned or under a former-use name, stays (owner 2026-10-13: keep all standing abandoned landmarks; third list 11: former in a name is not read as gone)",
    "relation/11207153": "'Ex monastero domenicano della Santa Croce', A landmark that stands, ruined, abandoned or under a former-use name, stays (owner 2026-10-13: keep all standing abandoned landmarks; third list 11: former in a name is not read as gone)",
    "way/1124689288": "'Ex mulino di Sant’Andrea a Rovezzano', A landmark that stands, ruined, abandoned or under a former-use name, stays (owner 2026-10-13: keep all standing abandoned landmarks; third list 11: former in a name is not read as gone)",
    "way/374064989": "'Ex oratorio del Bandino', A landmark that stands, ruined, abandoned or under a former-use name, stays (owner 2026-10-13: keep all standing abandoned landmarks; third list 11: former in a name is not read as gone)",
    "way/306240095": "'Ex oratorio di Gesù Pellegrino', A landmark that stands, ruined, abandoned or under a former-use name, stays (owner 2026-10-13: keep all standing abandoned landmarks; third list 11: former in a name is not read as gone)",
    "way/478229004": "'Area Cani Paolo Uccello', A place name plus a type word is a name; the bare-type rule takes only a name that is all type (BARE_TYPE_NAMES, matched as the whole name)",
    "way/760909959": "'Giardino Interno Via Argin Grosso', A place name plus a type word is a name; the bare-type rule takes only a name that is all type (BARE_TYPE_NAMES, matched as the whole name)",
    "way/306396530": "'Chiesa di San Giuliano (Firenze)', A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "way/484785562": "'Chiesa Evangelica Valdese di Firenze (Holy Trinity Church)', Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "way/771929814": "'Santo di Stefano in Pane', A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "way/465939106": "A castle is no home by its tags and its row stays; the web check on castles is owed and no rule is built (exclusions: considered and not built)",
    "way/255971544": "A landmark that stands, ruined, abandoned or under a former-use name, stays (owner 2026-10-13: keep all standing abandoned landmarks; third list 11: former in a name is not read as gone)",
    "way/627558686": "'Ex Giardino Zoologico', The not-there rule reads demolished, removed or not yet open; a place that stands today stays (lifecycle 2026-10-13; was: on a place is not read)",
    "way/474348946": "'Giardino Ex Caterina De' Medici', The not-there rule reads demolished, removed or not yet open; a place that stands today stays (lifecycle 2026-10-13; was: on a place is not read)",
    "node/6742519788": "'L'Ippopotamo', Statues, busts and public memorials stay, and monuments are not held to the notable rule (owner 2026-10-13, personal names 2; 2026-10-11 answer 5, measured and put back)",
    "way/443027894": "A historic building or palace with an article of its own stays (owner 2026-10-13, fifteen answers 12)",
    "relation/7071160": "'Palazzina della Meridiana', A historic building that is no home and no business by its tags stays; historic kinds need no article (landmark rules 2026-10-07)",
    "node/2426842882": "'Colonna della Giustizia', Public art stays on an entry of its own that has an article, asked of Wikidata (owner 2026-10-13, fourth pass)",
    "node/2732676607": "'Colonna dell’Abbondanza', Public art stays on an entry of its own that has an article, asked of Wikidata (owner 2026-10-13, fourth pass)",
    "Via Allievi Sottufficiali Carabinieri del Cinquantanovesimo Corso 1966-1967": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Via Madre Teresa di Calcutta": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Via della Maternità": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Via Esculapio": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Via Paracelso": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Via Franco Basaglia": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
}
PLACE_REVIEWED = {
    "Museo dell'Officina Profumo - Farmaceutica di Santa Maria Novella": "a museum (owner, 2026-10-13)",
}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "node/9687617360": "a freight yard, depot or operating point, not a passenger station (owner, 2026-10-13)",
    "way/1455775297": "a lane named for its mode (owner, 2026-10-13)",
    "way/1455775298": "a lane named for its mode (owner, 2026-10-13)",
    "way/192460803": "a lane named for its mode (owner, 2026-10-13)",
    "way/116487203": "a lane named for its mode (owner, 2026-10-13)",
    "way/162782248": "a lane named for its mode (owner, 2026-10-13)",
    "way/31101494": "a lane named for its mode (owner, 2026-10-13)",
    "way/583788623": "a lane named for its mode (owner, 2026-10-13)",
    "way/595068335": "a lane named for its mode (owner, 2026-10-13)",
    "way/900303357": "a lane named for its mode (owner, 2026-10-13)",
    "way/900303358": "a lane named for its mode (owner, 2026-10-13)",
    "way/1386997977": "a lane named for its mode (owner, 2026-10-13)",
    "way/779503329": "a lane named for its mode (owner, 2026-10-13)",
    "way/1198307081": "a lane named for its mode (owner, 2026-10-13)",
    "way/1201694730": "a lane named for its mode (owner, 2026-10-13)",
    "way/1201694731": "a lane named for its mode (owner, 2026-10-13)",
    "way/1310486871": "a lane named for its mode (owner, 2026-10-13)",
    "way/620127564": "a lane named for its mode (owner, 2026-10-13)",
    "way/890241171": "a lane named for its mode (owner, 2026-10-13)",
    "way/939389473": "a lane named for its mode (owner, 2026-10-13)",
    "way/942741443": "a lane named for its mode (owner, 2026-10-13)",
    "way/942741444": "a lane named for its mode (owner, 2026-10-13)",
    "way/953572027": "a lane named for its mode (owner, 2026-10-13)",
    "way/953572028": "a lane named for its mode (owner, 2026-10-13)",
    "way/953572029": "a lane named for its mode (owner, 2026-10-13)",
    "way/953572030": "a lane named for its mode (owner, 2026-10-13)",
    "way/1198307077": "a lane named for its mode (owner, 2026-10-13)",
    "way/1534919065": "a lane named for its mode (owner, 2026-10-13)",
    "way/623794860": "a lane named for its mode (owner, 2026-10-13)",
    "way/422288184": "a lane named for its mode (owner, 2026-10-13)",
    "way/623794868": "a lane named for its mode (owner, 2026-10-13)",
    "way/620127562": "a lane named for its mode (owner, 2026-10-13)",
    "way/422515715": "a lane named for its mode (owner, 2026-10-13)",
    "way/623794867": "a lane named for its mode (owner, 2026-10-13)",
    "way/637497276": "a lane named for its mode (owner, 2026-10-13)",
    "way/637497278": "a lane named for its mode (owner, 2026-10-13)",
    "way/953570011": "a lane named for its mode (owner, 2026-10-13)",
    "way/953570012": "a lane named for its mode (owner, 2026-10-13)",
    "way/953570013": "a lane named for its mode (owner, 2026-10-13)",
    "way/953570014": "a lane named for its mode (owner, 2026-10-13)",
    "way/1207855202": "a lane named for its mode (owner, 2026-10-13)",
    "way/419950205": "a lane named for its mode (owner, 2026-10-13)",
    "way/993483636": "a lane named for its mode (owner, 2026-10-13)",
    "way/799784923": "a lane named for its mode (owner, 2026-10-13)",
    "way/870882759": "a dog-training club tagged a park",
    "way/472637048": "a farmhouse ruin with no article",
    "way/478064678": "a description standing in for a name",
    "node/8669023184": "a memorial stone's inscription standing in for a name, no article",
    "node/7959956070": "a duplicate row: the same synagogue as way/102979678",
    "node/4713726602": "public art whose Wikipedia link is another subject's article, none of its own",
    "way/1444307352": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444315433": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307356": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307435": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307437": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307354": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307355": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1087438300": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1442609718": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307353": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307439": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444315434": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/1444307438": "an indoor aisle of the central market hall (indoor=yes), named after a town: no street",
    "way/912178164": "a path's variant marked in the name, a description: no street name",
    "way/680667747": "a list of house numbers standing in for a name",
    "way/637311392": "a glitched name: a mistyped street word (Vie for Via)",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "way/482461122": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/1205438727": "Duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M 2026-10-08 and 2026-10-13; six answers 6: second nodes of one district dropped); held rows settled 2026-10-13",
    "way/781613868": "A library with no article of its own is dropped (owner 2026-10-13, fourth pass 39); held rows settled 2026-10-13",
    "way/90940145": "a named hall or stand of a larger venue (owner, 2026-10-13)",
    "way/866278407": "a named hall or stand of a larger venue (owner, 2026-10-13)",
    "way/90940144": "a named hall or stand of a larger venue (owner, 2026-10-13)",
    "way/866278400": "a named hall or stand of a larger venue (owner, 2026-10-13)",
    "way/676644892": "A square a street row already names is a duplicate (SQUARE_DUP_M, 2026-10-08); held rows settled 2026-10-13",
    "way/305870493": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/305870475": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/853723911": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
}
