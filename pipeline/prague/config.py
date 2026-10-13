"""Prague-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

FIRST CZECH CITY. The national facts - ROS02, RES, RUIAN, the legal forms,
the CRS - live in `pipeline/countries/czechia.py`. What is Prague's own is
below: the obec, the metro, Flora, the palette and the catch-all verdict.
"""

from pathlib import Path

SLUG = "prague"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "prague" / "raw"
DATA_PROCESSED = ROOT / "data" / "prague" / "processed"
OUTPUTS = ROOT / "outputs" / "prague"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the obec, if any - the brief measured all 60 metro
# station-line pairs inside it, so this is expected to be written EMPTY.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

# Until the tram rescope lands, steps 1 and 3 write and read a branch-only
# folder: data/ is shared by every worktree. At landing set TRAM_DIR =
# DATA_PROCESSED and re-run steps 1 and 3.
TRAM_DIR = DATA_PROCESSED / "tram"
STATIONS_CSV = TRAM_DIR / "stations.csv"
TRAM_SHAPES_JSON = TRAM_DIR / "tram_shapes.json"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs. `fetch_sources.py` downloads them; no step may fetch. ROS02, RES
# and the CZ-NACE codebooks are national (`czechia.SHARED_RAW`); RUIAN is per
# obec, and the rail and boundary are Prague's own.
GTFS_ZIP = DATA_RAW / "pid_gtfs.zip"
RUIAN_ZIP = DATA_RAW / "ruian_adr_554782.csv.zip"
# The RUIAN coordinate control czechia_register.ruian() re-checks: one known
# address IN THIS OBEC, as (RUIAN code, lat, lon, label). Prague Castle, Hrad
# I. nádvoří, measured in the brief at 50.08948, 14.39861 under EPSG:5513 with
# (X, Y) as published. The wrong axis orders land in Germany or the Arctic and
# still look like coordinates. Each Czech city declares its own - this lived
# in the shared module until 2026-09-27 and would have stopped Brno.
RUIAN_CRS_CONTROL = ("21690278", 50.08948, 14.39861, "Prague Castle")
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
OSM_RAIL_JSON = DATA_RAW / "osm_rail.json"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# PID - Pražská integrovaná doprava, via ROPID. Keyless, CC BY 4.0, credit
# ROPID and state the changes (pid.cz/o-systemu/opendata/, read 2026-09-24).
# ⚠ Its feed_info declares a TWO-WEEK window - a stale copy means refetch.
GTFS_URL = "https://data.pid.cz/PID_GTFS.zip"

# --- Scope ---------------------------------------------------------------
#
# Obec 554782, Praha - which is also the region, so the city IS its own
# kraj. The businesses are scoped by RUIAN's own address list for the obec
# (ROS02's PKODADM in it), never by a polygon.
OBEC = "554782"
# The boundary, for station scope and label anchoring only: OSM relation
# 435514 ("Praha", admin_level 4, ref:nuts CZ010) - the ONLY relation a
# bbox-bounded name search returns (2026-09-24). ČÚZK's INSPIRE polygon
# measured 496.2 km² in the brief; step 1 gates the OSM one on that.
OSM_BOUNDARY_RELATION = 435514
BOUNDARY_AREA_KM2 = (480.0, 510.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 33N: Prague's longitude (~14.44 E) falls in the 12-18 band. Derived
# per city, not copied. RUIAN's S-JTSK (EPSG:5513) is converted on read and
# never used for this city's geometry.
CRS_PROJECTED = "EPSG:32633"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# THE SHARED EDGES, on measured spacing: the 58 stations' nearest-neighbour
# distances are min 450, median 912, mean 935, max 1,491 m (2026-09-24) -
# sparser than Philadelphia's 711 m and Copenhagen's 708 m, which both keep
# these edges. The halved edges were taken only at medians of 341-541 m.
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# WHAT COUNTS - owner's calls, 2026-09-24 (before the pause, banked in the
# brief): METRO A, B, C ONLY (`route_type 1`). Prague's trams are a dense
# overlay on the metro across the whole centre, not a separate corridor; the
# Petřín funicular, the ferries and the S-trains go on the standing rules,
# as in Paris.
ROUTE_TYPE_METRO = "1"
LINE_NAMES = {"A": "Metro A", "B": "Metro B", "C": "Metro C"}
# The operator's own livery, from the feed's route_color, with ONE colour
# moved. The shared check (pipeline/linecolour.py, Delta-E floor 10) REFUSED
# metro A's #00A562 at 9.2 from the Personal services pins (#1baf7a) - the
# line would vanish under its own dots. Lightened in HSL lightness only, hue
# and saturation kept, by the smallest step that clears the floor with
# Copenhagen's ~13 margin: +0.04 -> #00b96e, 13.1 from the pins and 8.5 from
# DPP's green. Lighter, not darker, for Lille's reason (the dark basemap).
# B #F8B322 is 86.9 from its nearest pin; C #CF003D is 21.2 from Food
# service, below the preferred 45 and recorded rather than moved.
LINE_COLOURS = {"A": "#00b96e", "B": "#F8B322", "C": "#CF003D"}

# FLORA IS COUNTED, NOT DRAWN - owner, 2026-09-29, superseding the call of
# 2026-09-24 that drew it: stations closed for works are drawn as the
# timetable runs, in every city (docs/category_rules.md, "Station scope").
# Line A's Flora is CLOSED FOR RECONSTRUCTION (DPP: from 1 February 2026; first
# due back in early December 2026, now about the end of February 2027, since
# more of the platform ceiling needs replacing - expats.cz quoting DPP,
# 2026-08-23, read 2026-10-03), so no metro trip calls there and a trip-based station list has A at 16 where the
# operator has 17. Step 1 locates it from PID's own stops.txt (parent station
# U118S1) so the gates match the operator, then lists it in
# excluded_stations.csv as closed for works; it STOPS the build once the feed
# serves Flora again, so this override cannot outlive the closure.
FLORA_PARENT = "U118S1"
FLORA_NAME = "Flora"
FLORA_LINE = "A"
FLORA_REASON = ("line A, closed for works (reconstruction since 1 February 2026), "
                "reopening about the end of February 2027 (DPP)")

# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1. Measured
# 2026-09-24 against OSM relation 435514 (495.9 km²): every station of all
# three lines is inside the obec, Flora included, so commune scope costs the
# metro nothing - Paris's and Marseille's shape.
EXPECTED_INSIDE_PER_LINE = {"A": 17, "B": 24, "C": 20}

# GATE 3 - A 17 / B 24 / C 20, 58 distinct stations: English Wikipedia's
# Prague Metro article, read 2026-09-24 (a SECONDARY source). The feed gives
# 16 / 24 / 20 from its trips and 17 for A only with Flora added, and OSM's
# route relations give 16 / 24 / 20, omitting Flora too - so the operator's
# count is what shows Flora still belongs to line A.
OPERATOR_STATION_COUNTS = {"Metro A": 17, "Metro B": 24, "Metro C": 20,
                           "Metro (network)": 58}
OPERATOR_COUNTS_SOURCE = ("A 17 / B 24 / C 20, 58 stations: en.wikipedia Prague Metro "
                          "(secondary), read 2026-09-24")

# --- Trams (tram rescope, owner 2026-10-13) ------------------------------------
#
# SUPERSEDES "metro only" above: every day tram route at 15 minutes or better
# is drawn, one line each ("Tram N"), as the timetable runs (owner,
# 2026-10-13; docs/decisions_drafts/tram-rescope.md). Stops take the
# sub-transit-line filters in pipeline/prague/trams.py.
#
# The tram feed is a re-pull of GTFS_URL under its own name (data/ is shared
# by every worktree); the metro above still reads GTFS_ZIP. Its two-week
# window is asserted, so a new edition stops the build until the routes are
# re-read.
TRAM_GTFS_ZIP = DATA_RAW / "pid_gtfs_2026-10-13.zip"
TRAM_FEED_WINDOW = ("20261013", "20261026")
# 23 regular routes (no 14 or 16 in this feed) and five that run only for now:
# 30, 31 and 37 are the only trams on the Spojovací branch, 30 the only one at
# Třebenická, 32 and 40 the only ones at Smíchovské nádraží (measured
# 2026-10-13). 37 is flagged is_substitute_transport and drawn all the same
# (owner). Why the regular routes are off those stops was not read.
TRAM_LINES = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
              "15", "17", "18", "19", "20", "21", "22", "24", "25", "26",
              "30", "31", "32", "37", "40")
# Day routes not drawn, each with why. Night routes 90 to 99 (is_night) are
# not drawn on the per-route rule and need no row here.
TRAM_NOT_DRAWN = {"23": "every 30 minutes at midday, fails the 15-minute test"}
# Wednesday in the feed window; 10:00 to 15:00, the busier direction.
TRAM_HEADWAY_DAY = "20261014"
TRAM_MAX_HEADWAY_MIN = 15.0
# A stop pattern is regular at this share of its line's trips or more.
TRAM_REGULAR_TRIP_SHARE = 0.10
# A tram stop this close to a drawn metro station is that station; a stop of
# the station's own name, to the wider distance (Toronto's and Milan's values).
TRAM_PLACE_MAX_SPREAD_M = 200.0
# Stop names whose platforms sit farther apart than that, each read and kept
# as one place. A name appearing or leaving stops the build.
# Measured 2026-10-13: Vinice 210 m (platforms staggered along one street);
# Palmovka 256 m, Nádraží Holešovice 319 m and Želivského 326 m are metro
# stations with tram platforms on more than one side, and attach to them.
TRAM_WIDE_PLACES = ("Vinice", "Palmovka", "Nádraží Holešovice", "Želivského")
TRAM_ATTACH_M = 150.0
TRAM_ATTACH_NAMED_M = 400.0
TRAM_THIN_SPACING_MILES = 0.5
# ONE LABEL, LEGEND ROW AND COLOR PER GROUP OF ROUTES (owner, 2026-10-13). One
# label per route was built first and failed the phone label check: 5
# overlapping pairs at 375 px and 16 at 343, where the whole network shows in
# about 175 by 170 px. The groups are the project's, not PID's: routes merged
# by average shared track (track within 40 m, over the shorter route). Ten
# groups place every label at 1024, 375 and 343; eight and twelve did not.
# Two routes of a group share as little as 26% of their track (2 and 24).
# Re-measure the groups if TRAM_LINES changes.
#
# PID gives every tram one color (#7A0603), so these are the project's: each
# 45 or more (CIE76) from every category pin, 18 or more from every line
# within 500 m (closest such pair 41.9, groups 1 & 25 and 8 & 26), 3:1
# against both page backgrounds. Searched 2026-10-13 on the shapes step 1
# chose; re-run the search if the groups or the pin palette change.
TRAM_GROUPS = {
    ("1", "25"): "#9840A0",
    ("2", "18", "24"): "#2848F8",
    ("3", "17", "20", "40"): "#686818",
    ("4", "22"): "#D08068",
    ("5", "12", "15", "21", "32"): "#606070",
    ("6", "7", "19"): "#F86008",
    ("8", "26"): "#F800C8",
    ("9", "10"): "#C870C8",
    ("11", "13"): "#989800",
    ("30", "31", "37"): "#00A800",
}


def tram_group_name(group):
    """("1", "25") -> "Trams 1 & 25"; ("2", "18", "24") -> "Trams 2, 18, & 24"
    (the owner's label form, 2026-10-13)."""
    if len(group) == 2:
        return f"Trams {group[0]} & {group[1]}"
    return "Trams " + ", ".join(group[:-1]) + f", & {group[-1]}"


# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "czech_nace2025"
RAW_CLASSIFICATION_COLUMN = "nace2025_label"
CITY_KEEP = "PRAHA"   # kept for the scaffold's templates; OBEC filters

# The per-city catch-all verdict, which czech_nace2025.py declines to make.
# TAKEN 2026-09-24 on Prague's own numbers: NOTHING is excluded.
#
#     96990  Poskytování ostatních osobních služeb j. n.   3 rows
#
# The code that Oslo (96.990) and Copenhagen (969900) excluded is almost EMPTY
# here - CZ-NACE 2025 has already sent its contents to specific classes. The
# largest personal-services class after hairdressing is 96230, day spas,
# saunas and steam baths (1,638 rows, 80% natural persons): a SPECIFIC class,
# not residual wording, and mostly massage salons with a street door - kept.
# The retail catch-alls (47120, 47270, 47690, 47780, 47799) are kept, as in
# Oslo, Copenhagen and France: shops by product.
#
# SUPERSEDED 2026-09-29 for 96990: the "other personal services" catch-all is
# excluded in every city (owner, 2026-09-29), however few rows it holds here.
# 96230 stays - a specific class, as above.
# "969" too (owner, 2026-09-29, DECISIONS "Category check: the owner's calls"):
# the register is ragged, and 21 rows filed at the bare group reached the map
# while the match is exact. Exact rather than a prefix, so no other 969x class
# can go with it.
CATCH_ALL_EXCLUDE = ("96990", "969")   # (owner, 2026-09-29) R2

# Sanity bounds: the placed storefronts' measured extent (49.9488-50.1716 N,
# 14.2657-14.6867 E, 2026-09-24) plus ~0.02 deg. The join to RUIAN does the
# placing; this catches a CRS or axis error, which the castle control
# (RUIAN_CRS_CONTROL above) catches first.
PRAGUE_BBOX = {
    "lat_min": 49.93,
    "lat_max": 50.19,
    "lon_min": 14.24,
    "lon_max": 14.71,
}

# --- Place search (sample batch 2a, 2026-10-08) -------------------------------

# OSM's places inside the capital city of Prague (OSM_BOUNDARY_RELATION, 435514; looked up
# again 2026-10-08, one match),
# by pipeline/place_index_fetch.py (two queries), indexed by
# step2b_place_index.py (DECISIONS.md "Four ideas assessed", item 3); an area
# id is 3600000000 plus the relation's.
PLACE_AREA = "(id:3600435514)"
# NEW file names: data/ is shared by every worktree.
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-08.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-08.json"
# The local language(s) of OSM's names here: Czech.
PLACE_LANGUAGES = ("cs",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
PLACE_REVIEWED = {
    "Hotel Golf": "a tram stop (railway=tram_stop, PID U567), named for a nearby hotel",
}
# OSM objects a reading by eye found to be a business or a home that no rule
# in place_index.py catches, each with why (place_index.build, `dropped`).
PLACE_DROPPED = {
    # Counties that border Prague, tagged place=district with an article of
    # their own: no part of the city (owner, 2026-10-13). By id, since the
    # city's own districts carry the same tags.
    "relation/441584": "'okres Praha-východ', a county bordering Prague, not a district of the city",
    "relation/442269": "'okres Praha-západ', a county bordering Prague, not a district of the city",
    "node/3475173927": "'Rozhledna', a viewpoint under its type word (dropped by id: an artwork of the same title, with wikidata, keeps its name)",
    "node/11652593441": "'daněk bílý', an animal enclosure named for the animal",
}
