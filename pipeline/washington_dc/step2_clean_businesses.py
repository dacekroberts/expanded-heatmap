"""Step 2 - Clean D.C.'s Basic Business License register into one business table.

Input:  data/washington_dc/raw/basic_business_licenses.csv
Output: data/washington_dc/processed/businesses_clean.csv
        data/washington_dc/processed/businesses_prefilter.csv

ONE REGISTRY, ALL THREE BUCKETS - the first non-NAICS source in this project
that needs no assembly. What it does need is three specific corrections.

**The published latitude and longitude are useless.** `LATITUDE` is `39` and
`LONGITUDE` is `-77` on every one of the 76,107 active rows, so 0 of them fall
inside the District. This step ignores both columns and reprojects
`X_COORDINATE`/`Y_COORDINATE` from EPSG:26985 instead - NAD83 Maryland state
plane in METRES, verified by transformation during Step 0 rather than assumed.
The bounds check below is what would catch a wrong EPSG here.

**Nearly half the register is not a business.** 37,195 rows of 61,329 are
residential rentals and are dropped at download; `General Business` - 11,074
more - is the office and professional catch-all, and the taxonomy excludes it.
Both are printed as filters rather than hidden, because a raw row count means
nothing until the distribution is read: that is the Philadelphia lesson.

**One licensee can hold several licences at one address.** 812 of 5,215 do, and
121 of them hold exactly Cigarette Sales + Food Products + Patent Medicine -
one corner shop, not three businesses. The dedup key is
CUSTOMERNUMBER + MAR_ID, the register's own licensee id and the District's
Master Address Repository id, which is a real address identifier rather than
the address text Boston and Miami had to fall back on.

NO PERSONAL-NAME COLUMN IS EVER LOADED. The layer carries
BUSINESSOWNERFIRSTNAME, BUSINESSOWNERLASTNAME, BUSINESSOWNERMIDDLENAME,
AGENTFIRSTNAME, AGENTLASTNAME, AGENTMIDDLENAME, AGENTENTITY and BILLINGADDRESS,
populated on tens of thousands of rows. fetch_sources.py does not request any
of them and the assertion below is what makes that a guarantee.

Run:  python pipeline/washington_dc/step2_clean_businesses.py
"""

import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.washington_dc.config import (  # noqa: E402
    BUSINESS_CSV,
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_PREFILTER_CSV,
    CRS_GEOGRAPHIC,
    DC_BBOX,
    FORBIDDEN_COLUMNS,
    PREMISES_KEY,
    RAW_CLASSIFICATION_COLUMN,
    SOURCE_ENCODING,
    SOURCE_XY_CRS,
    TAXONOMY_SYSTEM,
)
from pipeline.taxonomies import (  # noqa: E402
    filter_to_storefront,
    load_taxonomy_module,
)

# "3110 MOUNT PLEASANT ST NW, WASHINGTON, DC, 20010, USA" - the Census
# geocoder in step 3 wants the street line and the ZIP separately.
_ADDR = re.compile(r"^(.*?),\s*WASHINGTON,\s*DC,\s*(\d{5})", re.IGNORECASE)
_WS = re.compile(r"\s+")


def split_address(value):
    s = _WS.sub(" ", str(value or "").strip())
    m = _ADDR.match(s)
    if m:
        return m.group(1).strip(), m.group(2)
    # No ZIP, or a differently-formatted line: keep the whole thing as the
    # street line so step 3 can still try it, and leave the ZIP empty.
    return s.rstrip(", USA").strip(), ""


def main():
    if not BUSINESS_CSV.exists():
        sys.exit(f"No file at {BUSINESS_CSV}.\n"
                 "Run pipeline/washington_dc/fetch_sources.py first.")

    header = list(pd.read_csv(BUSINESS_CSV, nrows=0,
                              encoding=SOURCE_ENCODING).columns)
    present = [c for c in FORBIDDEN_COLUMNS if c in header]
    assert not present, (
        f"{BUSINESS_CSV.name} carries personal-information column(s) "
        f"{present}. fetch_sources.py must not request them.")

    df = pd.read_csv(BUSINESS_CSV, dtype=str, encoding=SOURCE_ENCODING)
    print(f"Loaded {len(df):,} active, in-District, non-rental licences")

    # Scope cross-check. PREMISEINDC carries the filter (WARD is null on
    # 16,806 of the register's rows and mixes "Ward 2" with "2"), so WARD is
    # only ever reported, never trusted.
    off_scope = (df["PREMISEINDC"].fillna("") != "Yes").sum()
    assert off_scope == 0, f"{off_scope} rows are not PREMISEINDC='Yes'"
    blank_ward = (df["WARD"].fillna("").str.strip() == "").sum()
    print(f"  WARD is blank on {blank_ward:,} of them, which is why "
          f"PREMISEINDC carries the scope filter instead")

    module = load_taxonomy_module(TAXONOMY_SYSTEM)
    df = df.rename(columns={RAW_CLASSIFICATION_COLUMN: module.VALUE_COLUMN})

    # --- Report category values the taxonomy has never seen ----------------
    # classify() RAISES on an unknown category rather than dropping it, so
    # report the whole set first - one message beats discovering them one
    # exception at a time.
    seen_here = set(df[module.VALUE_COLUMN].dropna().str.strip()) - {""}
    unseen = sorted(seen_here - module.SEEN)
    if unseen:
        sys.exit(f"BUSINESSACTIVITY value(s) the taxonomy has never seen: "
                 f"{unseen}\nD.C. has added a licence category since "
                 f"2026-09-21. Sample each one and give it a verdict in "
                 f"pipeline/taxonomies/dc_businessactivity.py.")
    print(f"  all {len(seen_here)} licence categories present have a verdict "
          f"in the taxonomy")

    # --- Filter to storefront categories -----------------------------------
    before = len(df)
    dropped = df[~df[module.VALUE_COLUMN].isin(
        set(module._BUCKETS))][module.VALUE_COLUMN].value_counts()
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"\nStorefront filter ({TAXONOMY_SYSTEM}): {before:,} -> "
          f"{len(df):,} rows")
    print("  the five biggest exclusions:")
    for activity, n in dropped.head(5).items():
        print(f"    {n:>7,}  {activity}  "
              f"[{module.EXCLUDED.get(activity, '')}]")

    # --- Coordinates -------------------------------------------------------
    # LATITUDE/LONGITUDE are deliberately not read: they are 39 and -77 on
    # every row in the register.
    x = pd.to_numeric(df["X_COORDINATE"], errors="coerce")
    y = pd.to_numeric(df["Y_COORDINATE"], errors="coerce")
    usable = x.notna() & y.notna()
    pts = gpd.GeoSeries(gpd.points_from_xy(x[usable], y[usable]),
                        crs=SOURCE_XY_CRS).to_crs(CRS_GEOGRAPHIC)
    df["latitude"] = pd.NA
    df["longitude"] = pd.NA
    df.loc[usable, "latitude"] = [p.y for p in pts]
    df.loc[usable, "longitude"] = [p.x for p in pts]
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["coord_status"] = usable.map({True: "source", False: "needs_geocode"})
    print(f"\nCoordinates: {int(usable.sum()):,} of {len(df):,} rows "
          f"({usable.mean():.1%}) carry X/Y; {int((~usable).sum()):,} "
          f"({(~usable).mean():.1%}) are flagged needs_geocode for step 3")
    no_mar = (~usable) & (df["MAR_ID"].fillna("").str.strip() == "")
    print(f"  {int(no_mar.sum()):,} of those also have no MAR_ID - the same "
          f"rows, which is why MAR_ID cannot recover them")

    # Bounds check on the rows that DO have coordinates. This is what would
    # catch a wrong EPSG on X/Y: read as anything but EPSG:26985 they land
    # nowhere near the District.
    have = df[usable]
    b = DC_BBOX
    in_bounds = (have["latitude"].between(b["lat_min"], b["lat_max"])
                 & have["longitude"].between(b["lon_min"], b["lon_max"]))
    print(f"  {int(in_bounds.sum()):,} of {len(have):,} reprojected points "
          f"fall inside the District's bounds ({in_bounds.mean():.1%})")
    if in_bounds.mean() < 0.95:
        sys.exit(f"only {in_bounds.mean():.1%} of reprojected points are in "
                 f"bounds - SOURCE_XY_CRS is probably wrong.")
    out = have.index[~in_bounds]
    df.loc[out, ["latitude", "longitude"]] = pd.NA
    df.loc[out, "coord_status"] = "needs_geocode"

    # --- Display name ------------------------------------------------------
    # ENTITYTRADENAME when there is one, else the legal entity name.
    #
    # Step 0 read this as "the Los Angeles trap at half LA's severity", on a
    # 49% trade-name gap. That figure was measured before the category
    # exclusions: on the rows that actually reach the map the gap is 26.9%,
    # and 85.6% of those have an ENTITYNAME that reads as a company. The
    # person-like residual is 75 rows, of which 72 are incorporated entities -
    # an LLC or corporation registered under its founder's name, which is San
    # Diego's case exactly: a deliberate public commercial act, not a fallback
    # the pipeline substituted. Three rows are sole proprietorships, and all
    # three hold a licence (Grocery Store, Barber Shop, Delicatessen) that
    # requires commercial premises. scripts/check_personal_exposure.py
    # measures this rather than taking the claim on trust.
    trade = df["ENTITYTRADENAME"].fillna("").str.strip()
    trade = trade.mask(trade.str.upper().isin(["N/A", "NA", "NONE"]), "")
    df["business_name"] = trade.where(trade != "",
                                      df["ENTITYNAME"].fillna("").str.strip())
    blank = df["business_name"].str.strip() == ""
    if blank.any():
        print(f"\nDropping {int(blank.sum())} row(s) with neither a trade "
              f"name nor an entity name")
        df = df[~blank]

    street, zips = zip(*df["PREMISEADDRESS"].map(split_address))
    df["street_address"] = street
    df["zip_code"] = zips

    keep_cols = ["business_name", "street_address", "zip_code", "latitude",
                 "longitude", "coord_status", module.VALUE_COLUMN,
                 "CATEGORYSERVICETYPE", "ENTITYTYPE", "CUSTOMERNUMBER",
                 "MAR_ID", "SSL", "WARD"]
    df = df[keep_cols].reset_index(drop=True)
    df["record_id"] = df.index.astype(str)
    BUSINESSES_PREFILTER_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_PREFILTER_CSV, index=False)

    # --- Deduplicate to one row per licensee per premises ------------------
    df["bucket"] = [module.classify(r) for r in df.to_dict("records")]
    buc_rank = {b: i for i, b in enumerate(module.BUCKET_PRIORITY)}
    df["_buc"] = df["bucket"].map(buc_rank).fillna(len(buc_rank)).astype(int)
    # A blank MAR_ID must not collapse every un-geocoded row together, so
    # those rows key on their own record_id instead.
    df["_mar"] = df["MAR_ID"].fillna("").str.strip()
    df["_mar"] = df["_mar"].mask(df["_mar"] == "", "rec:" + df["record_id"])
    key = [PREMISES_KEY[0], "_mar"]

    before = len(df)
    multi = df.groupby(key)["bucket"].nunique().gt(1).sum()
    # Deterministic: sort by the priority and then by record_id, so two rows of
    # equal priority always resolve the same way on a re-run.
    df = (df.sort_values(["_buc", "record_id"])
            .drop_duplicates(subset=key, keep="first")
            .drop(columns=["_buc", "_mar"]))
    print(f"\nPremises dedup on {PREMISES_KEY}: {before:,} -> {len(df):,} rows")
    print(f"  {multi:,} premises held licences in more than one bucket; "
          f"priority {module.BUCKET_PRIORITY}")

    df = df.sort_values("record_id", key=lambda s: s.astype(int))
    df = df.reset_index(drop=True)
    df["record_id"] = df.index.astype(str)

    print(f"\nBy bucket:\n  "
          + df["bucket"].value_counts().to_string().replace("\n", "\n  "))
    print(f"\nBy coordinate status:\n  "
          + df["coord_status"].value_counts().to_string().replace("\n", "\n  "))

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(df):,} rows to {BUSINESSES_CLEAN_CSV}")
    print("Next: step3_geocode.py recovers the needs_geocode rows, then "
          "step4_map.py renders.")


if __name__ == "__main__":
    main()
