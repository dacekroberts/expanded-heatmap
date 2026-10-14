"""Göteborg-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

GÖTEBORG, on Stockholm's template (one food register, the city only,
`pipeline/taxonomies/sweden_livsmedel.py`) and the shared
`pipeline/osm_tram.py` (the tram-city skill). The register is Göteborgs Stad's
`Livsmedelsverksamheter` (CC0, refreshed daily), taken as its CSV
distribution, never the rowstore JSON (the brief). Rail from OpenStreetMap:
trams 1-13, every stop.
"""

from pathlib import Path

SLUG = "goteborg"

# The macro map's two keys and the scope (the brief's checks compare these).
MAP_MODE = "tram"
MAP_COVERAGE = "one_bucket"
SCOPE = "city"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "goteborg" / "raw"
DATA_PROCESSED = ROOT / "data" / "goteborg" / "processed"
OUTPUTS = ROOT / "outputs" / "goteborg"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Lines 4 and 12 run on into Mölndal: their stops there are drawn with the line
# but not ringed, listed here with the kommun each lies in (owner, call 21).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) ----------------

# Livsmedelsverksamheter (Göteborgs Stad, miljöförvaltningen), the CSV
# distribution in EntryStore context 6. utf-8-sig, ';'. CC0 1.0 is declared on
# the DISTRIBUTION's metadata node (57479), not the dataset node (35): the fetch
# re-reads it every run. One row per premises; no dates of any kind.
REGISTER_URL = "https://catalog.goteborg.se/store/6/resource/57478"
REGISTER_META_URL = "https://catalog.goteborg.se/store/6/metadata/57479"
REGISTER_LICENCE_MARK = "publicdomain/zero"
REGISTER_CSV = DATA_RAW / "livsmedelsverksamheter.csv"
REGISTER_COLUMNS = ("namn", "adress", "postnummer", "ort", "typ", "y_sweref991200",
                    "x_sweref991200", "lat", "lon")
REGISTER_MIN_ROWS = 4500
# The register's own position, SWEREF 99 12 00 (y = northing, x = easting in
# THIS file; the rowstore JSON swaps them). Step 2 checks lat/lon against it.
REGISTER_POSITION_CRS = "EPSG:3007"
# THE FALLBACK POINT. The distribution's own description (metadata 57479):
# premises "som inte har en korrekt adress eller är ambulerande är placerad på
# Miljöförvaltningens adresspunkt" - with no correct address, or mobile, they
# sit at the Environment Administration's address point. Measured 2026-09-30:
# 135 rows within 16.5 m of the median position of the 94 rows whose address
# is "AMBULERANDE" (101 within 3.1 m, the rest spread on a 10-17 m ring), then
# nothing nearer than 42 m; none has an address there. A premises there is not
# placed (Florida Pizzeria's own address is Väderlekstorget 6). The centre is
# re-derived every run from the AMBULERANDE rows.
FALLBACK_ADDRESS_PREFIX = "AMBULERANDE"
FALLBACK_MIN_ROWS = 50
FALLBACK_RADIUS_M = 25.0
# An address with an apartment number ("LGH 1202") is a home: left off
# (Houston's and Sacramento's rule). The three on 2026-09-30 sit at the fallback
# point too.
HOME_ADDRESS = r"(?i)\bLGH\b|lägenhet"

# OSM, one query each, one at a time: every tram relation in the network's box
# (out geom) with its nodes, and the kommuner (admin_level 7) around it.
RAIL_BBOX = (57.60, 11.80, 57.85, 12.15)          # south, west, north, east
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_KOMMUNER_JSON = DATA_RAW / "osm_kommuner.json"
# Göteborgs Stad, OSM relation 935611 (ref:scb 1480). The other kommuner only
# name where an outside stop lies (Mölndal).
GOTEBORG_RELATION = 935611
GOTEBORG_SCB = "1480"
# The box round lines 4's and 12's Mölndal ends, for the naming layer.
KOMMUNER_BBOX = (57.62, 11.98, 57.67, 12.05)
# Measured 2026-09-30 in UTM 32N, the polygon as OSM draws it (sea included).
KOMMUN_AREA_KM2 = (440.0, 1100.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 32N: the longitude (~11.97) falls in the 6-12 E band - not
# Stockholm's 34N. Derived per city, not copied.
CRS_PROJECTED = "EPSG:32632"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the in-city stops' median nearest-neighbour gap (the brief: 378 m
# over 127 stop names, 2026-09-30; the owner's spacing rule). Step 1 prints the
# median again and stops outside 320-430 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (320.0, 430.0)

# --- Station scope: trams 1-13, every stop in Göteborgs Stad -------------------
#
# Göteborgs Spårvägar's thirteen tram lines. 4 (Mölndal - Angered) and 12
# (Lisebergs station / Mölndal) run on into Mölndal: drawn to their ends, their
# stops there listed as outside (owner, call 21, on the stub test: 4 keeps 15 of
# 20 stops, 12 keeps 13 of 18). Lisebergslinjen, the heritage line, is out.
ROUTE = "tram"
OPERATOR = None
LINE_REFS = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13")
NOT_DRAWN = {
    444922: "Lisebergslinjen, the heritage line (no ref, no colour): out (the brief, owner)",
}
STATION_ADD = {}
NAME_ALIASES = {}
# {stop name: (line, ...)}: a line Västtrafik's timetable serves at a stop
# OSM's relations for that line leave out, where the stop is already drawn from
# other lines' relations (one Västtrafik stop code across the lines). Step 1
# adds the line to the stop's existing stop positions - no position is added, so
# the station does not move - and stops if the name is gone, or if the line's
# own relations now carry it (OSM filled the gap: remove the entry). Fixed
# 2026-10-01 (owner, "implement the station fixes"):
#   Korsvägen (003980): lines 4 (platforms A2/A3), 6 and 8 (B1/B2), 13 (B2)
#   Drottningtorget (002135): line 2 (A3/A6)
LINE_ADD = {
    "Korsvägen": ("4", "6", "8", "13"),
    "Drottningtorget": ("2",),
}
SPACING_MIN_M = 60.0
# Owner call 21's stub test: a line drawn to its end must keep at least half
# its stops inside the city.
STUB_MIN_SHARE = 0.5
STUB_LINES = ("4", "12")

# Gate 3: Västtrafik's own stops per line, from each line's timetable PDF
# (page 1's stop columns, both directions), the whole line before the kommun
# split (4's and 12's Mölndal stops included). A tram step 1 stops on a
# mismatch. Five lines' OSM relations leave out a stop the line's timetable
# serves (2, 4, 6, 8, 13); LINE_ADD above puts each line back on that stop's
# label, so the build matches (2026-10-01).
OPERATOR_STATION_COUNTS = {
    "1": 28,
    "2": 28,   # with Drottningtorget (002135) by LINE_ADD; OSM's relations alone give 27
    "3": 29,
    "4": 21,   # with Korsvägen (003980) by LINE_ADD; OSM alone 20
    "5": 33,
    "6": 46,   # with Korsvägen by LINE_ADD; OSM alone 45
    "7": 35,
    "8": 25,   # with Korsvägen by LINE_ADD; OSM alone 24
    "9": 21,
    "10": 13,
    "11": 35,
    "12": 18,
    "13": 21,  # with Korsvägen by LINE_ADD; OSM alone 20
}
OPERATOR_COUNTS_SOURCE = (
    "Västtrafik's line timetables 'Tidtabell linje 1' to '13', valid 2026-08-17 to "
    "2026-12-12, the PDF linked from each line's page "
    "https://www.vasttrafik.se/reseplanering/tidtabeller/linje/90110145<NNN>00000/ "
    "(page 1's stop columns, both directions), read 2026-10-01. The line page's own "
    "stop list names more stops than the PDF (line 7: six more), so the "
    "timetable PDF is the figure used.")

DRAWN_LINES = LINE_REFS
# The lines' public names: Västtrafik's "Spårvagn 1" ... "Spårvagn 13",
# labelled in English as Riga's and Daugavpils's are ("Tram 1").
LINE_NAMES = {r: f"Tram {r}" for r in LINE_REFS}
# OSM's own colours (2026-09-30). Each line is two direction relations, and
# seven of them disagree on the colour (the brief): the colour drawn is that of
# the relation load_osm_line_shapes draws (the one with the most geometry),
# except where it is a CSS word - 4's "green" and 11's "black" - where the
# other relation's hex is taken. Step 1 stops if OSM no longer records one.
#
# ONE MOVED, on Prague's precedent (its metro A, #00A562, the same green):
# the shared check (pipeline/linecolour.py, floor 10) refused 4's #00A261 at
# 8.8 from the Personal services pins (#1baf7a). Lightened in HSL lightness
# only, hue and saturation kept, by the smallest step that clears the floor
# with Prague's ~13 margin: +0.05 -> #00BB70, 13.3 from the pins and 36.5 from
# the nearest line (12). Lighter, not darker, for Lille's reason (the dark
# basemap). Below the preferred 45 and recorded, not moved (they are OSM's):
# 3 14.2 (Retail), 12 24.3, 8 38.3, 10 40.9.
LINE_COLOURS = {"1": "#FFFFFF", "2": "#FDDD04", "3": "#0079C2", "4": "#00BB70",
                "5": "#EB1923", "6": "#FA8719", "7": "#9C5506", "8": "#A54499",
                "9": "#B9E2F8", "10": "#C7DF8E", "11": "#231F20", "12": "#57B9A8",
                "13": "#FEE6C2"}
# {line: (OSM's colour, why the drawn one differs)}; step 1 checks the OSM one.
LINE_COLOUR_SHIFTS = {"4": ("#00A261", "8.8 from the Personal services pins; lightened +0.05")}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "sweden_livsmedel"
RAW_CLASSIFICATION_COLUMN = "typ"

# GÖTEBORG'S `typ` IS NOT STOCKHOLM'S `VerksamhetsTyp`. Göteborg's control
# records its own 47 local types (RESTAURANG, KAFÉ, LIVSMEDELSBUTIK, ...);
# Stockholm's layer carries Livsmedelsverket's national activity groups. So
# step 2 DERIVES the taxonomy's column from `typ`, here, and the module is
# untouched: each storefront type maps to the national group it belongs to,
# and the pin shows that group. Every other type is out, with its reason, and
# a type in neither table stops step 2. Read by name 2026-09-30.
FOOD_SERVICE = "Restaurang-, catering- och barverksamhet"
FOOD_SHOP = "Detaljhandel"
TYP_STOREFRONT = {
    "RESTAURANG": FOOD_SERVICE,
    "KAFÉ": FOOD_SERVICE,
    # Ice-cream kiosks and cafés with a counter; a cart (glassvagn) is dropped
    # by the module's no-counter rule.
    "GLASSKIOSK": FOOD_SERVICE,
    "LIVSMEDELSBUTIK": FOOD_SHOP,
    "BAGERI": FOOD_SHOP,
    "HÄLSOKOSTBUTIK": FOOD_SHOP,
    "FISKBUTIK": FOOD_SHOP,
    "KÖTTBUTIK": FOOD_SHOP,
    "KIOSK": FOOD_SHOP,
    # Ice-cream makers with a shop (the type says butik): Gelateria Positano,
    # Johannebergs Glass.
    "GLASSTILLVERKNING - butik": FOOD_SHOP,
}
_INSTITUTION = "institutional kitchen (preschool, school, care home, hospital, day centre)"
_NO_COUNTER = "no counter of its own (R1)"
_PRODUCTION = "food production, not a shop"
TYP_EXCLUDED = {
    "FÖRSKOLA - tillagning": _INSTITUTION,
    "FÖRSKOLA - mottagning": _INSTITUTION,
    "SKOLA - tillagning": _INSTITUTION,
    "SKOLA - mottagning": _INSTITUTION,
    "GRUPP/SERVICEBOENDE - tillagning": _INSTITUTION,
    "GRUPP/SERVICEBOENDE - mottagning": _INSTITUTION,
    "SERVICEHUSKÖK / ÄLDREBOENDE - tillagning": _INSTITUTION,
    "SERVICEHUSKÖK / ÄLDREBOENDE - mottagning": _INSTITUTION,
    "DAGVERKSAMHET - tillagning": _INSTITUTION,
    "DAGVERKSAMHET - mottagning": _INSTITUTION,
    # Open preschools, school cafés, day-activity cafés (all 15 read).
    "DAGVERKSAMHET - kafé": _INSTITUTION,
    "SJUKHUS - tillagning": _INSTITUTION,
    "SJUKHUS - mottagning": _INSTITUTION,
    "FRITIDSGÅRD": _INSTITUTION,
    # Restaurants that only receive food cooked elsewhere: staff restaurants
    # (ISS Trafikverket, Pågen's personalrestaurang, United Spaces, VGR Campus),
    # 11 of the 13 read (R1, canteens).
    "RESTAURANG - mottagning": "staff and institutional restaurants (R1, canteens)",
    # Hotel and hostel breakfast rooms and ISS sites (all 26 read): lodging.
    "FRUKOSTSERVERING": "hotel breakfast rooms and staff sites (lodging, R1)",
    "AMBULERANDE": "mobile food (R1)",
    "BASLOKAL": "base premises of food trucks and caterers (R1)",
    "LEVERANSKÖK - catering": "delivery kitchens and caterers (R1)",
    # Ferries and archipelago boats (all 20 read): not a fixed premises.
    "FARTYG": "ships and ferries, not a fixed premises",
    "APOTEK": "pharmacies: not food shops on a food-only register (Stockholm's precedent)",
    "GROSSIST": "wholesale",
    "LAGER": "warehouse",
    "HUVUDKONTOR": "head office",
    "MATMÄKLARE": "food broker, no premises open to the public",
    "TRANSPORTÖR": "transport",
    "MATTRANSPORTER - varmhållning": "transport",
    "ÖVRIG LIVSMEDELSTILLVERKNING": _PRODUCTION,
    "TILLVERKNING FÄRDIGLAGAD MAT": _PRODUCTION,
    "BRYGGERI": _PRODUCTION,
    "KONFEKTYRTILLVERKNING": _PRODUCTION,
    "GLASSTILLVERKNING": _PRODUCTION,
    "HÄLSOKOSTTILLVERKNING": _PRODUCTION,
    # Coffee roasters (8): production, as Stockholm's beverage production.
    "KAFFEROSTERI": _PRODUCTION,
    "ANIMALIEANLÄGGNING": "animal-product establishment (production)",
    "KONTAKTMATERIALFÖRETAG": "food-contact materials maker",
}
# A BLANK `typ` (274 rows on 2026-09-30; the rowstore JSON drops them): owner
# call 20 - classified by name where the name shows a counter (the module's
# name rules, Stockholm's untyped premises), and the rest dropped.
#
# Vending machines are out wherever the register files them (docs/
# category_rules.md, "Mobile units, kiosk carts, vending machines"): 24Seven
# Vending (a KIOSK) and SmartVend 24/7 (blank, a shop by its "24/7"). The
# module's name rules have carried the same words since 2026-10-01 (call C2);
# step 2 still drops them here first, so its log counts them.
VENDING_NAME = r"(?i)vending|smartvend"

# A PREMISES NAMED ONLY AS A PERSON shows its address (Kansas City's and New
# Orleans's rule). Read by eye on 2026-09-30 from the 738 shown names
# residence.looks_personal reads as a person's, and from a looser two-to-three-
# word scan of the rest; nearly all are trade names ("Kalle Glader", "Joe
# Farelli", "Evas Paley", "Gustav Vasa" are restaurants). Ambiguous names are
# listed, which only shows an address in place of a name.
# Keys, not names (pipeline/name_keys.py): a new name's key is its output.
PERSON_NAMED = (
    "578f1d18872ce082", "2a6687c3791234ab", "95b64a7872957160", "5c5c656aa410c114",
    "0392a0a211610fb8", "c31d7849e3dd9d35", "87e85dd2761c5313", "caea2d2f74adad27",
    "ca9b1295162aa7f3", "b6206474a043e5ba", "04f820ecc08b2e51", "c8a219d2dc0f3001",
    "8d78a7044f0bb59b",
)

# Sanity bounds for the register's points: Göteborg's extent (the brief's lat
# 57.5631-57.8583, lon 11.7044-12.2050) plus a margin. The kommun polygon does
# the filtering; this catches an axis or CRS error.
GOTEBORG_BBOX = {
    "lat_min": 57.54,
    "lat_max": 57.88,
    "lon_min": 11.68,
    "lon_max": 12.23,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600935611)"
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
    "way/798501733": "'Park Lagmansgatan', admitted by the index rule for its kind; no drop rule or ruling reaches it by tags or name",
    "node/7683661890": "admitted by the index rule for its kind; no drop rule or ruling reaches it by tags or name",
    "node/1834210643": "'Bergslagsunrnan', a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "node/7096292172": "'Berglärkan', admitted by the index rule for its kind; no drop rule or ruling reaches it by tags or name",
    "node/7713526547": "'Bällskär', admitted by the index rule for its kind; no drop rule or ruling reaches it by tags or name",
    "node/7096293809": "'Snäckeberget', admitted by the index rule for its kind; no drop rule or ruling reaches it by tags or name",
    "Campingvägen": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Stora Holm Övningsväg": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Kvarternästaregången": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Kvartermästaregången": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "Blå stråket": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Gula stråket": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Röda stråket": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Vita stråket": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Bruna stråket": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
    "Gröna stråket": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
}
PLACE_REVIEWED = {}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "node/11067485073": "public art with no article of its own: one part of a planet walk sharing the walk's article",
    "node/12087404769": "public art with no article of its own: one part of a planet walk sharing the walk's article",
    "node/11067485074": "public art with no article of its own: one part of a planet walk sharing the walk's article",
    "node/11067485071": "public art with no article of its own: one part of a planet walk sharing the walk's article",
    "node/11067485078": "public art with no article of its own: one part of a planet walk sharing the walk's article",
    "node/11067485064": "public art with no article of its own: one part of a planet walk sharing the walk's article",
    "node/11067485070": "public art with no article of its own: one part of a planet walk sharing the walk's article",
    "node/11067485075": "public art with no article of its own: one part of a planet walk sharing the walk's article",
    "node/11067485072": "public art with no article of its own: one part of a planet walk sharing the walk's article",
    "way/613388049": "a ride inside an amusement park (owner, 2026-10-13)",
    "way/127184047": "a ride inside an amusement park (owner, 2026-10-13)",
    "way/126771772": "a ride inside an amusement park (owner, 2026-10-13)",
    "node/1404439870": "a ride inside an amusement park (owner, 2026-10-13)",
    "way/306814849": "a ride inside an amusement park (owner, 2026-10-13)",
    "way/48171650": "a ride inside an amusement park (owner, 2026-10-13)",
    "way/119259952": "a ride inside an amusement park (owner, 2026-10-13)",
    "relation/14783881": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "way/49493305": "museum or zoo contents with no article of their own (owner, 2026-10-13)",
    "way/180600645": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/291353441": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/59054129": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/277126646": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/297343751": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/1031601615": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031601618": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031601656": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1057389857": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031605860": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/944134760": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/944134761": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/152524996": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/54680177": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/55966293": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031604681": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031604682": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031604683": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031604684": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1057425437": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1565662333": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/944134766": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/944134767": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031320162": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031599608": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031599609": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031599764": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031375457": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/152524992": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/152524998": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1363636524": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1363646605": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/199698208": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1363636527": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/55966313": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/54679992": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/55966300": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031602150": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031602155": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031598805": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031604836": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031604837": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/642880991": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/944135281": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1204688060": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1204688062": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031603697": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031603698": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/944135921": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/26390000": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1021544416": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031605617": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031605618": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1057425438": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1103778585": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/944134765": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031375287": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1031375290": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1540264312": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/775058862": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/775058864": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/775058866": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/775058871": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/115686188": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/115686189": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/115686192": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/115686193": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/116163643": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/27549124": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/926886724": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/926886725": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/132834845": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/132834839": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1067726591": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/131618423": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/132025926": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/132025947": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/132025949": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/132025951": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/28305628": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1109858289": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1109858290": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/120445784": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/120445789": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/27315497": "an estate courtyard path or campus yard, not a street (owner, 2026-10-13)",
    "way/1246865252": "a code-named private street (owner, 2026-10-13)",
    "way/1246865253": "a code-named private street (owner, 2026-10-13)",
    "way/1246865250": "a code-named private street (owner, 2026-10-13)",
    "way/1246865251": "a code-named private street (owner, 2026-10-13)",
    "way/1411443024": "a code-named private street (owner, 2026-10-13)",
    "way/462519269": "a code-named private street (owner, 2026-10-13)",
    "way/940452199": "a code-named private street (owner, 2026-10-13)",
    "way/1411442191": "a code-named private street (owner, 2026-10-13)",
    "way/1411442192": "a code-named private street (owner, 2026-10-13)",
    "way/359777305": "a code-named private street (owner, 2026-10-13)",
    "way/359779008": "a code-named private street (owner, 2026-10-13)",
    "way/359783522": "a code-named private street (owner, 2026-10-13)",
    "way/844636793": "a code-named private street (owner, 2026-10-13)",
    "node/3585966101": "a code standing in for a name, at a car plant's gate",
    "node/3585966117": "a code standing in for a name, at a car plant's gate",
    "node/3585966094": "a code standing in for a name, at a car plant's gate",
    "node/3585966115": "a code standing in for a name, at a car plant's gate",
    "node/3585966118": "a code standing in for a name, at a car plant's gate",
    "node/3585975094": "a business: a company reception tagged a locality",
    "node/3063973963": "a business: a carmaker's visitor centre tagged a locality",
    "way/45100033": "a business: a shopping mall building tagged a locality",
    "node/4364986335": "a business: a trampoline park tagged a stadium",
    "way/174855146": "museum contents: a vessel of the ship museum with no wikidata of its own",
    "way/174855140": "museum contents: a vessel of the ship museum with no wikidata of its own",
    "way/174855144": "museum contents: a vessel of the ship museum with no wikidata of its own",
    "way/1304804643": "museum contents: an aircraft on display whose wikidata is its model's",
    "way/171416772": "a cemetery's service road",
    "way/600818323": "a garden's service way",
    "way/172302210": "a local-history farm's access ways",
    "way/920900172": "a local-history farm's access ways",
    "way/1171744773": "a description: bridle path",
    "way/1295016681": "a description: cycle path",
    "way/67121023": "a description: cycle path",
    "way/1464183207": "a description: nature trail",
    "way/520074498": "a description: spare path",
    "way/44500668": "a staff footbridge",
    "way/203341552": "a description: underpass",
    "way/456553068": "a training track's service way; already dropped by the leak word",
    "way/456553066": "a training track's service way; already dropped by the leak word",
    "way/456553069": "a training track's service way; already dropped by the leak word",
    "way/331838613": "an address standing in for a name",
    "way/1116504803": "an English lane label, not a street name",
    "way/1363663883": "an English lane label, not a street name",
    "way/1116504806": "an English lane label, not a street name",
    "way/1363663884": "an English lane label, not a street name",
    "way/1116504804": "an English lane label, not a street name",
    "way/1363663885": "an English lane label, not a street name",
    "way/1116504807": "an English lane label, not a street name",
    "way/1363663886": "an English lane label, not a street name",
    "way/214791424": "a numbered quay of a port",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "relation/10753258": "a pool, club, pitch or office tagged a park is dropped by id (settled read call; third list no. 15); held rows settled 2026-10-13",
    "way/173692111": "a garden that is not notable is dropped (leisure=garden rule, 2026-10-07); held rows settled 2026-10-13",
    "way/52564823": "a home is kept only when open to visit or on an article of its own (home rule 2026-10-08; 15 answers no. 2); held rows settled 2026-10-13",
    "relation/10523765": "a code beside a type word is dropped (CODED_TYPE; 14 answers no. 4, planning-code parks); held rows settled 2026-10-13",
    "node/6612200789": "an underwater wreck (owner, 2026-10-13)",
    "node/12569811096": "an underwater wreck (owner, 2026-10-13)",
    "way/35577641": "a description standing in for a name is dropped by id (settled read call; wave 1 precedent); held rows settled 2026-10-13",
    "way/1364242067": "a description standing in for a name is dropped by id (settled read call; wave 1 precedent); held rows settled 2026-10-13",
}
# Kept by id: admitted as rows although a rule passes them over (owner, 2026-10-13;
# docs/decisions_drafts/search-final.md).
PLACE_KEPT = {
    "way/41530300": "'Feskekörka', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
}
