"""Step 2 - Clean Miami-Dade's Local Business Tax export.

Input:  data/miami/raw/businesses_active.csv
Output: data/miami/processed/businesses_clean.csv
        data/miami/processed/businesses_prefilter.csv  (unfiltered snapshot)

The file ships pre-geocoded and the coordinates are the best in this project:
all 35,732 active City of Miami rows carry a LAT/LON inside the county, with no
(0,0) placeholders and no corrupt values - so there is no geocoding step here
(steps are 1 stations, 2 clean businesses, 3 map).

NO in-city filter, on purpose. This map is regional (see config.py's header):
the county licenses all 34 of its municipalities in this one file, and the rail
network runs through six of them, so every municipality is kept and MUNBUSLOC
records which one each row came from.

DEDUPLICATION IS THE INTERESTING PART HERE. A premises can hold several licence
rows, one per category - "KIKI ON THE RIVER" holds Dancing + Eating + Retail,
pharmacies hold Pharmacy + Retail Sales, jewellers hold Pawnbroker + Retail
Sales. None of the obvious keys is a premises: RECEIPTNO is unique per row,
ACCOUNTNO is per account, and FOLIO is the PARCEL (6,631 candidate rows shared
only 1,849 folios, because a mall is one parcel). So rows collapse on
name-plus-address, and the taxonomy's BUCKET_PRIORITY picks the bucket.

Run:  python pipeline/miami/step2_clean_businesses.py
"""

import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.miami.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_PREFILTER_CSV,
    BUSINESSES_RAW_CSV,
    MIAMI_BBOX,
    MUNICIPALITY_COLUMN,
    PARCEL_COLUMN,
    PREMISES_KEY,
    RAW_CLASSIFICATION_COLUMN,
    TAXONOMY_SYSTEM,
)
from pipeline.residence import (  # noqa: E402
    flag_home_based,
    has_residential_unit,
    looks_organisational,
    looks_personal,
    report,
)
from pipeline.taxonomies import (  # noqa: E402
    filter_to_storefront,
    load_taxonomy_module,
)

# A "care of" or "attention" clause names a PERSON inside what is otherwise a
# company's registered name: "MIAMI RUBBER PRODUCTS CORP. C/O ADRIAN ALVARADO".
# The clause is stripped rather than the row dropped, because the trade name is
# right there next to it - but which SIDE holds it varies, so the sides are
# ranked rather than positionally assumed (see strip_care_of).
#
# The separator must carry its own punctuation. This project has now made the
# bare-"CO" mistake TWICE: once in check_personal_exposure.py, where it matched
# 567 company names, and once here, where `C\.?\s?O\.?` turned "STARBUCKS
# COFFEE CO 9699" into "9699". So the only accepted forms are "C/O", a
# fully-dotted "C.O." and ATTN/ATTENTION - never two bare letters, which is a
# word in half the company names in this file ("... COFFEE CO", "... TRADING
# CO").
_CARE_OF = re.compile(r"\s*\b(?:C/O|C\.\s?O\.|ATTN\.?|ATTENTION)\b[:,\s]*",
                      re.IGNORECASE)


def strip_care_of(name: str) -> str:
    """Remove a C/O or ATTN clause, keeping the side that is a trade name.

    Ranked by a POSITIVE company signal first, then by position. Two simpler
    rules were tried and both produced wrong names on real rows:

      "longest side that is not a person" turned "EL PATIO DE LOS JUGOS USA
      CORP C/O YOEL HERNANDEZ / ILEANA MARTINEZ" into the two people's names -
      looks_personal() does not flag a slash-joined pair, and that side was two
      characters longer than the company's.

      "first side that is not a person" turned "ANDREW L LEWIS TRS C/O MARRIOT
      HOTEL SERVICES LLC" into the trustee's name, because a "TRS" suffix
      defeats the two-token shape test, so the person did not read as one.

    Preferring a side with an actual organisation token fixes both, and falling
    back to position handles the pairs where neither side has one ("PRESLEY
    PATRICIA C/O LIBERTY MARKET").
    """
    raw = str(name or "").strip()
    parts = [p.strip(" ,.-") for p in _CARE_OF.split(raw) if p and p.strip(" ,.-")]
    if len(parts) < 2:
        return raw
    for part in parts:                       # a company signal wins outright
        if looks_organisational(part):
            return part
    for part in parts:                       # else the first non-person
        if not looks_personal(part):
            return part
    return ""          # every side reads as a person - drop the row

# Columns this step refuses to carry, asserted rather than assumed. OWNERNAME
# is populated on 100% of rows and is frequently a person's name; MAILADDR is a
# home address for a sole trader. fetch_sources.py does not download them, and
# this assertion is what makes that a guarantee rather than a habit.
FORBIDDEN = ["ownername", "mailname", "mailaddr", "mailaddr2", "mailaddr3",
             "mailcity", "mailstate", "mailzip"]


def main():
    if not BUSINESSES_RAW_CSV.exists():
        sys.exit(f"No file at {BUSINESSES_RAW_CSV}.\n"
                 "Run pipeline/miami/fetch_sources.py first.")

    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, low_memory=False)
    df.columns = [c.strip().lower() for c in df.columns]
    print(f"Loaded {len(df):,} rows (already ACCSTATUS='Active' at download)")

    present = [c for c in FORBIDDEN if c in df.columns]
    assert not present, (
        f"Personal-information columns present in the raw export: {present}. "
        f"fetch_sources.py must not download them - see its DOWNLOAD_FIELDS.")

    module = load_taxonomy_module(TAXONOMY_SYSTEM)
    value_column = module.VALUE_COLUMN
    if RAW_CLASSIFICATION_COLUMN != value_column:
        df = df.rename(columns={RAW_CLASSIFICATION_COLUMN: value_column})

    # --- Report classification values this taxonomy does not know ----------
    # An upstream rename would otherwise drop rows silently. All 150 values
    # active on 2026-09-21 carry an explicit verdict, so anything here is new.
    known = set(module.CATEGORY_BUCKETS_BY_NAME)
    seen = set(df[value_column].dropna().str.strip().str.upper())
    unknown = sorted(seen - known)
    if unknown:
        counts = (df[df[value_column].str.strip().str.upper().isin(unknown)]
                  [value_column].value_counts())
        print(f"\nWARNING: {len(unknown)} {value_column} value(s) not in the "
              f"taxonomy - classified as None and dropped. Add a verdict for "
              f"each in pipeline/taxonomies/miami_catgryname.py:")
        print("    " + counts.to_string().replace("\n", "\n    "))
    else:
        print(f"Every {value_column} value in this export has an explicit "
              f"taxonomy verdict.")

    # --- Filter to storefront categories -----------------------------------
    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"\nStorefront filter ({TAXONOMY_SYSTEM}): {before:,} -> {len(df):,} rows")

    # --- Coordinates -------------------------------------------------------
    before = len(df)
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df = df.dropna(subset=["lat", "lon"])
    print(f"Coordinate presence: {before:,} -> {len(df):,} rows")

    before = len(df)
    b = MIAMI_BBOX
    df = df[df["lat"].between(b["lat_min"], b["lat_max"])
            & df["lon"].between(b["lon_min"], b["lon_max"])]
    print(f"Coordinate sanity bounds: {before:,} -> {len(df):,} rows "
          f"(catches swapped lat/lon and wild mismatches)")

    # --- Rename to the shared column names the map step expects ------------
    df = df.rename(columns={"busname": "business_name", "busaddr": "address",
                            "lat": "latitude", "lon": "longitude"})
    blank = df["business_name"].fillna("").str.strip() == ""
    if blank.any():
        # Never happened on the measured population (BUSNAME is present on
        # 100% of rows), so this drops rather than falling back to a
        # registrant's name the way Los Angeles had to.
        print(f"Dropping {int(blank.sum())} row(s) with a blank BUSNAME - this "
              f"registry has no second name column that is safe to publish")
        df = df[~blank]

    # --- Deduplicate to one row per premises -------------------------------
    df["bucket"] = df.apply(lambda r: module.classify(r), axis=1)
    order = {b: i for i, b in enumerate(module.BUCKET_PRIORITY)}
    df["_rank"] = df["bucket"].map(order).fillna(len(order)).astype(int)

    key = [k for k in PREMISES_KEY]
    df["_norm_name"] = df["business_name"].str.strip().str.upper()
    df["_norm_addr"] = df["address"].fillna("").str.strip().str.upper()
    before = len(df)
    multi = (df.groupby(["_norm_name", "_norm_addr"])[value_column]
               .nunique().gt(1).sum())
    df = (df.sort_values("_rank")
            .drop_duplicates(subset=["_norm_name", "_norm_addr"], keep="first")
            .drop(columns=["_rank", "_norm_name", "_norm_addr"]))
    print(f"Premises dedup on {key}: {before:,} -> {len(df):,} rows "
          f"({multi:,} premises held licences in more than one category; "
          f"bucket priority {module.BUCKET_PRIORITY})")

    # --- Strip "C/O <person>" and "ATTN <person>" clauses ------------------
    before_names = df["business_name"].copy()
    df["business_name"] = df["business_name"].map(strip_care_of)
    changed = (df["business_name"] != before_names).sum()
    emptied = (df["business_name"].str.strip() == "")
    if changed:
        print(f"\nCare-of scrub: {int(changed):,} displayed name(s) had a "
              f"C/O or ATTN clause naming a person removed")
        for old, new in list(zip(before_names[df["business_name"] != before_names],
                                 df["business_name"][df["business_name"] != before_names]))[:6]:
            print(f"    {old!r}\n      -> {new!r}")
    if emptied.any():
        print(f"  dropped {int(emptied.sum())} row(s) where every side of the "
              f"clause read as a person, so no trade name remained")
        df = df[~emptied]

    df = df.reset_index(drop=True)
    df["record_id"] = df.index.astype(str)

    # Unfiltered snapshot, written before any residence-style filter. Kept
    # even though no such filter exists here yet: a cache built from filtered
    # output silently lets removed rows return, a trap this project has
    # introduced twice (Los Angeles, then San Diego an hour later).
    BUSINESSES_PREFILTER_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_PREFILTER_CSV, index=False)

    # --- Home-based businesses ---------------------------------------------
    # One rule, not the two that San Francisco and Los Angeles run, because
    # this city has only one usable signal. Those cities join a parcel roll for
    # a land-use class and a homeowner's exemption; Miami-Dade's FOLIO would
    # allow the same, but it is present on only 45.7% of the regional
    # storefront set (100% inside the City of Miami), so a parcel rule would
    # silently apply to half the map and not the other half. That is worse than
    # not running it, so the address rule runs alone and the parcel rule is
    # left recorded as available - see config.PARCEL_COLUMN.
    #
    # The signal is a dwelling-unit designator (APT/UNIT/PH/SPC, never
    # STE/FL/RM - the distinction that stopped Los Angeles' jewellery district
    # reading as residential) plus a name that reads as a person's.
    before = len(df)
    at_home = flag_home_based(
        df["business_name"],
        residential=df["address"].map(has_residential_unit),
    )
    report("person-like name + dwelling-unit address", at_home, before,
           extra={"catgryname": df[value_column],
                  "municipality": df[MUNICIPALITY_COLUMN]})
    df = df[~at_home].reset_index(drop=True)
    df["record_id"] = df.index.astype(str)

    print(f"\nBy bucket:\n"
          + df["bucket"].value_counts().to_string().replace("\n", "\n  "))
    print(f"\nBy municipality (regional scope - all kept):\n  "
          + df[MUNICIPALITY_COLUMN].value_counts().head(12)
              .to_string().replace("\n", "\n  "))
    got_parcel = df[PARCEL_COLUMN].notna().sum() if PARCEL_COLUMN in df else 0
    print(f"\nParcel id ({PARCEL_COLUMN}) present on {got_parcel:,} of "
          f"{len(df):,} rows - the join for a future residence check")

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(df):,} rows to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
