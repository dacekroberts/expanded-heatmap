"""Copenhagen-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

FIRST DANISH CITY. The national facts - Datafordeler, CVR's four-file join,
DAR, the columns never to load, the sole-trader guard - live in
`pipeline/countries/denmark.py`. What is Copenhagen's own is below: the two
kommuner, the rail scope, the palette and the catch-all verdict.
"""

from pathlib import Path

from pipeline.countries import denmark as DK

SLUG = "copenhagen"

# REGIONAL adds the eight kommuner Hovedstadens Letbane stands in, and the
# Letbane itself, the owner's call 66 of 2026-10-06
# (docs/build_briefs/copenhagen_regional.md; the regional-extension skill).
# False reproduces the city-alone build byte for byte, which the drift check
# proved before the switch went on.
REGIONAL = True
NAME = "Copenhagen (Regional)" if REGIONAL else "Copenhagen"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "copenhagen" / "raw"
DATA_PROCESSED = ROOT / "data" / "copenhagen" / "processed" / ("regional" if REGIONAL else "")
OUTPUTS = ROOT / "outputs" / "copenhagen"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the two kommuner, with the kommune each IS in - a citable
# scoping record. Most are S-tog stations on the lines' suburban reaches.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs. `fetch_sources.py` downloads them; no step may fetch. CVR and DAR
# are cached once for the country (`denmark.SHARED_RAW`); the two OSM files
# are Copenhagen's own.
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_KOMMUNER_JSON = DATA_RAW / "osm_kommuner.json"
# OSM's imported DAR address points (`osak:identifier`) in the ten kommuner,
# the regional map's placement; see PLACEMENT below.
OSM_ADDRESS_POINTS_TSV = DATA_RAW / "osm_osak_points.tsv"
# What was fetched, which generation, and when - committed, and never a URL
# with the key in it.
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Scope: TWO kommuner ------------------------------------------------------
#
# ✅ KOBENHAVN (0101) + FREDERIKSBERG (0147), owner's call 2026-09-24.
# Frederiksberg is a separate kommune ENTIRELY ENCLOSED by Kobenhavn and holds
# 7 Metro stations; scoped out, it is a hole in the middle of the map with
# three Metro lines drawn through it. By the worst-line rule the French cities
# and Oslo were scoped on:
#
#                 Kobenhavn only      + Frederiksberg
#     M1          10/15               15/15
#     M2           9/16 (56%)         14/16   (Kastrup, Lufthavnen: Taarnby)
#     M3          13/17               16/17   (to be re-measured at step 1)
#     M4          12/13               12/13
#
# Taarnby's two airport stations stay out and are named as excluded.
#
# ⚠ THE BUSINESS FILTER IS CVR's OWN `CVRAdresse_kommunekode` ON THE LOCATION
# ADDRESS, never a polygon - it is the register's authoritative field. The
# polygons below decide only which STATIONS are in scope.
CITY_KOMMUNER = {"101": "Kobenhavn", "147": "Frederiksberg"}   # CVR's unpadded codes
# The regional eight, one Letbane stop or more each (call 66 a). NEVER
# Albertslund (165), call 66 c, nor Gentofte, Ballerup or Rudersdal, whose
# share of an outer ring is disclosed rather than counted.
LETBANE_KOMMUNER = {
    "173": "Lyngby-Taarbaek", "159": "Gladsaxe", "163": "Herlev", "175": "Rodovre",
    "161": "Glostrup", "153": "Brondby", "187": "Vallensbaek", "183": "Ishoj",
}
KOMMUNER = CITY_KOMMUNER | LETBANE_KOMMUNER if REGIONAL else CITY_KOMMUNER
DAR_KOMMUNER = ("0101", "0147")                           # Datafordeler's padded
SCOPE_WORDS = "the ten kommuner" if REGIONAL else "Kobenhavn and Frederiksberg"

# --- Placement ------------------------------------------------------------
#
# The city alone: DAR's Adressepunkt via Datafordeler (98.3%). The regional
# map: OSM's DAR address points, Aarhus's and Odense's placement, for all ten
# kommuner (owner, 2026-10-07). The Datafordeler account was closed after
# Copenhagen published (2026-09-24), which call 66 d had not allowed for; one
# keyless source over the whole map was preferred to a split by area.
# Measured 2026-10-07 against the published map: 14,897 of the 14,922
# DAR-placed central storefronts placed (25 lost, none gained), half moved
# 0.03 m or less, 6 between 5 and 10 m, none further; the eight added
# kommuner 3,780 of 3,907 (96.7%; DAR's ceiling 97.0%). DAR via a reopened
# account remains a way back (docs/decisions_drafts/worktree-abroad-batch.md).
PLACEMENT = DK.PLACEMENT_OSM_OSAK if REGIONAL else DK.PLACEMENT_DAR

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# ETRS89 / UTM 33N. Copenhagen's longitude (~12.57 E) falls in UTM zone 33
# (12-18 E) - by 0.57 degrees, derived per city as the invariant asks. ⚠ DAR
# publishes its points in zone 32 (EPSG:25832) NATIONALLY, Copenhagen
# included; that is `denmark.DAR_CRS` and is converted on read, never used
# for this city's geometry.
CRS_PROJECTED = "EPSG:25833"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# THE SHARED EDGES, on Philadelphia's measured ground rather than by default.
# Measured 2026-09-24 across the 64 in-scope stations (nearest neighbour,
# ETRS89 / UTM 33N metres, after the name collapse):
#
#     min 358    median 708    mean 753    max 1,743
#
# Philadelphia's subway/el sits at a 711 m median and keeps these edges, "so
# the 0.6 mi outer ring still reads as a gradient rather than a wash". The
# halved edges were taken where the median was 341-541 m (Marseille, Oslo,
# Lille, Toulouse, Rennes); at 708 m their 483 m outer ring would stop well
# short of every neighbour. Settled on that measurement, not re-asked.
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# WHAT COUNTS - owner's calls, 2026-09-24:
#
#   * Metro M1-M4 (OSM `route=subway`).
#   * S-tog A, B, Bx, C, E, F, H (OSM `route=light_rail`, network S-tog) - on
#     the published spacing-and-frequency test, Dublin's DART precedent,
#     NOT as an exception to it. Inside the two kommuner S-tog's median
#     station spacing is 1,227 m (F: 892 m) against the Metro's 884 m, every
#     line but Bx (peak hours only, every 20 min; DSB s-tog-s26.pdf) runs
#     every 10 minutes through the day, and 22 of its 31 stations in
#     scope have no Metro station within 400 m. Paris's RER was excluded as an
#     overlay on a Metro that already covers the city; S-tog is the network in
#     the districts the Metro does not reach.
#   * NOT regional or InterCity trains (`route=train`), Lokaltog 910, or
#     Hovedstadens Letbane - the last opened in full on 22 August 2026 and has
#     no stop in either kommune.
#   * REGIONAL: Hovedstadens Letbane (L) joins, 29 stops in the eight
#     kommuner (call 66 a); every train serves every stop, every 5-8 minutes
#     on weekdays 08-17 (dinletbane.dk/da/koereplan/, read 2026-10-06).
#
# RAIL FROM OSM, NOT REJSEPLANEN - owner's call 2026-09-24, and the ground
# the osm-rail skill asks for. Rejseplanen's national GTFS is keyless and
# current, but its Labs guidelines ask users not to change the data so that
# it differs from the original, and document access as by request with those
# guidelines accepted. Neither point was resolved in this project's favour,
# so the feed was not downloaded. OSM (ODbL) names and colours every line.
METRO_REFS = ("M1", "M2", "M3", "M4")
STOG_REFS = ("A", "B", "Bx", "C", "E", "F", "H")
# A WHITELIST ON THREE TAGS, never on `network`: the Metro and S-tog relations
# carry network "Takst Sjaelland" - the fare zone, not the system - and the
# Letbane carries "Movia". Metro is `route=subway` by ref; S-tog is
# `route=light_rail` by ref AND operator, which is what keeps out Lokaltog 910
# (Lokaltog A/S) and the Letbane's "L" (no operator), both also light_rail.
STOG_OPERATOR = "DSB"
# The Letbane has no `operator` tag (only `operator:wikidata`), so it is kept
# on route + ref + the system's wikidata: `ref=L` alone is unique in the bbox
# today (Gribskovbanen is L41), and wikidata pins the system.
LETBANE_REFS = ("L",) if REGIONAL else ()
LETBANE_WIKIDATA = "Q10655459"

# OSM ref -> the name riders use. The mode word distinguishes Metro M1 from
# a bus and S-tog A from anything else lettered A. One Letbane line, so the
# system's name, Odense's precedent.
LINE_NAMES = {
    "M1": "Metro M1", "M2": "Metro M2", "M3": "Metro M3", "M4": "Metro M4",
    "A": "S-tog A", "B": "S-tog B", "Bx": "S-tog Bx", "C": "S-tog C",
    "E": "S-tog E", "F": "S-tog F", "H": "S-tog H",
} | ({"L": "Hovedstadens Letbane"} if REGIONAL else {})

# One station under two names, merged only where named here. Interchanges
# that share ONE name across the two modes (Norreport, Kobenhavn H, Osterport,
# Nordhavn, Kobenhavn Syd, Norrebro, Flintholm, Vanlose) collapse by name
# without an entry, and step 1 prints each one's spread before trusting it.
STATION_NAME_ALIASES = {}

SPACING_MIN_M = 400.0

# THE AGENCIES' OWN COLOURS, from the OSM route relations (read 2026-09-24),
# with TWO S-tog colours moved. The shared check (pipeline/linecolour.py,
# Delta-E floor 10) REFUSED two Metro / S-tog pairs, because DSB and
# Metroselskabet chose near-identical shades independently:
#
#   S-tog F  #fcc019 was  5.1 from Metro M2's #ffc600 - both yellow.
#            -> #fdcb41 (HSL lightness +0.08): 13.1 from M2; 9.9 from DSB's.
#   S-tog A  #00a4eb was  9.6 from Metro M4's #009cd3 - both blue.
#            -> #05b4ff (lightness +0.05): 13.7 from M4; 6.2 from DSB's.
#
# The METRO keeps its colours and the S-tog member moves - Oslo's rule for
# Trikk 12 against T-bane 3, one primary line per pair. LIGHTER, hue and
# saturation kept, for Lille's reason: the maps open on a dark basemap the
# check does not score. Each step is the smallest that clears the floor with
# Oslo's ~13 margin. H (#e63511) is 15.4 from M3's red and passes as DSB's.
# Below the preferred 45 against the pins, recorded rather than moved:
# M1 19.0 and E 21.7 (vs Personal services / Retail), A 29.8, M4 31.7,
# B 36.3, Bx 38.6.
#
# REGIONAL: the Letbane's OSM #32ac5c is 11.4 from M1's #008d41, over the
# floor but under Oslo's ~13 margin, so it moves on the same rule (the newer
# line, never the Metro): HSL lightness +0.02 -> #34b460, 14.4 from M1, 20.5
# from S-tog B, 3.6 from OSM's. 16.5 against the Personal services pins,
# below the preferred 45 and recorded, as M1's 19.0 is.
LINE_COLOURS = {
    "M1": "#008d41", "M2": "#ffc600", "M3": "#ff0a0a", "M4": "#009cd3",
    "A": "#05b4ff", "B": "#50ae30", "Bx": "#adce6d", "C": "#f68b1f",
    "E": "#7670b3", "F": "#fdcb41", "H": "#e63511",
} | ({"L": "#34b460"} if REGIONAL else {})

# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope
# decision is CHECKABLE rather than merely written down. Measured 2026-09-24
# on OSM's kommune polygons (Kobenhavn 94.4 km2 with Frederiksberg's 8.7 km2
# as its inner ring). Every Metro line keeps all its stations but M2, whose
# two missing are Kastrup and Lufthavnen in Taarnby; Gammel Strand, which
# DAWA's polygon left in the harbour, is inside OSM's. S-tog F is 12 of 12
# because Hellerup's platforms sit just inside Kobenhavn on BOTH DAWA's and
# OSM's boundary - its ring counts only the Kobenhavn side, since businesses
# are filtered on CVR's own kommune code. If these move, the scope decision
# is being re-taken and should be re-taken deliberately.
EXPECTED_INSIDE_PER_LINE = {
    "M1": 15, "M2": 14, "M3": 17, "M4": 13,
    "A": 11, "B": 12, "Bx": 12, "C": 17, "E": 11, "F": 12, "H": 9,
}

# CALL 66 b: the eight suburban S-tog stations in the Letbane kommuner are IN
# only if their line passes Copenhagen's S-tog test there (spacing and
# coverage measured by the brief; frequency read from DSB). Station name ->
# the reason excluded_stations.csv gives; empty when every line passes.
# Read 2026-10-07 in DSB's S-tog timetable (s-tog-s26.pdf, valid from
# 2025-12-14), weekday daytime: A every 10 min at Brondby Strand; B every 10
# min at Brondbyoster, Bagsvaerd, Kildebakke, Skovbrynet and Stengarden; E
# every 10 min at Sorgenfri and Virum (A stops there in the evening only).
# Bx fails (every 20 min, peak only), but its one station of the eight,
# Kildebakke, is on B. So all eight are IN and nothing is listed here.
STOG_TEST_OUT = {}
if REGIONAL:
    EXPECTED_INSIDE_PER_LINE = {
        "M1": 15, "M2": 14, "M3": 17, "M4": 13,
        "A": 17, "B": 19, "Bx": 15, "C": 18, "E": 15, "F": 12, "H": 10, "L": 29,
    }

# GATE 3, read 2026-09-24 - and neither figure is a clean first-party count.
#   * Metro: 15 / 16 / 17 / 13, network 44 - English Wikipedia's line table
#     (a secondary source; Metroselskabet's own pages were not read for it).
#   * S-tog: DSB's own S-tog page says BOTH "dækker 87 stationer" and, lower
#     down, "dækker 86 stationer og består af 7 linjer". 87 is used because it
#     is the page's first statement and Danish Wikipedia's figure; the other
#     is recorded rather than hidden. A one-station disagreement is a prompt
#     to look at the network list, not a pass.
#   * REGIONAL, Letbane: 29, first-party ("29 stationer", dinletbane.dk's
#     line page, read 2026-10-06 and by brief_check 2026-10-07).
OPERATOR_STATION_COUNTS = {
    "Metro M1": 15, "Metro M2": 16, "Metro M3": 17, "Metro M4": 13,
    "Metro (network)": 44, "S-tog (network)": 87,
} | ({"Letbane (network)": 29} if REGIONAL else {})
OPERATOR_COUNTS_SOURCE = (
    "Metro per line and 44: en.wikipedia Copenhagen Metro (secondary); S-tog 87: "
    "dsb.dk/s-tog, which also says 86 on the same page - read 2026-09-24"
    + ("; Letbane 29: dinletbane.dk line page, read 2026-10-06" if REGIONAL else ""))

# The Overpass bbox: the whole S-tog network, Koge to Hillerod and
# Frederikssund, so step 1 can name the kommune of every station it drops.
RAIL_BBOX = (55.40, 12.00, 56.00, 12.70)       # south, west, north, east

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "denmark_db25"
RAW_CLASSIFICATION_COLUMN = "db25_label"
CITY_KEEP = "COPENHAGEN"   # kept for the scaffold's templates; KOMMUNER filters

# The per-city catch-all verdict, which denmark_db25.py declines to make.
# Measured 2026-09-24 on Copenhagen's own profile (15,847 storefronts):
#
#     969900  Andre personlige serviceydelser i.a.n.
#             613 rows (3.9%) - personally owned 82%, above ground 50%
#             (all storefronts: 39% and 23%)
#
# Oslo's 96.990 signature (87% sole traders, 5% with employees) and France's
# 96.09Z, on Copenhagen's own numbers. A hand sample of the 109 company-form
# rows found tattoo studios (~70 across the whole code) and dog groomers
# beside coaching, healing, consulting, dog walking, a photo-booth company and
# a municipal public toilet - so the exclusion DOES lose some real shopfronts,
# tattoo studios above all, and says so on the page. The six RETAIL
# catch-alls and 561190 (øvrige spisesteder) are kept, as in Oslo and France:
# shops and eateries by product.
CATCH_ALL_EXCLUDE = ("969900",)

# Sanity bounds: the placed storefronts' measured extent (55.6166-55.7316 N,
# 12.4562-12.6655 E, 2026-09-24) plus ~0.02 deg. Catches a corrupt
# coordinate; the join to DAR does the placing, and it dropped none.
COPENHAGEN_BBOX = {
    "lat_min": 55.59,
    "lat_max": 55.76,
    "lon_min": 12.43,
    "lon_max": 12.69,
}
# REGIONAL: the ten kommuner's polygons span about 55.59-55.81 N,
# 12.21-12.69 E (the brief), plus ~0.02 deg; never the rail bbox.
if REGIONAL:
    COPENHAGEN_BBOX = {"lat_min": 55.57, "lat_max": 55.83, "lon_min": 12.19, "lon_max": 12.71}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602183062,3602186643,3602186660,3602187055,3602187129,3602190423,3602191207,3602191218,3602192190,3602192363)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("da",)
PLACE_FOLD = None
# Rows a reader held that the owner ruled to keep (2026-10-13;
# docs/decisions_drafts/search-final.md). A record only: no code reads it.
# A street is listed by name, a place by OSM id with its name. Not in
# PLACE_REVIEWED, which check E holds to names carrying a leak word.
PLACE_RULED_KEPT = {
    "Fabriksområdet": "a real local name on Christiania's paths (owner, 2026-10-13)",
    "Nordområdet": "a real local name on Christiania's paths (owner, 2026-10-13)",
    "Sydområdet": "a real local name on Christiania's paths (owner, 2026-10-13)",
    "Flaskehalsen": "a real local name on Christiania's paths (owner, 2026-10-13)",
    "Fredens Ark": "a real local name on Christiania's paths (owner, 2026-10-13)",
    "Psyak": "a real local name on Christiania's paths (owner, 2026-10-13)",
    "Løvehuset": "a real local name on Christiania's paths (owner, 2026-10-13)",
    "Mælkebøtten": "a real local name on Christiania's paths (owner, 2026-10-13)",
    "Mælkevejen": "a real local name on Christiania's paths (owner, 2026-10-13)",
    # Held rows kept by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    # A home, family or person row is listed by id alone.
    "node/12269322560": "'Engelsk Have', Named sections of public gardens stay (owner 2026-10-13, fifteen answers 14)",
    "node/12269322561": "'Cherry Grove', Named sections of public gardens stay (owner 2026-10-13, fifteen answers 14)",
    "node/12269322562": "'Nordamerikansk Skov', Named sections of public gardens stay (owner 2026-10-13, fifteen answers 14)",
    "node/12269322563": "'Egeskov', Named sections of public gardens stay (owner 2026-10-13, fifteen answers 14)",
    "node/12269322564": "'Birkeskov', Named sections of public gardens stay (owner 2026-10-13, fifteen answers 14)",
    "node/12269322565": "'Vinterhave', Named sections of public gardens stay (owner 2026-10-13, fifteen answers 14)",
    "way/134655236": "'Studio Oliver Gustav', An article of the object's own outweighs a private operator or a business reading (owner 2026-10-13, keep beats drop; dealer galleries go only without an article)",
    "node/6372863355": "'Edition Copenhagen', An article of the object's own outweighs a private operator or a business reading (owner 2026-10-13, keep beats drop; dealer galleries go only without an article)",
    "node/4886228802": "'Galerie Birch', An article of the object's own outweighs a private operator or a business reading (owner 2026-10-13, keep beats drop; dealer galleries go only without an article)",
    "way/1371647599": "'Nexus Landscape', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/330699477": "'Strandgården', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/330699476": "'Ågården', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/313263227": "'Emaljehaven', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/548176169": "'Søborghave \"Marken\"', A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/25567918": "A castle is no home by its tags and its row stays; the web check on castles is owed and no rule is built (exclusions: considered and not built)",
    "way/133721518": "'Margethehaven', A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "node/9804890264": "'Soka Gakkai Internatinal Danmark', A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "way/404898332": "A park tied to a housing complex, a company or a neighbour only by its name stays (owner 2026-10-13, second batch g; parks named only as an intersection stay)",
    "way/1472680157": "'Nordens Plads Byrum', The not-there rule reads demolished, removed or not yet open; a place that stands today stays (lifecycle 2026-10-13; was: on a place is not read)",
    "node/14133275087": "'Den Gule Plads', The not-there rule reads demolished, removed or not yet open; a place that stands today stays (lifecycle 2026-10-13; was: on a place is not read)",
    "way/946799580": "A tourism, amenity or aeroway landmark with a Wikidata entry meets the notable rule (NOTABLE_ONLY 2026-10-07)",
    "way/26181018": "A venue's own name is a public name, kept as OpenStreetMap gives it (owner 2026-10-03: a trade or venue name is no personal name)",
    "Rosengården": "A minor way is kept with an entry or article of its own (2026-10-07)",
    "Prins Jørgens Gård": "A minor way is kept with an entry or article of its own (2026-10-07)",
    "Klostergårdens Passage": "Shopping galleries and passages open to the public are kept (owner 2026-10-13, fourteen answers 11)",
    "Kemitorvet": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Matematiktorvet": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Biologiens Vej": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "DBU Allé": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Handelstorvet": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Bygningstorvet": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Kemikalievej": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Maskinvej": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Montagehalsvej": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Chokoladevej": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Grønjordskollegiet": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Kagsåkollegiet": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Voldboligerne": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Frankrigshusene": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Kamhusene": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Hegnshusene": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Mejerihusene": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Rødovre Centrum": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Brøndby Strand Centrum": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Gladsaxe Trafikplads": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Nokken Forgaden": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Nokken Hovedgaden": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Nyvang Hovedvej": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Nyvang Mellemvej": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Nyvang Nordvej": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Nyvang Sydvej": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Nyvang Vestvej": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Nyvang Åvej": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Nyvang Østvej": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
}
PLACE_REVIEWED = {}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    # Rows the owner's later rulings of 2026-10-13 decide, and the twin checks' drops (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "way/26274768": "a place of worship named only by a denomination, a body or a chain, with no place or dedication in the name and no branch tag, is dropped (four rulings 1; ruling 2; owner 2026-10-13, relayed by Cleanup)",
    # Rows the read-only screen helper gave a drop verdict (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "node/6512571485": "religious body's meeting hall: ruling 2 (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/185253291": "religious body's meeting hall: ruling 2 (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/350088175": "religious body's meeting hall: ruling 2 (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/199817432": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/199817433": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/199817434": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/209490451": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/25316710": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/25316719": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/25316720": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/25316724": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/25316726": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/25316728": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/25316731": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/25316737": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/25316742": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/307063770": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/320849903": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/320849907": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/320849908": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/320849913": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/386982102": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/33629014": "an allotment section code beside the estate's name (owner, 2026-10-13)",
    "way/118946532": "a mall's, estate's or facility's own name on its paths, not a street (owner, 2026-10-13)",
    "way/108175582": "a mall's, estate's or facility's own name on its paths, not a street (owner, 2026-10-13)",
    "way/116962121": "a mall's, estate's or facility's own name on its paths, not a street (owner, 2026-10-13)",
    "way/943619169": "a mall's, estate's or facility's own name on its paths, not a street (owner, 2026-10-13)",
    "way/943619172": "a mall's, estate's or facility's own name on its paths, not a street (owner, 2026-10-13)",
    "relation/27542": "building numbers standing in for a name",
    "way/145618061": "a youth school tagged a park",
    "way/162383253": "a scout group tagged a park",
    "way/222142140": "a glitched name (unclosed quote); a restaurant's garden tagged a park",
    "way/819016737": "a glitched name (stray backslash)",
    "node/2560055197": "a second name glued on in brackets",
    "node/10598601805": "public art with no article; the maker's name glued onto the title",
    "node/12373427503": "a manhole cover tagged a monument; a code-like name",
    "node/9544674716": "public art with no article or wikidata",
    "node/1440246013": "a memorial sculpture with no article or wikidata; a description standing in for a name",
    "node/6646676087": "an artwork its own description tag says was removed in 2020",
    "way/939307403": "a private estate courtyard tagged a locality",
    "way/1021370390": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/1021501021": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/1021501023": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/28280273": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/85939478": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/1021368397": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/1021368402": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/1021368403": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/145799925": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/91617717": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/1021368405": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/1054127116": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/27275321": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/27275320": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/91118827": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/91118832": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/91118815": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/91118836": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/155280117": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/8224001": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/93049289": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/91118824": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/91118844": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/91118837": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/93049283": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/91118845": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/91734948": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/1097986831": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/1097987459": "a code beside a type word on minor ways only (an allotment's numbered or lettered road)",
    "way/91622309": "an address standing in for a name, one service way",
    "way/122287837": "a glitched name (a tag key glued on)",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "way/341565866": "Museum, zoo and theme-park contents stay only with a Wikipedia article of their own (owner 2026-10-13, fifteen answers 4); held rows settled 2026-10-13",
    "way/133940331": "A business with nothing else is dropped (2026-10-07); only an article of its own outweighs it (owner 2026-10-13); held rows settled 2026-10-13",
    "way/266646050": "a chapel inside a prison (owner, 2026-10-13)",
    "way/266646075": "a chapel inside a prison (owner, 2026-10-13)",
    "way/480987209": "A description standing in for a name goes by id (owner 2026-10-11; skill: a description longer than a type word); held rows settled 2026-10-13",
    "way/25674413": "One object drawn in parts is one row (fourth pass 40, 2026-10-13); held rows settled 2026-10-13",
    "node/1017968484": "One row a station (second batch 5, 2026-10-13); held rows settled 2026-10-13",
    "node/4989664667": "One row a station (second batch 5, 2026-10-13); held rows settled 2026-10-13",
    "way/147007470": "A home with no sign of visiting is no row; an article or a heritage listing is not enough (home rule 2026-10-08; fifteen answers 2); held rows settled 2026-10-13",
}
