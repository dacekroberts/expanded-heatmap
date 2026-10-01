"""Den Haag-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

DEN HAAG, on Rotterdam's template (the BAG's shop-class units from PDOK, the
same query, with the vacancy disclosed from CBS) and Amsterdam's precedent for
a city's own hospitality-permit layer (owner, 2026-09-30). The food layer is
the Gemeente Den Haag's `Horeca_nieuw` layer 2, "Horecavergunningen", the layer
the city's own permit map reads. Rail from OpenStreetMap through the shared
`pipeline/osm_tram.py` (the tram-city skill): HTM's 14 tram lines, every stop.
"""

from pathlib import Path

SLUG = "den_haag"
NAME = "Den Haag"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "den_haag" / "raw"
DATA_PROCESSED = ROOT / "data" / "den_haag" / "processed"
OUTPUTS = ROOT / "outputs" / "den_haag"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Tram 1's and the other lines' stops outside the gemeente: drawn with their
# line, not ringed, listed here with the gemeente each lies in (owner, call 26).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) ----------------

HORECA_JSON = DATA_RAW / "horeca_vergunningen.json"
HORECA_META_JSON = DATA_RAW / "horeca_layer_meta.json"
BAG_UNITS_JSON = DATA_RAW / "bag_verblijfsobjecten_winkelfunctie.json"
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_GEMEENTEN_JSON = DATA_RAW / "osm_gemeenten.json"

# --- The permit layer --------------------------------------------------------

# ArcGIS Online, owner GemeenteDenHaagIntern, read by denhaag.nl's permit map.
# Licence SILENT; used on Amsterdam's precedent (owner, 2026-09-30): credit
# "Gemeente Den Haag", never call it current or complete.
HORECA_URL = ("https://services7.arcgis.com/b8OtZx5E96LVMxxJ/arcgis/rest/services/"
              "Horeca_nieuw/FeatureServer/2")
HORECA_PAGE = 1000
HORECA_MIN_ROWS = 2500
# THE FIELDS ASKED FOR, BY NAME. The layer also holds the applicant
# (AANVRAGER), the KvK number (KVKNUMMER) and the legal form (RECHTSVORM): a
# third of the permits are one-person firms, so the applicant is often a
# person, and the city's own map hides all three. They are never requested, and
# fetch_sources.py stops if one arrives anyway.
HORECA_FIELDS = ("FID", "ID", "JAAR", "DOSSIER", "STATUS", "OMSCHRIJVI", "STRAAT", "HUISNR",
                 "HUISLT", "TOEV", "POSTCODE", "STADSDEEL", "TYPEBEDRIJ", "CATEGORIE")
HORECA_FORBIDDEN = ("AANVRAGER", "KVKNUMMER", "RECHTSVORM")

# STATUS: granted or notified permits are kept; the 158 pending applications
# are left out (owner, call 24). A status not named here stops step 2.
STATUS_KEPT = ("Actueel", "Verleend", "Melding")
STATUS_PENDING = ("In behandeling", "Ingekomen", "Advies aangevraagd")

# --- The BAG -----------------------------------------------------------------

# PDOK's BAG WFS: shop-class units in use in gemeente 0518, served with their
# address and a WGS84 point - Rotterdam's query with Den Haag's code. A
# city-sized answer (about 6,500 units, a few MB), not the national file.
GEMEENTE_CODE = "0518"
BAG_WFS_URL = "https://service.pdok.nl/lv/bag/wfs/v2_0"
BAG_WFS_PAGE = 1000
BAG_MIN_ROWS = 5500
BAG_WFS_FILTER = (
    '<fes:Filter xmlns:fes="http://www.opengis.net/fes/2.0"><fes:And>'
    '<fes:PropertyIsLike wildCard="*" singleChar="." escapeChar="!"><fes:ValueReference>'
    'identificatie</fes:ValueReference><fes:Literal>' + GEMEENTE_CODE + '*</fes:Literal>'
    '</fes:PropertyIsLike>'
    '<fes:PropertyIsLike wildCard="*" singleChar="." escapeChar="!"><fes:ValueReference>'
    'gebruiksdoel</fes:ValueReference><fes:Literal>*winkelfunctie*</fes:Literal></fes:PropertyIsLike>'
    '<fes:PropertyIsEqualTo><fes:ValueReference>status</fes:ValueReference><fes:Literal>'
    'Verblijfsobject in gebruik</fes:Literal></fes:PropertyIsEqualTo></fes:And></fes:Filter>')
# A shop-class unit ALSO registered as a dwelling is left off - Amsterdam's
# owner call of 2026-09-24, applied in Rotterdam the same.
BAG_EXCLUDE_IF_ALSO = ("woonfunctie",)

# --- OSM ------------------------------------------------------------------------

# Every tram relation in HTM's box, and the gemeenten around it (Delft,
# Rijswijk, Leidschendam-Voorburg, Zoetermeer, Pijnacker-Nootdorp, Westland),
# which only name where an outside stop lies.
RAIL_BBOX = (51.96, 4.18, 52.14, 4.56)          # south, west, north, east
GEMEENTE_AREA_KM2 = (80.0, 105.0)               # CBS: 98 km2 including water

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 31N: the longitude (~4.30) falls in the 0 to 6 E band, as
# Rotterdam's (4.48) does. Derived per city, not copied.
CRS_PROJECTED = "EPSG:32631"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the in-gemeente stops' median nearest-neighbour gap (the brief:
# 335 m over 161 stop names, 2026-09-30; the owner's spacing rule). Step 1
# prints the median again and stops outside the bounds below.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (280.0, 400.0)

# --- Station scope: HTM's 14 tram lines, every stop in the gemeente ---------
#
# HTM's lines in the Rail Haaglanden network, every one OSM `route=tram` -
# RandstadRail 3, 4 and 34 included (OSM `brand` RandstadRail), so `mode` is
# `tram`. RandstadRail E is RET's metro (OSM `route=subway`), never in this
# query, and is left out as a stub: 4 of its 23 stops are in the gemeente
# (owner, call 22). Lines running on into Delft, Rijswijk, Leidschendam-
# Voorburg, Pijnacker-Nootdorp, Westland, Zoetermeer and Lansingerland are
# drawn to their ends; their stops there are listed, not ringed (tram 1, 19 of
# 37 inside: owner, call 26).
ROUTE = "tram"
OPERATOR = "HTM"
LINE_REFS = ("1", "2", "3", "4", "6", "9", "10", "11", "12", "15", "16", "17", "19", "34")
NOT_DRAWN = {
    19439816: "9S Hollands Spoor - Scheveningen Noord: a short working of tram 9, 4 stops, "
              "all on tram 9 (the brief: not drawn separately)",
    19439817: "9S Scheveningen Noord - Hollands Spoor: a short working of tram 9 (as above)",
    3009652: "RET's Rotterdam tram 8: another city's network, inside the fetch box only",
}
STATION_ADD = {}
# ONE INTERCHANGE, TWO NAMES: RandstadRail 3, 4 and 34 call it "Leidschenveen" and
# tram 19 "Leidschenveen Centrum", 10 m apart (2026-09-30) - merged by explicit
# alias, as Houston's couplet and New Orleans's Canal Street pairs were (Oslo's
# rule), so one interchange gets one ring set.
NAME_ALIASES = {"Leidschenveen Centrum": "Leidschenveen"}

# HTM GIVES SEVERAL STOPS ONE NAME. OSM's stop names carry no town or street
# qualifier, and six names belong to two separate stops each (measured
# 2026-09-30): Oosteinde (16 in Wateringen, 19 in Voorburg, 8.8 km apart),
# Beresteinlaan (4 / 9 and 10, 1.0 km), Fahrenheitstraat (2 / 3, 12 and 34,
# 905 m), Weimarstraat (11 / 12, 568 m), Loosduinseweg (11 / 12, 520 m) and
# Duinstraat (1 and 10 / 11, 351 m). Name collapse alone would average each
# pair into one point between them. So step 1 first groups a name's stop
# positions by distance (single linkage at SPLIT_LINK_M) and, where a name falls
# into several groups, labels each with the lines that serve it
# ("Weimarstraat (line 11)"). No name's groups are between 230 and 350 m apart,
# so 300 m separates the two cases with room on both sides.
SPLIT_LINK_M = 300.0
# One stop whose platforms stand apart, after the split: Station Hollands
# Spoor's A/B and C/D pairs (206 m) and Mozartlaan's two staggered platforms on
# RandstadRail 3 (228 m). The collapse's spread gate is widened to this from
# the shared 200 m for those two; a wider name still stops the step.
COLLAPSE_MAX_SPREAD_M = 250.0

SPACING_MIN_M = 100.0

# Gate 3: HTM's own stops per line - the distinct stops its timetable's
# journeys call at on Thursday 2026-10-01, from the endpoint htm.nl's line
# pages read - the whole line, before the gemeente split. A tram step 1 stops
# on a mismatch, but tram 11 disagrees, so that stop is commented out in step 1
# until the cleanup session takes it to the owner. Two stops carry other names
# in HTM's timetable and count the same: Delft's "Noordeinde" on 1 and 19 is
# OSM's "Nieuwe Plantage", and tram 12's terminus "Markenseplein" is OSM's
# "Zuiderstrand", each at the same place in the sequence.
OPERATOR_STATION_COUNTS = {
    "1": 37, "2": 29, "3": 40, "4": 33, "6": 27, "9": 27, "10": 33,
    # MISMATCH (cause found, not fixed): build 17. HTM's tram 11 calls at Groot
    # Hertoginnelaan (stop NL:S:32001109) between Laan van Meerdervoort and
    # Houtrust, both directions. OSM has its stop positions (nodes 3788117787,
    # 3788124865) on no relation, so the build neither draws nor rings it. It is
    # NOT tram 17's Groot Hertoginnelaan (NL:S:32001114, about 500 m away): a
    # third shared name for SPLIT_LINK_M once the stop is added.
    "11": 18,
    "12": 19, "15": 18, "16": 23, "17": 33, "19": 18, "34": 31,
}
OPERATOR_COUNTS_SOURCE = (
    "HTM's timetable for 2026-10-01, https://www.htm.nl/v1/Netex/GetDepartureTimes"
    "?lineNumber=<n>&date=2026-10-01 (the data behind htm.nl/dienstregeling/tram-<n>/), "
    "distinct stops over every journey, read 2026-10-01.")

DRAWN_LINES = LINE_REFS
# The public names: OSM's `wikipedia` tags name 3, 4 and 34 "RandstadRail 3/4/34"
# (`brand` RandstadRail) and the others "Tramlijn n".
LINE_NAMES = {ref: (f"RandstadRail {ref}" if ref in ("3", "4", "34") else f"Tram {ref}")
              for ref in LINE_REFS}
# OSM's own `colour` where it has one (2026-09-30), with three changes, each
# measured with pipeline/linecolour.py (CIE76) and the smallest HSL-lightness
# step that clears 13 from every other line - Rotterdam's rule:
#   * 1 and 19 share #c01115 (Delta-E 0, refused): tram 1 keeps it, the longer
#     line; 19 darker to #9f0e11 (L -7%; 13.1 from tram 1, 35.4 from the pins).
#   * 4 #fc751c and 16 #fa7222 are Delta-E 2.9 apart (refused, below the
#     floor of 10; the brief did not list this pair): RandstadRail 4 keeps its
#     colour; 16 lighter to #fb8540 (L +6%; 13.7 from 4, 59.9 from the pins).
#   * 10 and 34 carry no OSM colour: the project's palette, amber #fbc02d
#     (83.9 from the nearest pin) and brown #5d4037 (55.7), both more than 20
#     from every line.
# Tram 15's #e63a6b is 11.9 from Food service's pins: above the floor, kept
# as OSM's colour and reported by every render.
LINE_COLOURS = {"1": "#c01115", "2": "#006600", "3": "#703276", "4": "#fc751c",
                "6": "#0093de", "9": "#a6c116", "10": "#fbc02d", "11": "#cd853f",
                "12": "#ff66ff", "15": "#e63a6b", "16": "#fb8540", "17": "#006b8b",
                "19": "#9f0e11", "34": "#5d4037"}
OSM_COLOURS = {"1": "#c01115", "2": "#006600", "3": "#703276", "4": "#fc751c",
               "6": "#0093de", "9": "#a6c116", "11": "#cd853f", "12": "#ff66ff",
               "15": "#e63a6b", "16": "#fa7222", "17": "#006b8b", "19": "#c01115"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "den_haag_source"
RAW_CLASSIFICATION_COLUMN = "activity"

# Sanity bounds for the placed points: the gemeente plus a margin.
DEN_HAAG_BBOX = {
    "lat_min": 52.00,
    "lat_max": 52.14,
    "lon_min": 4.17,
    "lon_max": 4.42,
}
