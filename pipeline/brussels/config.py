"""Brussels-specific settings: the City of Brussels, the commune (NIS 21004).

Belgium's first city. One field survey for all three buckets: hub.brussels's
inventory of ground-floor shops in the City, published by the City on
opendata.brussels.be with a point on every row, so there is no geocoder and no
join. Rail is STIB-MIVB's own GTFS: the metro and premetro stations are the
central corridor, and the trams are drawn and thinned (Amsterdam's rule).
Brief: docs/build_briefs/brussels.md. The other 18 communes of the Region are
Brussels (Regional), a separate page on a different source, never merged here.
"""

from pathlib import Path

SLUG = "brussels"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "brussels" / "raw"
DATA_PROCESSED = ROOT / "data" / "brussels" / "processed"
OUTPUTS = ROOT / "outputs" / "brussels"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINE_SHAPES_JSON = DATA_PROCESSED / "line_shapes.json"

# Raw inputs, every one written by pipeline/brussels/fetch_sources.py, which
# records URL, bytes, sha256 and retrieval time in PROVENANCE_JSON.
HUB_JSON = DATA_RAW / "hub_brussels_commerces.json"
COMMUNES_GEOJSON = DATA_RAW / "communes_region_bruxelles.geojson"
GTFS_ZIP = DATA_RAW / "stib_gtfs.zip"
SOURCE_ENCODING = "utf-8"

# --- Endpoints ---------------------------------------------------------------

# opendata.brussels.be is Opendatasoft (Explore API v2.1). The export is
# requested with an explicit field list that leaves out `google_maps` and
# `google_street_view` (the licence read's condition: never stored, never a
# link to Google) and `geo_shape` (the same point again). The fetch stops if
# a column it did not ask for arrives.
ODS_BASE = "https://opendata.brussels.be/api/explore/v2.1/catalog/datasets"
HUB_DATASET = "commerces-recenses-par-hubbrussels-vbx"
HUB_PAGE = "https://opendata.brussels.be/explore/dataset/commerces-recenses-par-hubbrussels-vbx/"
HUB_FIELDS = ("objectid", "category_fr", "category_nl", "category_en",
              "type_fr", "type_nl", "type_en", "name_fr", "name_nl", "name_en",
              "address_fr", "postalcode", "municipality_fr", "geo_point_2d",
              "source", "last_update")
HUB_NEVER = ("google_maps", "google_street_view")
HUB_EXPECTED_ROWS = 6880
# One survey: every row carries this date (brief check brussels-hub-one-survey-date).
HUB_SURVEY_DATE = "2025-10-17"

# The Region's commune limits (PARADIGM, CC0 1.0), 19 features.
COMMUNES_DATASET = "limites-administratives-des-communes-en-region-de-bruxelles-capitale"
COMMUNES_PAGE = ("https://opendata.brussels.be/explore/dataset/"
                 "limites-administratives-des-communes-en-region-de-bruxelles-capitale/")
COMMUNE_CODE = "21004"   # Bruxelles / Brussel, the City
COMMUNE_AREA_KM2 = (30, 36)  # Statbel: 32.6 km2

# STIB-MIVB's static GTFS on the Belgian Mobility Company's portal, anonymous
# tier (no key; 100 requests a day). ACCESS IS ACCEPTANCE of the portal's Terms
# of Use (art. 2): the owner accepted them for this build's first fetch
# (2026-10-03, "recommendation accepted"), and a re-fetch after the terms
# change goes back to the owner. So the fetch compares the terms page's text
# with the hash recorded at that acceptance and refuses to download if it moved.
GTFS_URL = "https://api-management-discovery-production.azure-api.net/api/gtfs/feed/stibmivb/static"
BMC_PORTAL = "https://data.belgianmobility.io/"
BMC_TERMS_URL = "https://data.belgianmobility.io/en/terms.html"
# Measured 2026-10-04 on the terms "Last updated: December 2025, Effective
# date: January 1, 2026", the version the licence read covered.
BMC_TERMS_TEXT_SHA256 = "dc5be008d111bf2398d35c46358ca38ce4fc5d958f62653245314b36f3a4e55e"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 31N: longitude ~4.35 E falls in the 0-6 E band. Derived per city.
CRS_PROJECTED = "EPSG:32631"

# --- Ring geometry ---------------------------------------------------------
# HALVED RINGS: the 66 stations kept have a 377 m median nearest-neighbour gap
# (measured 2026-10-04), under the ~550 m line in docs/ring_rules.md, so a
# 0.6 mi outer ring would reach two stations deep (Paris's and Oslo's rule).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope -----------------------------------------------------------

# THE METRO AND THE TRAMS THAT ENTER THE COMMUNE. STIB's feed (window
# 2026-09-28 to 2026-10-25, measured 2026-10-04) runs metro 1, 2, 5 and 6
# (route_type 1) and 18 tram lines (route_type 0). Fifteen of the trams serve
# at least one stop inside the commune on their regular route and are drawn
# whole (25 and 55 only at Rogier, their premetro terminus); 18, 39 and 44
# never enter it and are not drawn. Buses are not
# drawn; SNCB trains are commuter rail, out as everywhere. Tram 3 is not in the
# feed (its North-South premetro is served by 4 and 10).
ROUTE_TYPES_RAIL = ("0", "1")
METRO_ROUTE_TYPE = "1"
METRO_LINES = ("1", "2", "5", "6")
TRAM_LINES = ("4", "7", "8", "9", "10", "19", "25", "35", "51", "55", "62", "81", "82",
              "92", "93")
TRAM_LINES_OUTSIDE = ("18", "39", "44")
LINE_ORDER = METRO_LINES + TRAM_LINES
LINE_NAMES = {ln: (f"Metro {ln}" if ln in METRO_LINES else f"Tram {ln}") for ln in LINE_ORDER}

# A line's regular route: the stop names it serves on at least half its days
# in the feed's window (Amsterdam's rule), so a works diversion or a short
# working on a few dates neither adds nor removes a station.
REGULAR_ROUTE_MIN_DAY_SHARE = 0.5
# And by at least this share of the line's trips: metro 1 runs 34 of its 3,932
# trips through to Erasme (the first and last runs, every day), which the day
# rule alone counts as nine more metro 1 stations. Measured 2026-10-04.
REGULAR_ROUTE_MIN_TRIP_SHARE = 0.10

# THE CENTRAL CORRIDOR: the 25 underground metro and premetro stations in the
# commune, by name (the City's entrances dataset, brief check
# brussels-underground-stations). Kept always, never thinned. Anneessens,
# Bourse and Lemonnier are North-South premetro stations served by trams
# alone, so the corridor is a name list, never "served by route_type 1".
# Feed spellings (upper case, accents dropped). Botanique, Madou, Porte de
# Namur and Rogier lie under the Petite Ceinture, the commune's boundary with
# Saint-Josse and Ixelles: their platforms' mean point falls just outside the
# polygon while the City's dataset files their entrances in Bruxelles. So a
# corridor station counts as inside by name.
CORRIDOR = ("ANNEESSENS", "ARTS-LOI", "BOCKSTAEL", "BOTANIQUE", "BOURSE",
            "DE BROUCKERE", "GARE CENTRALE", "HEYSEL", "HOTEL DES MONNAIES",
            "HOUBA-BRUGMANN", "LEMONNIER", "LOUISE", "MADOU", "MAELBEEK",
            "PANNENHUIS", "PARC", "PORTE DE HAL", "PORTE DE NAMUR", "ROGIER",
            "ROI BAUDOUIN", "SAINTE-CATHERINE", "SCHUMAN", "STUYVENBERGH",
            "TRONE", "YSER")

# Trams are thinned with the sub-transit-line filters
# (docs/sub_transit_line_filters.md), Amsterdam's rule: the corridor kept,
# each line's own two terminals inside the commune kept, a stop shared by two
# or more lines kept, the rest one per half mile along the line.
THIN_SPACING_MILES = 0.5
SPACING_MIN_M = 200.0

# Gate 3: fr.wikipedia's "Métro de Bruxelles", each line's "Nb. d'arrêts"
# (read 2026-10-04, a SECONDARY source; STIB publishes no count). Exact on all
# four lines. Its network figure, 59 (en.wikipedia: "as of 2011"), is one
# under the feed's 60 and the per-line figures' own union, which count
# Elisabeth and Simonis apart; it is not used. The corridor's 25 is the
# City's own entrances dataset, an independent count.
OPERATOR_STATION_COUNTS = {"Metro 1": 21, "Metro 2": 19, "Metro 5": 28, "Metro 6": 26}
OPERATOR_COUNTS_SOURCE = ("fr.wikipedia.org/wiki/Métro_de_Bruxelles, read 2026-10-04 - "
                          "secondary; 1: 21, 2: 19, 5: 28, 6: 26")
CORRIDOR_COUNT = 25

# A STIB stop name can name two places (a metro station and a surface stop of
# the same name some way off). Platforms of one name within PLACE_LINK_M of
# each other are one place; a place wider than COLLAPSE_MAX_SPREAD_M stops the
# build (Amsterdam's figures).
PLACE_LINK_M = 300
# No aliases: Elisabeth and Simonis, 103 m apart (both in Koekelberg), are
# two stations in STIB's feed and in the secondary source's per-line counts.
STOP_NAME_ALIASES = {}
COLLAPSE_MAX_SPREAD_M = 400

# --- Line colours --------------------------------------------------------------
#
# STIB's own `route_color` from the feed. STIB gives 19 and 92 one red and 51
# and 55 one yellow, and several pairs sit close, so five trams are shifted in
# HSL LIGHTNESS ONLY, by the smallest step that clears Delta-E 13 from every
# line before them (Amsterdam's rule: the metro keeps STIB's colour; between
# two trams the lower number keeps it). Measured 2026-10-04:
#   Tram 9   #C44F97 -> #c95ea0 (L +0.04): 8.5 from Metro 1's #B5378C
#   Tram 35  #336195 -> #2b527e (L -0.06): 7.3 from Metro 6's #0066A3
#   Tram 55  #F3C300 -> #cfa600 (L -0.07): the same yellow as 51
#   Tram 92  #E43C2E -> #e8594e (L +0.07): the same red as 19
#   Tram 93  #ED7807 -> #f8800b (L +0.03): 11.0 from Metro 2's #ED6C23
# Below the preferred 45 against a pin colour, kept as STIB's (recorded, the
# owner's branding call): Tram 4 14.4 and Tram 25 17.3 from Food service,
# Metro 6 21.0 from Retail, Metro 1 28.1 from Food service.
METRO_FEED_COLOURS = {"1": "#b5378c", "2": "#ed6c23", "5": "#f6a90b", "6": "#0066a3"}
TRAM_FEED_COLOURS = {"4": "#ea4f80", "7": "#efe048", "8": "#169fdb", "9": "#c44f97",
                     "10": "#8f4199", "19": "#e43c2e", "25": "#a12944", "35": "#336195",
                     "51": "#f3c300", "55": "#f3c300", "62": "#f29dc3", "81": "#4c8b33",
                     "82": "#91bee7", "92": "#e43c2e", "93": "#ed7807"}
LINE_COLOURS = {**METRO_FEED_COLOURS, **TRAM_FEED_COLOURS,
                "9": "#c95ea0", "35": "#2b527e", "55": "#cfa600", "92": "#e8594e",
                "93": "#f8800b"}

# DISPLAY NAMES: the feed's stop names are upper case; translations.txt
# carries each in French and Dutch, mixed case. A station shows "French /
# Dutch" where the two differ (as STIB signs them), else the one name.
NAME_LANGUAGES = ("fr", "nl")

# --- Business filtering ------------------------------------------------------

CITY_KEEP = "BRUSSELS"   # kept for the scaffold's templates; the scope is the polygon
TAXONOMY_SYSTEM = "brussels_hub"
RAW_CLASSIFICATION_COLUMN = "type_fr"

# Shop signs read as a person's own name, withheld (the dot shows its type):
# KEYS from pipeline/name_keys.py, never the names (scripts/check_name_keys.py).
PERSON_NAMED = frozenset()

# The commune's own extent (about 4.29-4.44 E, 50.79-50.92 N), padded.
BRUSSELS_BBOX = {"lat_min": 50.78, "lat_max": 50.93, "lon_min": 4.28, "lon_max": 4.45}
