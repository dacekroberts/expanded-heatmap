"""Riga-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Latvia's first city; the brief is docs/build_briefs/riga.md. Amsterdam's and
Rotterdam's two-layer shape:

  * FOOD SERVICE from the State Revenue Service's (VID) excise-licence register -
    the premises licensed to sell alcohol or tobacco, with a place type (café,
    bar, restaurant...) - placed by joining the address to Riga's own address
    points. The register's holder and tax-number columns are NEVER read.
  * SHOPS AND SERVICES from the State Land Service's (VZD) cadastre premise
    groups of use class 1230 whose name reads as a shop, placed at their
    building's footprint by cadastre number.

Rail: Rīgas satiksme's seven tram routes, from its own GTFS (CC0, monthly),
thinned like Amsterdam's and Rotterdam's. No suburban rail (owner).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "riga" / "raw"
DATA_PROCESSED = ROOT / "data" / "riga" / "processed"
OUTPUTS = ROOT / "outputs" / "riga"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (all keyless, on data.gov.lv; downloaded by fetch_sources.py) --
# data.gov.lv's CKAN lives at /dati/api/3/action/, not /api/3/.
CKAN_API = "https://data.gov.lv/dati/api/3/action/"
DL = "https://data.gov.lv/dati/dataset/"
SOURCES = {
    # key: (url, local file) - the owner approved each download 2026-09-24
    "excise": (DL + "a1adb6dd-a4a1-41c9-9177-c1cd942e012e/resource/f88cd5ea-61b0-42e8-a0a8-25504dfbcdc9/"
               "download/pdb_akclicences_odata.csv", "pdb_akclicences_odata.csv"),
    "premise_groups": (DL + "be841486-4af9-4d38-aa14-6502a2ddb517/resource/5d8b1cfa-1e67-4b77-a6ac-b4e37eba0d7e/"
                       "download/premisegroup.zip", "premisegroup.zip"),
    "cadastral_map": (DL + "b28f0eed-73b0-4e44-94e7-b04b11bf0b69/resource/bf88b763-98b8-445d-a51f-b76f45c362c5/"
                      "download/0001000_kk_shp.zip", "0001000_kk_shp.zip"),
    "address_points": (DL + "4e2bd2d1-69e1-4598-b2f0-713e963e55e3/resource/7fc97d43-2c34-4301-8776-a5682273115e/"
                       "download/adreses.gpkg", "adreses.gpkg"),
    "neighbourhoods": (DL + "ddc24ef1-4db4-46ce-a035-258b6ed69d91/resource/7c652b48-c5ca-44a9-8dd2-32e869253f29/"
                       "download/apkaimes.gpkg", "apkaimes.gpkg"),
    "degrading_buildings": (DL + "9789c471-5751-4b20-87ac-7aba43c42f8b/resource/b9521b89-d158-4884-8e6d-c60873cf5241/"
                            "download/vidi_degradejosas_buves.gpkg", "vidi_degradejosas_buves.gpkg"),
}
# The GTFS is a new resource every month; fetch_sources.py takes the newest
# `marsrutusaraksti*.zip` in this dataset and records which.
GTFS_DATASET = "6d78358a-0095-4ce3-b119-6cde5d0ac54f"
GTFS_ZIP = DATA_RAW / "gtfs_rigas_satiksme.zip"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# The cadastre and the address points arrive in LKS-92 / Latvia TM.
CRS_SOURCE_LV = "EPSG:3059"
# UTM zone 35N: Riga's longitude (~24.1) falls in the 24 to 30 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32635"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# All seven tram routes (owner), by the feed's route_short_name. OSM's route 8a
# is in neither the feed nor the operator's list and is not drawn.
LINE_ORDER = ["1", "5", "7", "8", "10", "11", "14"]
LINE_NAMES = {s: f"Tram {s}" for s in LINE_ORDER}
# THIS PROJECT'S colours (owner, 2026-09-24): Rīgas satiksme's feed and OSM
# give every tram line the same red (#FF000C), and its only tram map is dated
# 2 September 2013. Chosen apart from each other and from the two business
# categories; check_line_colours and check_map_markup measure them.
# SHOPS AND SERVICES VIOLET (#7e57c2, 2026-10-07) arrived later: tram 8's
# #9467bd sat 14.0 from it, under the owner's floor of 20 (2026-10-07), and
# moved to #b480cc, a lighter violet: the colour nearest its own that reads
# 3:1 on both pages and clears 25 from both pins and 18 from every other line
# (violet 25.0, between 20 and 45: an accepted trade; nearest line tram 7
# 52.6).
LINE_COLOURS = {"1": "#d62728", "5": "#ff7f0e", "7": "#8c564b", "8": "#b480cc",
                "10": "#17becf", "11": "#6b8e23", "14": "#e6ac00"}
# A stopping pattern counts as regular when it runs this share of a route's
# trips in one direction; depot runs and one-off diversions fall below it.
PATTERN_MIN_SHARE = 0.10
COLLAPSE_MAX_SPREAD_M = 300.0
# Two differently named places closer than this, sharing a line and served in
# opposite directions, are one stop (step 1).
ALIAS_MAX_M = 60.0
SPACING_MIN_M = 200.0
THIN_SPACING_MILES = 0.5

# Gate 3: each route's stops as Rīgas satiksme's timetable lists them, against
# the build's stations per route BEFORE thinning (step 1 compares there; the
# thinning to one stop per THIN_SPACING_MILES is the owner's call and the only
# reason the drawn set is smaller - after it, 1 draws 32, 8 36, 10 15, 11 19,
# and 5, 7 and 14 all theirs). Distinct stops over both directions of the main
# terminal-to-terminal variants, reconciled where the difference is known:
OPERATOR_STATION_COUNTS = {
    # 37 stops each way; 39 names, because two stops carry a different name in
    # each direction (K.Barona iela / Brīvības iela, Jūrmalas gatve / Kurzemes
    # prospekts), which step 1 merges by its measured rule (ALIAS_MAX_M).
    "1": 37,
    "5": 34,       # 34 each way, the same 34
    "7": 23,       # 23 each way; 24 names, Autoosta / Centrāltirgus one stop
    # 37 each way on Mīlgrāvis - Tapešu iela, plus Stacijas laukums: the
    # terminus of route 8's Stacijas laukums - Tapešu iela short working, which
    # the timetable lists as a variant of route 8 and which runs at least
    # PATTERN_MIN_SHARE of a direction's trips, so step 1 keeps it.
    "8": 38,
    # 18 one way, 16 the other, 20 names; Jelgavas iela and Jelgavas iela/Bērnu
    # slimnīca are one stop named per direction (merged in step 1).
    "10": 19,
    "11": 23,      # 22 one way, 23 the other
    "14": 33,      # 33 each way; 34 names, Autoosta / Centrāltirgus one stop
}
OPERATOR_COUNTS_SOURCE = (
    "Rīgas satiksme's tram timetable as 1188.lv (Tet's directory) republishes it, "
    "one page per route variant: www.1188.lv/satiksme/pilsetas/riga/ routes 2313 "
    "(1), 116 (5), 118 (7), 3602 (8), 120 (10), 121 (11), 3603 (14), read "
    "2026-10-01 - SECONDARY. The operator's own timetable host, "
    "saraksti.rigassatiksme.lv, did not answer (2026-10-01), and its only "
    "per-route publication outside the feed is a route-scheme PDF with no stop "
    "list to read (rigassatiksme.lv/files/06_1_tramvaju_marsruts_shema.pdf). "
    "Latvian Wikipedia's per-route articles agree on 1, 7, 11 and 14 but are "
    "stale on 5 (35, pre-renaming names) and were not used.")
# The union of Riga's 58 neighbourhoods: measured 304.0 km2 (= OSM 13048688).
CITY_AREA_KM2 = (300.0, 308.0)
LINE_SHAPES_JSON = DATA_PROCESSED / "line_shapes.json"

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "riga_source"
RAW_CLASSIFICATION_COLUMN = "activity"

# --- Layer 1: the excise register (food service) ------------------------------
# Columns are selected BY EXACT NAME. `Nodoklu_maksatajs` (the licence holder,
# who may be a person) and `NMR_kods` (tax number) are never read - step 2
# asserts they are absent.
EXCISE_COLUMNS = ["Statuss", "Darbibas_vietas_tips", "Darbibas_vietas_adrese", "Darba_laiks",
                  "Darbiba_uzsakta_darbibas_vieta", "Darbiba_izbeigta_darbibas_vieta"]
EXCISE_NEVER = ("Nodoklu_maksatajs", "NMR_kods")
EXCISE_CURRENT = "Spēkā"
# Place types that are food service. The brief's earlier pattern also matched
# viesn|hotel; hotels are lodging, so they are out.
FOOD_RE = r"kafejn|restor|bār|bistro|ēdn|krog|pub\b|picērij|ēdin|klub|kafe|suši|burger|grill"
# "Strēlnieku iela 1B - 12": the unit after the dash is dropped for the second join stage.
UNIT_SUFFIX_RE = r"\s+-\s*\d+[A-Za-z]?$"

# --- Layer 2: the cadastre premise groups (shops and services) ----------------
CADASTRE_NS = "{http://ivis.eps.gov.lv/XMLSchemas/100007/CadastreRegistry/v1-0}"
TRADE_USE_KIND = "1230"
# The staging session's name rules for class 1230 (reprobes/riga/pg_classify.py,
# 2026-09-24), in order - FIRST MATCH WINS, so "veikals-kafejnīca" is a shop and
# "frizētava" a service. Kept: shop_retail and personal_service ("Shops and
# services"). Dropped: fuel, wholesale and storage, food (the excise register is
# the food layer), gambling, offices, residential, ancillary and generic names.
# Three changes on 2026-09-29 (owner, DECISIONS "Category check: the owner's
# calls"): fuel stations are KEPT (R4 keeps them everywhere; they were dropped
# with no stated reason); repair workshops, shoe and key repair and sewing
# (remont, darbnīc, apavu, atslēg, šūšan) moved out of personal_service into
# a dropped class of their own (repairs are out everywhere); and stands
# (stends, ^lete) moved out of shop_retail into a dropped class ahead of it -
# a stand is a stall. Market pavilions (tirgus, paviljon) and kiosks stay:
# buildings of fixed shops, and small walk-in shops.
NAME_RULES = [
    ("fuel", r"degviel|uzpild|dus\b|gāzes"),
    ("wholesale_storage", r"noliktav|^vairumtirdzniecība$|^vairumtirdzniecības (bāze|noliktava)|sklad|glabātuv|angār"),
    ("food_service", r"kafej|restorān|bār(s|a)\b|ēdnīc|picērij|bistro|krog|ēdināš|kafetēr|konditorej|ceptuv"),
    ("repair", r"šūšan|remont|darbnīc|apavu|atslēg"),
    ("personal_service", r"frizētav|frizier|skaistumkop|kosmēt|solārij|pirt|sauna|masāž|nagu|manikīr|salons? ?- ?frizētava|veļas|tīrītav|ķīmisk|foto|lombard|spa\b"),
    ("gambling", r"spēļu|azart|kazino|loto"),
    ("stall", r"stends|^lete"),
    ("shop_retail", r"veikal|tirdzniec|aptiek|kiosk|paviljon|salon|mazumtirdz|tirgus|tirdzn|autosalon|grāmat|zied|optik|pārtik|preču|butik|magazin"),
    ("office", r"birojs|biroj|administrat"),
    ("generic_nonres", r"nedzīvojam|neapdzīvoj"),
    ("residential", r"dzīvok|dzīvojam"),
    ("reverse_vending", r"taromāt|taras"),
    ("technical_or_ancillary", r"tehnisk|pagrab|saimniecīb|nojume|garāž|palīgtelp|koridor|kāpņ|sanmezgl|katlu|tualet|ventkamer"),
    ("generic_commercial", r"komerc|nedzīvojam|neapdzīvoj|telpu grupa|telpas$|telpa$|kompleks|vairumtirdzniecības un mazumtirdzniecības"),
]
NAME_KEEP = ("shop_retail", "personal_service", "fuel")
# The kind each kept class shows as (the tooltip's "Kind").
NAME_KIND = {"shop_retail": "Shop", "personal_service": "Service", "fuel": "Fuel station"}

RIGA_BBOX = {"lat_min": 56.85, "lat_max": 57.09, "lon_min": 23.93, "lon_max": 24.33}
