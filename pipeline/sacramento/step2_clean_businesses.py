"""Step 2 - Sacramento's storefronts from the City's Business Operation Tax
register. No coordinates yet: step 3 geocodes them.

Input:  data/sacramento/raw/business_operation_tax_active.csv
Output: data/sacramento/processed/businesses_clean.csv

What a reader should know before trusting the counts printed below:

  * **Active is not enough**: a licence counts only while Current_Expire_Date
    is on or after config.AS_OF_DATE, the fetch date (Chicago's rule).
  * **"ON FILE" is a withheld address** - mostly home businesses - and those
    rows cannot be placed, by construction.
  * **The owner's name, phone and mailing address are never read**: the
    download names its columns and this step asserts none arrived.
  * **One row per premises**: an account is a licence, and one business at
    one address can hold several; they collapse on name + address.

Run:  python pipeline/sacramento/step2_clean_businesses.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.residence import looks_personal  # noqa: E402
from pipeline.sacramento import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies.sacramento import EXCLUDED  # noqa: E402


CARE_OF = r"\s*\bC/O\b|\s*\bC\.O\.\s|\s*\bATTN\b"


def _s(col):
    return col.fillna("").astype(str).str.strip()


def main():
    if not config.REGISTER_CSV.exists():
        sys.exit(f"missing {config.REGISTER_CSV}\nRun: python pipeline/sacramento/fetch_sources.py")
    df = pd.read_csv(config.REGISTER_CSV, dtype=str, keep_default_na=False, na_values=[""])
    leaked = [c for c in df.columns if c in config.FORBIDDEN_COLUMNS]
    assert not leaked, f"forbidden columns reached step 2: {leaked}"
    print(f"Loaded {len(df):,} Active rows")

    expiry = pd.to_datetime(df["Current_Expire_Date"], errors="coerce")
    live = expiry >= pd.Timestamp(config.AS_OF_DATE)
    print(f"  unexpired on {config.AS_OF_DATE}: {int(live.sum()):,} "
          f"({int((~live).sum()):,} past Current_Expire_Date)")
    df = df[live]
    emit("unexpired", len(df))

    city = _s(df["Location_City"]).str.upper()
    print(f"  Location_City: SACRAMENTO {int((city == config.CITY_KEEP).sum()):,}, "
          f"ON FILE {int((city == 'ON FILE').sum()):,} (address withheld), "
          f"elsewhere {int(((city != config.CITY_KEEP) & (city != 'ON FILE')).sum()):,}")
    df = df[city == config.CITY_KEEP].copy()

    df["business_category"] = _s(df["Business_Description"])
    upper = df["business_category"].str.upper()
    print("  storefront-shaped descriptions left out (taxonomy EXCLUDED):")
    for desc, why in EXCLUDED.items():
        n = int((upper == desc).sum())
        if n:
            print(f"      {desc.title():<40} {n:>5}  {why}")
    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"  storefront descriptions: {before:,} -> {len(df):,}")
    emit("storefront_rows", len(df))

    # The street as the geocoder wants it: number, direction, name, type.
    df["street"] = (_s(df["Location_Street_Number"]) + " " + _s(df["Location_Direction"]) + " "
                    + _s(df["Location_Street_Name"]) + " " + _s(df["Location_Street_Type"]))
    df["street"] = df["street"].str.replace(r"\s+", " ", regex=True).str.strip()
    df["unit"] = _s(df["Location_Unit"])
    df["zip"] = _s(df["Location_Zip_code"]).str.slice(0, 5)
    df["business_name"] = _s(df["Business_Name"])
    no_number = ~df["street"].str.match(r"^\d")
    print(f"  no street number (cannot be geocoded): {int(no_number.sum()):,}")
    df = df[~no_number & (df["business_name"] != "")]

    # "C/O <person>" names someone who is not the business: cut at the marker
    # (1 business, 2026-09-29: "MORRISON MANAGEMENT SPECIALISTS, INC.C/O ...").
    care_of = df["business_name"].str.contains(CARE_OF, regex=True)
    df.loc[care_of, "business_name"] = df.loc[care_of, "business_name"] \
        .str.split(CARE_OF, n=1, regex=True).str[0].str.strip(" ,.-")
    print(f"  'C/O' cut from {int(care_of.sum()):,} name(s)")

    # AT AN APARTMENT, A BUSINESS IS A HOME: left off (owner, 2026-09-29).
    # Only APT: in this register "UNIT" and "SPC" are strip-mall and mall
    # spaces (Arden Fair's "SPC 1334"), measured on the placed rows.
    home = df["unit"].str.upper().str.match(r"^(APT|APARTMENT)\b")
    print(f"  at an apartment unit: {int(home.sum()):,} left off as homes")
    emit("apartment_dropped", int(home.sum()))
    df = df[~home]

    key = (df["business_name"].str.upper().str.replace(r"[^A-Z0-9]", "", regex=True) + "|"
           + df["street"].str.upper() + "|" + df["unit"].str.upper())
    before = len(df)
    df = df.assign(_k=key).sort_values(["_k", "Account_Number"]).drop_duplicates("_k")
    print(f"  one row per premises (name + address): {before:,} -> {len(df):,}")

    # A NAME THAT READS AS A PERSON'S SHOWS THE BUSINESS DESCRIPTION INSTEAD
    # (owner, 2026-09-29): the register has no legal form and no home signal,
    # and a sole proprietor often registers under their own name ("SHEILA
    # ABRAHAM"). Vancouver's "type in place of a personal name", on the shared
    # test (pipeline.residence.looks_personal). Measured: ~1 in 5 flagged names
    # is really a person; the rest are trade names ("TACO BELL") that lose
    # their name too - the cost of having no better signal. After the dedup,
    # so two such premises at one address stay two pins.
    # "BRUCE ARANA (CAPITOL CASINO)": a person, then the trade name in
    # brackets - the trade half is shown (Philadelphia's LEGAL (TRADE) rule).
    pair = df["business_name"].str.extract(r"^(?P<who>[^()]+?)\s*\((?P<trade>[^()]+)\)\s*$")
    bracket = pair["who"].map(looks_personal).fillna(False).astype(bool)
    df.loc[bracket, "business_name"] = pair.loc[bracket, "trade"].str.strip()
    print(f"  'person (trade name)': {int(bracket.sum()):,} show the trade half")
    person = df["business_name"].map(looks_personal)
    df.loc[person, "business_name"] = df.loc[person, "business_category"]
    print(f"  names that read as a person's: {int(person.sum()):,} show the business "
          f"description instead")
    emit("name_as_type", int(person.sum()))

    out = df.rename(columns={"Account_Number": "account"})[
        ["account", "business_name", "business_category", "street", "unit", "zip"]]
    out = out.sort_values("account").reset_index(drop=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    emit("premises", len(out))
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
