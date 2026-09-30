"""Step 2 - Houston's storefronts from the Texas Comptroller's Active Sales Tax
Permit Holders. No coordinates yet: step 3 places them.

Input:  data/houston/raw/sales_tax_permits_houston.csv
Output: data/houston/processed/businesses_clean.csv

What a reader should know before trusting the counts printed below:

  * **The taxpayer is never read**: not the name, the address or the number
    (for an individual, a Texas taxpayer number is built from their Social
    Security number). The download names its columns and this step asserts
    none of those arrived. Only `outlet_*` and the organisation type.
  * **NAICS, the shared module**: 454 non-store retailers, parking,
    caterers and the other shared carve-outs leave by code
    (pipeline/taxonomies/naics.py).
  * **A person's business shows its address, not its name**: sole owners,
    individuals' general partnerships and estates (the organisation types in
    PERSONAL_FORMS) - Copenhagen's and Oslo's rule, the brief's call.
  * **At an apartment or a trailer, a business is a home**, and is left off
    (Sacramento's owner call, 2026-09-29).
  * **One row per premises**: a permit is per outlet, and one business at one
    address can hold several.

Run:  python pipeline/houston/step2_clean_businesses.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.houston import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront  # noqa: E402
from pipeline.taxonomies.naics import VALUE_COLUMN  # noqa: E402

# The Comptroller's organisation types that ARE a person (its record layout,
# read 2026-09-29): IS individual - sole owner, S sole proprietorship, PI
# individual general partnership, P general partnership, PZ individual
# successor partnership, ES estate. General partnerships are in on Denmark's
# precedent (owner, 2026-09-24): the partners are liable personally, and
# their names are often the business's. PB, a partnership of businesses, is not.
PERSONAL_FORMS = ("IS", "S", "PI", "P", "PZ", "ES")

# A dwelling in the business's own address. APT is Sacramento's owner call;
# TRLR (a mobile home) is pipeline/residence.py's. UNIT and SPC are NOT: here
# they are strip-centre and mall spaces ("5015 WESTHEIMER RD SPC 1395"),
# measured on a sample 2026-09-29.
HOME_UNIT = r"\s(?:APT|APARTMENT|TRLR)\b"

# The unit tail, cut to make the street the join and the geocoder read.
UNIT_TAIL = (r"\s*(?:,\s*)?(?:\bSTE\b|\bSUITE\b|\bUNIT\b|\bBLDG\b|\bSPC\b|\bSPACE\b|\bRM\b|"
             r"\bROOM\b|\bFL\b|\bFLOOR\b|\bLOT\b|#).*$")


def _s(col):
    return col.fillna("").astype(str).str.strip()


def main():
    if not config.REGISTER_CSV.exists():
        sys.exit(f"missing {config.REGISTER_CSV}\nRun: python pipeline/houston/fetch_sources.py")
    df = pd.read_csv(config.REGISTER_CSV, dtype=str, keep_default_na=False, na_values=[""])
    leaked = [c for c in df.columns if c in config.FORBIDDEN_COLUMNS]
    assert not leaked, f"forbidden columns reached step 2: {leaked}"
    print(f"Loaded {len(df):,} outlets (Houston, inside city limits)")

    df[VALUE_COLUMN] = _s(df[config.RAW_CLASSIFICATION_COLUMN]).str.replace(r"\.0$", "", regex=True)
    before = len(df)
    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    print(f"  storefront NAICS: {before:,} -> {len(df):,}")
    emit("storefront_rows", len(df))

    # Not trading yet: a permit whose first sales date is after the fetch date.
    first = pd.to_datetime(df["outlet_first_sales_date"], errors="coerce")
    later = first > pd.Timestamp(config.AS_OF_DATE)
    print(f"  first sales after {config.AS_OF_DATE}: {int(later.sum()):,} not trading yet, left off")
    df = df[~later].copy()

    df["address"] = _s(df["outlet_address"]).str.upper().str.replace(r"\s+", " ", regex=True)
    df["zip"] = _s(df["outlet_zip_code"]).str.slice(0, 5)
    df["business_name"] = _s(df["outlet_name"])
    df["org_type"] = _s(df["taxpayer_organization_type"])

    home = df["address"].str.contains(HOME_UNIT, regex=True)
    print(f"  at an apartment or trailer: {int(home.sum()):,} left off as homes")
    emit("home_unit_dropped", int(home.sum()))
    df = df[~home]

    df["street"] = df["address"].str.replace(UNIT_TAIL, "", regex=True).str.strip(" ,.-")
    df["unit"] = [a[len(s):].strip(" ,") for a, s in zip(df["address"], df["street"])]
    no_number = ~df["street"].str.match(r"^\d")
    print(f"  no street number (a mall or building name alone; cannot be placed): "
          f"{int(no_number.sum()):,}")
    df = df[~no_number & (df["business_name"] != "")]

    key = (df["business_name"].str.upper().str.replace(r"[^A-Z0-9]", "", regex=True) + "|"
           + df["address"])
    before = len(df)
    df = df.assign(_k=key).sort_values(["_k", ":id"]).drop_duplicates("_k")
    print(f"  one row per premises (name + address): {before:,} -> {len(df):,}")

    # A PERSON'S BUSINESS SHOWS ITS ADDRESS (the brief; Copenhagen's and Oslo's
    # sole-trader rule): the Comptroller records the legal form, so no guess at
    # the name is needed.
    df["name_is_address"] = df["org_type"].isin(PERSONAL_FORMS)
    df.loc[df["name_is_address"], "business_name"] = df.loc[df["name_is_address"], "address"]
    print(f"  personally owned ({'/'.join(PERSONAL_FORMS)}): "
          f"{int(df['name_is_address'].sum()):,} show the address; by type "
          f"{df.loc[df['name_is_address'], 'org_type'].value_counts().to_dict()}")
    emit("name_as_address", int(df["name_is_address"].sum()))

    out = df.rename(columns={":id": "permit"})[
        ["permit", "business_name", VALUE_COLUMN, "address", "street", "unit", "zip",
         "org_type", "name_is_address"]]
    out = out.sort_values("permit").reset_index(drop=True)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    emit("premises", len(out))
    print(f"\n{len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
