"""Geneva (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/geneva.md). Switzerland's second city: Zurich's tram leg
(the shared `pipeline/osm_tram.py`, LV95, the Gemeinde polygons from OSM)
with a new business leg, the canton's business register (REG, SITG Level A),
classified by `pipeline/taxonomies/geneva_noga.py`. Regional scope: the 12
Swiss communes TPG's trams serve (owner, 2026-10-04).
"""

from pathlib import Path

SLUG = "geneva"
# What the brief's checks compare with (`brief_check.py geneva --vs-config`).
MAP_MODE = "tram"
MAP_COVERAGE = "full"
SCOPE = "regional"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "geneva" / "raw"
DATA_PROCESSED = ROOT / "data" / "geneva" / "processed"
OUTPUTS = ROOT / "outputs" / "geneva"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stops of drawn lines outside the 12 communes (tram 17's French end):
# drawn, not ringed, listed with the commune each lies in.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- The register (fetch_sources.py downloads; no step fetches) --------------
#
# Répertoire des entreprises du canton de Genève (REG), SITG dataset
# REG_ENTREPRISE_ETABLISSEMENT, contributor OCIRT; SITG Level A "Accès libre"
# (licence-read 2026-10-04; the narrow indemnity accepted by the owner the
# same day). The CSV zip, UTF-8 with BOM, ";", 35 fields, LV95 E/N on every
# row. Daily; the build uses one dated extract and the page states its date.
REG_URL = "https://ge.ch/sitg/geodata/SITG/OPENDATA/REG_ENTREPRISE_ETABLISSEMENT-CSV.zip"
REG_ZIP = DATA_RAW / "REG_ENTREPRISE_ETABLISSEMENT-CSV.zip"
REG_MEMBER = "REG_ENTREPRISE_ETABLISSEMENT.csv"
REG_DATE_MEMBER = "DOC/Informations_date.txt"
REG_CONDITIONS_URL = "https://sitg.ge.ch/ressources/conditions-utilisation-donnees"
REG_DATASET_PAGE = "https://sitg.ge.ch/donnees/reg-entreprise-etablissement"
# 100,588 rows on 2026-10-04; a file far below it is a failed fetch.
REG_MIN_ROWS = 90_000
# The columns step 2 reads, by exact name. The phone, fax, e-mail and legal-
# name columns are never written to processed/ (the brief); RAISON_SOCIALE is
# read in memory ONLY to test whether a sole trader's trade name is their own
# name (the owner's call 2, 2026-10-04), and is then dropped.
REG_COLUMNS = ("TYPE_REG", "ID_ETABLISSEMENT", "ID_ENTREPRISE", "NOM", "STATUT_REG",
               "TYPE_LOCAL", "CODE_NOGA", "BRANCHE", "PHYS_RUE", "PHYS_NUMRUE",
               "PHYS_NPA", "PHYS_LOCALITE", "PHYS_COMMUNE", "NATURE_JURID",
               "RAISON_SOCIALE", "E", "N")
# Records: establishment rows only (the brief). Company rows with no
# establishment row are left out and disclosed (owner, call 1, 2026-10-04).
RECORD_TYPE = "Etablissement"
# Premises types dropped before classification: home-based and itinerant
# (the brief) and market stands (owner, call 3, 2026-10-04: R1 and the
# mobile-units row).
DROP_PREMISES = ("Activité à domicile", "Activité itinérante", "Stand ambulant")
SOLE_TRADER = "Entreprise individuelle"
# The 326 kept establishments typed as an office stay on the map (owner,
# 2026-10-07), except that a person-shaped name there shows the street
# address whatever the legal form: a practice in an office building named for
# its practitioner is the person's name, not a trade name (the owner's
# condition). Measured 2026-10-07: 37 such names (Sàrl 23, SA 11, SNC 2, a
# branch 1); every office-typed sole trader already falls under the rule above.
OFFICE_PREMISES = "Bureau/étude/cabinet"

# --- OpenStreetMap: one query for the city (osm-rail) ------------------------

# S, W, N, E: the five lines with tram 17's French end (Annemasse) and
# tram 14's Bernex end, plus a margin.
RAIL_BBOX = (46.15, 6.03, 46.25, 6.26)
OSM_ALL_JSON = DATA_RAW / "osm_all.json"
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_COMMUNES_JSON = DATA_RAW / "osm_communes.json"
BFS_TAG = "swisstopo:BFS_NUMMER"
# The 12 Swiss communes the trams serve (the brief's TPG stop table), by
# swisstopo's BFS number as OSM tags it, with the names step 1 checks.
COMMUNES = {
    "6621": "Genève", "6628": "Lancy", "6630": "Meyrin", "6608": "Carouge",
    "6607": "Bernex", "6643": "Vernier", "6633": "Plan-les-Ouates",
    "6612": "Chêne-Bougeries", "6613": "Chêne-Bourg", "6640": "Thônex",
    "6631": "Onex", "6618": "Confignon",
}
# Their summed area, 77.0 km2 measured 2026-10-07; a polygon that fails to
# close moves it.
REGION_AREA_KM2 = (74.0, 80.0)
# The register's PHYS_COMMUNE labels for the same 12 (the Ville appears as
# five), cross-checked against the polygons in step 2.
REG_COMMUNE_LABELS = {
    "Genève", "Genève-Cité", "Genève-Eaux-Vives", "Genève-Petit-Saconnex",
    "Genève-Plainpalais", "Lancy", "Meyrin", "Carouge", "Bernex", "Vernier",
    "Plan-les-Ouates", "Chêne-Bougeries", "Chêne-Bourg", "Thônex", "Onex", "Confignon",
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# CH1903+ / LV95, in metres: the register's E/N are already in it (Zurich's
# precedent; the tram-city skill, section 3). The derived UTM zone would be
# 32N (EPSG:32632).
CRS_PROJECTED = "EPSG:2056"
CRS_REGISTER = "EPSG:2056"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
# HALVED: the median nearest-neighbour gap among the 81 in-scope stops is
# 330 m (measured 2026-10-07; the spacing rule's line is about 550 m). Step 1
# stops outside 290-370 m.
MEDIAN_GAP_BOUNDS_M = (290.0, 370.0)

# --- Station scope: TPG's five trams, every stop in the 12 communes -----------

ROUTES = ("tram", "light_rail")
OPERATOR = None
LINE_REFS = ("12", "14", "15", "17", "18")
NOT_DRAWN = {}
STATION_ADD = {}
NAME_ALIASES = {}
# OSM names many of Geneva's stop positions with TPG's platform letter,
# "Bel-Air (A)", "Bel-Air (B)": one stop, two names, so the collapse counted
# it twice (gate 3 caught it: 102 stations against TPG's 85, 30 pairs within
# 40 m, 2026-10-07). Step 1 strips a trailing platform letter before the
# collapse, which then merges by name within MAX_SPREAD_M as usual; TPG's line
# pages name each stop once. osm_tram's NAME_ALIASES cannot do it, since it
# requires the target spelling to be present and here none is. The stops it
# applies to are listed, and step 1 stops if the list and OSM disagree (a
# letter added or fixed in OSM), so a stale fold cannot outlive the gap.
PLATFORM_LETTER_STOPS = {
    "Acacias", "Avanchets-Étang", "Balexert", "Bel-Air", "Bois-du-Lan", "Coutance",
    "Forumeyrin", "Gare Cornavin", "Industrielle", "Jardin-Alpin-Vivarium",
    "Meyrin-Village", "Place de Neuve", "Plainpalais", "Uni-Mail",
}
# The build of 2026-10-07: 85 stops, 81 in the 12 communes, tram 17's 4 in
# France (Gaillard 2, Ambilly 1, Annemasse 1), the brief's figures exactly.
EXPECTED_IN_SCOPE = 81
EXPECTED_OUTSIDE = 4
# Gate 3: TPG's own line pages, both directions, distinct stop names, the
# whole line before the scope split (tram 17's French stops included).
OPERATOR_STATION_COUNTS = {"12": 25, "14": 30, "15": 22, "17": 26, "18": 31}
OPERATOR_COUNTS_SOURCE = (
    "TPG (Transports publics genevois), line pages https://www.tpg.ch/fr/lignes/<n>, "
    "both directions, distinct stop names; timetable valid 2025-12-14 to 2026-12-12; "
    "read 2026-10-04 (the brief).")
SPACING_MIN_M = 80.0
MAX_SPREAD_M = 200
DRAWN_LINES = LINE_REFS
LINE_NAMES = {ref: f"Tram {ref}" for ref in LINE_REFS}
# TPG's colours as OSM tags them on both relations of each line (read
# 2026-10-07); step 3 asserts they are still OSM's and pipeline/linecolour.py
# measures them against the pins.
OSM_COLOURS = {"12": "#F5A300", "14": "#5A1E82", "15": "#84471C", "17": "#00ACE7",
               "18": "#B82F89"}
LINE_COLOURS = dict(OSM_COLOURS)

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "geneva_noga"
RAW_CLASSIFICATION_COLUMN = "activity_label"

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3601685451,3601685459,3601685465,3601685466,3601685472,3601685488,3601685502,3601685516,3601685520,3601685523,3601685534,3601685540)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("fr",)
PLACE_FOLD = None
# Rows a reader held that the owner ruled to keep (2026-10-13;
# docs/decisions_drafts/search-final.md). A record only: no code reads it.
# A street is listed by name, a place by OSM id with its name. Not in
# PLACE_REVIEWED, which check E holds to names carrying a leak word.
PLACE_RULED_KEPT = {
    # Held rows kept by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    # A home, family or person row is listed by id alone.
    "relation/1301860": "'Hôtel de Ville', A bare type word is kept on a Wikipedia article of the object's own (owner 2026-10-13, keep beats drop)",
    "way/1554778805": "'Friche de l'étang', A place name plus a type word is a name; the bare-type rule takes only a name that is all type (BARE_TYPE_NAMES, matched as the whole name)",
    "way/118190141": "'Parc des Molliers', same-named parks more than 300 m apart are two rows (owner, 2026-10-13)",
    "way/85344453": "'Morillon-Parc', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "Esplanade Théodelinde (Esplanade Théodore-de-Bèze)": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "way/40022875": "'Parc Eglantyne-Jebb (Parc des Acacias)', Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "way/77945334": "'Place Beatriz-Consuelo (Place Charles-Sturm)', Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "way/894896702": "'Le Lièvre et la Truite', A title is not a type (owner 2026-10-12)",
    "Ch. de la Parouse": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "La Promenade": "The description, code and ramp-name rules read minor or ramp-class ways only; another street keeps such a name (owner 2026-10-13: The Avenue stays; German answers 3: Weg A and Weg B)",
    "Route Blau": "A named private street is kept, a code-named one dropped (owner 2026-10-13, fourteen answers 8; PRIVATE_STREET_LEAD 2026-10-11)",
    "Allée Paul": "A named private street is kept, a code-named one dropped (owner 2026-10-13, fourteen answers 8; PRIVATE_STREET_LEAD 2026-10-11)",
    "Chemin Charles Baudouin": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Chemin François Joulet": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Allée du Vieil Orme": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Avenue Jules Crosnier": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Promenade Louise Boulaz": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Chemin des Longues Rasses": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Chemin J. Philibert de Sauvage": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Place Jean-HERIDIER": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
}
PLACE_REVIEWED = {
    "Chemin de l'Auberge": "a tertiary road, a real street name; the read of 2026-10-13",
}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "node/427495962": "'Acacias (F)': the stop Acacias under a platform letter, 11 m from the row Acacias (E) (node/1572466631), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1549447290": "'Avanchets-Étang (S)': the stop Avanchets-Étang under a platform letter, 11 m from the row Avanchets-Étang (R) (node/428676747), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1550806751": "'Balexert (Q)': the stop Balexert under a platform letter, 11 m from the row Balexert (P) (node/35416998), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1538653729": "'Bel-Air (B)': the stop Bel-Air under a platform letter, 7 m from the row Bel-Air (A) (node/1538653712), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1538555915": "'Bel-Air (E)': the stop Bel-Air under a platform letter, 109 m from the row Bel-Air (A) (node/1538653712), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1533266934": "'Bel-Air (F)': the stop Bel-Air under a platform letter, 134 m from the row Bel-Air (A) (node/1538653712), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1550672415": "'Bois-du-Lan (P)': the stop Bois-du-Lan under a platform letter, 11 m from the row Bois-du-Lan (O) (node/1550672534), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1538653739": "'Coutance (Z)': the stop Coutance under a platform letter, 13 m from the row Coutance (node/1033244930), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1550168468": "'Forumeyrin (L)': the stop Forumeyrin under a platform letter, 23 m from the row Forumeyrin (K) (node/698911254), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1549433444": "'Gare Cornavin (H)': the stop Gare Cornavin under a platform letter, 160 m from the row Gare Cornavin (node/1541473508), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/428678599": "'Gare Cornavin (I)': the stop Gare Cornavin under a platform letter, 163 m from the row Gare Cornavin (node/1541473508), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/306575952": "'Industrielle (Q)': the stop Industrielle under a platform letter, 7 m from the row Industrielle (P) (node/1572508529), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1550168376": "'Jardin-Alpin-Vivarium (W)': the stop Jardin-Alpin-Vivarium under a platform letter, 11 m from the row Jardin-Alpin-Vivarium (V) (node/695825965), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1550672568": "'Meyrin-Village (G)': the stop Meyrin-Village under a platform letter, 13 m from the row Meyrin-Village ( F) (node/1550672389), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1588234221": "'Place de Neuve (J)': the stop Place de Neuve under a platform letter, 11 m from the row Place de Neuve (I) (node/297914745), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/1562689375": "'Plainpalais (C)': the stop Plainpalais under a platform letter, 69 m from the row Plainpalais (node/1082706650), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    "node/427495963": "'Uni-Mail (P)': the stop Uni-Mail under a platform letter, 7 m from the row Uni-Mail (O) (node/1582369226), which would stay (lane 4 borderline read; owner, 2026-10-16)",
    # Rows the owner's later rulings of 2026-10-13 decide, and the twin checks' drops (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "way/81482906": "a place of worship named only by a denomination, a body or a chain, with no place or dedication in the name and no branch tag, is dropped (four rulings 1; ruling 2; owner 2026-10-13, relayed by Cleanup)",
    "node/1481253448": "a place of worship named only by a denomination, a body or a chain, with no place or dedication in the name and no branch tag, is dropped (four rulings 1; ruling 2; owner 2026-10-13, relayed by Cleanup)",
    "node/13266892496": "a place of worship named only by a denomination, a body or a chain, with no place or dedication in the name and no branch tag, is dropped (four rulings 1; ruling 2; owner 2026-10-13, relayed by Cleanup)",
    "node/13249887750": "a place of worship named only by a denomination, a body or a chain, with no place or dedication in the name and no branch tag, is dropped (four rulings 1; ruling 2; owner 2026-10-13, relayed by Cleanup)",
    "node/12284825261": "a place of worship named only by a denomination, a body or a chain, with no place or dedication in the name and no branch tag, is dropped (four rulings 1; ruling 2; owner 2026-10-13, relayed by Cleanup)",
    # Rows the read-only screen helper gave a drop verdict (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "way/1444049197": "twin of a dropped row: twins of PLACE_DROPPED (a description standing in for a name) (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/77946745": "duplicate within 300 m: duplicates of one object (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "node/2283383170": "worship named only by a denomination: worship named only by a denomination, a body or a chain (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "relation/4013107": "a freight yard, depot or operating point, not a passenger station (owner, 2026-10-13)",
    "node/12837201056": "a freight yard, depot or operating point, not a passenger station (owner, 2026-10-13)",
    "node/2406735664": "a business website name tagged a place of worship",
    "node/10848739906": "a code name duplicating the church 23 m away",
    "way/1444049097": "a description standing in for a name",
    "way/877866134": "a description standing in for a name, tagged a park",
    "way/440946686": "a spillway description glued on a river name",
    "way/1457818734": "a name that says the thing is temporary",
    "way/1457818735": "a name that says the thing is temporary",
    "way/1457818736": "a name that says the thing is temporary",
    "way/1457814057": "a status note glued on a river name; the river has its own row",
    "way/1457814058": "a status note glued on a river name; the river has its own row",
    "way/1457814068": "a status note glued on a river name; the river has its own row",
    "way/77946742": "a duplicate row of the square 45 m away, the weaker one",
    "node/13764446244": "a duplicate row of the park's own outline, the weaker one",
    "node/12822448853": "a locality node duplicating the park row",
    "node/12822076592": "a locality node duplicating the square row",
    "node/13712206211": "a locality node duplicating the garden row",
    "node/2562526841": "a parish node duplicating its church 45 m away",
    "node/12467398443": "English glued on the name; a stone kept at a museum",
    "way/83210157": "a lower-case duplicate of Chemin de Claire-Vue",
    "way/1276734116": "a bare type word standing as the whole name",
    "way/1276734120": "a bare type word standing as the whole name",
    "way/1276734121": "a bare type word standing as the whole name",
    "way/180632918": "an all-caps duplicate of Passage de la Tour",
    "way/798427820": "a mis-capitalized duplicate of Chemin du 23-Août",
    "way/409057998": "a direction label on a roundabout part",
    "way/409257973": "a direction label on a roundabout part",
    "way/408267999": "a direction label on a roundabout part",
    "way/26180222": "a direction label glued to the name",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "node/1917475456": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/85233022": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "node/2184046195": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/1191912503": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "way/1191912502": "A bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; a Wikidata entry alone does not keep it, keep-against-drop ruling 5); held rows settled 2026-10-13",
    "node/9629273704": "Duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M 2026-10-08 and 2026-10-13; six answers 6: second nodes of one district dropped); held rows settled 2026-10-13",
    "way/632236534": "A wrong object's name is a glitch and goes by id (owner 2026-10-11); held rows settled 2026-10-13",
    "way/754072344": "Station corridors and tunnels are no streets (owner 2026-10-13, language calls 8: Riga's station tunnels); held rows settled 2026-10-13",
}
# Kept by id: admitted as rows although a rule passes them over (owner, 2026-10-13;
# docs/decisions_drafts/search-final.md).
PLACE_KEPT = {
    "way/313487068": "'Banc de la Treille', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "node/2362831289": "'Maison Rousseau et Littérature', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "way/5170038": "'Île Jean-Jacques-Rousseau', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "way/1464178616": "'Mur des Réformateurs', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "node/3436729151": "'Patek Philippe Museum', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "way/87603849": "'Maison Tavel', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
}
