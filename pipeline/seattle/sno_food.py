"""Snohomish County's "Food Service Establishments (2025)" layer, read for
Lynnwood, Mountlake Terrace and the unincorporated county around them.
Read-only: nothing here fetches or writes. `pipeline/seattle/fetch_sources.py`
downloads the layer to config.SOURCES["sno_food"]["file"].

What a reader should know before trusting the rows `load()` returns:

  * **Points are PERMITS, not places.** 3,699 permits at 3,131 facilities
    (`USER_Facility_ID`), every permit with a point. `load()` returns one row
    per facility. Measured 2026-10-02: every facility's permits share one
    name, one site address, one jurisdiction and one coordinate (0 of 3,131
    differ on any), so the facility's first permit supplies all four.
  * **Restaurant and Grocery permits only, by the layer's `Icon`** (owner,
    2026-10-02, the brief's "Open for the owner" item 4; category_rules R1).
    School kitchens, donated-food distributors, food trucks, catering,
    vending and concessions are out. A facility is kept when ANY of its
    permits is Restaurant or Grocery; its excluded permits are ignored (59
    kept facilities across the county also hold one).
  * **Jurisdiction by `User_Fld`, never the postal `USER_City`.** Postal
    Lynnwood is 598 permits; the City of Lynnwood is 398 permits at 345
    facilities, and every one of the 345 lies inside the Census place
    polygon (Mountlake Terrace: 74 at 66, all inside). UNINCORPORATED is
    also kept (601 permits county-wide): Lynnwood City Center's 0.6 mi ring
    reaches 0.34 km2 of unincorporated county, and the brief's rule 7 gives
    such a ring the neighbour's data, which is this layer. Step 2 scopes by
    point-in-place; nothing here cuts by distance.
  * **A BLANK `User_Fld` is not another jurisdiction** (219 permits; 32
    Restaurant/Grocery facilities with a blank value lie inside the
    Lynnwood and Mountlake Terrace polygons). Left out unless
    `include_blank=True`: the owner's rule reads the field, and a blank
    gives it nothing to read. Step 2 takes them (owner, 2026-10-02), placed by
    the place their point falls in, as every other source is.
  * **The name shown is `USER_Name`**, the facility's trade name.
    `USER_Program_Identifier` is a permit's department label, not a place
    name: blank on 2,524 of 3,699 permits, and 1,056 of the 1,175 filled
    ones are one of eleven words (GROCERY 354, DELI 226, MEAT/FISH 82,
    BAKERY 72, MICROMARKET 58, FOOD BANK 47, STARBUCKS 37, ...).
  * **A facility holding both a Restaurant and a Grocery permit is a
    Grocery.** 250 such facilities county-wide (Lynnwood 24, Mountlake
    Terrace 5, unincorporated 47): each is a store with a GROCERY permit
    (249 of 250) whose Restaurant permits are its counters (DELI 223,
    MEAT/FISH 82, BAKERY 64, STARBUCKS 34 of 453), so the store, not a
    restaurant, is the storefront.
  * **No registrant name is read.** The layer carries none; `USER_Name` is
    the facility's name as permitted. Names that read as a person's own are
    counted by step 2's privacy check, not here.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.seattle import config  # noqa: E402

SPEC = config.SOURCES["sno_food"]
SOURCE = "sno_food"
PLACEMENT = "layer point"
# The layer's own Icon words, shown to the reader as the category.
KEEP_ICONS = ("Restaurant", "Grocery")
# A facility with both kinds of permit is a store with counters (above).
ICON_PRIORITY = ("Grocery", "Restaurant")
# User_Fld values kept. Two cities and the unincorporated county (owner,
# 2026-10-02; the brief's rule 7 for Lynnwood City Center's ring).
JURISDICTIONS = ("LYNNWOOD", "MOUNTLAKE TERRACE", "UNINCORPORATED")
COLUMNS = ["source", "source_key", "business_name", "business_category", "address",
           "latitude", "longitude", "placement", "jurisdiction"]


def _read():
    f = SPEC["file"]
    if not f.exists():
        sys.exit(f"missing {f}\nRun: python pipeline/seattle/fetch_sources.py")
    df = pd.read_csv(f, dtype=str, keep_default_na=False)
    missing = set(SPEC["fields"].split(",")) - set(df.columns)
    if missing:
        sys.exit(f"{f.name} lacks {sorted(missing)}; re-run fetch_sources.py --force")
    for c in df.columns:
        df[c] = df[c].str.strip()
    return df


def load(include_blank=False):
    """One row per kept facility, in COLUMNS order, sorted by facility id.

    `include_blank` also keeps facilities whose User_Fld is blank (see the
    module docstring); their `jurisdiction` is the empty string.
    """
    df = _read()
    keep_fld = set(JURISDICTIONS) | ({""} if include_blank else set())
    df = df[df["Icon"].isin(KEEP_ICONS) & df["User_Fld"].isin(keep_fld)]

    # Permits that disagree within a facility would make "first permit"
    # arbitrary; 0 did on 2026-10-02.
    g = df.groupby("USER_Facility_ID")
    for c in ("USER_Name", "USER_Full_Site_Address", "User_Fld", "latitude", "longitude"):
        n = int((g[c].nunique() > 1).sum())
        if n:
            sys.exit(f"{n} facilities' permits disagree on {c}; the collapse needs a rule")

    icons = g["Icon"].agg(set)
    category = icons.map(lambda s: next(i for i in ICON_PRIORITY if i in s))
    first = (df.assign(_oid=df["OBJECTID"].astype(int))
             .sort_values(["USER_Facility_ID", "_oid"])
             .drop_duplicates("USER_Facility_ID"))
    first = first.set_index("USER_Facility_ID")

    out = pd.DataFrame({
        "source": SOURCE,
        "source_key": first.index,
        "business_name": first["USER_Name"].values,
        "business_category": category.reindex(first.index).values,
        "address": first["USER_Full_Site_Address"].values,
        "latitude": first["latitude"].astype(float).values,
        "longitude": first["longitude"].astype(float).values,
        "placement": PLACEMENT,
        "jurisdiction": first["User_Fld"].values,
    })
    return out.sort_values("source_key").reset_index(drop=True)[COLUMNS]
