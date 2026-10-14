"""Brussels (Regional)-specific settings: the 18 communes of the
Brussels-Capital Region outside the City of Brussels.

Companies' establishment units from KBO/BCE Open Data (FPS Economy), placed by
joining their addresses to BeST-Address Brussels (FPS BOSA) and filtered by
four storefront rules: a different method from the City's page (hub.brussels's
street survey), said on the page; the two are never merged. Rail is STIB-MIVB
beyond the City, on the City's shared STIB module. Brief:
docs/build_briefs/brussels_regional.md.
"""

from pathlib import Path

SLUG = "brussels_regional"
# The brief's proposals, checked against app/cities.py by scripts/brief_check.py.
MAP_MODE = "metro"
MAP_COVERAGE = "narrowed"
SCOPE = "regional"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "brussels_regional" / "raw"
DATA_PROCESSED = ROOT / "data" / "brussels_regional" / "processed"
OUTPUTS = ROOT / "outputs" / "brussels_regional"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Step 2's cached KBO extract (parquet, rebuilt when the KBO zip changes) and
# its measurements.
KBO_EXTRACT_DIR = DATA_PROCESSED / "kbo_extract"
STEP2_REPORT_JSON = DATA_PROCESSED / "step2_report.json"

# Raw inputs. The business leg's two files are shared Belgian caches
# (pipeline/countries/belgium.py: KBO_ZIP, BEST_BRUSSELS_ZIP), verified by
# pipeline/brussels_regional/fetch_sources.py against their meta JSON. KBO is
# placed by the owner (the portal needs the owner's login; a download at least
# yearly, licence 10.5, due by KBO_DOWNLOAD_DUE); BeST may be re-fetched by
# that script's --refresh-best, which means re-running the control.
BEST_URL = "https://opendata.bosa.be/download/best/openaddress-bebru.zip"
KBO_PORTAL = "https://kbopub.economie.fgov.be/kbo-open-data/login?lang=en"
KBO_DOWNLOAD_DUE = "2027-10-02"
GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "businesses.csv"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# The control's survey side: hub.brussels's inventory of the City (2025-10-17),
# and the City page's stations for the near-a-City-station count.
HUB_JSON = ROOT / "data" / "brussels" / "raw" / "hub_brussels_commerces.json"
CITY_STATIONS_CSV = ROOT / "data" / "brussels" / "processed" / "stations.csv"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 31N: the longitude (~4.37) falls in the 0 to 6 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32631"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
# HALVED RINGS: the 145 stations kept have a 437 m median nearest-neighbour
# gap (measured 2026-10-04), under the ~550 m line in docs/ring_rules.md (the
# City's rule; its own median is 377 m).
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# STIB-MIVB's whole rail network, read from the City of Brussels page's feed
# (the same download, `pipeline/brussels/fetch_sources.py`; the owner accepted
# the portal's terms for it). Every one of STIB's 22 rail lines serves at least
# one stop in the 18 communes, so all are drawn: metro 1, 2, 5, 6 and 18 tram
# lines. The machinery, its rules and the STIB facts (regular routes, places,
# thinning, bilingual names, gate 3) are the City's, shared through
# pipeline/countries/belgium_stib.py and imported from its config here.
from pipeline.brussels.config import (  # noqa: E402
    COLLAPSE_MAX_SPREAD_M,
    CORRIDOR as CITY_CORRIDOR,
    GTFS_ZIP,
    LINE_SHAPES_JSON as _CITY_LINE_SHAPES_JSON,
    METRO_FEED_COLOURS,
    METRO_LINES,
    METRO_ROUTE_TYPE,
    OPERATOR_COUNTS_SOURCE,
    OPERATOR_STATION_COUNTS,
    PLACE_LINK_M,
    REGULAR_ROUTE_MIN_DAY_SHARE,
    REGULAR_ROUTE_MIN_TRIP_SHARE,
    ROUTE_TYPES_RAIL,
    SPACING_MIN_M,
    STOP_NAME_ALIASES,
    THIN_SPACING_MILES,
)
from pipeline.brussels.config import COMMUNES_GEOJSON, LINE_COLOURS as _CITY_COLOURS  # noqa: E402
from pipeline.brussels.config import TRAM_FEED_COLOURS as _CITY_TRAM_FEED  # noqa: E402

TRAM_LINES = ("4", "7", "8", "9", "10", "18", "19", "25", "35", "39", "44", "51", "55",
              "62", "81", "82", "92", "93")
TRAM_LINES_OUTSIDE = ()
LINE_ORDER = METRO_LINES + TRAM_LINES
LINE_NAMES = {ln: (f"Metro {ln}" if ln in METRO_LINES else f"Tram {ln}") for ln in LINE_ORDER}
LINE_SHAPES_JSON = DATA_PROCESSED / "line_shapes.json"
del _CITY_LINE_SHAPES_JSON

# The City page's colours, and the three trams the City does not draw shifted
# in HSL lightness only to clear Delta-E 13 from every other line (the City's
# rule), measured 2026-10-04: 18 #91bee7 -> #bbd7f0 (L +0.10, the same blue as
# 82), 39 #e43c2e -> #ec7369 (L +0.13, the red of 19 and 92), 44 #f3c300 ->
# #ac8a00 (L -0.14, the yellow of 51).
TRAM_FEED_COLOURS = {**_CITY_TRAM_FEED, "18": "#91bee7", "39": "#e43c2e", "44": "#f3c300"}
LINE_COLOURS = {**_CITY_COLOURS, "18": "#bbd7f0", "39": "#ec7369", "44": "#ac8a00"}

# THE CORRIDOR: STIB's parent stations (`location_type` 1) are exactly the
# underground metro and premetro stations, 70 network-wide (measured
# 2026-10-04). The City's 25 are the Brussels page's, so 45 are this page's.
CORRIDOR_COUNT = 45
# The 18 communes by NIS code: SCOPE_CODES, below with the business filters.
CITY_COMMUNE_CODE = "21004"

# --- Scope: the 18 communes, by NIS code, never by postcode ------------------

# The City's Avenue Louise strip and European quarter carry 1050 and 1040,
# Ixelles's and Etterbeek's postcodes, so a business's key is the matched BeST
# point's municipality_id, checked against the commune polygons and KBO's own
# municipality field (step 2 reports the disagreements).
SCOPE_CODES = {
    "21001": "Anderlecht", "21002": "Auderghem / Oudergem",
    "21003": "Berchem-Sainte-Agathe / Sint-Agatha-Berchem", "21005": "Etterbeek",
    "21006": "Evere", "21007": "Forest / Vorst", "21008": "Ganshoren",
    "21009": "Ixelles / Elsene", "21010": "Jette", "21011": "Koekelberg",
    "21012": "Molenbeek-Saint-Jean / Sint-Jans-Molenbeek", "21013": "Saint-Gilles / Sint-Gillis",
    "21014": "Saint-Josse-ten-Noode / Sint-Joost-ten-Node", "21015": "Schaerbeek / Schaarbeek",
    "21016": "Uccle / Ukkel", "21017": "Watermael-Boitsfort / Watermaal-Bosvoorde",
    "21018": "Woluwe-Saint-Lambert / Sint-Lambrechts-Woluwe",
    "21019": "Woluwe-Saint-Pierre / Sint-Pieters-Woluwe",
}
CITY_POSTCODES = ("1000", "1020", "1120", "1130")
# The Region's postcodes (special ones such as 1099, 1105 and 1110 included):
# the KBO extract keeps establishment addresses in this range.
REGION_POSTCODE_RANGE = (1000, 1299)

# --- Business filtering ------------------------------------------------

CITY_KEEP = "BRUSSELS (REGIONAL)"   # kept for the scaffold's templates; the scope is SCOPE_CODES
TAXONOMY_SYSTEM = "belgium_kbo"
RAW_CLASSIFICATION_COLUMN = "nace_code"

# Personal services is OFF on this page (owner, 2026-10-03, call 12):
# companies only drops most salons (0.47 times the survey's count, 51% recall).
# The bucket priority runs first, so only a personal-only unit leaves.
BUCKETS_OFF = ("Personal services",)

# The four storefront rules (the brief's definitions, exactly).
RULE_B_MIN_UNITS = 5          # companies' units at one address (box ignored), any activity
RULE_B_IN_BUCKET_SHARE = 0.5  # dropped when fewer than half of them are in a bucket
RULE_D_MIN_CODES = 10         # distinct MAIN codes, at least one outside the buckets

# The "other postcode or loose street name" join tier (0.8% in the screen):
# kept only if it holds (step 2 reports the street keys that recur in more
# than one postcode and the tier's agreement with the survey).
KEEP_LOOSE_TIER = True

# The agreement with hub.brussels inside the City (the control).
SURVEY_DATE = "2025-10-17"
MATCH_RADIUS_M = 15.0
# The control must reproduce before any count is trusted (the brief, measured
# 2026-10-03 on extract 501): the join on the City's four postcodes, and the
# agreement after rules A-D (precision, recall) per bucket.
CONTROL_JOIN = {"exact": 88.5, "placed": 97.2}
# Re-based on this build's `brussels_hub` typing (owner, 2026-10-04): the
# brief's targets, Retail 78.2 / 76.1 and Food service 84.4 / 84.0, were
# measured with the screen's survey typing. With that typing on the same KBO
# units: Retail 78.1 / 76.0, Food service 83.9 / 84.1, so the typing explains
# Retail's gap but leaves a 0.5-point Food precision residual, unexplained and
# accepted inside the 1-point tolerance. Re-measure if either typing changes.
CONTROL_AGREEMENT = {"Retail": (78.2, 75.4), "Food service": (83.8, 84.1)}
CONTROL_TOLERANCE_PTS = 1.0

# Placed units near a City station but no regional one: the ring's outer edge.
NEAR_CITY_STATION_M = 0.3 * METERS_PER_MILE

# Company or commercial names read as a person's own, withheld (the dot shows
# its activity): KEYS from pipeline/name_keys.py, never the names
# (scripts/check_name_keys.py). The one name check_personal_exposure.py
# found person-like at an address it reads as a residential unit, by key,
# never read by eye (owner, 2026-10-04: "1 yes").
PERSON_NAMED = frozenset({"696bc4d0b2c984f0"})

# The Region's extent (about 4.24-4.48 E, 50.76-50.92 N), padded.
BRUSSELS_REGIONAL_BBOX = {"lat_min": 50.75, "lat_max": 50.93, "lon_min": 4.23, "lon_max": 4.49}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

# The 18 communes this map is cut to. The City of Brussels (relation 58274)
# is the Brussels page's own map and index, and holds none of this map's
# stations: the fetch's scope stop refused it here (2026-10-13).
PLACE_AREA = "(id:3600058248,3600058249,3600058250,3600058252,3600058253,3600058254,3600058255,3600058256,3600058257,3600058258,3600058260,3600058262,3600058263,3600058264,3600060140,3600060144,3600060167,3600060168)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("fr", "nl")
PLACE_FOLD = None
# Rows a reader held that the owner ruled to keep (2026-10-13;
# docs/decisions_drafts/search-final.md). A record only: no code reads it.
# A street is listed by name, a place by OSM id with its name. Not in
# PLACE_REVIEWED, which check E holds to names carrying a leak word.
PLACE_RULED_KEPT = {
    # Held rows kept by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    # A home, family or person row is listed by id alone.
    "way/998222835": "'Cité Jouët-Rey', Housing estates tagged as places are kept (owner 2026-10-13, fourteen answers 6, asked on the nine built cities)",
    "node/9970637900": "'Cité Nogent - Tuinwijk Nogent', Housing estates tagged as places are kept (owner 2026-10-13, fourteen answers 6, asked on the nine built cities)",
    "node/496816293": "'Cité Van Lindt', Housing estates tagged as places are kept (owner 2026-10-13, fourteen answers 6, asked on the nine built cities)",
    "node/10185837291": "'Cité Volta - Voltawijk', Housing estates tagged as places are kept (owner 2026-10-13, fourteen answers 6, asked on the nine built cities)",
    "node/9970808596": "'Cité-jardin Chomé - Tuinwijk Chomé', Housing estates tagged as places are kept (owner 2026-10-13, fourteen answers 6, asked on the nine built cities)",
    "node/11620057021": "'Germinal', Housing estates tagged as places are kept (owner 2026-10-13, fourteen answers 6, asked on the nine built cities)",
    "node/1285044547": "'Les Jardins Saint-Lambert', Housing estates tagged as places are kept (owner 2026-10-13, fourteen answers 6, asked on the nine built cities)",
    "way/998217237": "'Cité Forest Vert', Housing estates tagged as places are kept (owner 2026-10-13, fourteen answers 6, asked on the nine built cities)",
    "node/9975914968": "'Jardins de Jette - Tuinen van Jette', Housing estates tagged as places are kept (owner 2026-10-13, fourteen answers 6, asked on the nine built cities)",
    "way/1331392238": "'Jardins de la Chasse - Jachthof', Housing estates tagged as places are kept (owner 2026-10-13, fourteen answers 6, asked on the nine built cities)",
    "way/1124236591": "'Square du Bois - Bossquare', Housing estates tagged as places are kept (owner 2026-10-13, fourteen answers 6, asked on the nine built cities)",
    "way/200673325": "Brussels' châteaux are kept (owner 2026-10-13, fourteen answers 5)",
    "way/233650796": "Brussels' châteaux are kept (owner 2026-10-13, fourteen answers 5)",
    "way/225633344": "Brussels' châteaux are kept (owner 2026-10-13, fourteen answers 5)",
    "way/225203717": "Brussels' châteaux are kept (owner 2026-10-13, fourteen answers 5)",
    "way/260452424": "Brussels' châteaux are kept (owner 2026-10-13, fourteen answers 5)",
    "way/244020440": "Brussels' châteaux are kept (owner 2026-10-13, fourteen answers 5)",
    "way/226410659": "Brussels' châteaux are kept (owner 2026-10-13, fourteen answers 5)",
    "way/226554341": "Brussels' châteaux are kept (owner 2026-10-13, fourteen answers 5)",
    "way/226405293": "Brussels' châteaux are kept (owner 2026-10-13, fourteen answers 5)",
    "way/997942297": "Brussels' châteaux are kept (owner 2026-10-13, fourteen answers 5)",
    "way/245897885": "Brussels' châteaux are kept (owner 2026-10-13, fourteen answers 5)",
    "node/6739130225": "'Marquis de Villalobar - Markies de Villalobar', Statues, busts and public memorials stay, and monuments are not held to the notable rule (owner 2026-10-13, personal names 2; 2026-10-11 answer 5, measured and put back)",
    "node/4327004903": "'Monument de commémoration des victimes de mars 2016 - Herdenkingmonument slachtoffers maart 2016', Statues, busts and public memorials stay, and monuments are not held to the notable rule (owner 2026-10-13, personal names 2; 2026-10-11 answer 5, measured and put back)",
    "node/9977870562": "'Monument à Edith Cavell et Marie Depage - Standbeeld voor Edith Cavell en Marie Depage', Statues, busts and public memorials stay, and monuments are not held to the notable rule (owner 2026-10-13, personal names 2; 2026-10-11 answer 5, measured and put back)",
    "way/722051451": "'Plaine Limite - Plein Grensstraat', A place that stands and is closed is kept (owner 2026-10-13, PLACE_CLOSED_FOR_WORKS: a playground among them)",
    "way/365723197": "'Parc de la petite Senne - Park van de Kleine Zenne', A place that stands and is closed is kept (owner 2026-10-13, PLACE_CLOSED_FOR_WORKS: a playground among them)",
    "way/404657842": "'Ancient Stokkel Railway Station', A landmark that stands, ruined, abandoned or under a former-use name, stays (owner 2026-10-13: keep all standing abandoned landmarks; third list 11: former in a name is not read as gone)",
    "way/847795742": "'Institut d'enseignement supérieur social de l'information et de la documentation', A department or site carrying its institution's entry stays (owner 2026-10-13, fifteen answers 8)",
    "way/793076936": "'Clos de la Balance - Weegschaalbinnenhof', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/112409831": "'Clos du Parnasse - Parnassusgaarde', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/507306356": "'Carré aux Platanes - Platanenwijk', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/30670741": "'Parc de la Cité Jouët-Rey - Cité Jouët-Rey park', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/30089206": "'Parc ING - ING Park', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/31356453": "'Jardin Delhaize - Tuin Delhaize', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "node/13911607839": "'Jardin du Delhaize Saint-Antoine- Tuin van Delhaize Sint-Antoon', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/553438019": "'Saint-Pie X', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/227395225": "'Aux Trois Rois', A historic building named for the business it housed is a historic site (Panama Hotel precedent 2026-10-08)",
    "way/241553744": "a home tagged an attraction with a Wikipedia article of its own is kept (owner, 2026-10-13)",
    "way/30498629": "'Château Latour de Frein', Brussels' châteaux are kept (owner 2026-10-13, fourteen answers 5)",
    "way/47353486": "'Domaine Latour de Freins', A tourism, amenity or aeroway landmark with a Wikidata entry meets the notable rule (NOTABLE_ONLY 2026-10-07)",
    "node/9001639449": "'Tintin et Milou - Kuifje en Bobbie', A tourism, amenity or aeroway landmark with a Wikidata entry meets the notable rule (NOTABLE_ONLY 2026-10-07)",
    "way/158927030": "A place of worship under a name of its own needs no article (NOTABLE_ONLY 2026-10-07; Anyang 2026-10-13: where the tags show worship or cannot tell, it stays)",
    "Chemin Elena Milashina": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Chemin François Englert": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Chemin Henri Storck": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Chemin Ilya Prigogine": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Chemin Isabelle Stengers": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Chemin Marie Popelin": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Chemin Robert Brout": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Voie 1 - Spoor 1": "A registered code is a name (owner 2026-10-12); a minor way with an entry of its own is kept (2026-10-07)",
    "Voie 2 - Spoor 2": "A registered code is a name (owner 2026-10-12); a minor way with an entry of its own is kept (2026-10-07)",
    "Avenue des Cosaques de la Meuse - Maaskozakkenlaan": "A named private street is kept, a code-named one dropped (owner 2026-10-13, fourteen answers 8; PRIVATE_STREET_LEAD 2026-10-11)",
    "Cité Fontainas - Fontainashof": "A named private street is kept, a code-named one dropped (owner 2026-10-13, fourteen answers 8; PRIVATE_STREET_LEAD 2026-10-11)",
    "Drève des Dames Blanches - Witte Vrouwendreef": "A named private street is kept, a code-named one dropped (owner 2026-10-13, fourteen answers 8; PRIVATE_STREET_LEAD 2026-10-11)",
    "Passage Linthout": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Square Charles Jordens - Charles Jordenssquare": "A named private street is kept, a code-named one dropped (owner 2026-10-13, fourteen answers 8; PRIVATE_STREET_LEAD 2026-10-11)",
    "Square Charles-Maurice Wiser - Charles-Maurice Wiserplein": "A named private street is kept, a code-named one dropped (owner 2026-10-13, fourteen answers 8; PRIVATE_STREET_LEAD 2026-10-11)",
    "Square Gérard Van Caulaert - Gérard Van Caulaertsquare": "A named private street is kept, a code-named one dropped (owner 2026-10-13, fourteen answers 8; PRIVATE_STREET_LEAD 2026-10-11)",
    "Square Sans Souci - Sans Soucisquare": "A named private street is kept, a code-named one dropped (owner 2026-10-13, fourteen answers 8; PRIVATE_STREET_LEAD 2026-10-11)",
    "Voie Minckelers": "A named private street is kept, a code-named one dropped (owner 2026-10-13, fourteen answers 8; PRIVATE_STREET_LEAD 2026-10-11)",
    "Voie Montefiore": "A named private street is kept, a code-named one dropped (owner 2026-10-13, fourteen answers 8; PRIVATE_STREET_LEAD 2026-10-11)",
    "Chemin de Delleweg - De Delleweg": "A named private street is kept, a code-named one dropped (owner 2026-10-13, fourteen answers 8; PRIVATE_STREET_LEAD 2026-10-11)",
    "Espace Louise - Louiza Espace": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Galerie Horta - Hortagalerij": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Galerie Louise - Louizagalerij": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Galerie M - M-galerij": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Galerie Matongé - Matongégalerij": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Galerie Pacific": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Galerie Saint-Josse - Sint-Joost Galerij": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Galerie Sud - Zuidgalerij": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Galerie Toison d'Or - Galerij Toison d’Or": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Galerie de la Porte Louise - Galerij van de Louizapoort": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Galerie de la Porte de Namur - Galerij van de Naamsepoort": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Galerie des Argousiers - Duindoorngalerij": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Galerie du Cinquantenaire - Jubelgalerij": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Alsembergsesteenweg": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Eversestraat": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Kasterlindenstraat": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Kerselaarstraat": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Leuvensesteenweg": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Molenweg": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Place du Nord": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Quai de Biestebroeck": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Terhulpsesteenweg": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Tervuursesteenweg": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Tumulidreef": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Vieressendreef": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Woluwedal": "A street keeps a row under each name OpenStreetMap gives its ways; a one-language name is no glitch and none is repaired (owner 2026-10-11, answer 4)",
    "Avenue de Castonier - de Castonierlaan / de Castonierlaan - Avenue de Castonier": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Gouvernementsweg - Route Gouvernementale / Route Gouvernementale - Goevernementsweg": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Rue François Vander Elst - François Vander Elststraat / Frans Vander Elststraat - Rue François Vander Elst": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Rue Longue - Langestraat / Langestraat - Rue Longue": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Rue Pannenhuis - Pannenhuisstraat / Rue du Pannenhuys - Pannenhuisstraat": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Rue Walckiers - Walckiersstraat / Rue Walkiers - Walkiersstraat": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Rue de la Duchesse - Hertoginstraat / Rue de la Duchesse - Hertoginnestraat": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Rue de la Longue Haie - Langehaagstraat / Rue de la Longue Haie - Lange-Haagstraat": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Rue du Cardinal - Kardinaalstraat / Rue du Cardinal - Kardinaalsstraat": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Rue du Noyer - Notelaarsstraat / Rue du Noyer - Notelaarstraat": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Rue du Pannenhuys - Pannenhuisstraat / Rue Pannenhuis - Pannenhuisstraat": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
}
PLACE_REVIEWED = {
    "Avenue de la Brasserie - Brouwerijlaan": "a residential street, a real street name; the read of 2026-10-13",
    "Rue de la Brasserie - Brouwerijstraat": "a secondary road, a real street name; the read of 2026-10-13",
    "Rue de l'Hôtel des Monnaies - Munthofstraat": "a secondary road named for the former mint; the read of 2026-10-13",
    "Rue de la Clinique - Kliniekstraat": "a residential street, a real street name; the read of 2026-10-13",
    "Hôtel des Monnaies - Munthof": "a metro station (railway=station), named for the former mint",
    "Hôtel Communal de Forest - Gemeentehuis Vorst": "a town hall (amenity=townhall), not a hotel",
    "Hôtel communal de Woluwe-Saint-Pierre - Gemeentehuis Sint-Pieters-Woluwe": "a town hall (amenity=townhall), not a hotel",
}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    # Places of worship named by a body, left for the rules and still rows (the flag read of 2026-10-13, applied on the owner's word;
    # docs/decisions_drafts/search-final.md).
    "way/230206208": "a place of worship named only by its denomination, body or hall type is dropped (four rulings 1; sixteen rulings 2; left for the rules and still a row, owner 2026-10-13)",
    "way/1108911535": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885700": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885696": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/1109010017": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885686": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885687": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134890264": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/1109190289": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/1109190287": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885701": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885689": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/1109010015": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885695": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885690": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885685": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885694": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885698": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885702": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/1109019586": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/1109019588": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/134885692": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "way/1189933257": "a number or letter beside a type on a campus road (owner, 2026-10-13)",
    "node/6418483682": "a convent tagged a place of worship, no article",
    "node/4220717790": "public art whose wikidata and article are its subject's, not its own",
    "way/23160587": "a school's play ground tagged a park, a description standing in for a name",
    "way/396618811": "a metro station outline duplicating the station's own row",
    "way/471829535": "a metro station outline duplicating the station's own row",
    "way/473067545": "a metro station outline duplicating the station's own row",
    "way/475650100": "a metro station outline duplicating the station's own row",
    "way/475902135": "a metro station outline duplicating the station's own row",
    "way/471563850": "a metro station outline duplicating the station's own row",
    "way/475296532": "a metro station outline duplicating the station's own row",
    "way/396618816": "a metro station outline duplicating the station's own row",
    "way/474809937": "a metro station outline duplicating the station's own row",
    "way/471837285": "a metro station outline duplicating the station's own row",
    "way/628016575": "two streets joined in one name (corner segment); each street has its own row",
    "way/81030457": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/14794030": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/495559612": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/590784379": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/147764381": "two streets in one name",
    "way/224526004": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/25416670": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/412420814": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/147759792": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/245954575": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/1088286509": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/245230343": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/41178449": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/421916135": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/845098764": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/845100721": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/1562582119": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/1562582121": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/166989247": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/448760378": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/823329986": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/13868560": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/31669634": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/510217179": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/510217181": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/114899993": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/227349390": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/237827232": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/624210938": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/146291412": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/1478683677": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/176295379": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/34633131": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/806451615": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/39627639": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/542907431": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/39189278": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/1551699500": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/172761061": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/34627001": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/409836310": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/712633567": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/16089716": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/34561996": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/1024105863": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/23161179": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/367314299": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/33685256": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/1496576506": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/954232742": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/147764378": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/24614101": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/24614100": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/247891881": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/71811321": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/789007644": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/789007645": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/789007646": "one street twice, two spellings joined by a slash; a clean row exists",
    "way/973281723": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281722": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281725": "a cemetery lane named by ordinal number (code beside a type)",
    "way/93377984": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281711": "a cemetery lane named by ordinal number (code beside a type)",
    "way/528811464": "a cemetery lane named by ordinal number (code beside a type)",
    "way/528811463": "a cemetery lane named by ordinal number (code beside a type)",
    "way/528811465": "a cemetery lane named by ordinal number (code beside a type)",
    "way/528811460": "a cemetery lane named by ordinal number (code beside a type)",
    "way/528809332": "a cemetery lane named by ordinal number (code beside a type)",
    "way/528811461": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281714": "a cemetery lane named by ordinal number (code beside a type)",
    "way/93377934": "a cemetery lane named by ordinal number (code beside a type)",
    "way/528811459": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281716": "a cemetery lane named by ordinal number (code beside a type)",
    "way/29545985": "a cemetery lane named by ordinal number (code beside a type)",
    "way/93378000": "a cemetery lane named by ordinal number (code beside a type)",
    "way/93377956": "a cemetery lane named by ordinal number (code beside a type)",
    "way/93377935": "a cemetery lane named by ordinal number (code beside a type)",
    "way/93377939": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281717": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281712": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281715": "a cemetery lane named by ordinal number (code beside a type)",
    "way/93377963": "a cemetery lane named by ordinal number (code beside a type)",
    "way/29546003": "a cemetery lane named by ordinal number (code beside a type)",
    "way/93377955": "a cemetery lane named by ordinal number (code beside a type)",
    "way/93377988": "a cemetery lane named by ordinal number (code beside a type)",
    "way/29545994": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281720": "a cemetery lane named by ordinal number (code beside a type)",
    "way/44421344": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281724": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281718": "a cemetery lane named by ordinal number (code beside a type)",
    "way/44421355": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281719": "a cemetery lane named by ordinal number (code beside a type)",
    "way/93377918": "a cemetery lane named by ordinal number (code beside a type)",
    "way/528809344": "a cemetery lane named by ordinal number (code beside a type)",
    "way/973281721": "a cemetery lane named by ordinal number (code beside a type)",
    "way/44421373": "a cemetery lane named by ordinal number (code beside a type)",
    "way/29545967": "a cemetery lane named by ordinal number (code beside a type)",
    "way/29545973": "a cemetery lane named by ordinal number (code beside a type)",
    "way/93377929": "a cemetery lane named by ordinal number (code beside a type)",
    "way/528811462": "a cemetery lane named by ordinal number (code beside a type)",
    "way/93377971": "a cemetery lane named by ordinal number (code beside a type)",
    "way/40915599": "a station hall corridor",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "way/30355564": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/661611166": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/261670528": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "node/6407667593": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/1395714219": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/541176037": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/101985891": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "node/3136263140": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/556952194": "Campus lawns and courts go by id (owner 2026-10-13, wave 1's lettered list); held rows settled 2026-10-13",
    "way/361553872": "A minor-way street named by a description or a generic type word is dropped (street_description, owner 2026-10-13; six answers 3); held rows settled 2026-10-13",
    "way/443083277": "A minor-way street named by a description or a generic type word is dropped (street_description, owner 2026-10-13; six answers 3); held rows settled 2026-10-13",
    "way/443083280": "A minor-way street named by a description or a generic type word is dropped (street_description, owner 2026-10-13; six answers 3); held rows settled 2026-10-13",
    "way/1051122049": "A minor-way street named by a description or a generic type word is dropped (street_description, owner 2026-10-13; six answers 3); held rows settled 2026-10-13",
    "way/30445992": "An access description standing in for a name is dropped (owner 2026-10-13, fourteen answers 13); held rows settled 2026-10-13",
    "way/173091083": "A code beside a path type on minor ways is dropped (owner 2026-10-13, German answers 3; third pass PATH_CODE); held rows settled 2026-10-13",
    "way/1040904555": "A code beside a path type on minor ways is dropped (owner 2026-10-13, German answers 3; third pass PATH_CODE); held rows settled 2026-10-13",
    "way/125133472": "A code beside a path type on minor ways is dropped (owner 2026-10-13, German answers 3; third pass PATH_CODE); held rows settled 2026-10-13",
    "way/129523149": "A code beside a path type on minor ways is dropped (owner 2026-10-13, German answers 3; third pass PATH_CODE); held rows settled 2026-10-13",
    "way/851455273": "A code beside a path type on minor ways is dropped (owner 2026-10-13, German answers 3; third pass PATH_CODE); held rows settled 2026-10-13",
    "way/33903762": "A code beside a path type on minor ways is dropped (owner 2026-10-13, German answers 3; third pass PATH_CODE); held rows settled 2026-10-13",
    "way/1227013799": "A code beside a path type on minor ways is dropped (owner 2026-10-13, German answers 3; third pass PATH_CODE); held rows settled 2026-10-13",
}
