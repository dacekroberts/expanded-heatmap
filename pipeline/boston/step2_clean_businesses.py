"""Step 2 - Assemble Boston's three registries into one clean business table.

Input:  data/boston/raw/isd_food_active.csv     (one row per premises+category)
        data/boston/raw/licensing_board.csv     (package stores)
        data/boston/raw/cannabis.csv
Output: data/boston/processed/businesses_clean.csv
        data/boston/processed/businesses_prefilter.csv

THREE SOURCES, TWO COORDINATE SYSTEMS, AND ONE REAL OVERLAP.

  isd_food         `location` is a "(lat, lon)" STRING, not numeric columns.
  licensing_board  `gpsx`/`gpsy` in EPSG:2249 - Massachusetts State Plane in
  cannabis         US survey FEET - which must be reprojected, not read as
                   degrees. Verified by transformation during Step 0.

The overlap that matters is package stores: a shop can hold both an ISD `RF`
food licence and a Licensing Board "Retail All Alc." licence. On 2026-09-21
"Go Fresh 365" / "Ming's Supermarket" held both at 1102 Washington St. So the
sources are deduplicated AGAINST EACH OTHER on name-plus-address, not just
within themselves, and `source` records which registry each surviving row came
from.

Addresses need normalising before that comparison can work at all: ISD writes
"1102 WASHINGTON ST" and the Licensing Board writes "1102-  WASHINGTON ST" for
the same premises.

NO PERSONAL-NAME COLUMN IS EVER LOADED. The ISD table carries `legalowner`,
`namelast` and `namefirst`, and the Licensing Board table carries `applicant`,
`manager`, `day_phone` and `evening_phone`. fetch_sources.py does not select
any of them, and the assertion below is what makes that a guarantee.

Run:  python pipeline/boston/step2_clean_businesses.py
"""

import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.boston.config import (  # noqa: E402
    BOSTON_BBOX,
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_PREFILTER_CSV,
    CANNABIS_CSV,
    CRS_GEOGRAPHIC,
    GPS_XY_CRS,
    ISD_FOOD_CSV,
    LICENSING_BOARD_CSV,
    PREMISES_KEY,
    RAW_CLASSIFICATION_COLUMNS,
    SOURCE_ENCODING,
    TAXONOMY_SYSTEM,
)
from pipeline.taxonomies import (  # noqa: E402
    filter_to_storefront,
    load_taxonomy_module,
)

FORBIDDEN = ["legalowner", "namelast", "namefirst", "applicant", "manager",
             "day_phone", "evening_phone", "dayphn_cleaned"]

_LOCATION = re.compile(r"\(\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\)")
_HOUSE_DASH = re.compile(r"^(\d+)\s*-\s*")
_WS = re.compile(r"\s+")


def parse_location(value):
    """ISD publishes '(42.35925954972639, -71.05890048027378)' as text."""
    m = _LOCATION.search(str(value or ""))
    if not m:
        return None, None
    return float(m.group(1)), float(m.group(2))


def normalise_address(value):
    """Make two registries' spellings of one address comparable.

    The Licensing Board writes a house number with a trailing hyphen and
    padding ("3094-  Washington ST"); ISD does not ("3094 WASHINGTON ST").
    Without collapsing that, no package store would ever match its own food
    licence and every one would be counted twice.
    """
    s = str(value or "").upper().strip()
    s = _HOUSE_DASH.sub(r"\1 ", s)
    s = s.replace(".", " ").replace(",", " ")
    return _WS.sub(" ", s).strip()


def load_isd():
    df = pd.read_csv(ISD_FOOD_CSV, dtype=str, encoding=SOURCE_ENCODING)
    df.columns = [c.strip().lower() for c in df.columns]
    latlon = df["location"].map(parse_location)
    df["latitude"] = [p[0] for p in latlon]
    df["longitude"] = [p[1] for p in latlon]
    # `businessname`, NOT `dbaname`: dbaname is blank on 99.0% of this
    # registry's rows while businessname always holds the trade name - the
    # reverse of every other city here.
    df["business_name"] = df["businessname"]
    df["source"] = "isd_food"
    df["business_category"] = df[RAW_CLASSIFICATION_COLUMNS["isd_food"]]
    return df[["business_name", "address", "city", "zip", "latitude",
               "longitude", "source", "business_category", "property_id"]]


def load_gps_xy(path, source):
    """The Licensing Board and cannabis sets: gpsx/gpsy in EPSG:2249."""
    df = pd.read_csv(path, dtype=str, encoding=SOURCE_ENCODING)
    df.columns = [c.strip().lower() for c in df.columns]
    x = pd.to_numeric(df["gpsx"], errors="coerce")
    y = pd.to_numeric(df["gpsy"], errors="coerce")
    ok = x.notna() & y.notna()
    pts = gpd.GeoSeries(gpd.points_from_xy(x[ok], y[ok]), crs=GPS_XY_CRS
                        ).to_crs(CRS_GEOGRAPHIC)
    df["latitude"] = pd.NA
    df["longitude"] = pd.NA
    df.loc[ok, "latitude"] = [p.y for p in pts]
    df.loc[ok, "longitude"] = [p.x for p in pts]
    # Here dba_name IS the trade name and business_name the legal entity - the
    # normal convention, and the opposite of the ISD table above.
    df["business_name"] = (df["dba_name"].fillna("").str.strip()
                           .replace("", pd.NA).fillna(df["business_name"]))
    df["source"] = source
    df["business_category"] = df[RAW_CLASSIFICATION_COLUMNS[source]]
    df["property_id"] = pd.NA
    return df[["business_name", "address", "city", "zip", "latitude",
               "longitude", "source", "business_category", "property_id"]]


def main():
    for path in (ISD_FOOD_CSV, LICENSING_BOARD_CSV, CANNABIS_CSV):
        if not path.exists():
            sys.exit(f"No file at {path}.\n"
                     "Run pipeline/boston/fetch_sources.py first.")

    for path in (ISD_FOOD_CSV, LICENSING_BOARD_CSV, CANNABIS_CSV):
        cols = [c.strip().lower() for c in
                pd.read_csv(path, nrows=0, encoding=SOURCE_ENCODING).columns]
        present = [c for c in FORBIDDEN if c in cols]
        assert not present, (
            f"{path.name} carries personal-information column(s) {present}. "
            f"fetch_sources.py must not select them.")

    frames = [load_isd(),
              load_gps_xy(LICENSING_BOARD_CSV, "licensing_board"),
              load_gps_xy(CANNABIS_CSV, "cannabis")]
    df = pd.concat(frames, ignore_index=True)
    print("Loaded per source:")
    print("  " + df["source"].value_counts().to_string().replace("\n", "\n  "))

    module = load_taxonomy_module(TAXONOMY_SYSTEM)

    # --- Report category values the taxonomy has never seen ---------------
    lb = df[df["source"] == "licensing_board"]["business_category"].dropna()
    unseen = sorted(set(lb) - module.LICENSING_BOARD_SEEN)
    if unseen:
        print(f"\nWARNING: Licensing Board licence type(s) not in the "
              f"taxonomy's SEEN set: {unseen}. If any is a retail type it is "
              f"being dropped - add it to LICENSING_BOARD_KEPT.")
    else:
        print("\nEvery Licensing Board licence type present is one the "
              "taxonomy has already seen.")

    # --- Filter to storefront categories ----------------------------------
    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"\nStorefront filter ({TAXONOMY_SYSTEM}): {before:,} -> {len(df):,} rows")
    print("  by source: " + df["source"].value_counts().to_dict().__str__())

    # --- Coordinates -------------------------------------------------------
    before = len(df)
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude"])
    print(f"Coordinate presence: {before:,} -> {len(df):,} rows")

    before = len(df)
    b = BOSTON_BBOX
    df = df[df["latitude"].between(b["lat_min"], b["lat_max"])
            & df["longitude"].between(b["lon_min"], b["lon_max"])]
    print(f"Coordinate sanity bounds: {before:,} -> {len(df):,} rows "
          f"(also the check that would catch a wrong EPSG on gpsx/gpsy - a "
          f"metre-based reading of them lands near 60N)")

    blank = df["business_name"].fillna("").str.strip() == ""
    if blank.any():
        print(f"Dropping {int(blank.sum())} row(s) with no usable trade name")
        df = df[~blank]

    df = df.reset_index(drop=True)
    df["record_id"] = df.index.astype(str)
    BUSINESSES_PREFILTER_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_PREFILTER_CSV, index=False)

    # --- Deduplicate, ACROSS sources as well as within them ---------------
    df["bucket"] = [module.classify(r) for r in df.to_dict("records")]
    src_rank = {s: i for i, s in enumerate(module.SOURCE_PRIORITY)}
    buc_rank = {b: i for i, b in enumerate(module.BUCKET_PRIORITY)}
    df["_src"] = df["source"].map(src_rank).fillna(len(src_rank)).astype(int)
    df["_buc"] = df["bucket"].map(buc_rank).fillna(len(buc_rank)).astype(int)
    df["_name"] = df["business_name"].str.upper().str.strip()
    df["_addr"] = df["address"].map(normalise_address)

    before = len(df)
    cross = (df.groupby(["_name", "_addr"])["source"].nunique().gt(1).sum())
    multi = (df.groupby(["_name", "_addr"])["bucket"].nunique().gt(1).sum())
    df = (df.sort_values(["_buc", "_src"])
            .drop_duplicates(subset=["_name", "_addr"], keep="first")
            .drop(columns=["_src", "_buc", "_name", "_addr"]))
    print(f"\nPremises dedup on {PREMISES_KEY}: {before:,} -> {len(df):,} rows")
    print(f"  {cross:,} premises appeared in more than one REGISTRY "
          f"(the package-store overlap this dedup exists for)")
    print(f"  {multi:,} premises held licences in more than one bucket; "
          f"priority {module.BUCKET_PRIORITY}")

    df = df.reset_index(drop=True)
    df["record_id"] = df.index.astype(str)

    print(f"\nBy bucket:\n  "
          + df["bucket"].value_counts().to_string().replace("\n", "\n  "))
    print(f"\nBy source:\n  "
          + df["source"].value_counts().to_string().replace("\n", "\n  "))

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(df):,} rows to {BUSINESSES_CLEAN_CSV}")
    print("Personal services is ABSENT from this city, not thin - "
          "Massachusetts publishes no address-bearing cosmetology licence. "
          "See pipeline/taxonomies/boston_licensecat.py.")


if __name__ == "__main__":
    main()
