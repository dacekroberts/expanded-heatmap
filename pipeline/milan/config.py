"""Milan-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Step 0 evidence and its checks: docs/build_briefs/milan.md (13/13).

Milan is a SIX-SOURCE build - the most of any city here, ahead of New York's
four - and the six are measurably DISJOINT registers rather than overlapping
views of one. See SOURCES below for why that means no cross-source
deduplication, which runs opposite to New York's decision.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "milan" / "raw"
DATA_PROCESSED = ROOT / "data" / "milan" / "processed"
OUTPUTS = ROOT / "outputs" / "milan"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

# Metro and tram stations together since the tram rescope (owner
# 2026-10-13). TRAM_DIR was a branch-only folder until the landing.
TRAM_DIR = DATA_PROCESSED
STATIONS_CSV = TRAM_DIR / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# One feature per drawn line, written by step 1 from ds539's 31
# alignment variants - which is the shape map_common's GeoJSON loader
# expects, and the reason step 1 rather than step 3 does the selecting.
LINES_GEOJSON = TRAM_DIR / "metro_lines.geojson"

# Raw inputs, all downloaded by fetch_sources.py - deliberately NOT named
# step*.py, so drift_check.py never runs it.
BUSINESSES_RAW_DIR = DATA_RAW
BOUNDARY_GEOJSON = DATA_RAW / "confine_comune.geojson"
METRO_STOPS_GEOJSON = DATA_RAW / "tpl_metrofermate.geojson"
METRO_LINES_GEOJSON = DATA_RAW / "tpl_metropercorsi.geojson"
METRO_SEQUENCE_GEOJSON = DATA_RAW / "tpl_metrosequenza.geojson"
GTFS_ZIP = DATA_RAW / "gtfs.zip"

CKAN = "https://dati.comune.milano.it/api/3/action"

# --- The six registers -------------------------------------------------

# THE SIX ARE SEPARATE REGISTERS OF DIFFERENT ACTIVITIES, NOT OVERLAPPING
# VIEWS OF ONE, AND THAT IS MEASURED: `Codice` is unique within every register
# and there are ZERO collisions between any pair - the prefixes are distinct
# (EV/C-EV, PA/C-PA, AE/C-AE, PE/C-PE, FP/C-FP).
#
# SO THERE IS NO CROSS-SOURCE DEDUPLICATION, which runs opposite to New York.
# multi-source-city says to merge on address AND a normalised name because one
# storefront can hold several licences. Neither half transfers here:
#   - Address cannot be a key at all. 15,613 of 28,131 `vicinato` rows already
#     share an address with another row in the SAME register, and vicinato x
#     pe_in_piano share 4,855 addresses. Milan's buildings hold many premises;
#     merging on address would delete real businesses wholesale.
#   - Name-based merging is unavailable: `insegna` is 17.6% populated and
#     absent entirely from three of the six.
# A shop and a bar at one Milan address are two premises. The residual risk is
# an over-count where one business holds two licences; under-merging is the
# safer error and the city page says so.
#
# `bucket` here IS the classification. `Area di Competenza` is a single clean
# value per dataset at 100%, where every in-dataset classification field is
# 26-64% blank or corrupted by concatenation - so membership is the
# classification, which is multi-source-city's rule in its purest form.
#
# `label_col`: the source's own best field for the tooltip's activity line.
# All of them are dirty, so step 2 normalises case and splits concatenations,
# and falls back to `label_fallback` when blank (26-64% of the food rows).
SOURCES = {
    "vicinato": dict(
        resource="95ef10f2-c825-451d-aa3d-6ff4ed7fd267",
        package="ds49-economia-esercizi-vicinato-sede-fissa",
        rows=28131, bucket="Retail",
        name_col="insegna", label_col="settore_merceologico",
        label_fallback="Neighbourhood shop"),
    "pe_in_piano": dict(
        resource="d70a4002-af24-42db-9ace-00d4a102ccb8",
        package="ds58_economia_pubblici_esercizi_in_piano",
        rows=9269, bucket="Food service",
        name_col="insegna", label_col="tipo_eser_storico_pe",
        label_fallback="Bar or restaurant"),
    "servizi_persona": dict(
        resource="1f7244e8-a6ae-4777-a09f-06a325338be8",
        package="ds62_economia_parrucchieri_estetisti_centri_abbronzatura",
        rows=5732, bucket="Personal services",
        name_col=None, label_col="tipo_eser_pa",
        label_fallback="Personal services"),
    "pe_fuori_piano": dict(
        resource="bdb64cee-0f60-4271-8e35-dcda7a07de33",
        package="ds59-economia-pubblici-esercizi-fuori-piano",
        rows=3799, bucket="Food service",
        name_col="insegna", label_col="settore_storico_pe",
        label_fallback="Bar or restaurant"),
    "artigianato_alim": dict(
        resource="31bedae7-6fc3-473d-bc0f-316d9db9114d",
        package="ds250-economia-artigianato-settore-alimentare",
        rows=1471, bucket="Food service",
        name_col=None, label_col="tipo_eser_ae",
        label_fallback="Artisan food"),
    "panificatori": dict(
        resource="59cb72c3-a810-4f10-afad-9d7d2fe597b9",
        package="ds251-economia-panificatori",
        rows=443, bucket="Retail",
        # A baker's shop is NAICS 445 retail, the same line Dublin's BAKERY
        # takes - not food service, which is consumption on the premises.
        name_col=None, label_col="prevalente",
        label_fallback="Bakery"),
}

# `fuori piano` licenses premises OUTSIDE Milan's commercial plan, and at least
# 15.9% of it is not a public storefront: 472 staff canteens, 132 private
# clubs, 53 parish clubs. Owner's call 2026-09-22: include the register and
# filter what is nameable.
#
# 15.9% IS A FLOOR, NOT THE FIGURE. The `fuori_piano` clause column is 62.4%
# blank, so premises exempted under `art.3 comma 6 lett.*` cannot be classified
# from it at all. The city page must say some non-public premises remain.
FUORI_PIANO_EXCLUDE = ("mensa", "club privato", "circol", "parrocch")

# --- Boundary --------------------------------------------------------------

BOUNDARY_RESOURCE = "f56cb432-83e6-48de-ae30-d39b4be61e85"
BOUNDARY_PACKAGE = "ds2841-confini-amministrativi-del-comune-di-milano"
# One Polygon, 181.8 km2. No multipart dissolve needed - unlike Dublin's
# 90-part layer - and not an async Hub download.
BOUNDARY_AREA_KM2 = (175.0, 190.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 32N: Milan's longitude (~9.19) falls in the 6-12 band. An ordinary
# per-city UTM, derived not copied. Italy's national grids (Monte Mario,
# EPSG:3003/3004) are NOT used, because - unlike Dublin's ITM - no source here
# publishes in them: every register and both rail layers are EPSG:4326.
CRS_PROJECTED = "EPSG:32632"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail ------------------------------------------------------------------

# RAIL IS THE AGENCY'S OWN, AND BOTH osm-rail STEPS WERE RUN. ATM publishes
# metro stations and alignments as SEPARATE layers, both CRS84, plus a GTFS
# whose route_color carries the five official line colours. OSM is not used.
METRO_STOPS_RESOURCE = "dd6a770a-b321-44f0-b58c-9725d84409bb"
METRO_LINES_RESOURCE = "df024fd8-9c4e-4e22-a39e-7e91295b7a7b"
METRO_SEQUENCE_RESOURCE = "2d868218-3a74-4850-ac1c-0a151214577e"
# A stable short URL documented in the dataset's own notes, byte-identical to
# the long resource URL (sha256 matched 2026-09-22).
GTFS_URL = "https://dati.comune.milano.it/gtfs.zip"

# METRO ONLY. The 17 tram routes are NOT drawn - Barcelona excluded its T1-T6
# and Toronto its streetcars, and Milan's trams are a dense street-running
# network whose stops sit one or two blocks apart: San Francisco's Muni Metro
# shape, which needs docs/sub_transit_line_filters.md rather than a line list.
# They would also need 17 invented colours, because `route_color` is populated
# ONLY for the metro. Recorded as a costed extension, not a discard - the
# geometry is in the GTFS `shapes.txt` and the decision is reversible.
#
# THE COLOURS ARE THE AGENCY'S OWN, read from the GTFS `route_color`, so the
# project's rule keeps them even if they score badly against the category pins.
# That is the opposite of Dublin, where `route_color` was empty and the palette
# was therefore this project's to choose.
#
# `route_short_name` IS "1".."5", NOT "M1".."M5" - the M lives only in
# `route_id` and `route_long_name`, so the label is BUILT here, not copied.
LINES = {
    "M1": ("M1", "#ff0000", "M1 (linea rossa)"),
    "M2": ("M2", "#73ff01", "M2 (linea verde)"),
    "M3": ("M3", "#fcff01", "M3 (linea gialla)"),
    "M4": ("M4", "#0000ee", "M4 (linea blu)"),
    "M5": ("M5", "#c876b1", "M5 (linea lilla)"),
}

# The longest alignment variant per line, of ds539's 31, measured 2026-09-22.
# Each is the full end-to-end run; the others are short workings.
LINE_PERCORSI = {
    "M1": "100035",   # 123 verts, 21.16 km, Sesto 1 Maggio FS - Rho Fieramilano
    "M2": "100053",   # 354 verts, 33.25 km, Assago Milanofiori - Gessate
    "M3": "100081",   # 349 verts, 15.63 km, Comasina - San Donato
    "M4": "100164",   # 110 verts, 14.16 km, San Cristoforo - Linate Aeroporto
    "M5": "100084",   # 129 verts, 12.18 km, Bignami - San Siro Stadio
}

# ds535's 130 FEATURES ARE NOT 130 PHYSICAL STATIONS. Interchanges are modelled
# two incompatible ways: four are ONE point carrying both lines (CENTRALE FS
# "2,3", GARIBALDI FS "2,5", ZARA "3,5", SAN BABILA "1,4"), and the rest are
# TWO points needing three different rules. Suffix-strip alone gives 127; the
# aliases below take it to ~125.
#
# A DISTANCE THRESHOLD IS WRONG IN BOTH DIRECTIONS and must not be used:
# WAGNER <-> BUONARROTI at 277 m and DUOMO <-> CORDUSIO at 259 m are genuinely
# different stations, while LORETO M2 <-> LORETO M1 at 231 m are one. This is
# the per-city collapse osm-rail says is never inheritable.
STATION_NAME_SUFFIX = r"\s+M[1-5]$"        # DUOMO M3 -> DUOMO
STATION_ALIASES = {
    "S.AMBROGIO": "SAN AMBROGIO",           # 22 m apart, spelling variant
    "LOTTO FIERAMILANOCITY": "LOTTO",       # 71 m apart, name alias
    "CADORNA FN M1": "CADORNA FN",
    "CADORNA FN M2": "CADORNA FN",
}

# --- Trams (tram rescope, owner 2026-10-13) ---------------------------------

# All 17 ATM tram routes are drawn, one label and one legend row each
# ("Tram N"), on the per-route rule Amsterdam, Brussels and Zurich follow.
# Stops are thinned by docs/sub_transit_line_filters.md, as Toronto's
# streetcars are (pipeline/milan/trams.py). Reasoning and measurements:
# docs/decisions_drafts/tram-rescope.md, "Milan".
TRAM_SHAPES_JSON = TRAM_DIR / "tram_shapes.json"

# The feed's 17 route_short_names (route_type 0). trams.py stops if the feed
# carries another set: a route added or withdrawn is a scope decision.
TRAM_LINES = ("1", "2", "3", "4", "5", "7", "9", "10", "12", "14", "15",
              "16", "19", "24", "27", "31", "33")

# The feed's tram timetable runs 2026-09-14 to 2026-10-02
# (feed_info.txt surface_end_date); the portal still served that edition on
# 2026-10-13. Five routes are on diversion for works in it (2, 4, 7, 14, 16,
# by their own route_long_name) and are drawn as the timetable runs them.
# Re-read when AMAT republishes: docs/recheck_calendar.md.
TRAM_TIMETABLE = ("2026-09-14", "2026-10-02")
# The weekday the 15-minute test is read on (10:00 to 15:00, the busier
# direction). 7 and 33 run exactly every 15.0 minutes and pass.
TRAM_HEADWAY_DAY = "20260930"
TRAM_MAX_HEADWAY_MIN = 15.0

# A stop pattern is regular when it carries at least this share of its
# line's trips; depot runs and short workings fall under it.
TRAM_REGULAR_TRIP_SHARE = 0.10
# The feed has no parent_station; stops of one name are grouped first, then
# by distance, never past MAX_SPREAD (Toronto's measured values).
TRAM_PLACE_LINK_M = 60.0
TRAM_PLACE_CROSS_M = 120.0
TRAM_PLACE_MAX_SPREAD_M = 200.0
# A tram stop this close to a drawn metro station is that station, or within
# the NAMED distance when its name carries the station's ("duomo m1 m3").
TRAM_ATTACH_M = 150.0
TRAM_ATTACH_NAMED_M = 400.0
TRAM_THIN_SPACING_MILES = 0.5

# ATM gives the trams no route_color, so these are the project's, searched
# with pipeline/linecolour.py against the five metro colours and the pins:
# CIE76 45 or more from every pin, 18 or more from every line within 500 m.
# Re-run the search if a line or a metro colour changes.
TRAM_COLOURS = {
    "1": "#8800F8", "2": "#C08068", "3": "#B88888", "4": "#50A800",
    "5": "#0088A0", "7": "#889800", "9": "#C870C8", "10": "#D07800",
    "12": "#00A0C0", "14": "#689000", "15": "#B86000", "16": "#F800D8",
    "19": "#606820", "24": "#00A800", "27": "#7850E8", "31": "#F83800",
    "33": "#F840F0",
}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "milan_source"
RAW_CLASSIFICATION_COLUMN = "attivita"

# NO REGISTER CARRIES A PERSONAL NAME - no titolare, ragione_sociale or
# nominativo in any of the six, confirmed against live headers. This is the
# France/Edmonton pattern: the publisher already did the stripping, so the
# residence-filter work San Diego, Los Angeles and Philadelphia each needed
# does not arise.
#
# `insegna` is a TRADE NAME and is used where present (17.6% / 23.8% / 9.1% on
# the three registers that have it); `Ubicazione` is the fallback and is 100%
# on every source. Because the fallback is an ADDRESS rather than an owner,
# Los Angeles' failure mode cannot occur - there is no person to fall back to.
NAME_FALLBACK_COLUMN = "Ubicazione"

MILAN_BBOX = {
    "lat_min": 45.35,
    "lat_max": 45.56,
    "lon_min": 9.02,
    "lon_max": 9.30,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

# The search area is the map's: the Comune di Milano, relation 44915
# (admin_level 8), the boundary the businesses are cut to (BOUNDARY_GEOJSON).
# All 193 drawn stations sit in it (read from the nord-ovest extract,
# 2026-10-13), so the scope rule adds nothing. The caches are filtered from
# that extract by pipeline/place_extract_fetch.py, no Overpass request.
PLACE_AREA = "(id:3600044915)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("it",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
PLACE_REVIEWED = {
    # OSM node 4895322676, tourism=attraction, with a Wikipedia article of its own.
    "Albergo diurno Venezia": "the 1920s public baths under Piazza Oberdan, a heritage site open to visitors; 'albergo diurno' is a day bathhouse, not lodging",
}
# Stop platforms drawn as footways and named for their stop (highway=footway
# with public_transport=platform or railway=platform), which the street pass
# reads as streets because the stop's name leads with a street word ("V.le
# Sarca Via Chiese"). A platform is no street (docs/place_search_exclusions.md,
# Streets, first row; SKIP_HIGHWAY reads highway=platform only). Listed are
# the 527 ways of the 372 street names whose EVERY cached way is such a
# platform, measured 2026-10-13 on the cache of that date. A rule on the
# platform tag would replace this list (Prague has 20 such names): re-measure
# and remove it when one lands or the cache changes.
_STOP_PLATFORM_WAYS = (
    134765959, 134765978, 136292570, 136292573, 136293669, 137206432, 137206434, 137207549,
    137207550, 137207945, 137208456, 137208459, 137208711, 137208712, 137208713, 137208714,
    137208735, 137208736, 137209406, 137209409, 137209410, 137209411, 137209412, 137209415,
    244137561, 246516158, 247467422, 247467424, 247467539, 247467605, 247469559, 248094182,
    248094364, 248204449, 248204450, 249742789, 249742791, 249743983, 249743984, 249747196,
    250298609, 250298610, 250515941, 250515942, 252061518, 254765326, 254765329, 254765374,
    254765375, 254765418, 254765419, 256998633, 257167910, 257167912, 257168227, 260923805,
    261076201, 265863457, 288813879, 355519433, 365969887, 365969892, 381220781, 381220784,
    386386540, 387912220, 401248527, 401248529, 403677480, 403677482, 423617220, 423617238,
    497436205, 497436210, 498023304, 498023306, 498385018, 498520133, 548544434, 591402145,
    591402146, 669158569, 669158811, 734802316, 845987176, 901095041, 901098025, 941863455,
    941863456, 941863459, 1026953270, 1027033816, 1027047614, 1027047618, 1028076809, 1028104778,
    1028106216, 1028106219, 1030359828, 1034763168, 1042578002, 1046864511, 1046894462, 1047096894,
    1047096895, 1047096896, 1047820141, 1047821150, 1049260558, 1049260854, 1049613331, 1049629195,
    1049629196, 1065105083, 1065456267, 1069219160, 1069221460, 1069266539, 1069266543, 1072681843,
    1072691391, 1072982046, 1072983325, 1072996436, 1073019983, 1073025529, 1078766367, 1078766368,
    1078767272, 1078767843, 1078773689, 1078820405, 1078827445, 1078827598, 1078831605, 1079414369,
    1079414371, 1079414654, 1079421536, 1079432109, 1079460931, 1079983808, 1079994392, 1080004971,
    1080032408, 1080032411, 1080032817, 1080032818, 1080043381, 1080050234, 1080050997, 1080052908,
    1080054096, 1080054930, 1080066858, 1080066929, 1080206423, 1080210602, 1080211744, 1080211990,
    1080212756, 1080214275, 1080216143, 1080219519, 1080236570, 1080236572, 1080236824, 1080236825,
    1080237451, 1080237589, 1080237682, 1080238246, 1080238248, 1080238411, 1080252058, 1080270620,
    1080272175, 1080275020, 1080504100, 1088407970, 1088492081, 1088801809, 1088802519, 1088851912,
    1089029340, 1089081348, 1089081569, 1089081947, 1089430635, 1089430737, 1089431616, 1089433947,
    1089434067, 1089439943, 1089439945, 1090139141, 1090140091, 1090140486, 1090144547, 1090144579,
    1090146393, 1090148211, 1090158707, 1090165463, 1090177890, 1090177892, 1090178489, 1090178598,
    1090186868, 1090186869, 1090186870, 1090186872, 1090206954, 1090230913, 1090231380, 1090237361,
    1090237362, 1090240426, 1090241199, 1090243298, 1090246567, 1090248635, 1090439682, 1090510680,
    1092109480, 1092110161, 1092111802, 1092113494, 1092114535, 1092115878, 1092116068, 1092116612,
    1092117520, 1092121484, 1092125394, 1092125719, 1092126029, 1092126305, 1092126469, 1092126791,
    1092127520, 1092128125, 1092134652, 1092135067, 1092135181, 1092354560, 1092355014, 1092566729,
    1092590613, 1092594711, 1092621075, 1092621076, 1092624012, 1092624667, 1092625503, 1092633795,
    1092633869, 1092634347, 1092634348, 1092638629, 1092641645, 1092641647, 1092642608, 1092643778,
    1092643779, 1092644474, 1092645629, 1092645630, 1092646561, 1092646562, 1092647146, 1092835796,
    1092835872, 1092837090, 1092837306, 1092837724, 1092837934, 1092840158, 1092845308, 1092852856,
    1092853725, 1092855021, 1092855022, 1092855380, 1092864557, 1092870784, 1092883572, 1092890173,
    1092903009, 1093086450, 1093086982, 1093093815, 1093094560, 1093141120, 1093143552, 1093169502,
    1093760262, 1093809712, 1093810330, 1093813854, 1093822567, 1115228995, 1115960402, 1115974449,
    1115974536, 1115975149, 1115977261, 1115977262, 1116003711, 1116227371, 1116227372, 1116227459,
    1116227461, 1116233335, 1116248622, 1116248624, 1116248865, 1116248868, 1116249884, 1116249885,
    1116249886, 1116249974, 1116250032, 1116529388, 1116529390, 1116529392, 1116529394, 1116530250,
    1116531716, 1116896478, 1116896480, 1116896482, 1116896484, 1116896485, 1116896513, 1116897754,
    1116899442, 1116910423, 1116911546, 1118028192, 1118920287, 1121713932, 1128429963, 1128433475,
    1128447577, 1128452764, 1128464923, 1128541734, 1134762348, 1135438559, 1144666890, 1148010447,
    1148226677, 1148442028, 1148442029, 1148443026, 1148443029, 1148443853, 1148443854, 1148446981,
    1148446982, 1151964176, 1153992768, 1153992770, 1154282842, 1154284734, 1154286575, 1154286971,
    1154288215, 1154288680, 1154511089, 1154513650, 1155983397, 1180104613, 1183418698, 1184412398,
    1184413048, 1184455791, 1185977162, 1186695389, 1186698078, 1190138592, 1190138593, 1190170198,
    1190170964, 1190555396, 1190557614, 1190606908, 1190608078, 1190619180, 1195080703, 1204918329,
    1204928507, 1204929606, 1205710412, 1205714809, 1205716660, 1205716911, 1205717552, 1205728785,
    1205733757, 1205733885, 1205745665, 1205745667, 1205881063, 1205885081, 1205885723, 1205885725,
    1205891086, 1205898635, 1205899163, 1206846271, 1206865912, 1206868587, 1206868683, 1206870664,
    1206870665, 1206872435, 1206872879, 1206873078, 1206874636, 1206875278, 1206879350, 1206881537,
    1206888027, 1206888029, 1206916471, 1206916473, 1207187498, 1207712989, 1207750481, 1207753650,
    1207755977, 1207758240, 1208716215, 1208716481, 1208716550, 1208716588, 1208804973, 1208805047,
    1208808238, 1208808536, 1208808876, 1208812542, 1209009148, 1209023783, 1209031526, 1209033522,
    1209033524, 1209064992, 1209076799, 1209080709, 1209087611, 1209099889, 1209101809, 1209103769,
    1209104694, 1209108975, 1209339928, 1209341466, 1209341467, 1209360187, 1209362012, 1209414890,
    1209697200, 1209698123, 1209703825, 1209704008, 1209708083, 1209708589, 1209734635, 1209735392,
    1209736079, 1211224594, 1211224696, 1211249008, 1211263778, 1211769774, 1211769776, 1211770216,
    1211771760, 1211772062, 1211834013, 1212455611, 1212456030, 1212457691, 1212457862, 1212457951,
    1212504418, 1212980680, 1212985229, 1215020751, 1216793293, 1216797751, 1217711171, 1217973366,
    1217981152, 1217982296, 1217987337, 1218042654, 1218042655, 1218517501, 1240719444, 1240721035,
    1240721236, 1240721363, 1240721645, 1240722217, 1244856743, 1331650739, 1349804710, 1349804994,
    1349806429, 1349841561, 1350939390, 1350943822, 1351211577, 1351584569, 1351851387, 1351856612,
    1351906502, 1351906809, 1351907245, 1351909198, 1351909200, 1396702221, 1396702223,
)
# OSM objects a reading by eye found that no rule in place_index.py catches,
# each with why (place_index.build, `dropped`).
PLACE_DROPPED = {
    **{f"way/{i}": "a stop platform drawn as a footway and named for its stop" for i in _STOP_PLATFORM_WAYS},
    "way/1210693372": "'Area esterna', a description (outside area) on a park; a description goes by id (owner, 2026-10-11)",
    "node/12278859101": "'ricostruzione di sarcofago romano con coperchio originale', a description standing in for a name (owner, 2026-10-11)",
    "node/11701168833": "'Nuova Zona Residenziale', a description (new residential zone) on a neighbourhood node (owner, 2026-10-11)",
    "node/487236104": "'Molino della Torretta / Casa di Maurizio', a locality named as a person's house; a place named for a home is out (exclusions, Neighborhoods)",
    "node/4127952389": "a place of worship named only by its body, Chiesa di Gesu Cristo dei Santi degli Ultimi Giorni, no article (fifth pass; sixth pass, ruling 2; the Italian list does not hold it)",
    "node/4129960591": "a place of worship named only by its body, the same name as node 4127952389 (fifth pass; ruling 2)",
    "way/317741575": "a place of worship named only by its body, the same name as node 4127952389 (fifth pass; ruling 2)",
    "node/252641374": "a place of worship named only by its denomination, Chiesa Cristiana Avventista del Settimo Giorno, no article (fifth pass; ruling 2)",
    "node/308832288": "a place of worship named only by its denomination, Chiesa Evangelica Metodista, no article (fifth pass; ruling 2)",
    "way/39600109": "a place of worship named only by its denomination, Chiesa Neo-apostolica, no article (fifth pass; ruling 2)",
    "way/498032877": "a place of worship named only by its denomination, Chiesa Cristiana Evangelica Pentecostale, no article (fifth pass; ruling 2)",
    "way/381749179": "a place of worship named only by its body, Chiesa Evangelica ADI, no article (fifth pass; ruling 2)",
    "node/4895158258": "a place of worship named only by its body, Chiesa Cristiana Evangelica delle Assemblee di Dio in Italia, no article (fifth pass; ruling 2)",
    "node/5033959323": "a place of worship named only by its body, Chiesa di Cristo, no article (fifth pass; ruling 2)",
    # The owner's rulings on the read of 2026-10-13 ("all approved"), each id checked against its cached name.
    "relation/7147393": "'Casa Castini', a historic building named as a house, no article of its own (owner, 2026-10-13)",
    "way/483746402": "'Casa Cicchieri', a historic building named as a house, no article of its own (owner, 2026-10-13)",
    "way/434686810": "'Casa Pirovano', a historic building named as a house, no article of its own (owner, 2026-10-13)",
    "relation/383081": "'Casa Rovida', a historic building named as a house, a Wikidata entry and no article (owner, 2026-10-13)",
    "relation/5230029": "'Casa del Cedro', a historic building named as a house, a Wikidata entry and no article (owner, 2026-10-13)",
    "way/40500643": "'Casa a Igloo', a house whose article and entry are the Maggiolina quarter's, not its own (owner, 2026-10-13)",
    "node/5012707146": "'Cascina Gobba', a tram stop closed in 1978, disused:railway=tram_stop (owner, 2026-10-13)",
    "node/5012719007": "'Cimiano', a tram stop closed in 1978, disused:railway=tram_stop (owner, 2026-10-13)",
    "node/5012706744": "'Crescenzago', a tram stop closed in 1978, disused:railway=tram_stop (owner, 2026-10-13)",
    "node/5012719006": "'Molino / Deposito Molino Nuovo', a tram stop closed in 1978, disused:railway=tram_stop (owner, 2026-10-13)",
    "way/1315555952": "'East Garden (ex De Nora)', a development's brand as a place (owner, 2026-10-13)",
    "node/7739405052": "'La Viridiana', a development's brand as a place (owner, 2026-10-13)",
    "node/12321144590": "'Giunglabuca', a nickname for a lot beside a development, as a place (owner, 2026-10-13)",
    "way/1046937862": "'EuroMilano', a developer's name as a place (owner, 2026-10-13)",
    "relation/7350160": "'Milano 2', outside the Comune di Milano (owner, 2026-10-13)",
    "relation/6589616": "'Pero', outside the Comune di Milano, its own municipality (owner, 2026-10-13)",
    "way/637300770": "'Armenia Films', a company's name on a park (owner, 2026-10-13)",
    "node/5355438258": "'Hayabusa Reiki Dojo', a business tagged a place of worship (owner, 2026-10-13)",
    "node/13185691618": "'Lanciatore Vega', an exhibit under its kind's Wikidata entry (owner, 2026-10-13)",
    "way/49876675": "'PalaSharp', a venue closed in 2011, end_date behind the cache (owner, 2026-10-13)",
    "relation/8254358": "'Tranvia Milano-Lodi', a closed tramway as a route relation (owner, 2026-10-13)",
    "node/11368588671": "'Precotto (Interno deposito)', a tram stop inside the depot (owner, 2026-10-13)",
    "node/9353157893": "'Chiesa di San Dionigi in Santi Clemente e Guido', a grotto and memorial under the church's name; the church is way 35839780 (owner, 2026-10-13)",
    "relation/6708199": "'Cassina Triulza', a second row for Cascina Triulza, node 4499103326, one Wikidata entry (owner, 2026-10-13)",
    "way/404140241": "'Ronchetto Sul Naviglio', a second row for the node Ronchetto sul Naviglio (owner, 2026-10-13: true duplicates only)",
    "way/404140229": "'Parco Sempione', a census area repeating the park's own landmark row (owner, 2026-10-13: true duplicates only)",
    "way/1389243680": "'Stadio San Siro Milano', a second row for the stadium, Stadio Giuseppe Meazza (owner, 2026-10-13)",
    "way/1528994787": "'Giardino Gonin Giordani', the second of two rows for one garden, just past the merge distance (owner, 2026-10-13)",
    "way/330106398": "'Giardino Mario Capponi', the second of two rows for one garden, just past the merge distance (owner, 2026-10-13)",
    "way/4017879": "'Parco di via Dezza', the second of two rows for one park, just past the merge distance (owner, 2026-10-13)",
    "node/10676509698": "'Circo Romano', a second row for way 421120725, one Wikidata entry (owner, 2026-10-13)",
}
