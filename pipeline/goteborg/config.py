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
SPACING_MIN_M = 60.0
# Owner call 21's stub test: a line drawn to its end must keep at least half
# its stops inside the city.
STUB_MIN_SHARE = 0.5
STUB_LINES = ("4", "12")

# Gate 3: Västtrafik's own stops per line, from each line's timetable PDF
# (page 1's stop columns, both directions), the whole line before the kommun
# split (4's and 12's Mölndal stops included). A tram step 1 stops on a
# mismatch, but FIVE LINES DISAGREE and the cause is in OSM, so the stop is
# commented out in step 1 until the cleanup session takes it to the owner:
# OSM's relations leave out a stop the line's timetable serves. The station is
# drawn and ringed in each case (it is on other lines' relations, and
# Västtrafik gives it one stop code across the lines); what is missing is the
# line on its label.
OPERATOR_STATION_COUNTS = {
    "1": 28,
    "2": 28,   # MISMATCH (cause found, not fixed): build 27. Drottningtorget (stop 002135, platforms A3/A6) is in line 2's timetable, not on OSM's line-2 relations
    "3": 29,
    "4": 21,   # MISMATCH (cause found, not fixed): build 20. Korsvägen (003980, A2/A3) is in line 4's timetable, not on OSM's line-4 relations
    "5": 33,
    "6": 46,   # MISMATCH (cause found, not fixed): build 45. Korsvägen (003980, B1/B2) missing from OSM's line-6 relations
    "7": 35,
    "8": 25,   # MISMATCH (cause found, not fixed): build 24. Korsvägen (003980, B1/B2) missing from OSM's line-8 relations
    "9": 21,
    "10": 13,
    "11": 35,
    "12": 18,
    "13": 21,  # MISMATCH (cause found, not fixed): build 20. Korsvägen (003980, B2) missing from OSM's line-13 relation
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
PERSON_NAMED = (
    "Abo Wadea", "Anders Gullberg", "Anshu Lodha", "Astrid Gustafsson", "Batoul Rammal",
    "Diana Afro", "Juan Font", "Kamel Nassim", "Lib-Wam Leslaw Mielniczuk", "Naji Ayoub",
    "Radhika Khaterpal", "Ramona Bejat", "Traktör Mikael Sande",
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
