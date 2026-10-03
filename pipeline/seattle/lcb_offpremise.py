"""The Liquor and Cannabis Board's off-premise licensee list: a partial
retail layer ("shops licensed to sell alcohol only") for every city outside
Seattle and Bellevue (owner, 2026-10-01; the brief's "What the build has to
pull", item 5).

    fetch(force=False)  downloads the list (called by fetch_sources.py only)
    load()              reads the cached list and places it; never fetches

The list carries no coordinates, so each premises address is JOINED to the
county address points (the address-join skill), never geocoded:

    King County       data/seattle/raw/kc_address_points.csv   (County fields only)
    Snohomish County  data/seattle/raw/sno_address_points.csv  (the Lynnwood and
                      Mountlake Terrace box only)

What a reader should know before trusting the counts:

  * **One row per privilege, not per shop.** A licence holding grocery
    beer/wine and spirits appears twice; `load()` returns one row per
    premises and names it by LABEL_ORDER.
  * **"Active" is read at two levels.** The licence's `Status` is ACTIVE
    (ISSUED), AND the privilege row is current: approved (the Board writes
    "0" for a pending privilege) and not terminated (a date). 149 of 2,010
    active King and Snohomish licences hold no current privilege
    (2026-09-29 list: 51 pending rows, 112 terminated rows) and are left out.
  * **The premises address is two fixed-width fields.** `Loc Address` is cut
    at 30 characters and runs on into `Loc Room` (25), sometimes mid-word
    ("... BL" + "VD"); split_premises() reads every way the two can join.
  * **Never read:** `Licensee`, `ID Number`, `Phone`, every `Mail` column.
    They are not in `usecols`, and `load()` asserts they never enter the
    frame. The trade name is the only name kept.
  * **No city is scoped here.** King and Snohomish premises are both
    returned; step 2 scopes by point-in-boundary.
  * **The Snohomish points cover the Lynnwood and Mountlake Terrace box
    only**, so Snohomish premises elsewhere (Everett, Marysville, most of
    Edmonds) never place: 336 of 470 Snohomish premises, 2026-09-29.

The join, 2026-10-02 (list of 2026-09-29; match() names the tiers):

    1,837 premises: exact 1,114, base 272, city 3, renamed 9, loose_dir 11
    placed (1,409, 76.7%); loose_type 2, ambiguous 10, unmatched 416 left off.
    King County alone: 1,312 of 1,367 placed (96.0%).
    Snohomish, postal Lynnwood, Mountlake Terrace, Edmonds and Brier: 97 of
    120 (80.8%).

The control that must reproduce (address-join skill): King County's food
inspections, 12,305 businesses, joined by the same matcher. 10,173 placed
rows carry a parcel number; the matched points carry that PIN for 96.28%,
and 96.59% are placed within 50 m of a point on that parcel. Re-run it after
any change to the normalisation or the tiers.

The Board's lists page carried this notice on 2026-10-02, which the page
discloses (owner, 2026-10-02): "These list reports contain possible errors
due to a known data transfer issue."
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.seattle import config  # noqa: E402

LISTS_PAGE_URL = "https://lcb.wa.gov/records/frequently-requested-lists"
XLSX_URL = "https://lcb.wa.gov/sites/default/files/2026-09/Off%20Premise09292026.xlsx"
LIST_DATE = "2026-09-29"
RAW_XLSX = config.DATA_RAW / "lcb_off_premise_09292026.xlsx"
PLACED_CSV = config.DATA_PROCESSED / "lcb_offpremise_placed.csv"
HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
# The 2026-09-29 list is 1,537,979 bytes; anything far smaller is an error page.
MIN_BYTES = 500_000

SOURCE = "lcb_retail"

# The only columns read. The Board spells the licence-number header
# "License Numner" (2026-09-29).
COL_LICENCE = "License Numner"
COL_TRADE = "Tradename"
COL_ADDRESS = "Loc Address"
COL_ROOM = "Loc Room"
COL_CITY = "Loc City"
COL_ZIP = "Loc Zip"
COL_COUNTY = "County"
COL_STATUS = "Status"
COL_PRIVILEGE = "Privilege"
COL_APPROVED = "Privilege - date approved"
COL_TERMINATED = "Privilege - date terminated"
USECOLS = [COL_TRADE, COL_LICENCE, COL_ADDRESS, COL_ROOM, COL_CITY, COL_ZIP, COL_COUNTY,
           COL_STATUS, COL_PRIVILEGE, COL_APPROVED, COL_TERMINATED]
NEVER_READ = ("Licensee", "ID Number", "Phone", "Mail Address", "Mail City", "Mail State",
              "Mail Zip")

ACTIVE_STATUS = "ACTIVE (ISSUED)"
COUNTIES = ("KING", "SNOHOMISH")

# Walk-in retail privileges. Active King and Snohomish rows, 2026-09-29
# (privilege rows, before the current-privilege filter):
#   GROCERY STORE - BEER/WINE 1,600; SPIRITS RETAILER 527; BEER/WINE
#   SPECIALTY SHOP 346; COMBO GROCERY OFF PREM S/B/W 49; SLS SPIRITS
#   RETAILER 38; COMBO SPECIALTY OFF PREM S/B/W 10; CLS SPIRITS RETAILER 8;
#   GROCERY RESTRICT F-WINE/STRONG BEER 3; GROCERY STORE-RESTRICT FORT WINE
#   2; COMBO GROCERY OFF PREM S/B/W CLS 1.
# SLS and CLS are the former state and contract liquor stores (I-1183).
RETAIL_PRIVILEGES = (
    "GROCERY STORE - BEER/WINE",
    "GROCERY RESTRICT F-WINE/STRONG BEER",
    "GROCERY STORE-RESTRICT FORT WINE",
    "COMBO GROCERY OFF PREM S/B/W",
    "COMBO GROCERY OFF PREM S/B/W CLS",
    "SPIRITS RETAILER",
    "SLS SPIRITS RETAILER",
    "CLS SPIRITS RETAILER",
    "BEER/WINE SPECIALTY SHOP",
    "COMBO SPECIALTY OFF PREM S/B/W",
)
# Not a storefront on its own, with the reason. Same list and rows:
#   WINE RETAILER RESELLER 166 (an add-on that lets a grocery or spirits
#     retailer also sell wine to restaurants; every current holder in the
#     two counties also holds a retail privilege above, so no shop is lost);
#   BEER/WINE GIFT DELIVERY 26 (gift baskets sold for delivery, often from an
#     office or a home; 22 current licences hold nothing else).
NOT_STOREFRONT = {
    "WINE RETAILER RESELLER": "an add-on to a retail privilege (wholesale wine to restaurants)",
    "BEER/WINE GIFT DELIVERY": "gift baskets for delivery, not a walk-in shop",
}

# Which privilege names a premises holding several: a grocery licence
# requires a stock of groceries, so its holder is a grocery store whatever
# else it sells; then the spirits shops; then the beer and wine shops.
LABEL_ORDER = (
    "GROCERY STORE - BEER/WINE",
    "COMBO GROCERY OFF PREM S/B/W",
    "COMBO GROCERY OFF PREM S/B/W CLS",
    "GROCERY RESTRICT F-WINE/STRONG BEER",
    "GROCERY STORE-RESTRICT FORT WINE",
    "SLS SPIRITS RETAILER",
    "CLS SPIRITS RETAILER",
    "SPIRITS RETAILER",
    "COMBO SPECIALTY OFF PREM S/B/W",
    "BEER/WINE SPECIALTY SHOP",
)
assert sorted(LABEL_ORDER) == sorted(RETAIL_PRIVILEGES)

OUT_COLUMNS = ["source", "source_key", "business_name", "business_category", "address",
               "latitude", "longitude", "placement", "postal_city"]

# A key whose points lie within this distance of their centroid is one place.
SAME_PLACE_M = 50.0
# A key spread wider whose PRIMARY points are one place is one lot with
# outbuildings up to this far out (collapse()).
COMPLEX_M = 400.0


def fetch(force=False):
    """Download the list. Called by fetch_sources.py; no step calls it, and
    the HTTP client is imported here only, so importing this module for
    load() never loads one."""
    import requests
    if RAW_XLSX.exists() and not force:
        print(f"  lcb off-premise: cached {RAW_XLSX.name} ({RAW_XLSX.stat().st_size:,} bytes)")
        return RAW_XLSX
    r = requests.get(XLSX_URL, headers=HEADERS, timeout=300)
    r.raise_for_status()
    if len(r.content) < MIN_BYTES or not r.content.startswith(b"PK"):
        sys.exit(f"  lcb off-premise: a {len(r.content):,}-byte answer that is not the list "
                 f"(a failed fetch, not a negative). Check {LISTS_PAGE_URL} for a newer file.")
    RAW_XLSX.parent.mkdir(parents=True, exist_ok=True)
    RAW_XLSX.write_bytes(r.content)
    print(f"  lcb off-premise: {len(r.content):,} bytes -> {RAW_XLSX.name}")
    return RAW_XLSX


# --- Address normalisation (found by reading misses) ----------------------

# One spelling for words filed two ways, applied to BOTH sides of the join.
WORDS = {
    "STREET": "ST", "AVENUE": "AVE", "AV": "AVE", "BOULEVARD": "BLVD", "ROAD": "RD",
    "DRIVE": "DR", "PLACE": "PL", "WY": "WAY", "LANE": "LN", "COURT": "CT",
    "PARKWAY": "PKWY", "HIGHWAY": "HWY", "CIRCLE": "CIR", "TERRACE": "TER",
    "PLAZA": "PLZ", "SQUARE": "SQ", "TRAIL": "TRL", "CROSSING": "XING", "MOUNT": "MT",
    "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W", "NORTHEAST": "NE",
    "NORTHWEST": "NW", "SOUTHEAST": "SE", "SOUTHWEST": "SW",
    "FIRST": "1", "SECOND": "2", "THIRD": "3", "FOURTH": "4", "FIFTH": "5",
    "SIXTH": "6", "SEVENTH": "7", "EIGHTH": "8", "NINTH": "9", "TENTH": "10",
}
# Whole-name spellings of one street, applied to both sides ("MLK JR WAY S"
# and "M L KING JR WAY S" are King County's "MARTIN LUTHER KING JR WAY S").
PHRASES = (
    (re.compile(r"\b(?:MLK|M L K|M L KING|ML KING)\b"), "MARTIN LUTHER KING"),
)
DIRECTIONS = {"N", "S", "E", "W", "NE", "NW", "SE", "SW"}
STREET_TYPES = {"ST", "AVE", "BLVD", "RD", "DR", "PL", "WAY", "LN", "CT", "PKWY", "HWY",
                "CIR", "TER", "PLZ", "SQ", "LOOP", "TRL", "XING", "HTS", "PT", "CRES",
                "KY", "VW", "MALL", "SPUR", "ROW", "WALK", "RUN", "PATH", "ALY", "CRST"}
# A unit designator ends the street; everything after it is the unit. A
# directional run into one ("DR SSTE H") is split first.
UNIT_WORDS = ("STE|SUITE|UNIT|APT|BLDG|BLD|BUILDING|SPACE|SP|RM|ROOM|FL|FLOOR|LOCKER|"
              "LOWER|UPPER|BSMT|SITE")
UNIT_RE = re.compile(r"(?:^|[\s,])(?:" + UNIT_WORDS + r")(?=[\s\-.,0-9#]|$).*$|\s*#.*$")
GLUED_UNIT_RE = re.compile(r"\b(N|S|E|W|NE|NW|SE|SW)(STE|SUITE|UNIT)\b")
# A code the Board appends to some premises fields ("SMP - 2"; 32 of the
# 1,837 premises, 2026-09-29), never part of the street: removed before
# either key is built.
SMP_RE = re.compile(r"\bSMP\s*-\s*\d+\b")
ORDINAL_RE = re.compile(r"^(\d+)(?:ST|ND|RD|TH)$")
ADDRESS_WIDTH = 30


def canon_tokens(text):
    """Upper case, punctuation to spaces, one spelling per word, ordinals as
    bare numbers ('240TH' -> '240'): the form both sides are compared in. PT
    is POINT inside a name ('SE HIGH PT WAY') and a street type at the end."""
    s = re.sub(r"[^A-Z0-9/ ]", " ", str(text).upper())
    for pat, rep in PHRASES:
        s = pat.sub(rep, s)
    toks = s.split()
    out = []
    for i, t in enumerate(toks):
        t = WORDS.get(t, t)
        if t == "PT" and i < len(toks) - 1:
            t = "POINT"
        m = ORDINAL_RE.match(t)
        out.append(m.group(1) if m else t)
    return out


def _clean(street):
    s = re.sub(r"\s+", " ", street).strip().upper()
    s = SMP_RE.sub("", s).strip(" ,-")
    s = GLUED_UNIT_RE.sub(r"\1 \2", s)
    return s, UNIT_RE.sub("", s).strip(" ,-")


def split_premises(raw_address, raw_room=""):
    """The register's fixed-width fields -> [(street as filed, street with its
    unit cut), ...], the first reading first.

    `Loc Address` is padded to 30 characters and runs on into `Loc Room`:
    mid-word ("... BL" + "VD") when the cut falls inside a word, as a new
    word ("... JR WAY" + "S") when it falls on a space. The two cannot be
    told apart, so a full-width address yields both readings and the join takes
    whichever answers. The address also wraps at a word short of 30
    ("... TUKWILA INTERNATIONAL" + "BLVD S"). A room can instead be a unit or
    a note ("STE B", "ALDERWOOD MANOR"), so the last reading is the address
    alone, its room kept on the address as filed but out of the key."""
    a, r = str(raw_address or ""), str(raw_room or "")
    if not r.strip():
        return [_clean(a)]
    readings = []
    if len(a.rstrip()) >= ADDRESS_WIDTH and not r.startswith(" "):
        readings.append(_clean(a + r))
    readings.append(_clean(a.rstrip() + " " + r.strip()))
    readings.append((_clean(f"{a.strip()} {r.strip()}")[0], _clean(a)[1]))
    out = []
    for x in readings:
        if x not in out:
            out.append(x)
    return out


def premises_keys(street):
    """(house number, canonical street tokens) for a street with its unit cut.
    '1234A', '1234-B' and '1234-1240' read as 1234; a fraction after the
    number ('1/2') belongs to the door, not the street."""
    toks = canon_tokens(re.sub(r"^\s*(\d+)\s*-\s*[A-Z0-9]+\b", r"\1", str(street).upper()))
    if not toks:
        return None, []
    m = re.match(r"^(\d+)", toks[0])
    if not m:
        return None, toks
    rest = toks[1:]
    while rest and re.fullmatch(r"\d+/\d+", rest[0]):
        rest = rest[1:]
    return m.group(1), rest


def exact_key(number, toks):
    return f"{number} " + " ".join(toks) if number and toks else None


def loose_dir_key(number, toks):
    """Directionals dropped, the street type kept: a directional the record
    left off or wrote on the other side ('NE 8TH ST' / '8TH ST NE')."""
    core = [t for t in toks if t not in DIRECTIONS]
    return f"{number} " + " ".join(core) if number and core else None


def loose_type_key(number, toks):
    """The street type dropped, directionals kept, for a NAMED street only.
    A numbered street's type is never dropped: on King County's grid
    '8TH ST' and '8TH AVE' are perpendicular streets."""
    core = [t for t in toks if t not in STREET_TYPES]
    name = [t for t in core if t not in DIRECTIONS]
    if not number or not name or any(t.isdigit() for t in name):
        return None
    return f"{number} " + " ".join(core)


# Highway 99 through Tukwila, SeaTac and Des Moines is filed under three
# names (the list still uses the old PACIFIC HWY S where King County's
# points carry the new names). A number that answers under exactly one
# other name of its group is that place ("renamed"): 9 premises and 10
# control businesses, all 10 within 50 m of their parcel (2026-10-02).
RENAMED = (
    ("PACIFIC HWY S", "INTERNATIONAL BLVD", "TUKWILA INTERNATIONAL BLVD"),
)


# --- The address points -----------------------------------------------------

def _need(path):
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/seattle/fetch_sources.py "
                 f"(no step fetches; lcb_offpremise.load() reads the cache only)")


def _project(lon, lat):
    """WGS84 -> the city's UTM zone (config.CRS_PROJECTED), in metres."""
    from pyproj import Transformer
    t = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
    return t.transform(np.asarray(lon, dtype=float), np.asarray(lat, dtype=float))


def _num(series):
    """The house number's digits. King County files a door letter in the
    number ('1234 B', 2.7% of points), read as a unit, so the door joins the
    key of its building."""
    return series.fillna("").astype(str).str.extract(r"^\s*(\d+)", expand=False).fillna("")


def king_points():
    """King County's address points: number, street, point, PIN, the
    County's primary-address flag, and the city polygon each lies in. Only
    the County's own fields are read."""
    _need(config.KC_ADDRESS_CSV)
    cols = ["PIN", "ADDR_HN", "ADDR_PD", "ADDR_PT", "ADDR_SN", "ADDR_ST", "ADDR_SD",
            "PRIM_ADDR", "latitude", "longitude"]
    ap = pd.read_csv(config.KC_ADDRESS_CSV, usecols=cols, dtype=str, keep_default_na=False)
    street = (ap["ADDR_PD"] + " " + ap["ADDR_PT"] + " " + ap["ADDR_SN"] + " " + ap["ADDR_ST"]
              + " " + ap["ADDR_SD"])
    df = _point_frame(_num(ap["ADDR_HN"]), street, ap["latitude"], ap["longitude"],
                      ap["PIN"], ap["PRIM_ADDR"].str.strip() == "1", pd.Series("", index=ap.index))
    df["city"] = _point_cities(df).values
    return df


def snohomish_points():
    """Snohomish County's address points (the Lynnwood and Mountlake Terrace
    box), same shape. There is no parcel number and no primary flag; a point
    with no `Unit` (57% of them) is read as the building's own address. The
    city is the County's own `Inc_Muni`."""
    _need(config.SNO_ADDRESS_CSV)
    cols = ["Add_Number", "St_PreDir", "St_PreTyp", "St_Name", "St_PosTyp", "St_PosDir",
            "Unit", "Inc_Muni", "latitude", "longitude"]
    ap = pd.read_csv(config.SNO_ADDRESS_CSV, usecols=cols, dtype=str, keep_default_na=False)
    street = (ap["St_PreDir"] + " " + ap["St_PreTyp"] + " " + ap["St_Name"] + " "
              + ap["St_PosTyp"] + " " + ap["St_PosDir"])
    return _point_frame(_num(ap["Add_Number"]), street, ap["latitude"], ap["longitude"],
                        pd.Series("", index=ap.index), ap["Unit"].str.strip() == "",
                        ap["Inc_Muni"].str.strip().str.upper())


def _point_frame(number, street, lat, lon, pin, prim, city):
    toks = street.map(canon_tokens)
    df = pd.DataFrame({"number": number, "pin": pin.astype(str).str.strip(),
                       "prim": prim.values, "city": city.values,
                       "latitude": pd.to_numeric(lat, errors="coerce"),
                       "longitude": pd.to_numeric(lon, errors="coerce")})
    df["exact"] = [exact_key(n, t) for n, t in zip(df["number"], toks)]
    df["loose_dir"] = [loose_dir_key(n, t) for n, t in zip(df["number"], toks)]
    df["loose_type"] = [loose_type_key(n, t) for n, t in zip(df["number"], toks)]
    df = df[(df["number"] != "") & df["exact"].notna() & df["latitude"].notna()]
    df = df.reset_index(drop=True)
    df["x"], df["y"] = _project(df["longitude"], df["latitude"])
    return df


def _point_cities(points):
    """The King County city polygon (CITYNAME, upper case) each point lies
    in; blank outside every polygon."""
    import geopandas as gpd
    _need(config.KC_CITIES_GEOJSON)
    cities = gpd.read_file(config.KC_CITIES_GEOJSON)[["CITYNAME", "geometry"]]
    cities = cities.to_crs(config.CRS_GEOGRAPHIC)
    gp = gpd.GeoDataFrame(index=points.index, geometry=gpd.points_from_xy(
        points["longitude"], points["latitude"]), crs=config.CRS_GEOGRAPHIC)
    j = gpd.sjoin(gp, cities, how="left", predicate="within")
    j = j[~j.index.duplicated()]
    return j["CITYNAME"].fillna("").str.upper().reindex(points.index)


def collapse(points, key):
    """One place per key, or none.

      * All the key's points within SAME_PLACE_M of their centroid: one
        place, drawn at the mean of its primary points (King County's
        PRIM_ADDR; Snohomish's points with no unit), else at the centroid.
      * Wider, but its primary points within SAME_PLACE_M of each other and
        everything within COMPLEX_M: one lot with outbuildings, drawn at the
        primary points ("primary_lot").
      * Otherwise AMBIGUOUS: never placed.
    """
    p = points[points[key].notna()]
    g = p.groupby(key)
    spread = np.hypot(p["x"] - g["x"].transform("mean"),
                      p["y"] - g["y"].transform("mean")).groupby(p[key]).max()
    agg = g.agg(points=("x", "size"), latitude=("latitude", "mean"),
                longitude=("longitude", "mean"), prims=("prim", "sum"))
    agg["spread_m"] = spread
    pp = p[p["prim"]]
    pg = pp.groupby(key)
    pspread = np.hypot(pp["x"] - pg["x"].transform("mean"),
                       pp["y"] - pg["y"].transform("mean")).groupby(pp[key]).max()
    pmean = pg[["latitude", "longitude"]].mean()
    agg["prim_spread_m"] = pspread.reindex(agg.index)
    tight = agg["spread_m"] <= SAME_PLACE_M
    lot = (~tight & (agg["prims"] > 0) & (agg["prim_spread_m"] <= SAME_PLACE_M)
           & (agg["spread_m"] <= COMPLEX_M))
    use = agg.index[(tight & (agg["prims"] > 0) & (agg["points"] > 1)) | lot]
    agg.loc[use, ["latitude", "longitude"]] = pmean.loc[use].values
    agg["how"] = np.select([agg["points"] == 1, lot, agg.index.isin(use)],
                           ["single", "primary_lot", "primary"], "centroid")
    agg["ambiguous"] = ~(tight | lot)
    pins = p[p["pin"] != ""].drop_duplicates([key, "pin"]).groupby(key)["pin"].agg("|".join)
    agg["pins"] = pins.reindex(agg.index).fillna("")
    cities = p.drop_duplicates([key, "city"]).groupby(key)["city"].agg("|".join)
    agg["cities"] = cities.reindex(agg.index).fillna("")
    return agg


PLACED_TIERS = ("exact", "base", "city", "renamed", "loose_dir", "loose_type")
# The tiers the layer keeps. The control (King County food inspections,
# 12,305 businesses, 2026-10-02): share placed within 50 m of a point on the
# record's own parcel, by tier: exact 96.8%, base 96.7%, city 90.6%, renamed
# 100% (10), loose_dir 91.5%, loose_type 86.8% (5.9% and 7.9% over 500 m).
# loose_type falls below 90% and is left off; re-measure if the matcher
# changes (address-join skill, step 5).
LAYER_TIERS = ("exact", "base", "city", "renamed", "loose_dir")
_COLS = ("latitude", "longitude", "how", "spread_m", "points", "pins", "cities")


def match(frame, points, city_column):
    """Join `frame` (column `readings`, from split_premises; `city_column`,
    the postal city) to `points`. Adds placement and _COLS. Tiers, the first
    that answers:

      exact    the street as filed, no unit present, equals a point's number
               + street (directionals and street type included)
      base     the same with the unit cut
      city     an exact or base key that is AMBIGUOUS county-wide (one number
               on two streets of one name, in two cities) and is one place
               among the points in the row's postal city
      renamed  a Highway 99 name (RENAMED) that answers under exactly one
               of its other names
      loose_dir   the key with directionals dropped (loose_dir_key), one
                  place among the points in the row's postal city
      loose_type  the key with the street type dropped, named streets only
                  (loose_type_key), one place in the postal city
      ambiguous / unmatched   not placed; never geocoded, never fuzzy
    """
    ex = collapse(points, "exact")
    ex_place = ex[~ex["ambiguous"]]
    groups = {}

    def in_city(key_col, key, postal):
        """The key's points inside the postal city, collapsed, or None."""
        if key_col not in groups:
            groups[key_col] = points.groupby(key_col).indices
        ii = groups[key_col].get(key)
        if ii is None:
            return None
        cand = points.iloc[ii]
        cand = cand[cand["city"] == postal]
        if cand.empty:
            return None
        return collapse(cand.assign(k="k"), "k").iloc[0]

    rows = []
    for readings, postal in zip(frame["readings"], frame[city_column].str.upper().str.strip()):
        res = {"placement": "unmatched"}
        keys = []
        for full, base in readings:
            nf, tf = premises_keys(full)
            nb, tb = premises_keys(base)
            if full == base:
                keys.append(("exact", exact_key(nf, tf)))
            keys.append(("base", exact_key(nb, tb)))
        hit = next(((t, k) for t, k in keys if k and k in ex.index), None)
        if hit and not ex.at[hit[1], "ambiguous"]:
            res = {"placement": hit[0], **{c: ex.at[hit[1], c] for c in _COLS}}
        elif hit:
            res = {"placement": "ambiguous", "spread_m": ex.at[hit[1], "spread_m"]}
            one = in_city("exact", hit[1], postal)
            if one is not None and not one["ambiguous"]:
                res = {"placement": "city", **{c: one[c] for c in _COLS if c != "cities"},
                       "cities": postal}
        else:
            for full, base in readings:
                nb, tb = premises_keys(base)
                group = next((g for g in RENAMED if " ".join(tb) in g), None)
                if not group:
                    continue
                alts = [exact_key(nb, canon_tokens(n)) for n in group if n != " ".join(tb)]
                alts = [k for k in alts if k in ex_place.index]
                if len(alts) == 1:
                    res = {"placement": "renamed", **{c: ex_place.at[alts[0], c] for c in _COLS}}
                    break
            for tier, keyer in (("loose_dir", loose_dir_key), ("loose_type", loose_type_key)):
                if res["placement"] != "unmatched":
                    break
                for full, base in readings:
                    k = keyer(*premises_keys(base))
                    one = in_city(tier, k, postal) if k else None
                    if one is not None and not one["ambiguous"]:
                        res = {"placement": tier, **{c: one[c] for c in _COLS if c != "cities"},
                               "cities": postal}
                        break
        rows.append(res)
    found = pd.DataFrame(rows, index=frame.index)
    for c in ("placement",) + _COLS:
        if c not in found:
            found[c] = None
    return frame.join(found[["placement", *_COLS]])


# --- The list ----------------------------------------------------------------

def read_list():
    """The cached list, ONLY the USECOLS columns; never fetches."""
    _need(RAW_XLSX)
    df = pd.read_excel(RAW_XLSX, usecols=USECOLS, dtype=str, keep_default_na=False)
    leaked = [c for c in df.columns if c in NEVER_READ or c not in USECOLS]
    assert not leaked, f"columns that must never be read reached the frame: {leaked}"
    for c in USECOLS:
        if c not in (COL_ADDRESS, COL_ROOM):     # fixed-width; padding is read as data
            df[c] = df[c].str.strip()
    return df


def premises(verbose=True):
    """Active retail premises in King and Snohomish Counties, one row per
    premises, before the join."""
    df = read_list()
    say = print if verbose else (lambda *a, **k: None)
    say(f"  Liquor Board off-premise list ({LIST_DATE}): {len(df):,} privilege rows")
    df = df[df[COL_COUNTY].isin(COUNTIES)]
    say(f"  King and Snohomish Counties: {len(df):,}")
    df = df[df[COL_STATUS] == ACTIVE_STATUS]
    say(f"  licence {ACTIVE_STATUS}: {len(df):,} rows, {df[COL_LICENCE].nunique():,} licences")
    unknown = set(df[COL_PRIVILEGE]) - set(RETAIL_PRIVILEGES) - set(NOT_STOREFRONT)
    if unknown:
        sys.exit(f"  privileges neither kept nor dropped: {sorted(unknown)}; classify them "
                 f"in RETAIL_PRIVILEGES or NOT_STOREFRONT")
    df = df[(df[COL_APPROVED] != "0") & (df[COL_TERMINATED] == "0")]
    say(f"  current privileges (approved, not terminated): {len(df):,} rows, "
        f"{df[COL_LICENCE].nunique():,} licences")
    dropped = df[~df[COL_PRIVILEGE].isin(RETAIL_PRIVILEGES)]
    df = df[df[COL_PRIVILEGE].isin(RETAIL_PRIVILEGES)].copy()
    for priv, n in dropped[COL_PRIVILEGE].value_counts().items():
        say(f"    not a storefront: {priv} ({n} rows): {NOT_STOREFRONT[priv]}")
    say(f"  retail privileges: {len(df):,} rows, {df[COL_LICENCE].nunique():,} licences")

    rank = {p: i for i, p in enumerate(LABEL_ORDER)}
    df["rank"] = df[COL_PRIVILEGE].map(rank)
    df = df.sort_values([COL_LICENCE, "rank"])
    lic = df.groupby(COL_LICENCE, sort=True).first().reset_index()
    lic["readings"] = [split_premises(a, r) for a, r in zip(lic[COL_ADDRESS], lic[COL_ROOM])]
    lic["full"] = [r[0][0] for r in lic["readings"]]
    lic["base"] = [r[0][1] for r in lic["readings"]]
    # Two licences at one door under one trade name are one shop.
    lic["name_key"] = lic[COL_TRADE].str.upper().str.replace(r"[^A-Z0-9]", "", regex=True)
    before = len(lic)
    lic = lic.drop_duplicates(["base", COL_CITY, "name_key"], keep="first")
    say(f"  premises: {len(lic):,} ({before - len(lic)} licences at a door and trade name "
        f"already counted)")
    return lic


def place(lic, verbose=True):
    """Join each premises to its own county's address points."""
    say = print if verbose else (lambda *a, **k: None)
    parts = []
    for county, loader in (("KING", king_points), ("SNOHOMISH", snohomish_points)):
        sub = lic[lic[COL_COUNTY] == county]
        if sub.empty:
            continue
        pts = loader()
        say(f"  {county.title()} County address points: {len(pts):,} with a number and street")
        parts.append(match(sub, pts, COL_CITY))
        del pts
    out = pd.concat(parts)
    if verbose:
        for county, g in out.groupby(COL_COUNTY):
            tiers = g["placement"].value_counts()
            say(f"  join, {county.title()}: " + ", ".join(
                f"{t} {tiers.get(t, 0):,}" for t in (*PLACED_TIERS, "ambiguous", "unmatched")))
    return out


def load(verbose=True):
    """The placed layer, in OUT_COLUMNS order. Reads the cache only; writes
    nothing."""
    out = place(premises(verbose), verbose)
    placed = out[out["placement"].isin(LAYER_TIERS)]
    if verbose:
        print(f"  placed {len(placed):,} of {len(out):,} premises; the other "
              f"{len(out) - len(placed):,} are left off (never geocoded)")
    return pd.DataFrame({
        "source": SOURCE,
        "source_key": placed[COL_LICENCE].values,
        "business_name": placed[COL_TRADE].values,
        "business_category": placed[COL_PRIVILEGE].values,
        "address": placed["full"].values,
        "latitude": placed["latitude"].astype(float).round(7).values,
        "longitude": placed["longitude"].astype(float).round(7).values,
        "placement": placed["placement"].values,
        "postal_city": placed[COL_CITY].values,
    }, columns=OUT_COLUMNS)
