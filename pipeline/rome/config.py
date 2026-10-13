"""Rome-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Italy's second city and nothing like its first: Milan reads six premises
registers from its own portal, Rome ONE - Roma Capitale's SUAP register of
productive activities, which records premises by the city's own street code
and civic number with no coordinates - JOINED to ANNCSU, Italy's national
house-number archive, which carries the same street code with WGS84 points.
No geocoder. Brief: docs/build_briefs/rome.md.
"""

from pathlib import Path

SLUG = "rome"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "rome" / "raw"
DATA_PROCESSED = ROOT / "data" / "rome" / "processed"
OUTPUTS = ROOT / "outputs" / "rome"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

SUAP_CSV = DATA_RAW / "opendata_suap_luglio_2025.csv"
ANNCSU_ZIP = DATA_RAW / "indirizzario_lazio.zip"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
OSM_RAIL_JSON = DATA_RAW / "osm_rail.json"
OSM_NEIGHBOURS_JSON = DATA_RAW / "osm_neighbour_comuni.json"
OSM_FOOD_JSON = DATA_RAW / "osm_food_control.json"
# Tram 8 (the tram rescope, 2026-09-27): its own small fetch, so the metro
# cache above is untouched. BOTH candidate relation pairs are fetched - the
# base service and the "8 prolungato" - and step 1 keeps the pair that
# config.TRAM_8_RELATIONS names, chosen against the GTFS's route 8.
OSM_TRAM8_JSON = DATA_RAW / "osm_tram8.json"
TRAM_8_CANDIDATE_RELATIONS = (385213, 1674659, 5376334, 5376335)

# --- Endpoints ---------------------------------------------------------------

# SUAP's "Elenco delle attività produttive", monthly files; JULY 2025 IS THE
# NEWEST and no 2026 dataset exists (brief, measured 2026-09-24).
SUAP_URL = ("https://dati.comune.roma.it/catalog/it/dataset/94848d96-0197-486b-b143-485f00285928/"
            "resource/3fc5fd67-6ed5-428a-88c4-cf5245f9ec0f/download/opendata_suap_luglio_2025.csv")
# ANNCSU's Lazio address list. It refuses HEAD (403) and answers GET; the
# file inside names its own date (indirizzarioLazio<yyyymmdd>.csv).
ANNCSU_URL = "https://anncsu.open.agenziaentrate.gov.it/age-inspire/opendata/anncsu/getds.php?INDIR_LAZI"

# --- Scope ---------------------------------------------------------------------

ISTAT_COMUNE = "058091"
# OSM relation 41485, "Roma", admin_level 8, ref:ISTAT 058091 - a bounded
# name search's only candidate. The comune is 1,287 km² and includes Ostia.
OSM_BOUNDARY_RELATION = 41485
BOUNDARY_AREA_KM2 = (1250, 1320)

# The comune runs from Ostia (41.7 N) to Cesano (42.1 N); padded slightly.
ROME_BBOX = {"lat_min": 41.60, "lat_max": 42.18, "lon_min": 12.20, "lon_max": 12.90}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 33N: longitude ~12.49 falls in the 12-18 E band. Derived per city.
CRS_PROJECTED = "EPSG:32633"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail ------------------------------------------------------------------------
#
# THE RAIL SOURCE IS OPENSTREETMAP, on a recorded ground (osm-rail's order is
# agency GIS layers, then agency GTFS, then OSM) - PUT TO THE OWNER 2026-09-24:
#   * Roma Mobilità's static GTFS is AMBIGUOUS IN A WAY THAT MATTERS
#     (`licence-read`, 2026-09-24): its own open-data page says the data "possono
#     essere utilizzati ... esclusivamente a titolo di supporto al viaggio" (only
#     as travel support) and reserves action against "utilizzo improprio", and
#     the one file carries five inconsistent licence declarations - CC BY-SA
#     with no version, "Licenza Sconosciuta", CC BY 4.0 by harvest. Not
#     resolved in the project's favour; not used.
#   * RSM's own ArcGIS metro layers are CC BY 4.0 but last edited 2023-05-19:
#     Metro C stops at San Giovanni, missing Porta Metronia and Colosseo - Fori
#     Imperiali (opened 2025-12-16).
#   * OSM (ODbL, notice 1) carries all four lines to the current termini.
RAIL_SOURCE_GROUND = "agency GTFS terms ambiguous; agency GIS layers stale (Metro C)"

# OSM relation ids, both directions per line. B1 is tagged ref "B" in OSM (its
# relations end at Jonio), so lines are keyed on RELATION IDS, never on ref.
LINE_RELATIONS = {
    "A": (207973, 1720955),
    "B": (207926, 1720959),
    "B1": (2172804, 2172805),
    "C": (398053, 2172845),
    "RV": (387417, 1721478),
    # TRAM 8 (the tram rescope, 2026-09-27): the BASE service, Casaletto -
    # Venezia, 16 stops. Chosen against the GTFS's route 8 (read only as a
    # check, its terms being ambiguous): 2,985 of 3,207 trips (93%) run the
    # 16-stop pattern, the "8 prolungato" to Porta Maggiore about 213.
    "8": (385213, 1674659),
}
LINE_ORDER = ("A", "B", "B1", "C", "RV", "8")
LINE_NAMES = {"A": "Metro A", "B": "Metro B", "B1": "Metro B1", "C": "Metro C",
              "RV": "Roma–Viterbo", "8": "Tram 8"}
# Where each relation is read from: the metro cache, or tram 8's own.
TRAM_LINES = frozenset({"8"})
# COMMUTER RAIL, MEASURED AGAINST THE PUBLISHED TEST - the owner's call of
# 2026-09-24: draw it where it runs at metro spacing and frequency in districts
# the metro does not reach (Dublin's DART, Copenhagen's S-tog), not by who runs
# the trains. Both COTRAL lines lie wholly inside the comune:
#   * Roma-Viterbo's URBAN service, Flaminio-Montebello (387417/1721478) -
#     DRAWN: 15 stations, median 895 m apart (S-tog 1,227 m), every 10-15
#     minutes, "servizio di tipo metropolitano" (it.wikipedia, read
#     2026-09-24), and 14 of its 15 stations have no metro within 800 m. Only
#     the urban relations are kept; the line beyond Montebello is regional.
#   * Metromare, the Roma-Lido railway (208013/1721156, tagged route=subway) -
#     LEFT OUT: median 2,171 m apart, gaps to 3.97 km, every 15-20 minutes in
#     July 2026 (the 10-minute service promised for March 2026 had not
#     started) - though 11 of its 14 stations, Ostia's and Acilia's, have no
#     metro nearby, which the page says.
# Always out: OSM's "Metro D" (2703073, a line not yet built - no stops) and
# Palestrina's scala mobile.
LEFT_OUT_RELATIONS = {208013: "Metromare", 1721156: "Metromare",
                      2703073: "Metro D (not built)", 2581270: "Palestrina escalator",
                      2581271: "Palestrina escalator",
                      5376334: "8 prolungato (7% of route 8's trips)",
                      5376335: "8 prolungato (7% of route 8's trips)"}
# Trams 2, 3, 5, 14 and 19 are NOT fetched: 0 trips in the GTFS (19 is not in
# it at all), bus-replaced during works (spec, 2026-09-27). Tram 3 is the
# exception on the street: ATAC reactivated it on 7 September 2026, Trastevere
# to Porta Maggiore, buses still covering Porta Maggiore - Valle Giulia (ATAC's
# tram status page, read 2026-10-03). The cached GTFS (built 2026-09-24,
# calendar 2026-09-17 to 2026-12-06) still has 0 trips on route 3, and no tram
# 3 relation is cached, so drawing it waits on a fresh fetch and the owner's
# call (docs/recheck_calendar.md: the whole network is due back by 23 Nov).

# OSM's colours, ATAC's brand colours (A orange, B blue, C green). B and B1
# share one blue, and this project's check refuses two lines under Delta-E
# 10, so B1 moves in HSL lightness only by the smallest step that clears 13 -
# Amsterdam's and Oslo's rule: #3783C6 -> #629ed3 (L +0.11), 13.7 from B.
# Roma-Viterbo is OSM's own #7e7bb4, unchanged: 19.4 from B, 21.2 from B1,
# 25.8 from the Retail pins.
LINE_COLOURS = {"A": "#F68B1F", "B": "#3783C6", "B1": "#629ed3", "C": "#008751",
                "RV": "#7e7bb4", "8": "#bfdf14"}   # 8: OSM's = ATAC's

# Step 1 writes the kept relations here for step 3, with B1 relabelled and cut
# to its OWN ways (Bologna to Jonio): OSM tags it ref "B", and its relations
# run the whole trunk to Laurentina, which would lay B1 on top of B.
OSM_LINES_JSON = DATA_PROCESSED / "osm_lines.json"

# One interchange under two names: ATAC's Colosseo (B) and Colosseo - Fori
# Imperiali (C), connected underground. Wikipedia's 74 stations network-wide
# counts it once.
STATION_NAME_ALIASES = {"Colosseo – Fori Imperiali": "Colosseo"}

# Gate 3: English Wikipedia's "Rome Metro" (read 2026-09-24, SECONDARY): A 27,
# B 26 including B1's four, C 24, network 74.
OPERATOR_STATION_COUNTS = {"Metro A": 27, "Metro B + B1": 26, "Metro C": 24,
                           "Metro (network)": 74, "Roma–Viterbo (urban)": 15,
                           "Tram 8": 16}
OPERATOR_COUNTS_SOURCE = ("en.wikipedia.org/wiki/Rome_Metro, read 2026-09-24 - secondary; "
                          "A 27, B 26 (with B1), C 24, network 74. "
                          "it.wikipedia.org/wiki/Ferrovia_Roma-Civita_Castellana-Viterbo, "
                          "read 2026-09-24 - secondary; the urban section's 15 stations. "
                          "Tram 8: the cached Roma Mobilità GTFS, route 8's base pattern, "
                          "16 distinct stop names (read 2026-09-27, as a check only)")
SPACING_MIN_M = 400.0
COLLAPSE_MAX_SPREAD_M = 400

# TRAM 8 IS THINNED, San Francisco's filter as Amsterdam and Rotterdam run it
# (docs/sub_transit_line_filters.md): measured 2026-09-27, its 16 stops sit a
# median 322 m from the next (min 144, Arenula's two), and 15 of 16 are more
# than the 966 m outer ring from any metro or Roma-Viterbo station - the
# street-running offshoot shape the filter was written for. One stop per half
# mile along the line, every terminus and every interchange kept.
THINNED_LINES = ("8",)
THIN_SPACING_M = 0.5 * 1609.344

# --- Business filtering ------------------------------------------------------

TAXONOMY_SYSTEM = "rome_suap"
RAW_CLASSIFICATION_COLUMN = "activity"
CITY_KEEP = "ROMA"   # kept for the scaffold's templates; the register is Roma Capitale's own

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600041485)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("it",)
PLACE_FOLD = None
PLACE_REVIEWED = {}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "node/888509033": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/126527506": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/575661620": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "node/11005533027": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/582366065": "a denomination or its hall type as the whole name (owner, 2026-10-13)",
    "way/44639492": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/44639497": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/44639637": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/44639639": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/191484464": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/191484540": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/204145793": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/687345945": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/732744103": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/801343349": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/803364166": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/825461228": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/989513354": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/998191511": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/998191562": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/998191644": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/1002990317": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/1005832772": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/1006455125": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/1006628589": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/1050857480": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/1050857483": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/1072072260": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/1072072267": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/1072583143": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/1145454396": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/801351285": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/801351287": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/842260575": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/842260577": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/842351343": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/998191581": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/1000800330": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/1000800331": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/367242223": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/781950837": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/835565684": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/837026530": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/317695840": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/997532434": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/167270558": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/191477264": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/191477266": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "way/191477271": "one segment of a monument that keeps one row (owner, 2026-10-13)",
    "node/10106139087": "an excavation plot code as the name (owner, 2026-10-13)",
    "node/10106139089": "an excavation plot code as the name (owner, 2026-10-13)",
    "node/10274653605": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/1009198674": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/1069797006": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/1069797030": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/1069797331": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/965094788": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/965052524": "an excavation plot code as the name (owner, 2026-10-13)",
    "node/9311460884": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/1009195803": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/1009198671": "an excavation plot code as the name (owner, 2026-10-13)",
    "node/10111875136": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/1069678047": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/1069678048": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/1069678049": "an excavation plot code as the name (owner, 2026-10-13)",
    "node/8927332517": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/982027344": "an excavation plot code as the name (owner, 2026-10-13)",
    "node/10312862776": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/952683659": "an excavation plot code as the name (owner, 2026-10-13)",
    "way/228049982": "an excavation plot code as the name (owner, 2026-10-13)",
    "node/1573148905": "an excavation plot code as the name (owner, 2026-10-13)",
    "node/14091043733": "a find named by a description of where it lies (owner, 2026-10-13)",
    "node/14090980638": "a find named by a description of where it lies (owner, 2026-10-13)",
    "way/1549240866": "a find named by a description of where it lies (owner, 2026-10-13)",
    "way/1339150086": "a find named by a description of where it lies (owner, 2026-10-13)",
    "way/142141278": "a find named by a description of where it lies (owner, 2026-10-13)",
    "node/2602493589": "a find named by a description of where it lies (owner, 2026-10-13)",
    "node/7598776568": "a find named by a description of where it lies (owner, 2026-10-13)",
    "node/5405989440": "a find named by a description of where it lies (owner, 2026-10-13)",
    "way/1411911238": "a find named by a description of where it lies (owner, 2026-10-13)",
    "node/2518991634": "a find named by a description of where it lies (owner, 2026-10-13)",
    "way/1095626213": "a find named by a description of where it lies (owner, 2026-10-13)",
    "way/1237649253": "a find named by a description of where it lies (owner, 2026-10-13)",
    "node/11968350253": "a find named by a description of where it lies (owner, 2026-10-13)",
    "node/13482999691": "a find named by a description of where it lies (owner, 2026-10-13)",
    "way/32726502": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1180477949": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1180477950": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1180477958": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1180477960": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/184817980": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/184817988": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/185555868": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/185555869": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24009021": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24009060": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24009066": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24009083": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/24009087": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/77740753": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1181756985": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1181756986": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1181756991": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1181756992": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27633067": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27633175": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27633345": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/82226581": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/32504595": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/32504608": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/32504610": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/62215678": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/62215685": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/87705579": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/87705584": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/32504593": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/183920514": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27932078": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27932159": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27932161": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27932275": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27932316": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27932317": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27932326": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/27932328": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/28573421": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/32668116": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/32668794": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/32668795": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/32670423": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/32678225": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/61399941": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/62215679": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/104292922": "a lane named for its mode (owner, 2026-10-13)",
    "way/104294726": "a lane named for its mode (owner, 2026-10-13)",
    "way/664219554": "a lane named for its mode (owner, 2026-10-13)",
    "way/1396195921": "a lane named for its mode (owner, 2026-10-13)",
    "way/1420543089": "a lane named for its mode (owner, 2026-10-13)",
    "way/1420543090": "a lane named for its mode (owner, 2026-10-13)",
    "way/1422126038": "a lane named for its mode (owner, 2026-10-13)",
    "way/891581718": "a lane named for its mode (owner, 2026-10-13)",
    "way/891581719": "a lane named for its mode (owner, 2026-10-13)",
    "way/907355135": "a lane named for its mode (owner, 2026-10-13)",
    "way/231621076": "a lane named for its mode (owner, 2026-10-13)",
    "way/1164887371": "a lane named for its mode (owner, 2026-10-13)",
    "way/1164887372": "a lane named for its mode (owner, 2026-10-13)",
    "way/1162815387": "a lane named for its mode (owner, 2026-10-13)",
    "way/1162815388": "a lane named for its mode (owner, 2026-10-13)",
    "way/1162815389": "a lane named for its mode (owner, 2026-10-13)",
    "way/1162815391": "a lane named for its mode (owner, 2026-10-13)",
    "way/1162815393": "a lane named for its mode (owner, 2026-10-13)",
    "way/1162815394": "a lane named for its mode (owner, 2026-10-13)",
    "way/1408661605": "a lane named for its mode (owner, 2026-10-13)",
    "way/1408661606": "a lane named for its mode (owner, 2026-10-13)",
    "way/639139588": "a lane named for its mode (owner, 2026-10-13)",
    "way/699076480": "a lane named for its mode (owner, 2026-10-13)",
    "way/699076481": "a lane named for its mode (owner, 2026-10-13)",
    "way/977903711": "a lane named for its mode (owner, 2026-10-13)",
    "way/1286752616": "a lane named for its mode (owner, 2026-10-13)",
    "way/1286752617": "a lane named for its mode (owner, 2026-10-13)",
    "way/1347294007": "a lane named for its mode (owner, 2026-10-13)",
    "way/1174758490": "a lane named for its mode (owner, 2026-10-13)",
    "way/1306670863": "a lane named for its mode (owner, 2026-10-13)",
    "way/1306686221": "a lane named for its mode (owner, 2026-10-13)",
    "way/1306686222": "a lane named for its mode (owner, 2026-10-13)",
    "way/1327515616": "a lane named for its mode (owner, 2026-10-13)",
    "way/1334755406": "a lane named for its mode (owner, 2026-10-13)",
    "way/1334755407": "a lane named for its mode (owner, 2026-10-13)",
    "way/1335024163": "a lane named for its mode (owner, 2026-10-13)",
    "way/1336109248": "a lane named for its mode (owner, 2026-10-13)",
    "way/1336109249": "a lane named for its mode (owner, 2026-10-13)",
    "way/1336109250": "a lane named for its mode (owner, 2026-10-13)",
    "way/1336109251": "a lane named for its mode (owner, 2026-10-13)",
    "way/1338327478": "a lane named for its mode (owner, 2026-10-13)",
    "way/1338327479": "a lane named for its mode (owner, 2026-10-13)",
    "way/1338763313": "a lane named for its mode (owner, 2026-10-13)",
    "way/1338763314": "a lane named for its mode (owner, 2026-10-13)",
    "way/143326127": "a lane named for its mode (owner, 2026-10-13)",
    "way/367163877": "a lane named for its mode (owner, 2026-10-13)",
    "way/78675994": "a lane named for its mode (owner, 2026-10-13)",
    "way/1175936731": "a lane named for its mode (owner, 2026-10-13)",
    "way/1175936732": "a lane named for its mode (owner, 2026-10-13)",
    "way/1175936733": "a lane named for its mode (owner, 2026-10-13)",
    "way/1175936734": "a lane named for its mode (owner, 2026-10-13)",
    "way/1175936736": "a lane named for its mode (owner, 2026-10-13)",
    "way/1175936740": "a lane named for its mode (owner, 2026-10-13)",
    "way/1175936741": "a lane named for its mode (owner, 2026-10-13)",
    "way/1307318220": "a lane named for its mode (owner, 2026-10-13)",
    "way/1307318223": "a lane named for its mode (owner, 2026-10-13)",
    "way/1490850381": "a lane named for its mode (owner, 2026-10-13)",
    "way/1490850382": "a lane named for its mode (owner, 2026-10-13)",
    "way/1175936744": "a lane named for its mode (owner, 2026-10-13)",
    "way/1175936745": "a lane named for its mode (owner, 2026-10-13)",
    "way/1175936749": "a lane named for its mode (owner, 2026-10-13)",
    "way/1175936750": "a lane named for its mode (owner, 2026-10-13)",
    "way/1499358021": "a lane named for its mode (owner, 2026-10-13)",
    "way/1499358022": "a lane named for its mode (owner, 2026-10-13)",
    "way/1499358023": "a lane named for its mode (owner, 2026-10-13)",
    "way/1499358024": "a lane named for its mode (owner, 2026-10-13)",
    "way/1566298636": "a lane named for its mode (owner, 2026-10-13)",
    "way/1536439020": "a lane named for its mode (owner, 2026-10-13)",
    "way/1536439021": "a lane named for its mode (owner, 2026-10-13)",
    "way/1546881246": "a lane named for its mode (owner, 2026-10-13)",
    "way/1482834902": "a lane named for its mode (owner, 2026-10-13)",
    "way/1482834903": "a lane named for its mode (owner, 2026-10-13)",
    "way/1531218946": "a lane named for its mode (owner, 2026-10-13)",
    "way/1531218947": "a lane named for its mode (owner, 2026-10-13)",
    "way/1531218948": "a lane named for its mode (owner, 2026-10-13)",
    "way/1531218949": "a lane named for its mode (owner, 2026-10-13)",
    "way/1565123256": "a lane named for its mode (owner, 2026-10-13)",
    "way/48440475": "a lane named for its mode (owner, 2026-10-13)",
    "way/741653543": "a lane named for its mode (owner, 2026-10-13)",
    "way/1078308301": "a lane named for its mode (owner, 2026-10-13)",
    "way/427502182": "a lane named for its mode (owner, 2026-10-13)",
    "way/427502183": "a lane named for its mode (owner, 2026-10-13)",
    "way/935446023": "a lane named for its mode (owner, 2026-10-13)",
    "way/936763004": "a lane named for its mode (owner, 2026-10-13)",
    "way/1263518530": "a lane named for its mode (owner, 2026-10-13)",
    "way/1319043398": "a lane named for its mode (owner, 2026-10-13)",
    "way/1319043399": "a lane named for its mode (owner, 2026-10-13)",
    "way/1319043400": "a lane named for its mode (owner, 2026-10-13)",
    "way/154380538": "a lane named for its mode (owner, 2026-10-13)",
    "way/419321164": "a lane named for its mode (owner, 2026-10-13)",
    "way/485702516": "a lane named for its mode (owner, 2026-10-13)",
    "way/485702517": "a lane named for its mode (owner, 2026-10-13)",
    "way/1071584898": "a lane named for its mode (owner, 2026-10-13)",
    "way/1137377801": "a lane named for its mode (owner, 2026-10-13)",
    "way/1137377802": "a lane named for its mode (owner, 2026-10-13)",
    "way/1230572375": "a lane named for its mode (owner, 2026-10-13)",
    "way/1240422946": "a lane named for its mode (owner, 2026-10-13)",
    "way/1240422947": "a lane named for its mode (owner, 2026-10-13)",
    "way/1252893072": "a lane named for its mode (owner, 2026-10-13)",
    "way/1255031453": "a lane named for its mode (owner, 2026-10-13)",
    "way/1255031454": "a lane named for its mode (owner, 2026-10-13)",
    "way/131189026": "a lane named for its mode (owner, 2026-10-13)",
    "way/1319048234": "a lane named for its mode (owner, 2026-10-13)",
    "way/1319048235": "a lane named for its mode (owner, 2026-10-13)",
    "way/1319048236": "a lane named for its mode (owner, 2026-10-13)",
    "way/1319048237": "a lane named for its mode (owner, 2026-10-13)",
    "way/1319048238": "a lane named for its mode (owner, 2026-10-13)",
    "way/1319048239": "a lane named for its mode (owner, 2026-10-13)",
    "way/1319048240": "a lane named for its mode (owner, 2026-10-13)",
    "way/1376786489": "a lane named for its mode (owner, 2026-10-13)",
    "way/1382815285": "a lane named for its mode (owner, 2026-10-13)",
    "way/1414141808": "a lane named for its mode (owner, 2026-10-13)",
    "way/1420542457": "a lane named for its mode (owner, 2026-10-13)",
    "way/1420542458": "a lane named for its mode (owner, 2026-10-13)",
    "way/1562163537": "a lane named for its mode (owner, 2026-10-13)",
    "way/1562167404": "a lane named for its mode (owner, 2026-10-13)",
    "way/168612313": "a lane named for its mode (owner, 2026-10-13)",
    "way/175301268": "a lane named for its mode (owner, 2026-10-13)",
    "way/183413932": "a lane named for its mode (owner, 2026-10-13)",
    "way/232132601": "a lane named for its mode (owner, 2026-10-13)",
    "way/232132616": "a lane named for its mode (owner, 2026-10-13)",
    "way/23946445": "a lane named for its mode (owner, 2026-10-13)",
    "way/23946446": "a lane named for its mode (owner, 2026-10-13)",
    "way/23946454": "a lane named for its mode (owner, 2026-10-13)",
    "way/247496662": "a lane named for its mode (owner, 2026-10-13)",
    "way/26209379": "a lane named for its mode (owner, 2026-10-13)",
    "way/26209436": "a lane named for its mode (owner, 2026-10-13)",
    "way/275759325": "a lane named for its mode (owner, 2026-10-13)",
    "way/28325109": "a lane named for its mode (owner, 2026-10-13)",
    "way/28325211": "a lane named for its mode (owner, 2026-10-13)",
    "way/33052778": "a lane named for its mode (owner, 2026-10-13)",
    "way/33052779": "a lane named for its mode (owner, 2026-10-13)",
    "way/33116984": "a lane named for its mode (owner, 2026-10-13)",
    "way/33116985": "a lane named for its mode (owner, 2026-10-13)",
    "way/381454430": "a lane named for its mode (owner, 2026-10-13)",
    "way/454016121": "a lane named for its mode (owner, 2026-10-13)",
    "way/454016124": "a lane named for its mode (owner, 2026-10-13)",
    "way/454016130": "a lane named for its mode (owner, 2026-10-13)",
    "way/50650262": "a lane named for its mode (owner, 2026-10-13)",
    "way/51244777": "a lane named for its mode (owner, 2026-10-13)",
    "way/51244856": "a lane named for its mode (owner, 2026-10-13)",
    "way/543752949": "a lane named for its mode (owner, 2026-10-13)",
    "way/551466301": "a lane named for its mode (owner, 2026-10-13)",
    "way/77073130": "a lane named for its mode (owner, 2026-10-13)",
    "way/778187928": "a lane named for its mode (owner, 2026-10-13)",
    "way/84203825": "a lane named for its mode (owner, 2026-10-13)",
    "way/871958036": "a lane named for its mode (owner, 2026-10-13)",
    "way/887833680": "a lane named for its mode (owner, 2026-10-13)",
    "way/903421711": "a lane named for its mode (owner, 2026-10-13)",
    "way/903463232": "a lane named for its mode (owner, 2026-10-13)",
    "way/93997050": "a lane named for its mode (owner, 2026-10-13)",
    "way/973480402": "a lane named for its mode (owner, 2026-10-13)",
    "way/973480403": "a lane named for its mode (owner, 2026-10-13)",
    "way/1056510509": "a lane named for its mode (owner, 2026-10-13)",
    "way/33119882": "a lane named for its mode (owner, 2026-10-13)",
    "way/376509625": "a lane named for its mode (owner, 2026-10-13)",
    "way/376509626": "a lane named for its mode (owner, 2026-10-13)",
    "way/376509627": "a lane named for its mode (owner, 2026-10-13)",
    "way/885603750": "a lane named for its mode (owner, 2026-10-13)",
    "way/585789604": "a cemetery sector label tagged a locality",
    "way/585789597": "a cemetery sector label tagged a locality",
    "node/4322351299": "a duplicate row: the same neighbourhood 300 m away carries the article",
    "way/597452722": "an excavation room number standing in for a name",
    "way/848452248": "a description (a dirt football pitch) tagged a park",
    "node/2688549543": "a single tree labelled by species and number, tagged a park",
    "node/2688549545": "a single tree labelled by species and number, tagged a park",
    "node/2688549554": "a single tree labelled by species, tagged a park",
    "node/10131301855": "a description of a mission cross, tagged a place of worship",
    "node/14266373405": "a description in English standing in for a name",
    "node/4637408714": "a description (a building's style and year) standing in for a name",
    "way/616379123": "a description in English standing in for a name",
    "way/1240185741": "a description in English standing in for a name",
    "node/2597000964": "a description standing in for a name",
    "node/2396866901": "a description standing in for a name",
    "way/158036052": "a description standing in for a name",
    "way/1365858684": "a description in French of an inscription, no article",
    "node/12648707297": "an inscription catalogue number standing in for a name, no article",
    "way/734121324": "a description (a flowerbed at a metro station) tagged a park",
    "way/109371863": "a description (a flowerbed on a square) tagged a park, with a mistyped numeral",
    "way/739110009": "a generic municipal playground label standing in for a name",
    "node/7010464021": "an association's premises tagged a square",
    "way/1378598782": "a customers-only venue tagged a park",
    "way/997532415": "a cut name",
    "way/123530979": "a glitched name: a stray question mark in brackets",
    "relation/5969408": "a glitched name: a second label glued on after a slash",
    "node/11045948500": "a glitched name: two scripts glued together",
    "node/4607987555": "a religious house tagged a place of worship, no article",
    "way/476934285": "a religious house tagged a place of worship, no article",
    "node/5809313735": "a religious house tagged a place of worship, no article",
    "node/4711818760": "a religious house tagged a place of worship, no article",
    "way/254678923": "a religious house tagged a place of worship, no article",
    "node/13150971501": "a religious house tagged a place of worship, no article",
    "node/280990403": "a seminary college tagged a place of worship, no article",
    "way/88114643": "a priestly fraternity's house tagged a place of worship, no article",
    "way/1418890587": "a religious house's private chapel under an English description",
    "way/637313789": "a cemetery mausoleum with no article of its own",
    "way/636983848": "a cemetery mausoleum with no article of its own",
    "way/679913478": "a cemetery mausoleum with no article of its own",
    "node/7142449839": "public art with no article, inscribed with a company name",
    "node/9007845910": "a memorial whose whole name is a person's name, no article",
    "node/12585439955": "a duplicate row: the statue at the same spot carries the article",
    "node/12544253674": "a duplicate row: the same site 34 m away as a relation",
    "way/190124659": "a service road named with a house number: an address, no street name",
    "way/681296202": "a gated estate's perimeter track, a description",
    "way/990945570": "a gated estate's perimeter track, a description",
    "way/990946176": "a gated estate's perimeter track, a description",
    "way/990953765": "a gated estate's perimeter track, a description",
    "way/990954868": "a gated estate's perimeter track, a description",
    "way/993101542": "a gated estate's perimeter track, a description",
    "way/998207742": "a gated estate's perimeter track, a description",
    "way/1037229884": "a gated estate's perimeter track, a description",
    "way/990944823": "a gated estate's perimeter track, a description",
    "way/1135746056": "a country club's own track, named for the club",
    "way/999039651": "a country club's own track, named for the club",
    "way/999039654": "a country club's own track, named for the club",
    "way/1050717989": "a description (a way round a gate), no name",
    "way/1298768213": "a gorge's name on a path, read as a way by the word ponte: no street",
    "way/687398232": "a park's name on its footways, read as a way by the word ponte",
    "way/832383534": "a park's name on its footways, read as a way by the word ponte",
    "way/119431987": "a single letter standing in for a name",
    "way/225727346": "a typo of a name that has its own row",
    "way/1436886992": "an English description on a footway",
    "way/36779949": "a bare type word as the whole name",
    "way/929796288": "an address number as a name",
    "way/83016311": "an address number as a name",
    "way/758389663": "an address number as a name",
    "way/1033010508": "a scrapyard business",
    "way/1033010509": "a scrapyard business",
    "way/1033010510": "a scrapyard business",
    "way/128914999": "a cut name that has a full row",
    "way/128926578": "a cut name that has a full row",
}
