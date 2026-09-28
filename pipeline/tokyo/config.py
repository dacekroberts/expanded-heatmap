"""Tokyo-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

The brief is docs/build_briefs/tokyo.md (7/7 checks, 2026-09-28). Japan's
sixth city and the last, on the shared modules Kobe built:
pipeline/countries/japan.py (rail, city line), japan_register.py (the address
join), japan_step1.py, japan_step2.py and japan_fetch.py. This file holds only
what is Tokyo's; WHICH wards and files is pipeline/tokyo/wards.py, the roster,
and this file builds every per-source setting from it.

Business leg: Tokyo is 23 publishers, not one (the tokyo-ward skill). Each
active ward's own food list is a source of its own, with the WARD as its
municipality (SOURCE_MUNICIPALITY): Chūō, Minato, Shinjuku, Taitō, Kōtō,
Meguro, Setagaya and Shibuya. MHLW's open-data slice is added to Chūō, Kōtō,
Minato and Shinjuku, one pin where a premises is in both (SUPERSEDES, the
ward's row kept). Personal services: the barber, beauty and laundry registers
of Minato, Taitō, Meguro and Shibuya (owner 2026-09-28: only where food is
on). All placed by a JOIN to MLIT's 位置参照情報 for the eight wards. Each
ward's share of the official restaurant count is measured every build
(OFFICIAL_SHARES) and written for the page.

Rail: MLIT N02 (not GTFS, not OSM), the Shinkansen left out, stations kept only
inside the city line - all 23 wards, the 15 without data drawn hollow
(NO_DATA_WARDS). English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline.tokyo import wards

wards.check()

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "tokyo" / "raw"
DATA_PROCESSED = ROOT / "data" / "tokyo" / "processed"
OUTPUTS = ROOT / "outputs" / "tokyo"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; fetch_sources.py records them) ---------------

NAME = "Tokyo"
SLUG = "tokyo"
# The 23 special wards together (東京都区部); every source names its own ward
MUNICIPALITY = "東京都区部"
PREFECTURE = "東京都"


def _build_sources():
    """source key -> (kind, ward code, [files]) from the roster: a ward's food
    list, each register, and MHLW's slice where the owner added it."""
    out = {}
    for code, w in wards.ACTIVE.items():
        out[f"food_{code}"] = ("food", code, list(w["food"]))
        for kind, files in w.get("personal", {}).items():
            out[f"{kind}_{code}"] = (kind, code, list(files))
        if code in wards.MHLW_WARDS:
            out[f"mhlw_{code}"] = ("mhlw", code, [str(w["mhlw"])])
    return out


_SRC = _build_sources()
# japan_step2 iterates these keys; the value is the first file (source_rows
# reads them all)
SOURCES = {k: Path(v[2][0]).name for k, v in _SRC.items()}
# What each source IS to japan_eigyo: food, mhlw, barber, beauty, laundry
SOURCE_KIND = {k: v[0] for k, v in _SRC.items()}
# The WARD is the municipality each source's addresses are read against
SOURCE_MUNICIPALITY = {k: wards.WARDS[v[1]]["ja"] for k, v in _SRC.items()}
MUNICIPALITY_CODES = {w["ja"]: c for c, w in wards.ACTIVE.items()}
# Stations of the wards without data: drawn hollow, not counted (owner 2026-09-28)
NO_DATA_WARDS = wards.NO_DATA_WARDS


def source_rows(key):
    """A source's rows: all its files in turn (Meguro's food list is two, the
    revised-law and old-law lists, which share no permit; the brief)."""
    from pipeline.countries import japan_register as jr
    from pipeline.countries.japan_step2 import need
    return [r for f in _SRC[key][2] for r in jr.city_rows(need(DATA_RAW / f, SLUG))]


# The fetch works per FILE: key -> (file under data/tokyo/raw/, or MHLW's
# absolute path; URL; dataset page). A one-file source keeps its source key;
# Meguro's two food files are food_13110_1 and food_13110_2.
SOURCE_FILES = {}
_FILE_SOURCE = {}
for _k, (_kind, _code, _files) in _SRC.items():
    for _i, _f in enumerate(_files):
        _fk = _k if len(_files) == 1 else f"{_k}_{_i + 1}"
        SOURCE_FILES[_fk] = (_f, *wards.URLS[_f])
        _FILE_SOURCE[_fk] = _k


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


# Declared, never inferred (docs/data_sources.md), read 2026-09-28 from each
# file's bytes (BOM, then a strict decode); japan_register.city_rows sniffs
# them all. The food lists' are the roster's; MHLW's are UTF-8 with a BOM, the
# registers UTF-8 without one.
SOURCE_ENCODING = {k: (wards.WARDS[v[1]]["encoding"] if v[0] == "food" else "utf-8-sig" if v[0] == "mhlw"
                       else "utf-8") for k, v in _SRC.items()}

# As of: the newest date each list holds, or the date it states where it
# states one, read 2026-09-28 (never a portal's label: Shinjuku's server
# re-stamped its 2023 file 2026-08-31). None = the source states no date: the
# page says "Fetched <date> (no source date)" (owner's wording rule).
_FOOD_AS_OF = {
    "13102": "2022-12-28",  # permits 2021-06-01 to 2022-12-28 only
    "13103": "2026-07-31",  # 許可年月日 to 2026-07-31
    "13104": "2023-01-01",  # the ward's stated snapshot; permits to 2022-12-28
    "13106": "2026-03-31",  # 許可開始日 to 2026-03-31, the ward's stated date
    "13108": "2022-11-30",  # permits 2021-06-01 to 2022-11-30 only
    "13110": "2026-04-01",  # the ward's stated date; permits to 2026-03-31
    "13112": "2026-03-31",  # the file's own date (R080331); 188 permits start 2026-04-01 to 05-01
    "13113": "2026-09-02",  # the newest 廃業日; permits to 2026-08-31 (the item says 2026-09-09)
}
SOURCE_AS_OF = {}
for _fk, _k in _FILE_SOURCE.items():
    _kind, _code = _SRC[_k][0], _SRC[_k][1]
    if _kind == "food":
        SOURCE_AS_OF[_fk] = _FOOD_AS_OF[_code]
    elif _code == "13110":
        SOURCE_AS_OF[_fk] = "2026-03-31"  # Meguro's registers, dated in their file names
    else:
        SOURCE_AS_OF[_fk] = None  # MHLW's slices and the catalogue registers state none
FOOD_AS_OF = None  # per ward, above

# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns are REQUIRED where a list has one,
# so the name rule (japan_register.name_is_operator; owner 2026-09-27) cannot
# silently compare nothing: read IN MEMORY by that rule only, and never kept.
# Never selected: the phones, 郵便番号, 法人住所, Taitō's food list's 営業者住所
# and the catalogue registers' 営業者_所在地_* (an operator's own address).
# The national-schema food lists (Chūō, Minato, Shinjuku, Kōtō, Shibuya) and
# MHLW's carry 法人名 only: the name rule cannot run on their rows, as on
# MHLW's in Fukuoka (DECISIONS 2026-09-28).
_NATIONAL_FOOD = ("施設名称", "営業の種類", "業態", "所在地_連結表記", "廃業年月日", "申請区分")
_CATALOGUE_REGISTER = ("名称", "所在地_連結表記", "営業者氏名", "法人代表者氏名")
_MEGURO_REGISTER = ("施設名称", "施設所在地", "施設（種別）等", "営業者名")
_COLUMNS = {
    "food_13102": _NATIONAL_FOOD,
    "food_13103": _NATIONAL_FOOD,
    "food_13104": _NATIONAL_FOOD,
    "food_13108": _NATIONAL_FOOD,
    "food_13106": ("屋号", "業種", "営業所所在地", "営業者名"),
    "food_13110": ("施設の名称", "業種", "施設所在地", "営業者氏名"),
    "food_13112": ("施設屋号", "業種", "施設所在地", "営業者名"),
    "food_13113": ("施設名称", "営業の種類もしくは営業の形態", "業態", "施設所在地_連結表記", "廃業日", "申請区分"),
    "barber_13103": ("施設名称", "施設所在地"),
    "beauty_13103": ("施設名称", "施設所在地"),
    "laundry_13103": ("施設名称", "施設所在地", "施設種別"),
    "barber_13106": _CATALOGUE_REGISTER,
    "beauty_13106": _CATALOGUE_REGISTER,
    "laundry_13106": (*_CATALOGUE_REGISTER, "営業形態"),
    "barber_13110": _MEGURO_REGISTER,
    "beauty_13110": _MEGURO_REGISTER,
    "laundry_13110": _MEGURO_REGISTER,
    "barber_13113": _CATALOGUE_REGISTER,
    "beauty_13113": _CATALOGUE_REGISTER,
    "laundry_13113": (*_CATALOGUE_REGISTER, "営業形態"),
}
for _code in wards.MHLW_WARDS:
    _COLUMNS[f"mhlw_{_code}"] = ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度",
                                 "申請区分", "廃業年月日")
# by source key (step 2) and by file key (the fetch)
REQUIRED_COLUMNS = {**_COLUMNS, **{fk: _COLUMNS[k] for fk, k in _FILE_SOURCE.items()}}

_MHLW = tuple(f"mhlw_{c}" for c in wards.MHLW_WARDS)
# MHLW publishes each field only where the filer agreed to it: a row with no
# address was withheld, not mobile (Fukuoka's mechanism).
ADDRESS_BY_CONSENT = set(_MHLW)
# Where the block join misses an MHLW row, MHLW's own point places it (Fukuoka's)
OWN_POINT_FALLBACK = set(_MHLW)
# One premises in the ward's list and MHLW's: the WARD's row is kept (the
# tokyo-ward skill; owner 2026-09-24: MHLW's slice is added, de-duplicated)
SUPERSEDES = {f"food_{c}": (f"mhlw_{c}",) for c in wards.MHLW_WARDS}
# Each ward's share is of its OWN list; MHLW's +0.1 to +3.1 pt is said once in
# prose (owner 2026-09-28)
SHARE_SKIP = _MHLW
OFFICIAL_SHARES = True

# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per active
# ward, side by side (load_city_isj keys each block by its ward).
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and tram stops (the
# Arakawa Line, the Tokyu Setagaya Line). Which stations exist is N02's.
# S, W, N, E: the 23 wards' N03 extent (35.528-35.818 N, 139.563-139.919 E,
# measured 2026-09-28; Haneda and the reclaimed islands included) rounded out;
# step 1 stops if the city leaves it.
OSM_BBOX = (35.50, 139.54, 35.84, 139.94)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Tokyo's 十条 is a name (Jūjō), not a street grid: no JO_IS_GRID.
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 54N: the longitude (~139.7) falls in the 138 to 144 band. Derived
# per city, not copied (the brief's check).
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# THE RAIL IS NOT CONFIGURED YET (the handoff's step 2): N02's legal lines to
# the public service lines that share their track, per operator, recommended
# to the owner first. japan_step1 stops on every in-city N02 line not named
# here.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
LINES = {}
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}
GATE3 = {"source": None, "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the 23 wards' N03 extent, rounded out.
CITY_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
