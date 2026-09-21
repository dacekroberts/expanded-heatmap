"""Step 2 - Clean Philadelphia's business licences to storefront businesses.

Input:  data/philadelphia/raw/business_licenses_active.csv  (Carto SQL API,
        server-filtered to Active + the taxonomy's kept licence types)
        data/philadelphia/raw/city_boundary.geojson          (cross-check)
Output: data/philadelphia/processed/businesses_clean.csv

Philadelphia licenses activities, not businesses, so the licence types this
project maps are chosen in pipeline/taxonomies/phl_licensetype.py and applied
as a server-side filter at download (config.KEPT_LICENSETYPES) - the ~94k
residential landlord registrations that make up 79% of the file are never
fetched. filter_to_storefront() then re-applies the same judgement locally, so
the taxonomy stays the single source of truth and a drift check is honest.

One storefront can hold several licences - a restaurant with pavement seating
holds "Food Preparing and Serving" AND "Sidewalk Cafe" - so after
classification there is one row per site (normalised address + business name),
with the most specific licence deciding (LICENSE_PRIORITY in config.py) and
adjunct permissions ranked last.

PRIVACY: no column holding an individual's name is downloaded at all
(legalfirstname, legallastname, legalname, opa_owner, ownercontact*name), and
the assertion below proves it for every run. business_name is the trade name
and is never blank in this registry, so unlike Los Angeles there is no
fallback to a registrant's own name - no pin here CAN be one. `legalentitytype`
IS loaded: it distinguishes Individual from corporate entities structurally,
which is a better residence signal than any name heuristic.

Run:  python pipeline/philadelphia/step2_clean_businesses.py
"""

import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.philadelphia.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_RAW_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    LICENSE_PRIORITY,
    PARCEL_RESIDENTIAL,
    PHILADELPHIA_BBOX,
    RAW_CLASSIFICATION_COLUMN,
    TAXONOMY_SYSTEM,
)
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

# Columns that hold an individual's name. None is in config.BUSINESSES_SELECT,
# and none may ever be: a public map of storefronts must not publish the person
# behind the licence. Same structural guarantee New York's salon registry
# needed, asserted rather than trusted.
FORBIDDEN_NAME_COLUMNS = (
    "legalfirstname", "legallastname", "legalname", "opa_owner",
    "ownercontact1name", "ownercontact2name",
)

# Street-type and punctuation noise that differs between two licences at the
# same address ("1021-25 S 9TH ST" vs "1021 S 9th Street").
_ADDR_NOISE = re.compile(r"[^A-Z0-9 ]+")
_ADDR_SUFFIX = re.compile(
    r"\b(STREET|ST|AVENUE|AVE|ROAD|RD|BOULEVARD|BLVD|PLACE|PL|DRIVE|DR|"
    r"LANE|LN|COURT|CT|TERRACE|TER|PARKWAY|PKWY|SQUARE|SQ|PIKE|WAY)\b")
_NAME_NOISE = re.compile(r"[^A-Z0-9 ]+")
_NAME_ORG = re.compile(
    r"\b(INC|LLC|LP|LLP|CORP|CORPORATION|CO|COMPANY|LTD|THE|AND|DBA|TA)\b")


def norm_address(value: str) -> str:
    s = _ADDR_NOISE.sub(" ", str(value or "").upper())
    s = _ADDR_SUFFIX.sub(" ", s)
    return " ".join(s.split())


# --- Displayed name: prefer the trade name over the licence holder ----------
# Philadelphia formats business_name as "LEGAL NAME (TRADE NAME)", so where the
# legal entity is an individual the raw field publishes their own name:
# "BRIAN WANG (FOUR SEASON JUICE BAR #89)", "Andrew Polhemus (Molto Bene
# Ravioli Co)". 287 of the first render's 4,958 pins (5.8%) looked like this,
# and none of the project's existing checks could see them - the parenthesis
# and digits make the string fail the person-name heuristic entirely.
#
# So the displayed name is chosen, not copied: take the first half that reads
# as a business rather than a person, and drop any bracket that holds a contact
# person ("CVS PHARMACY INC (ATTN: JOANNE P. AMITRANO)") outright. This is not
# only a privacy fix - the trade name is also the better label, because it is
# what is actually written above the shop.
#
# A bare personal name with no alternative ("Amanda Girard") is left alone: it
# is the trade name the owner registered, which is a deliberate public
# commercial act, and this project keeps those (see the San Diego reasoning in
# pipeline/taxonomies/naics.py).
_PAREN_GROUP = re.compile(r"\(([^)]*)\)")
_CONTACT_PERSON = re.compile(r"\b(ATTN|ATTENTION|C[/.]O|CARE\s+OF)\b", re.I)
_TRADE_PREFIX = re.compile(r"^(T\s*/\s*A|D\s*/?\s*B\s*/?\s*A)\s+", re.I)
# Two or three tokens where any middle token is a single initial - the same
# conservative shape scripts/check_personal_exposure.py uses. Deliberately
# duplicated rather than imported: the pipeline does not depend on scripts/.
_PERSON_SHAPE = re.compile(
    r"^[A-Za-z][A-Za-z'\-]{1,}(?:\s+[A-Za-z]\.?)?\s+[A-Za-z][A-Za-z'\-]{1,}$")
# The shape test alone is not enough, and getting this wrong is instructive:
# "STARBUCKS CORPORATION" is two alphabetic words and matches _PERSON_SHAPE, so
# without this guard the rule called it a person and preferred the bracket. A
# name carrying any of these tokens is an organisation whatever its shape.
_ORG_TOKEN = re.compile(
    r"\b(INC|LLC|L\.?L\.?C|CORP|CORPORATION|CO|COMPANY|LTD|LP|LLP|PC|GROUP|"
    r"ENTERPRISES?|HOLDINGS?|SERVICES?|SALON|SHOP|STORE|MARKET|CAFE|RESTAURANT|"
    r"BAR|GRILL|PIZZA|DELI|BAKERY|FOODS?|MART|CENTER|CENTRE|PARTNERS|BROS|"
    r"BROTHERS|THE|AND|OF|DBA|USA|MANAGEMENT|PROPERTIES|REALTY|SUPPLY|"
    r"WHOLESALE|RETAIL|AUTO|MOTORS|KITCHEN|CATERING|BEVERAGE|SEAFOOD|"
    r"PHARMACY|LIQUOR|TAVERN|LOUNGE|HOUSE|GARDEN|EXPRESS|TRUST|ASSOC\w*)\b",
    re.I)
_HAS_LETTER = re.compile(r"[A-Za-z]")
# A leading person-like name immediately before a bracket - the form that made
# this rule necessary. Used only to report how many pins it de-personalised.
PERSON_THEN_TRADE = re.compile(
    r"^([A-Za-z][A-Za-z'\-]{1,}(?:\s+[A-Za-z]\.?)?\s+[A-Za-z][A-Za-z'\-]{1,})\s*\(")


def _is_person(candidate: str) -> bool:
    return bool(_PERSON_SHAPE.match(candidate)
                and not _ORG_TOKEN.search(candidate))


def display_name(raw: str) -> str:
    """The name a pin shows.

    Preference order, and the bracket comes FIRST on purpose: in this registry
    the bracketed half is the trading name, which is both the better map label
    and the half that is not the licence holder. "A AND A II INC (AZAAN GROCERY
    STORE)" is more useful to a reader as "AZAAN GROCERY STORE".

      1. a bracketed name that is neither a contact nor a person's name
      2. the text outside the brackets, if that is not a person's name
      3. the text outside the brackets as it stands

    Step 3 is what keeps "Amanda Girard" - a person trading under their own
    name, with no alternative in the record - which this project publishes
    deliberately.
    """
    raw = str(raw or "").strip()
    if not raw:
        return raw
    outside = " ".join(_PAREN_GROUP.sub(" ", raw).split()).strip(" -,")
    groups = [
        _TRADE_PREFIX.sub("", g.strip())
        for g in _PAREN_GROUP.findall(raw)
        if not _CONTACT_PERSON.search(g)
    ]
    # A bracket holding only a code or a zip ("(19143)") is not a name.
    groups = [g for g in groups if _HAS_LETTER.search(g) and len(g) > 2]

    for group in groups:
        if not _is_person(group):
            return group
    if outside and not _is_person(outside):
        return outside
    return outside or raw


def norm_name(value: str) -> str:
    # A licence often carries "LEGAL NAME (TRADE NAME)"; the parenthesised
    # trade name is what the pin shows, but for matching two licences at one
    # site the leading legal part is the stabler half, so normalise the whole
    # string rather than picking one.
    s = _NAME_NOISE.sub(" ", str(value or "").upper())
    s = _NAME_ORG.sub(" ", s)
    return " ".join(s.split())


def main():
    if not BUSINESSES_RAW_CSV.exists():
        sys.exit(f"No file at {BUSINESSES_RAW_CSV}.\n"
                 "Run: python pipeline/philadelphia/fetch_sources.py")

    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, low_memory=False)
    print(f"Loaded {len(df):,} rows (Active + kept licence types, filtered at "
          f"download time)")

    present = [c for c in FORBIDDEN_NAME_COLUMNS if c in df.columns]
    assert not present, (
        f"{present} was downloaded for Philadelphia; those columns hold an "
        "individual's name and must not be. Fix BUSINESSES_SELECT in "
        "pipeline/philadelphia/config.py.")
    print(f"  privacy assertion: none of {len(FORBIDDEN_NAME_COLUMNS)} "
          f"registrant-name columns present")

    taxonomy = load_taxonomy_module(TAXONOMY_SYSTEM)
    value_column = taxonomy.VALUE_COLUMN
    df = df.rename(columns={RAW_CLASSIFICATION_COLUMN: value_column})

    # An upstream rename would otherwise classify as None and vanish silently.
    known = set(taxonomy.LICENSETYPE_TO_BUCKET)
    unmapped = sorted(set(df[value_column].fillna("").str.strip().str.upper()) - known)
    if unmapped:
        print(f"  WARNING: {len(unmapped)} licence type(s) not in the taxonomy, "
              f"so dropped: {unmapped}")
    else:
        print(f"  every licence type present is mapped in the taxonomy")

    # --- Storefront categories -----------------------------------------------
    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"Storefront filter ({TAXONOMY_SYSTEM}): {before:,} -> {len(df):,} rows")

    buckets = df[value_column].map(
        lambda v: taxonomy.classify({value_column: v}))
    print(f"  by bucket: {buckets.value_counts().to_dict()}")

    # --- Coordinates ----------------------------------------------------------
    # `the_geom` is non-null on every row, but 218 of them hold an EMPTY point
    # geometry, on which ST_X/ST_Y return NULL - so a non-null check overstates
    # coverage and only the extracted coordinate tells the truth.
    #
    # The 2.4% loss is NOT uniform, and is reported by licence type below
    # because of it: it takes 61 of the 75 newsstands, which are pavement
    # kiosks carrying neither a coordinate nor a street address. A geocoding
    # step would not fix that - 60 of those 61 have no address to geocode -
    # and the 79 rows that DO have an address are 0.86% of the file, so this
    # city drops them rather than carrying a geocoder for under 1% of pins.
    # Decided 2026-09-21; see DECISIONS.md.
    before = len(df)
    df = df.assign(latitude=pd.to_numeric(df["latitude"], errors="coerce"),
                   longitude=pd.to_numeric(df["longitude"], errors="coerce"))
    dropped = df[df["latitude"].isna() | df["longitude"].isna()]
    df = df.dropna(subset=["latitude", "longitude"])
    print(f"Coordinate presence: {before:,} -> {len(df):,} rows "
          f"({len(dropped):,} with an empty geometry, "
          f"{100 * len(dropped) / before:.1f}%)")
    if len(dropped):
        geocodable = int((dropped["address"].fillna("").str.strip() != "").sum())
        print(f"  dropped by licence type: "
              f"{dropped[value_column].value_counts().to_dict()}")
        print(f"  {geocodable:,} of the {len(dropped):,} have a street address "
              f"(so are recoverable by geocoding); "
              f"{len(dropped) - geocodable:,} have neither")

    before = len(df)
    b = PHILADELPHIA_BBOX
    df = df[df["latitude"].between(b["lat_min"], b["lat_max"])
            & df["longitude"].between(b["lon_min"], b["lon_max"])]
    print(f"Coordinate sanity bounds: {before:,} -> {len(df):,} rows "
          f"(catches swapped lat/lng and wild mismatches)")

    # --- One row per site, most specific licence first ------------------------
    # Address AND name, never address alone: one Philadelphia address routinely
    # holds several separate shops, and merging on address alone would delete
    # real businesses. 401 rows carry no address (mostly Curb Market stalls),
    # so those fall back to their rounded coordinate, which is what actually
    # distinguishes two stalls on the same block.
    before = len(df)
    addr_key = df["address"].map(norm_address)
    coord_key = (df["latitude"].round(5).astype(str) + ","
                 + df["longitude"].round(5).astype(str))
    site_addr = addr_key.where(addr_key != "", coord_key)
    df = df.assign(site=site_addr + "|" + df["business_name"].map(norm_name))
    print(f"  {int((addr_key == '').sum()):,} row(s) have no address; keyed on "
          f"rounded coordinates instead")

    rank = {name: i for i, name in enumerate(LICENSE_PRIORITY)}
    df = df.assign(_rank=df[value_column].map(rank).fillna(len(rank)))
    adjunct = df[value_column].map(taxonomy.is_adjunct)
    df = df.sort_values(["site", "_rank", "licensenum"]).drop_duplicates(
        subset=["site"])
    print(f"One row per site (normalised address + business name): "
          f"{before:,} -> {len(df):,} rows")
    print(f"  {int(adjunct.sum()):,} adjunct licence row(s) before the collapse "
          f"(sidewalk cafe / streetery / outdoor); "
          f"{int(df[value_column].map(taxonomy.is_adjunct).sum()):,} survive as "
          f"the only licence at their site")

    # --- Cross-check the coordinates against the boundary polygon -------------
    boundary = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    boundary = (boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None
                else boundary.to_crs(CRS_GEOGRAPHIC))
    pts = gpd.GeoSeries(
        gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs=CRS_GEOGRAPHIC, index=df.index)
    inside = pts.within(boundary.geometry.union_all())
    print(f"Boundary cross-check: {int(inside.sum()):,} of {len(df):,} rows fall "
          f"inside the Philadelphia polygon ({int((~inside).sum()):,} outside, "
          f"kept: the polygon edge and a geocoded point can differ slightly)")

    # --- Shared columns the map expects ---------------------------------------
    df["business_name"] = df["business_name"].fillna("").str.strip()
    blank = df["business_name"] == ""
    print(f"Blank business_name: {int(blank.sum()):,} "
          f"(this registry always carries a trade name, so there is no "
          f"registrant-name fallback to apply)")

    raw_names = df["business_name"]
    df["business_name"] = raw_names.map(display_name)
    changed = int((df["business_name"] != raw_names).sum())
    # The privacy-relevant subset: rows where the RAW name led with a person
    # and the displayed name no longer does.
    was_person = raw_names.map(
        lambda v: bool(PERSON_THEN_TRADE.match(str(v))
                       and _is_person(PERSON_THEN_TRADE.match(str(v)).group(1))))
    print(f"Displayed name: rewritten on {changed:,} of {len(df):,} rows "
          f"({100 * changed / len(df):.1f}%) to prefer the trading name; "
          f"{int(was_person.sum()):,} of those removed a licence holder's own "
          f"name from the pin")

    # --- Home-based businesses, tested against the City's property register --
    # A scope filter first: a food licence at a single-family house the owner
    # lives in is not a storefront. That it also removes the only residential
    # personal-name exposure this city has is the second reason, not the first -
    # the same framing as the `Rental` exclusion and the project-wide NAICS 454
    # one.
    #
    # All THREE conditions are required, and the pairing is the point. Measured
    # 2026-09-21: a purely residential parcel on its own flags 7.95% of pins, a
    # homestead exemption on its own 2.22%, and both over-fire on real
    # storefronts - ground-floor restaurants in apartment blocks, and mixed-use
    # rowhouses whose owner lives upstairs. Requiring a person-like displayed
    # name and an Individual entity as well is what makes it precise.
    # The homestead exemption is NOT one of the three conditions, and that was a
    # deliberate reversal. Using it as an alternative to the land-use test
    # removed 17 rows, but 8 of them sat on MIXED USE parcels - a rowhouse with
    # a shop below and the owner's flat above, which is a real storefront and
    # arguably the most characteristic one in Philadelphia. Removing those
    # contradicts the very justification for this filter (that the row is not a
    # storefront) and the reasoning that kept San Diego's sole proprietorships.
    # So the City's own land-use classification decides, and the exemption stays
    # in the data as a signal for scripts/check_personal_exposure.py to report
    # rather than one that silently deletes shops.
    before = len(df)
    owner_occupied = (df["parcel_owner_occupied"].astype(str).str.lower()
                      == "true")
    residential = df["parcel_landuse"].isin(PARCEL_RESIDENTIAL)
    at_home = (
        df["business_name"].map(_is_person)
        & df["legalentitytype"].fillna("").str.strip().eq("Individual")
        & residential
    )
    print(f"Residence filter (person-like name + Individual entity + a parcel "
          f"the City classifies as purely residential): "
          f"{before:,} -> {before - int(at_home.sum()):,} rows "
          f"({int(at_home.sum()):,} removed; "
          f"{int((at_home & owner_occupied).sum()):,} of them also claim the "
          f"homestead exemption)")
    if int(at_home.sum()):
        print(f"  by licence type: "
              f"{df.loc[at_home, value_column].value_counts().to_dict()}")
        print(f"  parcel land use: "
              f"{df.loc[at_home, 'parcel_landuse'].value_counts(dropna=False).to_dict()}")
    df = df[~at_home]

    keep = ["licensenum", "business_name", value_column, "legalentitytype",
            "address", "unit_type", "unit_num", "zip", "council_district",
            "parcel_landuse", "parcel_owner_occupied",
            "latitude", "longitude", "site"]
    df = df[keep].sort_values("licensenum").reset_index(drop=True)
    df["record_id"] = df.index.astype(str)

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(df):,} rows to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
