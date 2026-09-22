"""Step 2 - clean Toronto's MLS licences into a storefront set.

Input:  data/toronto/raw/business_licences.csv   (OGL - Toronto)
Output: data/toronto/processed/businesses_clean.csv

NO COORDINATES. NOT ONE. That is what makes Toronto the only one of six
Canadian candidates needing a geocoding step, so this step writes street
addresses and **step 3 geocodes them** - the map is step 4.

THREE PERSONAL COLUMNS, AND THE COUNT IS THE POINT. The register publishes
`Client Name`, `Business Phone` and `Business Phone Ext.` The Canada profile
recorded the first and missed the other two. All three are dropped on read and
asserted gone; `Operating Name` is blank on 0.8% of rows, so there is no
fallback pressure and no reason any of them would ever be needed.

ONE ROW PER LICENCE, WHICH IS CALGARY'S DOUBLE-COUNTING PROBLEM. `Category` is
single-valued, so a restaurant with a patio holds two licences and appears as
TWO rows. Endorsements are therefore dropped by category (the taxonomy maps
`SIDEWALK CAFE`, `NOISE EXEMPTION` and the two `EXPANDED ...` classes to None),
and this step then deduplicates on **address + normalised name**, because two
food licences at one address under one name are one storefront. Under-merging
is the safer error - see the multi-source-city skill - so both counts print.

Run:  python pipeline/toronto/step2_clean_businesses.py
"""

import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.counts import pct  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402
from pipeline.toronto.config import (  # noqa: E402
    ADDRESS_COLUMN,
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_RAW_CSV,
    CANCEL_DATE_COLUMN,
    CATEGORY_COLUMN,
    FORBIDDEN_COLUMNS,
    LICENCE_KEY,
    NAME_COLUMN,
    SOURCE_ENCODING,
    TAXONOMY_SYSTEM,
    WARD_COLUMN,
)

MODULE = load_taxonomy_module(TAXONOMY_SYSTEM)


def main():
    if not BUSINESSES_RAW_CSV.exists():
        sys.exit(f"Missing {BUSINESSES_RAW_CSV.name}. Run "
                 f"pipeline/toronto/fetch_sources.py first.")

    keep_cols = [LICENCE_KEY, CATEGORY_COLUMN, NAME_COLUMN, ADDRESS_COLUMN,
                 WARD_COLUMN, CANCEL_DATE_COLUMN]
    header = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, nrows=0,
                         encoding=SOURCE_ENCODING).columns.tolist()
    present_personal = [c for c in FORBIDDEN_COLUMNS if c in header]
    print(f"Register has {len(header)} columns; "
          f"{len(present_personal)} are personal and are NOT read: "
          f"{present_personal}")

    # usecols is the enforcement, not a filter applied afterwards: the personal
    # columns never enter the process.
    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, encoding=SOURCE_ENCODING,
                     usecols=[c for c in keep_cols if c in header],
                     low_memory=False)
    leaked = sorted(set(df.columns) & set(FORBIDDEN_COLUMNS))
    if leaked:
        sys.exit(f"{leaked} reached the dataframe. usecols failed; stop.")
    print(f"  loaded {len(df):,} rows, {len(df.columns)} columns, none personal")

    # --- active licences ---------------------------------------------------
    # THIS REGISTER IS A TERM HISTORY, not a snapshot: cancellations run back
    # to 2005, so about three quarters of rows carry a Cancel Date and dropping
    # them is correct rather than alarming. Only a cancellation ALREADY PAST
    # ends a licence - a handful carry a future date and are still trading - so
    # the comparison is against today, not against null.
    if CANCEL_DATE_COLUMN in df.columns:
        cd = pd.to_datetime(df[CANCEL_DATE_COLUMN], errors="coerce",
                            format="mixed")
        today = pd.Timestamp.today().normalize()
        cancelled = cd.notna() & (cd <= today)
        future = cd.notna() & (cd > today)
        print(f"\n{CANCEL_DATE_COLUMN}: {int(cancelled.sum()):,} already "
              f"cancelled ({100 * cancelled.mean():.1f}%), "
              f"{int(future.sum())} cancelled in the FUTURE and so still "
              f"trading (kept). The register is a history back to 2005.")
        df = df[~cancelled].copy()
        print(f"  active: {len(df):,}")

    # --- classification, BEFORE the name check ----------------------------
    # ORDER MATTERS HERE, and getting it wrong produces a frightening number on
    # the wrong denominator. `Operating Name` is blank on 21.4% of ACTIVE rows,
    # which reads as a serious gap - until you see it is almost entirely
    # `TAXICAB OWNER` (4,212), `MASTER PLUMBER` (969) and `DRIVING INSTRUCTOR`
    # (934): person-held licences with no trade name, which this map excludes
    # anyway. Filtering to storefront first makes the blank rate a fact about
    # the rows that actually reach the map. The build brief said 0.8%; measured
    # across all rows it is 19.4%.
    cats = df[CATEGORY_COLUMN].nunique()
    print(f"\n{CATEGORY_COLUMN}: {cats} distinct categories "
          f"(single-valued - no delimiter, unlike Calgary's and Edmonton's)")
    df[MODULE.VALUE_COLUMN] = df[CATEGORY_COLUMN]

    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"  storefront: {before:,} -> {len(df):,} "
          f"({before - len(df):,} dropped as out of scope, endorsements "
          f"included)")
    buckets = df[MODULE.VALUE_COLUMN].map(
        lambda v: MODULE.classify({MODULE.VALUE_COLUMN: v}))
    print("  by bucket:")
    for k, v in buckets.value_counts().items():
        print(f"      {v:>7,}  {k}")
    print("  NOTE: Retail is the REGULATED slice only - Toronto licenses no "
          "grocer, clothing shop, pharmacy or hardware store, so they are "
          "absent rather than thin. Stated on the city page.")

    # --- names, on the storefront subset ----------------------------------
    blank = df[NAME_COLUMN].isna() | df[NAME_COLUMN].fillna("").str.strip().eq("")
    # pct() names the set, which is the whole point here: this same figure read
    # 21.4% before the filters were reordered, because it was measured on active
    # rows rather than on the rows that reach the map.
    print(f"\n{NAME_COLUMN} blank on "
          f"{pct(int(blank.sum()), len(df), 'storefront rows')} - dropped "
          f"rather than filled, because the only other name column is the "
          f"registrant's and this project does not load it")
    df = df[~blank].copy()

    # --- addresses ---------------------------------------------------------
    blank_addr = (df[ADDRESS_COLUMN].isna()
                  | df[ADDRESS_COLUMN].fillna("").str.strip().eq(""))
    print(f"\n{ADDRESS_COLUMN} blank on {int(blank_addr.sum()):,} rows - "
          f"dropped, since the address IS the geocode key here")
    df = df[~blank_addr].copy()

    # --- deduplicate on address + normalised name --------------------------
    # NEVER address alone: one address routinely holds many separate shops.
    norm_name = (df[NAME_COLUMN].str.upper()
                 .str.replace(r"[^A-Z0-9 ]", "", regex=True)
                 .str.replace(r"\s+", " ", regex=True).str.strip())
    norm_addr = (df[ADDRESS_COLUMN].str.upper()
                 .str.replace(r"\s+", " ", regex=True).str.strip())
    before = len(df)
    df = df.assign(_k=norm_addr + " | " + norm_name).drop_duplicates("_k")
    print(f"\nDeduplicated on address + normalised name: {before:,} -> "
          f"{len(df):,} ({before - len(df):,} dropped)")
    print(f"  for contrast, on address ALONE it would be "
          f"{norm_addr.nunique():,} rows - which would delete real "
          f"storefronts, since a plaza is one address")

    out = df.rename(columns={NAME_COLUMN: "business_name",
                             ADDRESS_COLUMN: "address"})[
        ["business_name", "address", MODULE.VALUE_COLUMN, LICENCE_KEY,
         WARD_COLUMN]]
    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.sort_values(LICENCE_KEY).to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(out):,} storefronts to {BUSINESSES_CLEAN_CSV}")
    print("  no coordinates yet - step 3 geocodes them against the One "
          "Address Repository")


if __name__ == "__main__":
    main()
